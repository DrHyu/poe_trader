''' Parser for POE Client.txt '''
import time
import logging
import re

import config
import currency

from misc import StoppableThread, \
    AFK_STATUS, TRADE_OUTCOME, PLAYER_JOINED_MSG, PLAYER_JOINED_STATUS, TRADE_REQ_MSG, \
    trade_req_q, trade_outcome_q, player_joined_q, afk_mode_q, feedback_q

import random
logger = logging.getLogger('bot_log')


class LogParser():
    '''
    Class to parse the poe client log in an async manner.
    '''

    def __init__(self, log_path):
        self.log_path = log_path

        self.log = None
        try:
            self.log = open(log_path, "r", encoding="utf8")
        except Exception as exception:
            logger.error(
                "Failed to open log file {} with exception:\n{}".format(log_path, exception))

    def __del__(self):
        self.log.close()

    def start(self):
        '''
        Spawn a thread that will:
            Continuously poll the log file for updates.
            Process the new message.
            Push it to the corresponding queue.
        '''

        self.parser_thread = StoppableThread(
            target=self.monitor_log,
            args=(self.log,))
        self.parser_thread.daemon = True
        self.parser_thread.start()

    def end(self):
        '''
        End the thread and wait for it to join.
        '''
        self.parser_thread.stop()
        self.parser_thread.join()
        self.log.close()

    @staticmethod
    def monitor_log(log):
        '''
        Thread that will monitor and sort new messages
        '''
        for new_msg in LogParser.follow_file(log):
            LogParser.process_new_mesage(new_msg)

    @staticmethod
    def follow_file(log):
        '''
        Generator.
        Poll file until a new line is found.
        '''
        log.seek(0, 2)
        while True:
            line = log.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    @staticmethod
    def process_new_mesage(message):
        '''
        Interpret the string.
        It can follow under this categories:
            1. New trade message
            2. Trade feedback (accepted/declined)
            3. Player joined/left the area
            4. AFK ON/OFF
            5. Other
        '''

        logger.debug("Client.txt: {}".format(message))

        # match = re.search(
        #     "\[INFO Client \d+\] {}:(?P<message>.*)".format(config.PLAYER_NAME), message)
        # if match:
        #     feedback_q.put(match.group['message'])

        match = re.search(
            "@From (?:<\w+> )?(?P<player_name>\w+): Hi, I'd like to buy your (?P<give_ammount>\d+) (?P<give>.*) for my (?P<receive_ammount>\d+) (?P<receive>.*) in Delirium.?( \(stash tab \"(?P<stash_tab_name>\w+)\"; position: left (?P<left>\w+), top (?P<top>\w+)\))?", message)

        if match:

            # Match currencies
            give_curr = None
            give_ammount = int(match.group('give_ammount'))
            receive_curr = None
            receive_ammount = int(match.group('receive_ammount'))

            for curr in currency.CURRENCY_LIST:
                if re.match(curr.regex, match.group('receive')):
                    receive_curr = curr
                if re.match(curr.regex, match.group('give')):
                    give_curr = curr

            # Could not identify currency
            if not give_curr or not receive_curr:
                return

            trade_req_q.put(
                TRADE_REQ_MSG(
                    match.group('player_name'),
                    currency.CurrencyStack(give_curr, give_ammount),
                    currency.CurrencyStack(receive_curr, receive_ammount),
                    match.group('stash_tab_name'),
                    match.group('left'),
                    match.group('top')
                )
            )
            return

        # Trade accepted
        match = re.search("Trade accepted.", message)
        if match:
            trade_outcome_q.put(TRADE_OUTCOME.ACCEPTED)
            return

        # Trade declined
        match = re.search("Trade cancelled.", message)
        if match:
            trade_outcome_q.put(TRADE_OUTCOME.DECLINED)
            return

        # Player joined the area
        match = re.search(
            "\[INFO Client \d+\] : (?:<\w+> )?(?P<player_name>\w+) has joined the area.", message)
        if match:
            player_joined_q.put(
                PLAYER_JOINED_MSG(
                    match.group('player_name'),
                    PLAYER_JOINED_STATUS.JOINED
                )
            )
            return

        # Player left
        match = re.search(
            "\[INFO Client \d+\] : (?:<\w+> )?(?P<player_name>\w+) has left the area.", message)
        if match:
            player_joined_q.put(
                PLAYER_JOINED_MSG(
                    match.group('player_name'),
                    PLAYER_JOINED_STATUS.LEFT
                )
            )
            return

        # Went AFK
        match = re.search("AFK mode is now ON", message)
        if match:
            afk_mode_q.put(AFK_STATUS.ON)
            return

        # AFK off
        match = re.search("AFK mode is now OFF", message)
        if match:
            afk_mode_q.put(AFK_STATUS.OFF)
            return

        # else:
        #   ignore


log_parser = LogParser(config.LOG_PATH)

''' track players in hideout '''

import threading
import logging

from player import players
from misc import my_queue, player_joined_q, PLAYER_JOINED_STATUS

import config

logger = logging.getLogger('bot_log')


class Hideout():
    ''' monitor player activity in hideout '''

    def __init__(self):
        self.updater_thread = None

        self._new_activity_q = my_queue("players joined")

    def start(self):
        ''' Start a thread that peridically consumes player joined/left area events '''
        self.updater_thread = threading.Thread(
            target=self.track_hideout_activity, args=(player_joined_q,))

        self.updater_thread.daemon = True
        self.updater_thread.start()

    def track_hideout_activity(self, queue):
        ''' listen to the queue and update the players present in hideout '''

        while True:
            msg = queue.get()

            if msg.new_status == PLAYER_JOINED_STATUS.JOINED:
                player = players.get_player(msg.player_name)
                if player is None:
                    logger.warning(
                        "Player {} joined area but it is not in player list".format(msg.player_name))

                else:
                    player.joined_hideout()
                    logger.info(
                        "Player {} has joined the area".format(player))
                    logger.debug(
                        "Players in area {}".format(players.get_all()))

                    # Add this player to the "recently joined" queue
                    self._new_activity_q.put(player)

            elif msg.new_status == PLAYER_JOINED_STATUS.LEFT:
                player = players.get_player(msg.player_name)
                if player is None:
                    logger.warning(
                        "Player {} left area but it is not in player list".format(msg.player_name))

                else:
                    player.left_hideout()

                    # Stop tracking players when they leave the hideout
                    players.remove_player(player)

                    logger.info(
                        "Player {} has left the area".format(player))
                    logger.debug(
                        "Players in area {}".format(players.get_all()))

            else:
                pass

    def recently_joined_players(self):
        ''' returns an array of TRACKED players that have joined the area since last call '''
        players = []

        # Fetch all recent events
        while True:
            temp = self._new_activity_q.get(block=False)
            if temp is not None:
                players.append(temp)
            else:
                break
        return players


hideout = Hideout()


if __name__ == '__main__':

    logger.setLevel(level=logging.DEBUG)

    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    from log_parser import LogParser
    import time

    parser = LogParser(config.LOG_PATH)
    parser.start()

    hideout.start()

    while True:
        time.sleep(1)

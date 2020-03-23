import time
import logging
import copy

from threading import Lock
from uiactions import uiactions
from misc import trade_outcome_q, TRADE_OUTCOME

logger = logging.getLogger('bot_log')


class PlayerList():
    '''  synchronized list of players '''

    def __init__(self, player_limit=10):
        self._lock = Lock()
        self._players = []
        self._player_limit = player_limit

    def remove_player(self, rm_player):
        ''' remove player from PlayerList '''

        self._lock.acquire()
        for player in self._players:
            if rm_player == player.name:
                self._players.remove(player)
                self._lock.release()

                logger.info(
                    "Player {} removed from PlayerList".format(player))
                return True

        self._lock.release()
        logger.warning(
            "Failed to remove player {} as it was not PlayerList".format(rm_player))

        return False

    def add_player(self, player):
        ''' add player to PlayerList '''

        if not isinstance(player, Player):
            logger.warning(
                "Attempted to add non-Player object to PlayerList. {}".format(player))
            raise Exception

        self._lock.acquire()

        for ply in self._players:
            if ply.name == player.name:
                logger.warning(
                    "Failed to add {} to PlayerList as it is already in PlayerList.".format(player))
                self._lock.release()
                return False

        if len(self._players) == self._player_limit:
            logger.warning(
                "Failed to add {} to PlayerList as PlayerList if full.".format(player))
            self._lock.release()
            return False
        else:
            self._players.append(player)
            logger.info(
                "Player {} added to PlayerList".format(player))
            self._lock.release()
            return True

    def get_all(self):
        '''
            Returns a deepcopy of the list.
            Read only, since changes to the returned list will NOT be reflected in this PlayerList

        '''
        self._lock.acquire()
        temp = []
        for x in self._players:
            temp.append(x)
        self._lock.release()
        return temp

    def get_player(self, player_name):
        ''' return reference to player in the list '''

        self._lock.acquire()
        for player in self._players:
            if player_name == player.name:
                self._lock.release()
                logger.debug(
                    "Returned Player reference {} from PlayerList".format(player))
                return player

        self._lock.release()
        return None

    def debug_get(self):
        return self._players


class Player():
    ''' representation of a player '''

    def __init__(self, player_name):

        self.name = player_name

        self._buy = None
        self._sell = None
        self._trade_info_lock = Lock()

        self._in_hideout_lock = Lock()
        self._in_hideout = False

        self.trade_completed = False

        self.trade_msq_received_timestamp = None
        self.invite_sent_timestamp = None
        self.trade_req_sent_timestamp = None
        self.joined_hideout_timestamp = None

        self.trade_req_attempts = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_trade_info(self, trade_req_msg):

        self._trade_info_lock.acquire()
        if self.name != trade_req_msg.player_name:
            logger.error("Attempted to assign {} to {}".format(
                trade_req_msg, self))
            raise Exception

        self.trade_msq_received_timestamp = time.time()

        self._buy = trade_req_msg.give
        self._sell = trade_req_msg.receive

        self._trade_info_lock.release()

    def get_trade_info(self):
        ''' get the trade info '''
        self._trade_info_lock.acquire()
        temp = (self._buy, self._sell)
        self._trade_info_lock.release()

        return temp

    def invite(self):

        logger.debug("Invited {} to party".format(self.name))
        uiactions.invite_to_party(self.name)
        self.invite_sent_timestamp = time.time()

    def wrong_offer_response(self):
        uiactions.custom_message(self.name, "Sold out !")

    def farewell(self):
        uiactions.custom_message(self.name, "Thanks & Bye !")

    def kick(self):
        uiactions.kick_from_party(self.name)

    def trade_request(self):
        ''' 
            Perform a trade request. 
            Wait to see if the user accepts or declines.
            Retry up to 2 times
        '''

        self.trade_msq_received_timestamp = time.time()
        self.trade_req_attempts += 1

        # Flush queue just in case
        trade_outcome_q.flush()

        success = False

        while self.trade_req_attempts < 3:

            # Send trade request
            uiactions.trade_request(self.name)

            # Wait for either:
            #   - Trade Cancelled message
            #   - Trade window active
            #   - Timeout (5s)
            start_time = time.time()

            while True:

                if TRADE_OUTCOME.DECLINED == trade_outcome_q.get(block=False):
                    success = False
                    break

                if uiactions.check_trade_win_open():
                    success = True
                    break

                if start_time - time.time() > 16000:
                    success = False
                    break

            if success:
                break
            else:
                self.trade_req_attempts += 1

        return success

    def joined_hideout(self):
        self.joined_hideout_timestamp = time.time()
        self._in_hideout_lock.acquire()
        self._in_hideout = True
        self._in_hideout_lock.release()

    def left_hideout(self):
        self.joined_hideout_timestamp = time.time()
        self._in_hideout_lock.acquire()
        self._in_hideout = False
        self._in_hideout_lock.release()

    def is_in_hideout(self):
        self._in_hideout_lock.acquire()
        ret = self._in_hideout
        self._in_hideout_lock.release()
        return ret


players = PlayerList()

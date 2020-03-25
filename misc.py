

''' misc classes, func and exceptions '''

import logging
from queue import Queue, Empty
from enum import Enum
from threading import Thread, Event
from time import sleep, monotonic, time

logger = logging.getLogger('bot_log')


#####################################################################
#                           MISC CLASSES                            #
#####################################################################

class my_queue(Queue):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def put(self, item, block=True, timeout=None):
        super().put(item, block=block, timeout=timeout)

        # logger.debug("{} -> Pushing {}".format(self.name, item))

    def get(self, block=True, timeout=None):

        # If it is non-blocking we don't need to do anything
        item = None
        if not block:
            try:
                item = super().get(block=block, timeout=timeout)
            except Empty:
                pass
        else:
            if timeout is None:
                while True:
                    try:
                        # Allow check for Ctrl-C every second
                        item = super().get(timeout=1)
                        break
                    except Empty:
                        pass

            else:
                stoploop = monotonic() + timeout - 1
                while monotonic() < stoploop:
                    try:
                        # Allow check for Ctrl-C every second
                        item = super().get(timeout=1)
                        break
                    except Empty:
                        pass
                if item:
                    # Final wait for last fraction of a second
                    try:
                        item = super().get(timeout=max(0, stoploop + 1 - monotonic()))
                    except Empty:
                        pass

        # logger.debug("{} -> Poping {}".format(self.name, item))
        return item

    def flush(self):
        # Get all the elements untill we get None (no elements left)
        while self.get(block=False) is not None:
            pass


class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class TRADE_REQ_MSG():

    def __init__(self, player_name, give, receive, stash="", left="", top=""):
        self.player_name = player_name
        self.give = give
        self.receive = receive
        self.stash = stash
        self.left = left
        self.top = top

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "'{} buys {} {} -> {} {}'".format(self.player_name, self.give.ammount, self.give.curr, self.receive.ammount, self.receive.curr)


class PLAYER_JOINED_MSG():

    def __init__(self, player_name, new_status):
        self.player_name = player_name
        self.new_status = new_status


feedback_q = my_queue("Feedback Q")
trade_req_q = my_queue("Trade Req Q")
trade_outcome_q = my_queue("Trade Outcome Q")
player_joined_q = my_queue("Player Joined Q")
afk_mode_q = my_queue("AFK Mode Q")


#####################################################################
#                           MISC FUNC                               #
#####################################################################


def center_of_square(x1, y1, x2, y2):
    return (x1 + (x2 - x1)/2, y1 + (y2 - y1)/2)


def grid_to_point(coords, reference, spacing):

    results = []

    for cord_x, cord_y in coords:
        point_x = reference[0] + cord_x * spacing[0] + spacing[0]/2
        point_y = reference[1] + cord_y * spacing[1] + spacing[1]/2

        results += [[point_x, point_y]]

    return results


def match_point_to_grid(points, reference, spacing, dimensions):

    results = []

    inv_x_0 = reference[0]
    inv_y_0 = reference[1]

    for p_x, p_y in points:

        # print("p_x: {} p_y: {}".format(p_x, p_y))
        rel_x = p_x - inv_x_0
        rel_y = p_y - inv_y_0

        x_pos = rel_x // spacing[0]
        y_pos = rel_y // spacing[1]

        # print("rel_x: {} rel_y: {}".format(rel_x, rel_y))
        # print("x_pos: {} y_pos: {}".format(x_pos, y_pos))

        # Point outside range
        if (x_pos < 0 or y_pos < 0):
            continue
        elif (x_pos > dimensions[0]):
            continue
        elif (y_pos > dimensions[1]):
            continue
        elif ((x_pos, y_pos) not in results):
            results += [(int(x_pos), int(y_pos))]

    results.sort(key=lambda x: x[1])
    results.sort(key=lambda x: x[0])

    return results


def interruptable_acquire(l, timeout=None):

    if timeout is None:
        while not l.acquire(timeout=1):
            pass
        return True
    else:
        stoploop = monotonic() + timeout - 1
        while monotonic() < stoploop:
            try:
                # Allow check for Ctrl-C every second
                return l.acquire(timeout=1)
            except Empty:
                pass
        # Final wait for last fraction of a second
        return l.acquire(timeout=max(0, stoploop + 1 - monotonic()))


#####################################################################
#                           MISC ENUMS                              #
#####################################################################

class AFK_STATUS(Enum):
    OFF = 0
    ON = 1


class TRADE_OUTCOME(Enum):
    ACCEPTED = 0
    DECLINED = 1


class PLAYER_JOINED_STATUS(Enum):
    JOINED = 0
    LEFT = 1
    NOT_JOINED_YET = 2

#####################################################################
#                           MISC EXCEPTIONS                         #
#####################################################################


''' Collections of custom exceptions '''


class CouldNotFindStashException(Exception):
    ''' Could not locate stash !!! '''


class CouldNotOpenStashException(Exception):
    ''' Could not locate stash !!! '''


class CouldNotClearInventoryException(Exception):
    ''' Unable to clear the inventory ! '''


class POENotRuningException(Exception):
    ''' Unable to clear the inventory ! '''


class CouldNotIdentifyItemException(Exception):
    ''' Unable to identify item '''

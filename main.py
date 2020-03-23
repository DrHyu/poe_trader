
import queue
import time
import logging

from log_parser import LogParser
from misc import interruptable_get
from queues import afk_mode_q


LOG_PATH = r'C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs\Client.txt'
# LOG_PATH = r'C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs\testfile.txt'


def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

    log_parser = LogParser(LOG_PATH)

    log_parser.start()

    while True:

        new_msg = interruptable_get(afk_mode_q)

        print("Received msg {}".format(new_msg))

    pass

    print("Main prog ended")


if __name__ == '__main__':
    main()

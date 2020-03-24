
import sys
sys.path.append('../')  # nopep8

import config as cfg
import logging
import cv2
import numpy as np


logger = logging.getLogger(__name__)

PATH = "../assets/stash_templates/currency_tab_mask.png"


def main():

    stash_w = cfg.STASH_TAB_AREA[2] - cfg.STASH_TAB_AREA[0]
    stash_h = cfg.STASH_TAB_AREA[3] - cfg.STASH_TAB_AREA[1]

    mask = np.full((stash_h, stash_w), 0, np.uint8)

    sqr_w_half = cfg.CURR_TAB_X_OFFSET//2
    sqr_h_half = cfg.CURR_TAB_Y_OFFSET//2

    for x, y in cfg.CURR_STASH_TAB_DESCRIPTION:

        x_real = round(x * stash_w)
        y_real = round(y * stash_h)

        mask[y_real - sqr_h_half:y_real + sqr_h_half,
             x_real - sqr_w_half:x_real + sqr_w_half] = 255

    cv2.imwrite(PATH, mask)

    logger.info('Generated currency tab mask at: {}'.format(PATH))


if __name__ == '__main__':

    logger.setLevel(level=logging.DEBUG)
    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)
    main()

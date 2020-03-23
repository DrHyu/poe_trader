''' Helper class to do cv2 stuff '''

import os
import unittest
import time
from datetime import datetime
import shutil
import copy

import cv2
import numpy as np
from scipy.spatial import distance
import pyscreenshot as ImageGrab

import config
import currency

from misc import CouldNotFindStashException

from misc import match_point_to_grid, center_of_square


class VisionHelper():
    ''' Helper class to do cv2 stuff '''

    @staticmethod
    def find_stash():
        ''' try to locate the stash '''

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab())
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/stash_location.png',
            img
        )

        if len(matches) < 1:
            raise CouldNotFindStashException

        return center_of_square(matches[0][0][0], matches[0][0][1], matches[0][1][0], matches[0][1][1])

    @staticmethod
    def get_trade_win_accept_status():
        '''
            Get the status of the accept button in the trade window:
                Locked
                Ready to be pressed
                Pressed
        '''

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_WIN_ACCEPT_BUTTON_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Cannot tell appart between locked and ready
        # locked_matches = VisionHelper.template_match(
        #     'assets/other_templates/trade_window_accept_not_ready.png',
        #     copy.deepcopy(img),
        #     threshold=0.95
        # )
        locked_matches = []
        ready_matches = VisionHelper.template_match(
            'assets/other_templates/trade_window_accept_ready.png',
            copy.deepcopy(img),
            threshold=0.95
        )
        accepted_matches = VisionHelper.template_match(
            'assets/other_templates/trade_window_accept_ready2.png',
            copy.deepcopy(img),
            threshold=0.95
        )

        if len(locked_matches) > 0 and (len(ready_matches) > 0 or len(accepted_matches) > 0):
            return "UNKNOWN"
        elif len(ready_matches) > 0 and (len(locked_matches) > 0 or len(accepted_matches) > 0):
            return "UNKNOWN"
        elif len(accepted_matches) > 0 and (len(ready_matches) > 0 or len(locked_matches) > 0):
            return "UNKNOWN"
        elif len(locked_matches) > 0:
            return "LOCKED"
        elif len(ready_matches) > 0:
            return "READY"
        elif len(accepted_matches) > 0:
            return "ACCEPTED"
        else:
            return "UNKNOWN"

    @staticmethod
    def is_stash_tab_open():
        ''' Check if stash tab is open '''

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.STASH_TAB_ACTIVE_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/stash_active.png',
            img
        )
        return len(matches) > 0

    @staticmethod
    def is_trade_window_open():
        ''' Check if the trade window is currently open '''

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_WIN_ACTIVE_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/trade_window_active.png',
            img
        )
        return len(matches) > 0

    @staticmethod
    def is_trade_req_ongoing():
        ''' Check if the trade request is ongoing '''

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_REQUEST_ACTIVE_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/trade_request_ongoing.png',
            img
        )
        return len(matches) > 0

    @staticmethod
    def find_currency_in_currency_tab(currencies):

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.STASH_TAB_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        results = {}
        for curr in currencies:
            matches = VisionHelper.template_match(
                curr.template_path,
                copy.deepcopy(img)
            )
            temp = []
            for match in matches:

                (x, y) = center_of_square(match[0][0],
                                          match[0][1],
                                          match[1][0],
                                          match[1][1])

                temp += [(x + config.STASH_TAB_AREA[0],
                          y + config.STASH_TAB_AREA[1])]
            results[curr.name] = temp

        return results

    @staticmethod
    def find_currency_in_inventory(currencies):

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.INVENTORY_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        results = {}
        for curr in currencies:
            matches = VisionHelper.template_match(
                curr.template_path,
                # copy.deepcopy(img)
                # Not passing deep copy on purpose
                # This way the markings of other found currencies will persist
                img,
                resize=1.25
            )

            temp = []
            for match in matches:

                (x, y) = center_of_square(match[0][0],
                                          match[0][1],
                                          match[1][0],
                                          match[1][1])

                temp += [(x + config.INVENTORY_AREA[0],
                          y + config.INVENTORY_AREA[1])]
            results[curr.name] = temp

        return results

    @staticmethod
    def find_empty_slots_in_inventory2():

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.INVENTORY_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/empty_slot.png',
            # copy.deepcopy(img)
            # Not passing deep copy on purpose
            # This way the markings of other found currencies will persist
            img,
        )

        points = []
        for (x1, y1), (x2, y2) in matches:
            points += [[x1 + config.INVENTORY_AREA[0],
                        y1 + config.INVENTORY_AREA[1]]]

            points += [[x2 + config.INVENTORY_AREA[0],
                        y1 + config.INVENTORY_AREA[1]]]

            points += [[x2 + config.INVENTORY_AREA[0],
                        y2 + config.INVENTORY_AREA[1]]]

            points += [[x1 + config.INVENTORY_AREA[0],
                        y2 + config.INVENTORY_AREA[1]]]

        return match_point_to_grid(points,
                                   config.INVENTORY_POS_0_0,
                                   (config.NORMAL_TAB_X_OFFSET,
                                    config.NORMAL_TAB_Y_OFFSET),
                                   (config.INV_NUM_ROW, config.INV_NUM_COL)
                                   )

    @staticmethod
    def find_empty_slots_in_inventory():

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.INVENTORY_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/empty_slot3.png',
            copy.deepcopy(img)
        )

        points = []
        for (x1, y1), (x2, y2) in matches:
            points += [[x1 + ((x2 - x1)/2) + config.INVENTORY_AREA[0],
                        y1 + ((y2 - y1)/2) + config.INVENTORY_AREA[1]]]

        return match_point_to_grid(points,
                                   config.INVENTORY_POS_0_0,
                                   (config.NORMAL_TAB_X_OFFSET,
                                    config.NORMAL_TAB_Y_OFFSET),
                                   (config.INV_NUM_ROW, config.INV_NUM_COL)
                                   )

    @staticmethod
    def find_empty_slots_in_trade_win():

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_WIN_ITEMS_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/empty_slot3.png',
            copy.deepcopy(img)
            # Not passing deep copy on purpose
            # This way the markings of other found currencies will persist
            # img,
        )

        points = []
        for (x1, y1), (x2, y2) in matches:
            points += [[x1 + ((x2 - x1)/2) + config.TRADE_WIN_ITEMS_AREA[0],
                        y1 + ((y2 - y1)/2) + config.TRADE_WIN_ITEMS_AREA[1]]]

        return match_point_to_grid(points,
                                   config.TRADE_WIN_POS_0_0,
                                   (config.NORMAL_TAB_X_OFFSET,
                                    config.NORMAL_TAB_Y_OFFSET),
                                   (config.INV_NUM_ROW, config.INV_NUM_COL)
                                   )

    @staticmethod
    def find_currency_in_tradewindow(currencies):

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_WIN_ITEMS_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        results = {}
        for curr in currencies:
            matches = VisionHelper.template_match(
                curr.template_path,
                # copy.deepcopy(img)
                # Not passing deep copy on purpose
                # This way the markings of other found currencies will persist
                img,
                resize=1.25
            )
            results[curr.name] = matches

        return results

    @staticmethod
    def template_match(template, target,
                       threshold=0.8,
                       distance_cutoff=(config.NORMAL_TAB_X_OFFSET/2 - 1),
                       log_name="match_output/template_match",
                       resize=None):
        ''' Match a given template onto a target img '''

        assert os.path.exists(template)

        # If giving path to img
        if isinstance(target, str):
            assert os.path.exists(target)
            target_color = cv2.imread(target)
        # If giving the actual image
        else:
            target_color = target

        target_gray = cv2.cvtColor(target_color, cv2.COLOR_BGR2GRAY)

        template_gray = cv2.imread(template, cv2.IMREAD_GRAYSCALE)

        # Resize template if requested
        if resize is not None:
            width = int(template_gray.shape[1] * resize)
            height = int(template_gray.shape[0] * resize)
            dsize = (width, height)

            template_gray = cv2.resize(template_gray, dsize)

        width, height = template_gray.shape[::-1]

        res = cv2.matchTemplate(
            target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        coordinates_found = []

        for point in zip(*loc[::-1]):

            # Remove matches too close to eachother
            skip = False
            for (X, Y), (_, _) in coordinates_found:
                if distance.euclidean([X, Y], point) < distance_cutoff:
                    skip = True
                    break
            if skip:
                continue

            cv2.rectangle(target_color, point,
                          (point[0] + width, point[1] + height), (0, 0, 255), 2)

            coordinates_found.append(
                [[point[0], point[1]], [point[0] + width, point[1] + height]]
            )

        cv2.imwrite('{}_{}.png'.format(
            log_name, datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S_%f")), target_color)

        return coordinates_found


class VisionHelperTest(unittest.TestCase):
    ''' Tests for VisionHelper '''

    def test_find_all_currencies_in_stash_tab(self):
        ''' Find all currencies in a stash tab '''

        print("")
        test_output_folder = 'test_output/test_find_all_currencies_in_stash_tab'
        if not os.path.exists(test_output_folder):
            os.mkdir(test_output_folder)
        else:
            VisionHelperTest.cleanup_previous_results(test_output_folder)

        img = cv2.imread('test_files/test_currencies_in_stash.png')

        x1 = config.STASH_TAB_AREA[0]
        y1 = config.STASH_TAB_AREA[1]
        x2 = config.STASH_TAB_AREA[2]
        y2 = config.STASH_TAB_AREA[3]

        crop_img = img[y1:y2, x1:x2]

        results = {}
        for c in currency.CURRENCY_LIST:
            print("Looking for {}".format(c.pretty_name), end=" ")
            matches = VisionHelper.template_match(
                c.template_path,
                copy.deepcopy(crop_img),
                threshold=0.9,
                log_name="{}/{}".format(test_output_folder, c.name))

            if len(matches) == 1:
                print("- OK")
            else:
                print("- FAILED")

            results[c.name] = matches

        for c in currency.CURRENCY_LIST:
            self.assertEqual(len(results[c.name]), 1)

    def test_find_all_currencies_in_inventory(self):
        ''' Find all currencies in a inventory '''

        print("")
        test_output_folder = 'test_output/test_find_all_currencies_in_inventory'
        if not os.path.exists(test_output_folder):
            os.mkdir(test_output_folder)
        else:
            VisionHelperTest.cleanup_previous_results(test_output_folder)

        img = cv2.imread('test_files/test_currencies_in_inventory.png')

        x1 = config.INVENTORY_AREA[0]
        y1 = config.INVENTORY_AREA[1]
        x2 = config.INVENTORY_AREA[2]
        y2 = config.INVENTORY_AREA[3]

        crop_img = img[y1:y2, x1:x2]

        results = {}
        for c in currency.CURRENCY_LIST:
            print("Looking for {}".format(c.pretty_name), end=" ")
            matches = VisionHelper.template_match(
                c.template_path,
                copy.deepcopy(crop_img),
                threshold=0.8,
                log_name="{}/{}".format(test_output_folder, c.name),
                resize=1.25)

            if len(matches) == 1:
                print("- OK")
            else:
                print("- FAILED")

            results[c.name] = matches

        for c in currency.CURRENCY_LIST:
            self.assertEqual(len(results[c.name]), 1)

    def test_find_all_currencies_in_trade_window(self):
        ''' Find all currencies in a trade_window '''

        print("")
        test_output_folder = 'test_output/test_find_all_currencies_in_trade_window'
        if not os.path.exists(test_output_folder):
            os.mkdir(test_output_folder)
        else:
            VisionHelperTest.cleanup_previous_results(test_output_folder)

        img = cv2.imread('test_files/test_currencies_in_trade_window.png')

        x1 = config.TRADE_WIN_ITEMS_AREA[0]
        y1 = config.TRADE_WIN_ITEMS_AREA[1]
        x2 = config.TRADE_WIN_ITEMS_AREA[2]
        y2 = config.TRADE_WIN_ITEMS_AREA[3]

        crop_img = img[y1:y2, x1:x2]

        results = {}
        for c in currency.CURRENCY_LIST:
            print("Looking for {}".format(c.pretty_name), end=" ")
            matches = VisionHelper.template_match(
                c.template_path,
                copy.deepcopy(crop_img),
                threshold=0.8,
                log_name="{}/{}".format(test_output_folder, c.name),
                resize=1.25)

            if len(matches) == 1:
                print("- OK")
            else:
                print("- FAILED")

            results[c.name] = matches

        for c in currency.CURRENCY_LIST:
            self.assertEqual(len(results[c.name]), 1)

    def test_custom(self):
        # print(VisionHelper.get_trade_win_accept_status())

        res = VisionHelper.find_empty_slots_in_trade_win()

        # print(res)
        # res.sort(key=lambda x: x[1])
        # res.sort(key=lambda x: x[0])

        for p in res:
            print(p)
        # result = VisionHelper.find_currency_in_tradewindow(
        #     currency.CURRENCY_LIST)

        # for c in result:
        #     print("{}  {}".format(c, result[c]))

    @staticmethod
    def cleanup_previous_results(folder):

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':

    # Run tests
    unittest.main()

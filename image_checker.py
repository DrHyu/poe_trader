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

from inventory_model import inventory, StashTab
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
        # locked_matches = VisionHelper.template_match_currency(
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
    def find_currency_in_stash_tab(currencies, tab):

        if tab.kind == StashTab.CURRENCY_TAB_KIND:
            return VisionHelper.find_currency_in_currency_tab(currencies)
        elif tab.kind == StashTab.NORMAL_TAB_KIND:
            return VisionHelper.find_currency_in_normal_tab(currencies)
        else:
            raise Exception

    @staticmethod
    def find_currency_in_normal_tab(currencies):

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.STASH_TAB_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        results = {}
        for curr in currencies:
            matches = VisionHelper.template_match_currency(
                curr.template_path,
                copy.deepcopy(img),
                resize=config.NORMAL_STASH_TEMPLATE_RESIZE_FACTOR,
                log_name='match_output/' + curr.name
            )
            temp = []
            for (x, y) in matches:
                temp += [(x + config.CURR_TAB_X_OFFSET//2 + config.STASH_TAB_AREA[0],
                          y + config.CURR_TAB_Y_OFFSET//2 + config.STASH_TAB_AREA[1])]

            results[curr.name] = temp

        return results

    @staticmethod
    def find_currency_in_currency_tab(currencies):

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.STASH_TAB_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Mask the currency tab to only show currency and not background
        mask = cv2.imread('assets/stash_templates/currency_tab_mask.png', -1)
        img[mask == 0] = (255, 255, 255)

        results = {}
        for curr in currencies:
            matches = VisionHelper.template_match_currency(
                curr.template_path,
                copy.deepcopy(img),
                resize=config.CURR_STASH_TEMPLATE_RESIZE_FACTOR,
                log_name='match_output/' + curr.name
            )
            temp = []
            for (x, y) in matches:
                temp += [(x + config.CURR_TAB_X_OFFSET//2 + config.STASH_TAB_AREA[0],
                          y + config.CURR_TAB_Y_OFFSET//2 + config.STASH_TAB_AREA[1])]

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
            matches = VisionHelper.template_match_currency(
                curr.template_path,
                copy.deepcopy(img),
                resize=config.INVENTORY_TEMPLATE_RESIZE_FACTOR,
                log_name='match_output/' + curr.name
            )

            temp = []
            for (x, y) in matches:
                temp += [(x + config.CURR_TAB_X_OFFSET//2 + config.STASH_TAB_AREA[0],
                          y + config.CURR_TAB_Y_OFFSET//2 + config.STASH_TAB_AREA[1])]
            results[curr.name] = temp

        return results

    @staticmethod
    def find_currency_in_tradewindow(currencies):

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_WIN_ITEMS_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        results = {}
        for curr in currencies:
            matches = VisionHelper.template_match_currency(
                curr.template_path,
                copy.deepcopy(img),
                resize=config.TRADE_WINDOW_TEMPLATE_RESIZE_FACTOR,
                log_name='match_output/' + curr.name
            )

            temp = []
            for (x, y) in matches:
                temp += [(x + config.CURR_TAB_X_OFFSET//2 + config.STASH_TAB_AREA[0],
                          y + config.CURR_TAB_Y_OFFSET//2 + config.STASH_TAB_AREA[1])]
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

        cv2.imshow("", img)
        cv2.waitKey()
        return match_point_to_grid(points,
                                   config.INVENTORY_POS_0_0,
                                   (config.NORMAL_TAB_X_OFFSET,
                                    config.NORMAL_TAB_Y_OFFSET),
                                   (config.INV_NUM_ROW, config.INV_NUM_COL)
                                   )

    @staticmethod
    def find_empty_slots_in_inventory3():

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
    def find_empty_slots_in_inventory():

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.INVENTORY_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # change the blue item background to white
        # 2-4 2-4 28-32
        c = np.all((img >= (28, 2, 2)) & (img <= (32, 5, 5)), axis=2)
        img[c] = (255, 255, 255)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, gray = cv2.threshold(gray, 10, 255, 0)

        contours, _ = cv2.findContours(
            gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cell_area = config.NORMAL_TAB_X_OFFSET * config.NORMAL_TAB_Y_OFFSET

        empty_cells = []
        for contour in contours:
            contour_area = cv2.contourArea(contour)

            if (cell_area * 0.6) < contour_area < (cell_area * 1.4):

                (x, y, w, h) = cv2.boundingRect(contour)
                white_ratio = cv2.countNonZero(gray[y:y+h, x:x+w])/contour_area

                # print("Cnt:{} area {} white {} ".format(
                #     contour, cv2.contourArea(contour), white_ratio))

                if white_ratio < 0.3:
                    empty_cells += [[x + w/2 + config.INVENTORY_AREA[0],
                                     y + h/2 + config.INVENTORY_AREA[1]]]
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)

        empty_inv_slots = match_point_to_grid(
            empty_cells,
            config.INVENTORY_POS_0_0,
            (config.NORMAL_TAB_X_OFFSET, config.NORMAL_TAB_Y_OFFSET),
            (config.INV_NUM_ROW, config.INV_NUM_COL)
        )

        # Remove possible duplicates
        return list(dict.fromkeys(empty_inv_slots))

    @staticmethod
    def find_empty_slots_in_trade_win():

        # Take a screenshot of the relevant area
        img = np.array(ImageGrab.grab(
            bbox=config.TRADE_WIN_ITEMS_AREA))
        # PIL is RGB cv2 is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # change the blue item background to white
        # 2-4 2-4 28-32
        c = np.all((img >= (28, 2, 2)) & (img <= (32, 5, 5)), axis=2)
        img[c] = (255, 255, 255)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, gray = cv2.threshold(gray, 10, 255, 0)

        contours, _ = cv2.findContours(
            gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cell_area = config.NORMAL_TAB_X_OFFSET * config.NORMAL_TAB_Y_OFFSET

        empty_cells = []
        for contour in contours:
            contour_area = cv2.contourArea(contour)

            if (cell_area * 0.6) < contour_area < (cell_area * 1.4):

                (x, y, w, h) = cv2.boundingRect(contour)
                white_ratio = cv2.countNonZero(gray[y:y+h, x:x+w])/contour_area

                # print("Cnt:{} area {} white {} ".format(
                #     contour, cv2.contourArea(contour), white_ratio))

                if white_ratio < 0.3:
                    empty_cells += [[x + w/2 + config.INVENTORY_AREA[0],
                                     y + h/2 + config.INVENTORY_AREA[1]]]
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)

        empty_inv_slots = match_point_to_grid(
            empty_cells,
            config.INVENTORY_POS_0_0,
            (config.NORMAL_TAB_X_OFFSET, config.NORMAL_TAB_Y_OFFSET),
            (config.INV_NUM_ROW, config.INV_NUM_COL)
        )

        # Remove possible duplicates
        return list(dict.fromkeys(empty_inv_slots))

    @staticmethod
    def find_set_price_window(test_img=None):
        ''' Find the location of the set price window '''

        if test_img:
            img = cv2.imread(test_img, -1)
        else:
            # Take a screenshot of the relevant area
            img = np.array(ImageGrab.grab())
            # PIL is RGB cv2 is BGR
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        matches = VisionHelper.template_match(
            'assets/other_templates/set_price_template2.png',
            img,
            threshold=0.7,
        )

        return matches

    @staticmethod
    def template_match_currency(template, target,
                                threshold=0.9,
                                distance_cutoff=(
                                    config.NORMAL_TAB_X_OFFSET/2 - 1),
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
        template_full = cv2.imread(template, -1)

        # Resize template if requested
        if resize is not None:
            height = int(template_full.shape[0] * resize)
            width = int(template_full.shape[1] * resize)
            dsize = (width, height)

            template_full = cv2.resize(template_full, dsize)

        orig_h, orig_w, _ = template_full.shape

        # make mask of where the transparent bits are
        trans_area = template_full[:, :, 3] < 90
        template_full[trans_area] = (40, 5, 3, 255)

        template_gray = cv2.cvtColor(template_full, cv2.COLOR_BGRA2GRAY)

        # Change the 0 alpha regions to a suitable background

        ####################################################
        # NO MASK WAY
        ####################################################
        template_gray_no_mask = template_gray[(orig_h*50)//100:, :]

        height, width = template_gray_no_mask.shape

        no_mask_res = cv2.matchTemplate(
            target_gray, template_gray_no_mask, cv2.TM_CCOEFF_NORMED)

        loc = np.where(no_mask_res >= threshold)

        coordinates_found_no_mask = []

        for (px, py) in zip(*loc[::-1]):
            # Remove matches too close to eachother
            skip = False

            py -= (orig_h - height)

            for X, Y in coordinates_found_no_mask:

                if distance.euclidean([X, Y], (px, py)) < distance_cutoff:
                    skip = True
                    break
            if skip:
                continue

            cv2.rectangle(target_color, (px, py),
                          (px + width, py + height), (0, 0, 255), 2)

            coordinates_found_no_mask.append(
                [px, py])

        ####################################################

        ####################################################
        # MASK WAY
        ####################################################

        height, width = template_gray.shape
        mask = np.full((height, width), 255, np.uint8)

        # Mask Numbers area 70 % with 50 % heigh
        mask[0:(height*50)//100,
             0:(width*85) // 100] = 0

        mask_res = cv2.matchTemplate(
            target_gray, template_gray, cv2.TM_CCORR_NORMED, mask=mask)
        loc2 = np.where(mask_res >= threshold)

        coordinates_found_w_mask = []

        for point in zip(*loc2[::-1]):
            # Remove matches too close to eachother
            skip = False
            for X, Y in coordinates_found_w_mask:
                if distance.euclidean([X, Y], point) < distance_cutoff:
                    skip = True
                    break
            if skip:
                continue
            cv2.rectangle(target_color, point,
                          (point[0] + width, point[1] + height), (0, 0, 255), 2)

            coordinates_found_w_mask.append([point[0], point[1]])

        ####################################################
        # Merge the results of both searches #
        ####################################################

        result = []
        if len(coordinates_found_w_mask) == 0 and len(coordinates_found_no_mask) == 0:
            pass
        elif len(coordinates_found_w_mask) == 0 and len(coordinates_found_no_mask) == 1:
            result.append(coordinates_found_no_mask[0])
        elif len(coordinates_found_w_mask) == 1 and len(coordinates_found_no_mask) == 0:
            result.append(coordinates_found_w_mask[0])
        else:
            # If there is a cooincidence match the together
            for no_mask in coordinates_found_no_mask:
                for mask in coordinates_found_w_mask:
                    if distance.euclidean(no_mask, mask) < distance_cutoff:
                        result += [[(no_mask[0]+mask[0])//2,
                                    (no_mask[1]+mask[1])//2]]

        for point in result:
            cv2.rectangle(target_color,
                          (point[0], point[1]),
                          (point[0] + width, point[1] + height),
                          (255, 0, 0),
                          2)

        cv2.imwrite('{}_{}.png'.format(
            log_name, datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S_%f")), target_color)

        return result

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

        # Mask the currency tab to only show currency and not background
        mask = cv2.imread('assets/stash_templates/currency_tab_mask.png', -1)
        crop_img[mask == 0] = (255, 255, 255)

        results = {}
        for c in currency.CURRENCY_LIST:
            print("Looking for {}".format(c.pretty_name), end=" ")
            matches = VisionHelper.template_match_currency(
                c.template_path,
                copy.deepcopy(crop_img),
                threshold=0.9,
                resize=0.9,
                log_name="{}/{}".format(test_output_folder, c.name))

            if len(matches) == 1:
                print("- OK")
            else:
                print("- FAILED")

            results[c.name] = matches

        ok = 0
        for c in currency.CURRENCY_LIST:
            if len(results[c.name]) == 1:
                ok += 1

        print("TOTAL {}/{}".format(ok, len(results)))

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

        # Mask the currency tab to only show currency and not background
        # mask = cv2.imread('assets/stash_templates/currency_tab_mask.png', -1)
        # crop_img[mask == 0] = (255, 255, 255)

        results = {}
        for c in currency.CURRENCY_LIST:
            print("Looking for {}".format(c.pretty_name), end=" ")
            matches = VisionHelper.template_match_currency(
                c.template_path,
                copy.deepcopy(crop_img),
                threshold=0.9,
                resize=1.125,
                log_name="{}/{}".format(test_output_folder, c.name))

            if len(matches) == 1:
                print("- OK")
            else:
                print("- FAILED")

            results[c.name] = matches

        ok = 0
        for c in currency.CURRENCY_LIST:
            if len(results[c.name]) == 1:
                ok += 1

        print("TOTAL {}/{}".format(ok, len(results)))

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

        # Mask the currency tab to only show currency and not background
        # mask = cv2.imread('assets/stash_templates/currency_tab_mask.png', -1)
        # crop_img[mask == 0] = (255, 255, 255)

        results = {}
        for c in currency.CURRENCY_LIST:
            print("Looking for {}".format(c.pretty_name), end=" ")
            matches = VisionHelper.template_match_currency(
                c.template_path,
                copy.deepcopy(crop_img),
                threshold=0.9,
                resize=1.125,
                log_name="{}/{}".format(test_output_folder, c.name))

            if len(matches) == 1:
                print("- OK")
            else:
                print("- FAILED")

            results[c.name] = matches

        ok = 0
        for c in currency.CURRENCY_LIST:
            if len(results[c.name]) == 1:
                ok += 1

        print("TOTAL {}/{}".format(ok, len(results)))

        for c in currency.CURRENCY_LIST:
            self.assertEqual(len(results[c.name]), 1)

    def test_custom(self):
        # print(VisionHelper.get_trade_win_accept_status())
        print(VisionHelper.find_set_price_window(
            'test_files/test_set_price_template2.png'))
        # print(VisionHelper.find_set_price_window())

        # print(VisionHelper.find_empty_slots_in_inventory())
        # emtpy_cells2 = VisionHelper.find_empty_slots_in_inventory2()

        # exit()
        # res = VisionHelper.find_empty_slots_in_trade_win()

        # print(res)
        # res.sort(key=lambda x: x[1])
        # res.sort(key=lambda x: x[0])

        # for p in res:
        #     print(p)
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

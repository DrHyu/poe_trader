''' Contains all the user actions a bot will perform '''

import time
import unittest
import logging
import re
import random
import copy

import win32gui
import win32clipboard

import pyautogui as autogui
from image_checker import VisionHelper as vh

from inventory_model import inventory, bank, client_trade_window

import config
import currency
from misc import CouldNotOpenStashException, CouldNotClearInventoryException,\
    POENotRuningException, CouldNotIdentifyItemException


logger = logging.getLogger('bot_log')


class ActionsHelper():
    ''' Helper for UI actions '''

    def __init__(self):
        self._handle = None

        self.find_window("Path Of Exile")

        if self._handle is None:
            raise POENotRuningException

    ###################################
    # win32 gui stuff
    ###################################

    def find_window(self, window_name):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(None, window_name)
        logger.debug(
            "POE window found with hwnd: {}".format(self._handle))

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
        logger.debug(
            "POE window ({}) brought to foreground".format(self._handle))

        # Click at 0,0 to unlock game
        autogui.moveTo(1, 1)

    def is_foreground(self, set_foreground=False):
        ''' check if poe is currently in foreground '''

        active_hwnd = win32gui.GetForegroundWindow()

        if active_hwnd == self._handle:
            return True
        elif not set_foreground:
            return False
        else:
            # Bring it to foreground
            self.set_foreground()

            # Check again
            if not self.is_foreground():
                raise POENotRuningException

            return True

    ###################################
    # win32 clipboard stuff
    ###################################

    def get_clipboard_text(self):

        max_retries = 3
        retries = 0
        done = False

        while not done:
            try:
                # Attempt to open clipboard
                win32clipboard.OpenClipboard()
                done = True

            except Exception as exception:
                if retries > max_retries:
                    raise exception
                else:
                    logger.debug(
                        "Failed to get clipboard, retrying {}/{}".format(retries, max_retries))
                    retries += 1
                    time.sleep(0.5)
        try:
            text = win32clipboard.GetClipboardData(
                win32clipboard.CF_TEXT).decode("utf-8")
        except:
            text = ""

        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()

        return text

    ###################################
    # autogui stuff
    ###################################

    def get_text_at_position(self, pos, reset_mouse=True):

        autogui.moveTo(*pos)
        autogui.hotkey('ctrl', 'c')
        # Reset mouse to avoid screen polution
        if reset_mouse:
            autogui.moveTo(1, 1)

        return self.get_clipboard_text()

    def transfer_currency_stash_inv(self, curr, ammount):
        '''
            Takes a list of currencies to be transfered into the inventory.
            Will take care of ammounts that are not aligned with stack size.
        '''

        # Check we are in foreground, set otherwise
        self.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        self.check_stash_open(open_otherwise=True)

        # Find the position of this currency in stash
        matches = vh.find_currency_in_currency_tab([curr])
        matches = matches[curr.name]

        # Check if it is possible
        if not bank.withdraw(currency.CurrencyStack(curr, ammount)):
            raise Exception

        t_ammount_left = ammount

        for match in matches:

            # Read at that position
            (found_curr, f_ammount_left) = self.process_item_description(
                self.get_text_at_position(match, reset_mouse=False))

            if found_curr != curr:
                logger.error(
                    "Find mismatch ! Expected {} found {}".format(curr, found_curr))
                raise Exception

            # While we didnt finish or we didn't run out of currency here
            while (t_ammount_left > 0) and (f_ammount_left > 0):

                transfer_size = 0
                # Eg 5c left here and need to transfer 6c (stack size is 10)
                # Eg 11c left here and need to transfer 16c (stack size is 10) - Wouldn't work
                if (f_ammount_left < t_ammount_left) and (f_ammount_left < curr.stack_size):
                    transfer_size = f_ammount_left
                # Eg 50c left here and need to transfer 60c (stack size is 10)
                elif t_ammount_left > curr.stack_size:
                    transfer_size = curr.stack_size
                # Eg 50c left here and need to transfer 6c (stack size is 10)
                elif t_ammount_left <= curr.stack_size:
                    transfer_size = t_ammount_left

                # The transfer function will asume that if we are transfering less than a full stack
                # we will do it 'by hand' and not by control + click. Since it
                # This is the case most of the time. There is a corner case where we are transfering
                # less than a full stack and exactly the ammount left on the stash. In that case we have to
                # ctrl + click.
                force_ctrl_click = (transfer_size == f_ammount_left)
                (result, new_cell) = inventory.transfer(
                    currency.CurrencyStack(found_curr, transfer_size), force_ctrl_click=force_ctrl_click)

                if not result:
                    print(result)
                    print(new_cell)
                    print(inventory.dump())
                    print(bank.contents)
                    raise Exception

                # Can ctrl+click to transfer full stack
                if transfer_size == curr.stack_size or transfer_size == f_ammount_left:
                    # Transfer found_ammount of found_curr into inv
                    autogui.moveTo(*match)
                    autogui.keyDown('ctrl')
                    autogui.click()
                    autogui.keyUp('ctrl')
                # Need to split the stack
                else:
                    autogui.moveTo(*match)
                    autogui.keyDown('shift')
                    autogui.click()
                    autogui.keyUp('shift')

                    time.sleep(0.2)
                    # Split currency
                    autogui.typewrite(str(transfer_size))
                    time.sleep(0.2)
                    # Confirm
                    autogui.press('enter')

                    # Find next empty slot
                    autogui.moveTo(
                        *inventory.to_screen_position(*new_cell))

                    # Drop the currency
                    autogui.click()

                # Update remaining
                t_ammount_left -= transfer_size

        if t_ammount_left != 0:
            raise Exception

    def transfer_currency_inv_trade(self, ensure=False):
        '''
            Takes a list of positions in the inventory.
            The items in that positions will be ctrl + clicked to the trade window.
        '''

        # Check we are in foreground, set otherwise
        self.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        if not self.check_trade_win_open():
            logger.error(
                'Attempted to transfer from inventory to trade but trade window is not open !')
            raise Exception

        autogui.keyDown('ctrl')
        for item in inventory.iter():

            pos = inventory.to_screen_position(*item)
            autogui.moveTo(*pos)
            autogui.click()

        autogui.keyUp('ctrl')
        autogui.moveTo(1, 1)

    def accept_trade(self):
        ''' click the accept trade button '''

        if not self.check_trade_win_open():
            logger.error(
                'Attempted to accept trade but trade window is not open !')
            raise Exception

        if vh.get_trade_win_accept_status() == "ACCEPTED":
            logger.info(
                'Attempted to accept trade but trade is already accepted !')
            return True

        autogui.moveTo(*config.TRADE_WIN_ACCEPT_BUTTON_POS)
        autogui.click()
        autogui.moveTo(1, 1)

        return True

        # if vh.get_trade_win_accept_status() != "ACCEPTED":
        #     logger.info(
        #         'Failed to click accept button, probably customer not ready !')
        #     return False
        # else:
        #     logger.info(
        #         'Accept trade button clicked sucesfully !')
        #     return True

    def cancel_trade(self, ensure=False):
        ''' click the cancel trade button '''

        if not self.check_trade_win_open():
            logger.warning(
                'Attempted to close trade winow but it is not open !')

        autogui.moveTo(*config.TRADE_WIN_CANCEL_BUTTON_POS)
        autogui.click()
        autogui.moveTo(1, 1)

        return self.check_trade_win_open()

    def browse_over_customer_items(self):
        ''' move mouse over customer items so trade can be performed '''

        autogui.moveTo(*config.TRADE_WIN_POS_0_0)

        for col in range(config.INV_NUM_COL):
            autogui.moveTo(
                config.TRADE_WIN_POS_0_0[0],
                config.TRADE_WIN_POS_0_0[1] +
                col * config.NORMAL_TAB_Y_OFFSET +
                config.NORMAL_TAB_Y_OFFSET/2,
                0.3)

            autogui.moveTo(
                config.TRADE_WIN_POS_0_0[0] +
                config.NORMAL_TAB_X_OFFSET * config.INV_NUM_ROW,
                config.TRADE_WIN_POS_0_0[1] + col * config.NORMAL_TAB_Y_OFFSET +
                config.NORMAL_TAB_Y_OFFSET/2,
                0.3)

        autogui.moveTo(1, 1)

    def wiggle_mouse(self):
        autogui.moveTo(1, 2)
        autogui.moveTo(1, 1)
    ###################################
    # chat stuff
    ###################################

    def invite_to_party(self, player_name):
        ''' invite player to party through chat command '''

        autogui.press('enter')
        message = '/invite {}'.format(player_name)
        autogui.typewrite(message)
        autogui.press('enter')

        logger.info("Invited {} to party".format(player_name))

    def kick_from_party(self, player_name):
        ''' kick player from party through chat command '''

        autogui.press('enter')
        message = '/kick {}'.format(player_name)
        autogui.typewrite(message)
        autogui.press('enter')

        logger.info("Kicked {} from party".format(player_name))

    def custom_message(self, player_name, custom):
        ''' send custom message '''

        autogui.press('enter')
        message = '@{} '.format(player_name)
        autogui.typewrite(message)
        autogui.typewrite(custom)
        autogui.press('enter')

        logger.debug("Sent {} to {}".format(custom, player_name))

    def trade_request(self, player_name):
        ''' request a trade request with player '''

        autogui.press('enter')
        message = '/tradewith {}'.format(player_name)
        autogui.typewrite(message)
        autogui.press('enter')

    def veryfy_message_sent(self, message, queue):
        ''' wait to read message just sent on client.txt '''

        new_msg = queue.get(timeout=2)
        print(new_msg)
        print(message)
        return new_msg == message

    ###################################
    # vision stuff
    ###################################

    def check_stash_open(self, open_otherwise=False):
        # Check stash open

        if vh.is_stash_tab_open():
            return True
        elif not open_otherwise:
            return False
        else:
            logger.debug("Stash is closed")

            # Try to open otherwise
            stash_pos = vh.find_stash()
            logger.debug("Found stash @ {}".format(stash_pos))

            # Click on stash position
            autogui.moveTo(*stash_pos)
            time.sleep(0.5)
            autogui.click()
            # Reset mouse to avoid screen polution
            autogui.moveTo(1, 1)

            # Wait
            time.sleep(2)

            if not vh.is_stash_tab_open():
                raise CouldNotOpenStashException
            else:
                logger.debug("Stash is open")

    def check_trade_win_open(self):
        ''' ensure trade window is open '''

        return vh.is_trade_window_open()

    def trade_window_accept_button_status(self):
        return vh.get_trade_win_accept_status()

    ###################################
    # other
    ###################################

    def clean_inventory(self, force_sync=False, expected_items=None):
        '''
            Transfer back all items from inventory to stash.
            Move any trash item to recycle bin.
        '''

        # Check we are in foreground, set otherwise
        self.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        self.check_stash_open(open_otherwise=True)

        # Check if the inventory is synchronized
        if not inventory.synchronzed or force_sync:
            self.sync_inventory()

        autogui.keyDown('ctrl')

        for slot in inventory.iter():

            # Get item stack
            currency_stack = copy.deepcopy(inventory.get(*slot))

            # Request bank diposit
            if not bank.deposit(currency_stack):
                # bank is full or something went wrong
                raise CouldNotClearInventoryException

            else:
                # Transfer
                (point_x, point_y) = inventory.to_screen_position(*slot)
                logger.debug(
                    "Stashing item at ({},{})".format(*slot))
                autogui.moveTo(point_x, point_y)
                autogui.click()

                # Clear item from inventory
                inventory.clear(*slot)

        autogui.keyUp('ctrl')
        # Reset mouse to avoid screen polution
        autogui.moveTo(1, 1)

        # The picture gets disturbed by game notifications
        # Double check to make sure it is empty
        # empty_slots = vh.find_empty_slots_in_inventory()

        # if len(empty_slots) != (config.INV_NUM_ROW * config.INV_NUM_COL):
        #     raise CouldNotClearInventoryException

        return True

    def list_currency_trade_window(self):
        ''' generate a list of all the currencies in the trade window '''

        # Check we are in foreground, set otherwise
        self.is_foreground(set_foreground=True)

        # Check if trade window is open
        if not self.check_trade_win_open():
            logger.warning(
                'Attempted to list trade window contents, but trade window is not open !')
            return {}

        # Find empty slots in inventory
        empty_slots = vh.find_empty_slots_in_trade_win()

        full_slots = []
        # Find the non-empty slots
        for row in range(client_trade_window.num_rows):
            for col in range(client_trade_window.num_cols):
                if (row, col) not in empty_slots:
                    full_slots += [[row, col]]

        currencies = {}
        for slot in full_slots:
            # get item description
            item_description = self.get_text_at_position(
                client_trade_window.to_screen_position(*slot), reset_mouse=False)

            # classify description
            (curr, ammount) = self.process_item_description(item_description)

            if curr == "" and ammount == "":
                # Empty slot
                pass
            elif curr and ammount:
                if curr.name in currencies:
                    currencies[curr.name] += ammount
                else:
                    currencies[curr.name] = ammount
            else:
                if 'unknown' in currencies:
                    currencies['unknown'] += 1
                else:
                    currencies['unknown'] = 1

        # Reset Mouse Position
        autogui.moveTo(1, 1)

        logger.debug("Trade window scan:{}".format(currencies))

        return currencies

    def process_item_description(self, text):
        '''
            Only working for currencies
            Input: Item description from 'Ctrl+C' an Item in POE
            Output: Tuplpe(CurrencyClass, Ammount)
        '''
        match = re.match(
            'Rarity: Currency\r?\n(?P<curr_name>[^\r\n]+)\r?\n--------\r?\nStack Size: (?P<ammount>\d+)/\d+',
            text)

        if match is not None:
            # Try to identify the currency
            for curr in currency.CURRENCY_LIST:
                if re.match(curr.regex, match.group('curr_name')):
                    return (curr, int(float(match.group('ammount'))))

        elif text == "":
            return ("", "")

        # Text did not match currency template or currency could not be identified
        return (None, None)

    def sync_inventory(self):
        ''' Read inventory and sinchronize it '''

        # Check we are in foreground, set otherwise
        self.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        self.check_stash_open(open_otherwise=True)

        logger.info("Starting inventory sync ...")

        # Find empty slots in inventory
        empty_slots = vh.find_empty_slots_in_inventory()

        # Mark as empty
        for row, col in empty_slots:
            inventory.clear(row, col)

        full_slots = []
        # Find the non-empty slots
        for row in range(inventory.num_rows):
            for col in range(inventory.num_cols):
                if (row, col) not in empty_slots:
                    full_slots += [[row, col]]

        for slot in full_slots:
            # get item description
            item_description = self.get_text_at_position(
                inventory.to_screen_position(*slot), reset_mouse=False)

            # classify description
            (curr, ammount) = self.process_item_description(item_description)

            if curr == "" and ammount == "":
                # Empty slot
                inventory.clear(*slot)
            elif curr and ammount:
                new_stack = currency.CurrencyStack(curr, ammount)
                inventory.set(new_stack, slot[0], slot[1])
            else:
                raise CouldNotIdentifyItemException

        # Reset Mouse Position
        autogui.moveTo(1, 1)

        inventory.synchronzed = True

        logger.info("Inventory sync finished ...")

    def sync_bank(self):
        ''' Read inventory and sinchronize it '''

        # Check we are in foreground, set otherwise
        self.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        self.check_stash_open(open_otherwise=True)

        logger.info("Starting bank sync ...")

        # Find currencies in stash tab
        matches = vh.find_currency_in_currency_tab(currency.CURRENCY_LIST)

        # For every currency kind
        for curr in currency.CURRENCY_LIST:

            if curr.name in matches:
                # Every location where this curr was found
                for match in matches[curr.name]:

                    item_description = self.get_text_at_position(
                        match, reset_mouse=False)

                    # classify description
                    (found_curr, found_ammount) = self.process_item_description(
                        item_description)

                    # assert(curr == found_curr)
                    # Image Capture is not 100% reliable
                    # If there is a missmtach ctrl+c wins
                    if found_curr != None and found_curr != "":
                        temmp_stack = currency.CurrencyStack(
                            found_curr, found_ammount)

                        assert(bank.deposit(temmp_stack))

        # Reset Mouse Position
        autogui.moveTo(1, 1)

        bank.synchronzed = True
        logger.info("Bank sync finished ...")


uiactions = ActionsHelper()


class ActionsHelperTest(unittest.TestCase):
    ''' Tests for ActionsHelper '''

    def setUp(self):
        self.ah = ActionsHelper()

    def test_custom(self):
        self.custom_test()

    def test_move_random_currency(self):

        self.ah.sync_bank()
        self.ah.sync_inventory()

        test_sequence = [key for key in bank.contents]

        test_sequence = test_sequence * random.randint(1, 3)
        random.shuffle(test_sequence)

        for curr in test_sequence:
            remaining = bank.contents[curr]
            if remaining > 0:
                num = random.randint(1, remaining)
                self.ah.transfer_currency_stash_inv(
                    curr, num)
                logger.info("Transfer {} {}".format(num, curr.pretty_name))
        self.ah.clean_inventory()

    def custom_test(self):
        ''' test clean inventory '''

        self.ah.is_foreground(set_foreground=True)

        # print(self.ah.invite_to_party("AppendixGone"))

        print(self.ah.trade_request("AppendixGone"))

        # print(self.ah.accept_trade())
        # self.ah.browse_over_customer_items()
        # self.ah.list_currency_trade_window()

    def identify_currencies_in_stash(self):
        '''
            Find position of all available currencies in stash.
            Make sure they can be identified via Ctrl+c
        '''
        # Check we are in foreground, set otherwise
        self.ah.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        self.ah.check_stash_open(open_otherwise=True)

        matches = vh.find_currency_in_currency_tab(currency.CURRENCY_LIST)

        for curr in currency.CURRENCY_LIST:
            if curr.name in matches and matches[curr.name]:

                text = self.ah.get_text_at_position(matches[curr.name][0])

                if text is None or text == "":
                    logger.debug(
                        'Could not read item properties through Ctrl+C for {} @ {}'.format(curr.pretty_name, *matches[curr.name][0]))

                (found_curr, _) = self.ah.process_item_description(text)

                self.assertEqual(
                    curr, found_curr, "\n\tLooking for {} but found {}".format(curr, found_curr))

                logger.info("Found {} == {}".format(
                    curr.pretty_name, found_curr.pretty_name))

            else:
                logger.debug(
                    'Currency {} could not be found in stash.'.format(curr.pretty_name))

        # Reset mouse to avoid screen pollution
        autogui.moveTo(1, 1)

    def identify_currencies_in_inv(self):
        '''
            Find position of all available currencies in stash.
            Make sure they can be identified via Ctrl+c
        '''
        # Check we are in foreground, set otherwise
        self.ah.is_foreground(set_foreground=True)

        # Check if stash is open, open it otherwise
        self.ah.check_stash_open(open_otherwise=True)

        matches = vh.find_currency_in_inventory(currency.CURRENCY_LIST)

        for curr in currency.CURRENCY_LIST:
            if curr.name in matches and matches[curr.name]:
                autogui.moveTo(*matches[curr.name][0])
                autogui.hotkey('ctrl', 'c')

                # Get txt from clipboard
                text = self.ah.get_clipboard_text()

                if text is None or text == "":
                    logger.debug(
                        'Could not read item properties through Ctrl+C for {} @ {}'.format(
                            curr.pretty_name,
                            *matches[curr.name][0]))

                (found_curr, _) = self.ah.process_item_description(text)

                self.assertEqual(
                    curr, found_curr, "\n\tLooking for {} but found {}".format(curr, found_curr))

                logger.info("Found {} == {}".format(
                    curr.pretty_name, found_curr.pretty_name))

            else:
                logger.debug(
                    'Currency {} could not be found in stash.'.format(curr.pretty_name))


if __name__ == '__main__':

    logger.setLevel(level=logging.DEBUG)

    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    unittest.main()

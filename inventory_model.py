''' manage inventory/stash '''

import logging
import math

import config as cfg
import currency

logger = logging.getLogger('bot_log')


class Container():
    ''' generic class for a container (stash or inv) '''

    def __init__(self):
        self.num_rows = None
        self.num_cols = None

        self.cell_0_0_x_pos = None
        self.cell_0_0_y_pos = None

        self.cell_width = None
        self.cell_height = None

        self._contents = []

        self.synchronzed = False

    def get(self, pos, y_pos=None):
        ''' Get item at position pos.
            If y_pos is provided, return as if accessing a 2d array with pos representing X.
        '''
        if y_pos is None:
            return self._contents[pos]
        else:
            return self._contents[pos*self.num_cols + y_pos]

    def set(self, item, pos, y_pos=None):
        ''' Insert item at position pos.
            If y_pos is provided, insert as if accessing a 2d array with pos representing X.
        '''
        if y_pos is None:
            self._contents[pos] = item
            logger.debug("@ {} Inserted {}".format(pos, item))
        else:
            self._contents[pos*self.num_cols + y_pos] = item
            logger.debug("@ [{},{}] Inserted {}".format(pos, y_pos, item))

    def clear(self, x_pos, y_pos):
        self._contents[x_pos*self.num_cols + y_pos] = None
        logger.debug("@ [{},{}] Cleared".format(x_pos, y_pos))

    def add(self, item, x_pos, y_pos):
        ''' Insert item at position pos.
            If y_pos is provided, insert as if accessing a 2d array with pos representing X.
        '''
        if self._contents[x_pos*self.num_cols + y_pos].curr != item.curr:
            logger.error("Attempting to add {} to {}".format(
                item.curr, self._contents[x_pos*self.num_cols + y_pos].curr))
            raise Exception

        new_ammount = self._contents[x_pos *
                                     self.num_cols + y_pos].ammount + item.ammount

        if new_ammount > item.curr.stack_size:
            logger.error("Attempting to add {} bigger than stack size {}/{} ".format(
                item.curr, new_ammount, item.curr.stack_size))
            raise Exception

        self._contents[x_pos*self.num_cols + y_pos].ammount = new_ammount
        logger.debug("@ [{},{}] Add {} new {} ".format(
            x_pos, y_pos, item.ammount, item.curr.pretty_name))

    def iter(self):
        ''' iterate over all items currently in the inventory '''
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.get(row, col) is not None:
                    yield (row, col)

    def transfer(self, currency_stack, force_ctrl_click=False):
        '''
            Transfer a currency stack
        '''

        curr = currency_stack.curr
        ammount = currency_stack.ammount

        # If transfering less than a full stack it needs to be done by hand
        # Give the cell where the currency should be put
        #################################################################################
        # Unless they are the last orbs in the stash, so they need to be ctrl + clicked
        # force_ctrl_click comes in then
        #################################################################################
        if ammount < curr.stack_size and not force_ctrl_click:

            (row, col) = self.next_emtpy_cell()

            if row is None or col is None:
                # Inventory full or something went wrong
                return False, None
            else:
                self.set(currency_stack, row, col)
                return True, (row, col)

        # Check if currency can be distributed among non-complete stacks of the same currency
        for col in range(self.num_cols):
            for row in range(self.num_rows):

                cell = self.get(row, col)
                # Look for a non-complete stack of the same currency
                if cell is not None and cell.curr == curr and cell.ammount < curr.stack_size:

                    # Orbs currently in that position
                    current = cell.ammount
                    # Orbs to a full stack
                    remaining = curr.stack_size - \
                        cell.ammount

                    if ammount <= remaining:
                        self.add(currency.CurrencyStack(
                            curr, ammount), row, col)
                        ammount = 0
                    else:
                        self.add(currency.CurrencyStack(
                            curr, remaining), row, col)
                        ammount -= remaining

                if ammount == 0:
                    break
            if ammount == 0:
                break

        # It was not possible to distribute currency, it must take a new slot
        if ammount > 0:
            (row, col) = self.next_emtpy_cell()

            if row is None or col is None:
                # Inventory full or something went wrong
                return False, None

            self.set(currency.CurrencyStack(curr, ammount), row, col)

            return True, (row, col)
        else:
            return True, (None, None)

    def next_emtpy_cell(self):
        '''
            For now will only work with 1x1 items
            TODO Expand to arbitrary shapes
        '''

        # Fill order is columns first
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.get(row, col) is None:
                    return (row, col)

        # Could not find an empty cell, inventory full
        return (None, None)

    def to_screen_position(self, x_pos, y_pos):
        ''' Get the screen position of the requested cell '''

        x_temp = self.cell_0_0_x_pos + x_pos * self.cell_width + self.cell_width/2
        y_temp = self.cell_0_0_y_pos + y_pos * self.cell_width + self.cell_height/2

        return (x_temp, y_temp)


class Inventory (Container):
    ''' Class representing the inventory '''

    def __init__(self):
        super().__init__()

        self.num_rows = cfg.INV_NUM_ROW
        self.num_cols = cfg.INV_NUM_COL

        self.cell_0_0_x_pos = cfg.INVENTORY_POS_0_0[0]
        self.cell_0_0_y_pos = cfg.INVENTORY_POS_0_0[1]

        self.cell_width = cfg.NORMAL_TAB_X_OFFSET
        self.cell_height = cfg.NORMAL_TAB_Y_OFFSET

        self._contents = [None for x in range(self.num_rows * self.num_cols)]

    def dump(self):
        return self._contents


class ClientTradeWindow (Container):
    ''' Class representing the inventory '''

    def __init__(self):
        super().__init__()

        self.num_rows = cfg.INV_NUM_ROW
        self.num_cols = cfg.INV_NUM_COL

        self.cell_0_0_x_pos = cfg.TRADE_WIN_POS_0_0[0]
        self.cell_0_0_y_pos = cfg.TRADE_WIN_POS_0_0[1]

        self.cell_width = cfg.NORMAL_TAB_X_OFFSET
        self.cell_height = cfg.NORMAL_TAB_Y_OFFSET

        self._contents = [None for x in range(self.num_rows * self.num_cols)]

    def dump(self):
        return self._contents


class Bank():

    MAX_NUM_STACKS = 5000

    def __init__(self):
        self.contents = {}

        self.virtual_contents = {}

        for curr in currency.CURRENCY_LIST:
            self.contents[curr] = 0
            self.virtual_contents[curr] = 0

        self.current_number_of_stacks = 0

        self.synchronzed = False

    def deposit(self, transfer, target=None):
        ''' deposit a stack of currency '''

        if target is None:
            target = self.contents

        # Check that we don't go over the limit
        # Get number of stacks of this currency

        if transfer.curr in target:
            # Current number of stacks of this currency
            curr_n_stacks = math.ceil(target[transfer.curr] /
                                      transfer.curr.stack_size)

            # Number of stacks after depositing currency
            new_n_stacks = math.ceil((target[transfer.curr] +
                                      transfer.ammount) / transfer.curr.stack_size)
        else:
            curr_n_stacks = 0
            # Number of stacks after depositing currency
            new_n_stacks = math.ceil(
                transfer.ammount / transfer.curr.stack_size)

        # Does it fit ?
        if (self.current_number_of_stacks - curr_n_stacks + new_n_stacks) > Bank.MAX_NUM_STACKS:
            logger.warning("Failed to deposit {} {} ! \n\t Stash full !".format(
                transfer.ammount, transfer.curr.pretty_name))
            return False

        target[transfer.curr] += transfer.ammount

        self.current_number_of_stacks += -curr_n_stacks + new_n_stacks

        logger.info("Deposited {} {}".format(
            transfer.ammount, transfer.curr.pretty_name))
        return True

    def withdraw(self, transfer, target=None):
        ''' remove currency from the bank '''

        if target is None:
            target = self.contents

        if transfer.curr not in target:
            logger.warning("Failed to withdraw {} {}. Currency not in bank !".format(
                transfer.ammount, transfer.curr.pretty_name))
            return False
        elif target[transfer.curr] < transfer.ammount:
            logger.warning("Failed to withdraw {} {}. Only {} available !".format(
                transfer.ammount, transfer.curr, target[transfer.curr]))
            return False
        else:
            # Update the stack count

            # Current number of stacks of this currency
            curr_n_stacks = math.ceil(target[transfer.curr] /
                                      transfer.curr.stack_size)

            # Number of stacks after depositing currency
            new_n_stacks = math.ceil((target[transfer.curr] -
                                      transfer.ammount) / transfer.curr.stack_size)

            self.current_number_of_stacks += -curr_n_stacks + new_n_stacks
            target[transfer.curr] -= transfer.ammount

            logger.info("Withdrew {} {}".format(
                transfer.ammount, transfer.curr.pretty_name))

            return True

    def sync_virtual_bank(self):

        for curr in currency.CURRENCY_LIST:
            self.virtual_contents[curr] = self.contents[curr]

    def virtual_deposit(self, transfer):
        return self.deposit(transfer, self.virtual_contents)

    def virtual_withdraw(self, transfer):
        ret = self.withdraw(transfer, self.virtual_contents)
        # logger.debug(self.virtual_contents)
        return ret


client_trade_window = ClientTradeWindow()
inventory = Inventory()
bank = Bank()

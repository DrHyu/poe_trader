''' actual engine for the bot '''

import time
import logging
from player import players, Player

from misc import trade_req_q, trade_outcome_q, TRADE_OUTCOME

from hideout import hideout
from log_parser import log_parser
from uiactions import uiactions

from inventory_model import inventory, bank
from rates import Rates

logger = logging.getLogger('bot_log')


class POE_bot():

    def __init__(self):

        # Present trades is a subset of pending_trades
        self.present_trades = []

        logger.info("POE_bot starting ....")
        # Launch the event monitoring threads
        log_parser.start()
        hideout.start()

        # Initial scan of inventory and bank
        uiactions.sync_inventory()
        uiactions.sync_bank()
        bank.sync_virtual_bank()

        # Empty inventory for a clean start
        uiactions.clean_inventory()

        logger.info("POE_bot initialization finished correctly !")

    def run(self):
        ''' start operating '''

        # Main loop
        while True:

            self.check_for_new_trade_req()

            next_player = self.check_existing_trades()

            if next_player:
                logger.debug("Do trade")
                # Process 1 trade at a time
                self.do_trade(next_player)
            else:
                time.sleep(1)
                uiactions.wiggle_mouse()

    def check_for_new_trade_req(self):
        '''
            Check if there is a new trade request.
            Invite the player if the request makes sense.
        '''

        # While there are pending messages
        while True:

            # Get new message
            msg = trade_req_q.get(block=False)

            # Did we get a message ?
            if msg is None:
                break

            # Create a new Player
            new_player = Player(msg.player_name)

            # Fill out trade information
            new_player.add_trade_info(msg)

            # Check if trade makes sense
            (new_buy, new_sell) = new_player.get_trade_info()
            if not self.is_trade_feasable(new_buy, new_sell):
                new_player.wrong_offer_response()
                continue

            # Add player to the tracking list
            if not players.add_player(new_player):
                # Player already in players
                continue

            # Invite to party
            new_player.invite()

    def check_existing_trades(self):
        ''' Update old trades and return the next trade if available '''
        pls = players.get_all()

        remove_player = False
        for ply in pls:
            # Check for ppl who messaged but never joined
            if time.time() - ply.invite_sent_timestamp > 20 and not ply.is_in_hideout():
                ply.kick()
                players.remove_player(ply.name)
                remove_player = True

        # If a player was removed from the waiting list
        # The virtual bank needs to be recalculated
        if remove_player:
            self.recalculate_virtual_bank()

        for ply in pls:
            if ply.is_in_hideout():
                return ply

        return None

    def check_for_players_joined(self):

        joined_players = hideout.recently_joined_players()
        self.present_trades += joined_players

    def do_trade(self, ply):
        '''
            perform a trade operartion

            STATES:
                WITHDRAW
                TRADE_REQ
                TRANS_MY_ITEMS
                CHECK_CUSTOMER_ITEMS
                ACCEPT_TRADE
                CHECK_TRADE_COMPLETED
                DEPOSIT
                FAREWELL
                ERROR
        '''

        # Flush the queue to not have inputs from last operation
        trade_outcome_q.flush()

        c_state = ""
        n_state = "WITHDRAW"
        p_state = ""

        while True:

            p_state = c_state
            c_state = n_state

            logger.debug("STATE -> {}".format(c_state))

            if c_state == "WITHDRAW":
                (buy, sell) = ply.get_trade_info()

                # Withrdraw money from brank
                uiactions.transfer_currency_stash_inv(buy.curr, buy.ammount)
                n_state = "TRADE_REQ"

            elif c_state == "TRADE_REQ":
                # Request a trade
                if ply.trade_request():
                    logger.info("Started trade with {}".format(ply.name))
                    n_state = "TRANS_MY_ITEMS"
                else:
                    n_state = "ERROR"

            elif c_state == "TRANS_MY_ITEMS":
                # Put our items in
                uiactions.transfer_currency_inv_trade()
                n_state = "CHECK_CUSTOMER_ITEMS"

            elif c_state == "CHECK_CUSTOMER_ITEMS":

                # Wait and check customer items
                # Customer can:
                #   - Put the right items -> ACCEPT_TRADE
                #   - Put the wrong items -> CHECK_CUSTOMER_ITEMS
                #   - Cancel Trade  -> ERROR
                #   - Timeout -> ERRROR

                start_time = time.time()
                while True:

                    trade_outcome = trade_outcome_q.get(block=False)
                    found_curr = uiactions.list_currency_trade_window()

                    if TRADE_OUTCOME.ACCEPTED == trade_outcome:
                        # This cannot happen here
                        raise Exception
                    elif TRADE_OUTCOME.DECLINED == trade_outcome:
                        # Customer declined trade
                        n_state = "ERROR"
                        break

                    elif time.time() - start_time > 20:
                        n_state = "ERROR"
                        uiactions.cancel_trade()
                        logger.info("Timeout when waiting for {} {} - Last scanned was {}".format(
                            sell.ammount, sell.curr, found_curr))
                        break
                    elif len(found_curr) > 1 or \
                            sell.curr.name not in found_curr or \
                            found_curr[sell.curr.name] != sell.ammount:
                            # Currency not ready yet or not matching
                        continue
                    else:
                        n_state = "ACCEPT_TRADE"
                        break

            elif c_state == "ACCEPT_TRADE":
                # Try to accept trade
                if uiactions.accept_trade():
                    n_state = "CHECK_TRADE_COMPLETED"
                else:
                    # TODO limit this loop
                    n_state = "CHECK_CUSTOMER_ITEMS"

            elif c_state == "CHECK_TRADE_COMPLETED":
                # At this point the customer can:
                #   - Accept the trade -> DEPOSIT
                #   - Decline the trade -> ERROR
                #   - Modify items -> CHECK_CUSTOMER_ITEMS
                #   - Do nothing forever -> ERROR
                start_time = time.time()
                while True:
                    status = uiactions.trade_window_accept_button_status()
                    trade_outcome = trade_outcome_q.get(block=False)

                    if TRADE_OUTCOME.ACCEPTED == trade_outcome:
                        # Contents are not mapped since trade went through
                        inventory.synchronzed = False
                        n_state = "FAREWELL"
                        break
                    elif TRADE_OUTCOME.DECLINED == trade_outcome:
                        n_state = "ERROR"
                        logger.info("Customer declined trade")
                        break
                    elif time.time() - start_time > 10:
                        n_state = "ERROR"
                        uiactions.cancel_trade()
                        logger.info(
                            "Timeout when waiting for {}".format(c_state))
                        break
                    elif status == "ACCEPTED":
                        # Items haven't been moved/changed by the customer
                        pass
                    elif status != "ACCEPTED":
                        # The customer probably tried to cheat and moved the items
                        n_state = "CHECK_CUSTOMER_ITEMS"
                        break
                    else:
                        pass

            elif c_state == "FAREWELL":
                # Kick from party
                ply.kick()

                # Send farewell message
                ply.farewell()

                # Remove from players
                players.remove_player(ply.name)

                logger.info(
                    "Trade completed with {}".format(ply.name))

                # Clean inventory
                n_state = "DEPOSIT"

            elif c_state == "DEPOSIT":
                # Stash items in bank
                uiactions.clean_inventory()

                # Sync virtual bank
                # Aligns virtual with current bank
                self.recalculate_virtual_bank()

                break

            elif c_state == "ERROR":

                logger.info(
                    "Failed to trade with {}".format(ply.name))

                logger.debug(
                    "Previous state {}".format(p_state))

                players.remove_player(ply.name)
                ply.kick()

                # Return items to stash
                uiactions.clean_inventory()

                # Sync virtual bank
                # Aligns virtual with current bank
                self.recalculate_virtual_bank()

                break

    def is_trade_feasable(self, buy, sell):

        # Do we win money ?

        # Check if trade matches the established rates
        if not Rates.is_transaction_ok(buy, sell):
            return False

        # The money that we would theoretically get from the exchange is not used
        # Since it becomes much harder, because a trade might not happen
        # Also trade sequence is not guaranteed

        # Do we have enought currency (considering previous trades)
        if not bank.virtual_withdraw(buy):
            return False
        else:
            # Virtual bank updated
            # It would be possible to remove this much
            return True

    def recalculate_virtual_bank(self):
        '''
            Given a list of pending transactions
            Calculate the state of the bank after they have been carried over.
        '''
        pls = players.get_all()

        # Copy virtual bank = actual bank
        bank.sync_virtual_bank()

        # Apply transactions
        for ply in pls:
            (buy, _) = ply.get_trade_info()
            if not bank.virtual_withdraw(buy):
                logger.error(
                    "Not enough currency when recalculating the virtual bank !")
                raise Exception


if __name__ == '__main__':

    logger.setLevel(level=logging.DEBUG)

    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    bot = POE_bot()

    bot.run()

    # p = Player("AppendixGone")

    # from misc import TRADE_REQ_MSG
    # import currency

    # t = TRADE_REQ_MSG(
    #     "AppendixGone",
    #     currency.CurrencyStack(currency.ExaltedOrb, 1),
    #     currency.CurrencyStack(currency.ChaosOrb, 10),
    #     "", "", ""
    # )

    # p.add_trade_info(t)

    # bot.do_trade(p)

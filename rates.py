
''' currency exchange rates '''

import json

from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import quote

import logging
import pprint

import config as cfg

import currency
import math
from inventory_model import inventory, bank

logger = logging.getLogger(__name__)


class Rates(object):
    ''' currency exchange rates '''

    your_curr_for_my_c_allowed = {
        currency.ExaltedOrb,
        currency.OrbofFusing,
        currency.OrbofAlteration,
        currency.JewellerOrb
    }

    your_c_for_my_curr_allowed = {
        currency.ExaltedOrb,
        currency.OrbofFusing,
        currency.OrbofAlteration,
        currency.JewellerOrb
    }

    def __init__(self):

        self.your_curr_for_my_c = {}
        self.your_c_for_my_curr = {}

    def fetch_new_rates_from_api(self):

        try:
            with urlopen(
                    Request('https://poe.ninja/api/data/currencyoverview?league=Delirium&type=Currency',
                            headers={'User-Agent': 'Mozilla/5.0'})) as url:
                return json.loads(url.read().decode())
        except Exception as exception:
            logger.error(
                "Could not fetch from API: {}".format(exception))

        return None

    def update_rates(self):

        data = self.fetch_new_rates_from_api()

        if not data:
            logger.error('Failed to fetch currency rates from api !'.format())
            raise Exception

        data = data['lines']

        for rate in data:

            # You want to buy my exalt - I give you C - low
            _your_curr_for_my_c = None
            if rate['pay']:
                _your_curr_for_my_c = [1, 1/rate['pay']['value']]
            else:
                continue

            # You want to sell your C  - I give you Exalt - high
            _your_c_for_my_curr = None
            if rate['receive']:
                _your_c_for_my_curr = [rate['receive']['value'], 1]
            else:
                continue

            # logger.debug('pay {} sell {}'.format(buy_rate, sell_rate))

            for c in currency.CURRENCY_LIST:

                if c.pretty_name == rate['currencyTypeName']:  # and \
                        # (c.pretty_name == "Exalted Orb" or c.pretty_name == "Orb of Fusing"):

                    # Rules:
                    # Min transaction value 10c
                    # Min transaction gain 5% - (full flip 10%)

                    # BUY 1/126 SELL 124/1

                    # logger.debug('your {} for my c {}'.format(c.pretty_name,
                    #                                           _your_curr_for_my_c))
                    # logger.debug('your c for my {} {}'.format(c.pretty_name,
                    #                                           _your_c_for_my_curr))

                    # Min transaction value = 10c
                    min_trans_val = cfg.MIN_TRADE_VALUE

                    if _your_curr_for_my_c[1] < min_trans_val:
                        mult = 10 / _your_curr_for_my_c[1]
                        _your_curr_for_my_c[0] *= mult
                        _your_curr_for_my_c[1] *= mult

                    if _your_c_for_my_curr[0] < min_trans_val:
                        mult = 10 / _your_c_for_my_curr[0]
                        _your_c_for_my_curr[0] *= mult
                        _your_c_for_my_curr[1] *= mult

                    # logger.debug('your {} for my c {}'.format(c.pretty_name,
                    #                                           _your_curr_for_my_c))
                    # logger.debug('your c for my {} {}'.format(c.pretty_name,
                    #                                           _your_c_for_my_curr))

                    # At least 5% prof - 10% for a full flip  OR 2c
                    min_trans_profit_percent = cfg.MIN_TRADE_PROFIT_PERCENT
                    max_trans_profit_flat = cfg.MAX_TRADE_PROFIT_FLAT

                    avg_price = (
                        _your_curr_for_my_c[0] + _your_c_for_my_curr[1]) / 2

                    if (_your_curr_for_my_c[1] >= min_trans_val) and (_your_c_for_my_curr[0] >= min_trans_val):
                        avg_price = (
                            _your_curr_for_my_c[1] + _your_c_for_my_curr[0]) / 2
                    else:
                        avg_price = (
                            _your_curr_for_my_c[0] + _your_c_for_my_curr[1]) / 2

                    min_profit = avg_price * min_trans_profit_percent * 2

                    if min_profit > max_trans_profit_flat:
                        min_profit = max_trans_profit_flat

                    curr_profit = 0

                    if (_your_curr_for_my_c[1] >= min_trans_val) and (_your_c_for_my_curr[0] >= min_trans_val):
                        curr_profit = _your_c_for_my_curr[0] - \
                            _your_curr_for_my_c[1]
                    else:
                        curr_profit = _your_curr_for_my_c[0] - \
                            _your_c_for_my_curr[1]

                    # logger.debug('CP {} MP {}'.format(
                    #     curr_profit, min_profit))

                    # Spread the rates to get more profit
                    if curr_profit < min_profit:
                        remaining = min_profit - curr_profit
                        # logger.debug('MP {} CP {} REM {}'.format(
                        #     curr_profit, min_profit, remaining))

                        if _your_curr_for_my_c[1] >= min_trans_val:
                            _your_curr_for_my_c[1] -= remaining/2
                        else:
                            _your_curr_for_my_c[0] += remaining/2

                        if _your_c_for_my_curr[0] >= min_trans_val:
                            _your_c_for_my_curr[0] += remaining/2
                        else:
                            _your_c_for_my_curr[1] -= remaining/2

                    # logger.debug('your {} for my c {}'.format(c.pretty_name,
                    #                                           _your_curr_for_my_c))
                    # logger.debug('your c for my {} {}'.format(c.pretty_name,
                    #                                           _your_c_for_my_curr))

                    _your_curr_for_my_c[0] = math.ceil(_your_curr_for_my_c[0])
                    _your_curr_for_my_c[1] = math.floor(_your_curr_for_my_c[1])

                    _your_c_for_my_curr[0] = math.ceil(_your_c_for_my_curr[0])
                    _your_c_for_my_curr[1] = math.floor(_your_c_for_my_curr[1])

                    # logger.debug('your {} for my c {}'.format(c.pretty_name,
                    #                                           _your_curr_for_my_c))
                    # logger.debug('your c for my {} {}'.format(c.pretty_name,
                    #                                           _your_c_for_my_curr))

                    # Update the allowed rates

                    if c in Rates.your_curr_for_my_c_allowed:
                        self.your_curr_for_my_c[c.name] = _your_curr_for_my_c

                    if c in Rates.your_c_for_my_curr_allowed:
                        self.your_c_for_my_curr[c.name] = _your_c_for_my_curr

                    break

        logger.debug('Currency rates succesfull updated: \n{}'.format(self))

    def is_transaction_ok(self, i_give_them, they_give_me):

        print("I GIVE {} {}".format(
            i_give_them.curr.name, i_give_them.ammount))
        print("THEY GIVE {} {}".format(
            they_give_me.curr.name, they_give_me.ammount))

        # No tricky things
        if they_give_me.ammount == 0 or they_give_me.ammount == 0:
            logger.debug('Transaction rejected: ammount = 0')
            return False
        # Does it fit in inv/trade window ?
        elif they_give_me.ammount / they_give_me.curr.stack_size > (inventory.num_cols * inventory.num_cols):
            logger.debug('Transaction rejected: Does not fit in trade window')
            return False
        elif i_give_them.ammount / i_give_them.curr.stack_size > (inventory.num_cols * inventory.num_cols):
            logger.debug('Transaction rejected: Does not fit in trade window')
            return False
        # Does it fit in the bank ?
        elif bank.contents[they_give_me.curr] + they_give_me.ammount > 5000:
            logger.debug('Transaction rejected: Does not fit in bank {}/{}'.format(
                bank.contents[they_give_me.curr] + they_give_me.ammount, 5000))
            return False
        elif they_give_me.curr == currency.ChaosOrb:

            if i_give_them.curr.name not in self.your_c_for_my_curr:
                logger.debug(
                    'Transaction rejected: Not trading {}'.format(they_give_me.curr.pretty_name))
                return False

            requested_rate = i_give_them.ammount / they_give_me.ammount
            rate = self.your_c_for_my_curr[i_give_them.curr.name]
            official_rate = rate[1] / rate[0]

            if requested_rate <= official_rate:
                return True
            else:
                logger.debug('Transaction rejected: Incorrect rate')
                return False

        elif i_give_them.curr == currency.ChaosOrb:

            if they_give_me.curr.name not in self.your_curr_for_my_c:
                logger.debug(
                    'Transaction rejected: Not trading {}'.format(they_give_me.curr.pretty_name))
                return False

            requested_rate = they_give_me.ammount / i_give_them.ammount
            rate = self.your_curr_for_my_c[they_give_me.curr.name]
            official_rate = rate[0] / rate[1]

            logger.debug('RR {} OR {}'.format(requested_rate, official_rate))
            if requested_rate >= official_rate:
                return True
            else:
                logger.debug('Transaction rejected: Incorrect rate')
                return False

    def get_bo_message(self, curr, i_give_you_c):

        if i_give_you_c:
            return "~ b/o {}/{} {}".format(
                rates.your_curr_for_my_c[curr.name][0], rates.your_curr_for_my_c[curr.name][1], curr.pretty_name)
        else:
            return "~ b/o {}/{} {}".format(
                rates.your_c_for_my_curr[curr.name][0], rates.your_c_for_my_curr[curr.name][1], currency.ChaosOrb.pretty_name)

    def get_rates_easy(self):
        ''' Return the text that should be put on each currency '''

        ret = []

        for curr in self.your_c_for_my_curr_allowed:
            ret += [
                [curr, [self.get_bo_message(curr, False)]]
            ]

        ret += [
            [currency.ChaosOrb,
                map(lambda curr:
                    self.get_bo_message(curr, True),
                    self.your_curr_for_my_c_allowed)
             ]
        ]
        print(ret)
        # for curr in self.your_curr_for_my_c_allowed:
        #     ret[currency.ChaosOrb.name] += [self.get_bo_message(curr, True)]

        return ret

    def __str__(self):
        return self.__repr__()

    def __repr__(self):

        txt = "Your Currency For My Chaos:\n"
        txt += pprint.pformat(self.your_curr_for_my_c, indent=2)
        txt += "\n"
        txt += "Your Chaos For My Currency:\n"
        txt += pprint.pformat(self.your_c_for_my_curr, indent=2)
        txt += "\n"

        return txt


rates = Rates()

if __name__ == '__main__':

    logger.setLevel(level=logging.DEBUG)
    console_log = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    from uiactions import uiactions as ui  # nopep8
    rates.update_rates()

    ui.is_foreground(set_foreground=True)
    ui.set_currency_rates(rates.get_rates_easy())

    # for curr in currency.CURRENCY_LIST:
    #     if curr is not currency.ChaosOrb and curr:
    #         rate = "~ b/o {}/{} {}".format(
    #             rates.your_curr_for_my_c[curr.name][1], rates.your_curr_for_my_c[curr.name][0], currency.ChaosOrb.pretty_name)

    #         print(rate)

    # ui.set_currency_rates(currency.CURRENCY_LIST, rate)
    # print(rates.is_transaction_ok(
    #     currency.CurrencyStack(currency.ExaltedOrb, 1),
    #     currency.CurrencyStack(currency.ChaosOrb, 4999)
    # ))
    # print(rates.is_transaction_ok(
    #     currency.CurrencyStack(currency.ChaosOrb, 122),
    #     currency.CurrencyStack(currency.ExaltedOrb, 1)
    # ))

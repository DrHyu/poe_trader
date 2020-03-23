
class Rates(object):
    ''' currency exchange rates '''

    buy_rates = {'exalted_orb': (1, 138), 'chaos_orb': (1, 1)}
    sell_rates = {
        'exalted_orb': (1, 140),
        'chaos_orb': (1, 1),
        'jeweller_orb': (16, 2)}

    def __init__(self):
        pass

    @staticmethod
    def is_transaction_ok(buy, sell):

        print("BUY {} {}".format(buy.curr, buy.ammount))
        print("SELL {} {}".format(sell.curr, sell.ammount))

        if buy.curr != ChaosOrb and sell.curr != ChaosOrb:
            print("aaaaaa")
            return False

        elif buy.curr == ChaosOrb:
            # Supported curr ?
            if sell.curr.name not in Rates.buy_rates:
                print("bbbbb")
                return False
            elif Rates.buy_rates[sell.curr.name][0] > sell.ammount:
                return False
            # elif (Rates.buy_rates[sell.curr.name][1] * sell.ammount) >= buy.ammount:
            elif (Rates.buy_rates[sell.curr.name][0] / Rates.buy_rates[sell.curr.name][1]) <= (sell.ammount/buy.ammount):
                return True
            else:
                print("ccccc")
                return False

        elif sell.curr == ChaosOrb:
            # Supported curr ?
            if buy.curr.name not in Rates.sell_rates:
                print("ddddd")
                return False

            elif Rates.sell_rates[buy.curr.name][0] > buy.ammount:
                print("dick")

                return False

            elif (Rates.sell_rates[buy.curr.name][0] / Rates.sell_rates[buy.curr.name][1]) >= (buy.ammount/sell.ammount):
                return True
            else:
                print("eeeee")
                return False

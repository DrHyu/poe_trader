
''' Currencies '''


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


class CurrencyStack():
    ''' Stack of Currceny '''

    def __init__(self, curr, ammount):
        self.curr = curr
        self.ammount = ammount

    def __str__(self):
        return "Stack of {} {}".format(self.ammount, self.curr.pretty_name)


class Currency():
    ''' Currencies class '''

    name = None
    pretty_name = None
    stack_size = None
    regex = None
    template_path = None
    chaos_equivalent = None

    def __init__(self):
        pass

    def update_chaos_equivalent(self):
        ''' Check API to update the chaos equivalent value of this currency '''
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.pretty_name


class AlchemyOrb(Currency):
    ''' Alchemy Orb '''

    name = "alchemy_orb"
    pretty_name = "Alchemy Orb"
    stack_size = 10
    regex = "Orb of Alchemy"
    template_path = "assets/currency_templates/alchemyorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class AwakenedSextant(Currency):
    ''' Awakened Sextant '''

    name = "awakened_sextant"
    pretty_name = "Awakened Sextant"
    stack_size = 10
    regex = "Awakened Sextant"
    template_path = "assets/currency_templates/awakenedsextant.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class BlessedOrb(Currency):
    ''' Blessed Orb '''

    name = "blessed_orb"
    pretty_name = "Blessed Orb"
    stack_size = 20
    regex = "Blessed Orb"
    template_path = "assets/currency_templates/blessedorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class CartographerChisel(Currency):
    ''' Cartographer's Chisel '''

    name = "cartographer_chisel"
    pretty_name = "Cartographer's Chisel"
    stack_size = 20
    regex = "Cartographer's Chisel"
    template_path = "assets/currency_templates/cartographerchisel.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class ChaosOrb(Currency):
    ''' Chaos Orb '''

    name = "chaos_orb"
    pretty_name = "Chaos Orb"
    stack_size = 10
    regex = "Chaos Orb"
    template_path = "assets/currency_templates/chaosorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class ChromaticOrb(Currency):
    ''' Chromatic Orb '''

    name = "chromatic_orb"
    pretty_name = "Chromatic Orb"
    stack_size = 20
    regex = "Chromatic Orb"
    template_path = "assets/currency_templates/chromaticorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class ExaltedOrb(Currency):
    ''' Exalted Orb '''

    name = "exalted_orb"
    pretty_name = "Exalted Orb"
    stack_size = 10
    regex = "Exalted Orb"
    template_path = "assets/currency_templates/exaltedorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class GemcutterPrism(Currency):
    ''' Gemcutter's Prism '''

    name = "gemcutter_prism"
    pretty_name = "Gemcutter's Prism"
    stack_size = 10
    regex = "Gemcutter's Prism"
    template_path = "assets/currency_templates/gemcutterprism.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class GlassblowerOrb(Currency):
    ''' Glassblower's Orb '''

    name = "glassblower_orb"
    pretty_name = "Glassblower's Bauble"
    stack_size = 20
    regex = "Glassblower's Bauble"
    template_path = "assets/currency_templates/glassblowerorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class HarbingerOrb(Currency):
    ''' Harbinger's Orb '''

    name = "harbinger_orb"
    pretty_name = "Harbinger's Orb"
    stack_size = 20
    regex = "Harbinger's Orb"
    template_path = "assets/currency_templates/harbingerorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class JewellerOrb(Currency):
    ''' Jeweller's Orb '''

    name = "jeweller_orb"
    pretty_name = "Jeweller's Orb"
    stack_size = 20
    regex = "Jeweller's Orb"
    template_path = "assets/currency_templates/jewellerorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfAlteration(Currency):
    ''' Orb of Alteration '''

    name = "orb_of_alteration"
    pretty_name = "Orb of Alteration"
    stack_size = 20
    regex = "Orb of Alteration"
    template_path = "assets/currency_templates/orbofalteration.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfAnnulment(Currency):
    ''' Orb of Annulment '''

    name = "orb_of_annulment"
    pretty_name = "Orb of Annulment"
    stack_size = 20
    regex = "Orb of Annulment"
    template_path = "assets/currency_templates/orbofannulment.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfChance(Currency):
    ''' Orb of Chance '''

    name = "orb_of_chance"
    pretty_name = "Orb of Chance"
    stack_size = 20
    regex = "Orb of Chance"
    template_path = "assets/currency_templates/orbofchance.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfFusing(Currency):
    ''' Orb of Fusing '''

    name = "orb_of_fusing"
    pretty_name = "Orb of Fusing"
    stack_size = 20
    regex = "Orb of Fusing"
    template_path = "assets/currency_templates/orboffusing.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfHorizons(Currency):
    ''' Orb of Horizons '''

    name = "orb_of_horizons"
    pretty_name = "Orb of Horizons"
    stack_size = 20
    regex = "Orb of Horizons"
    template_path = "assets/currency_templates/orbofhorizons.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfRegret(Currency):
    ''' Orb of Regret '''

    name = "orb_of_regret"
    pretty_name = "Orb of Regret"
    stack_size = 40
    regex = "Orb of Regret"
    template_path = "assets/currency_templates/orbofregret.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfScouring(Currency):
    ''' Orb of Scouring '''

    name = "orb_of_scouring"
    pretty_name = "Orb of Scouring"
    stack_size = 30
    regex = "Orb of Scouring"
    template_path = "assets/currency_templates/orbofscouring.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfTransmutation(Currency):
    ''' Orb of Transmutation '''

    name = "orb_of_transmutation"
    pretty_name = "Orb of Transmutation"
    stack_size = 40
    regex = "Orb of Transmutation"
    template_path = "assets/currency_templates/orboftransmutation.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class PrimeSextant(Currency):
    ''' Prime Sextant '''

    name = "prime_sextant"
    pretty_name = "Prime Sextant"
    stack_size = 10
    regex = "Prime Sextant"
    template_path = "assets/currency_templates/primesextant.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class RegalOrb(Currency):
    ''' Regal Orb '''

    name = "regal_orb"
    pretty_name = "Regal Orb"
    stack_size = 10
    regex = "Regal Orb"
    template_path = "assets/currency_templates/regalorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class SilverCoin(Currency):
    ''' Silver Coin '''

    name = "silver_coin"
    pretty_name = "Silver Coin"
    stack_size = 30
    regex = "Silver Coin"
    template_path = "assets/currency_templates/silvercoin.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class SimpleSextant(Currency):
    ''' Simple Sextant '''

    name = "simple_sextant"
    pretty_name = "Simple Sextant"
    stack_size = 10
    regex = "Simple Sextant"
    template_path = "assets/currency_templates/simplesextant.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class VaalOrb(Currency):
    ''' Vaal Orb '''

    name = "vaal_orb"
    pretty_name = "Vaal Orb"
    stack_size = 10
    regex = "Vaal Orb"
    template_path = "assets/currency_templates/vaalorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class OrbOfAugmentation(Currency):
    ''' Orb of Augmentation '''

    name = "orb_of_augmentation"
    pretty_name = "Orb of Augmentation"
    stack_size = 30
    regex = "Orb of Augmentation"
    template_path = "assets/currency_templates/orbofaugmentation.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


class DivineOrb(Currency):
    ''' Divine Orb '''

    name = "divine_orb"
    pretty_name = "Divine Orb"
    stack_size = 10
    regex = "Divine Orb"
    template_path = "assets/currency_templates/divineorb.png"

    def __init__(self):
        super().__init__()
        self.update_chaos_equivalent()


CURRENCY_LIST = [AlchemyOrb, AwakenedSextant, BlessedOrb, CartographerChisel, ChaosOrb, ChromaticOrb, ExaltedOrb, GemcutterPrism, GlassblowerOrb, HarbingerOrb, JewellerOrb,
                 OrbOfAlteration, OrbOfAnnulment, OrbOfChance, OrbOfFusing, OrbOfHorizons, OrbOfRegret, OrbOfScouring, OrbOfTransmutation, PrimeSextant, RegalOrb, SilverCoin, SimpleSextant, VaalOrb, OrbOfAugmentation, DivineOrb]

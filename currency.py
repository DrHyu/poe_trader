
''' Currencies '''


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
    size_x = 0
    size_y = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.pretty_name


class ChaosOrb(Currency):
    ''' Chaos Orb '''

    name = "chaos_orb"
    pretty_name = "Chaos Orb"
    stack_size = 10
    regex = "Chaos Orb"
    template_path = "assets/new_currency_templates/chaos_orb.png"
    size_x = 1
    size_y = 1


class ExaltedOrb(Currency):
    ''' Exalted Orb '''

    name = "exalted_orb"
    pretty_name = "Exalted Orb"
    stack_size = 10
    regex = "Exalted Orb"
    template_path = "assets/new_currency_templates/exalted_orb.png"
    size_x = 1
    size_y = 1


class DivineOrb(Currency):
    ''' Divine Orb '''

    name = "divine_orb"
    pretty_name = "Divine Orb"
    stack_size = 10
    regex = "Divine Orb"
    template_path = "assets/new_currency_templates/divine_orb.png"
    size_x = 1
    size_y = 1


class OrbofAlchemy(Currency):
    ''' Orb of Alchemy '''

    name = "orb_of_alchemy"
    pretty_name = "Orb of Alchemy"
    stack_size = 10
    regex = "Orb of Alchemy"
    template_path = "assets/new_currency_templates/orb_of_alchemy.png"
    size_x = 1
    size_y = 1


class OrbofFusing(Currency):
    ''' Orb of Fusing '''

    name = "orb_of_fusing"
    pretty_name = "Orb of Fusing"
    stack_size = 20
    regex = "Orb of Fusing"
    template_path = "assets/new_currency_templates/orb_of_fusing.png"
    size_x = 1
    size_y = 1


class OrbofAlteration(Currency):
    ''' Orb of Alteration '''

    name = "orb_of_alteration"
    pretty_name = "Orb of Alteration"
    stack_size = 20
    regex = "Orb of Alteration"
    template_path = "assets/new_currency_templates/orb_of_alteration.png"
    size_x = 1
    size_y = 1


class RegalOrb(Currency):
    ''' Regal Orb '''

    name = "regal_orb"
    pretty_name = "Regal Orb"
    stack_size = 10
    regex = "Regal Orb"
    template_path = "assets/new_currency_templates/regal_orb.png"
    size_x = 1
    size_y = 1


class VaalOrb(Currency):
    ''' Vaal Orb '''

    name = "vaal_orb"
    pretty_name = "Vaal Orb"
    stack_size = 10
    regex = "Vaal Orb"
    template_path = "assets/new_currency_templates/vaal_orb.png"
    size_x = 1
    size_y = 1


class OrbofRegret(Currency):
    ''' Orb of Regret '''

    name = "orb_of_regret"
    pretty_name = "Orb of Regret"
    stack_size = 40
    regex = "Orb of Regret"
    template_path = "assets/new_currency_templates/orb_of_regret.png"
    size_x = 1
    size_y = 1


class CartographerChisel(Currency):
    ''' Cartographer's Chisel '''

    name = "cartographer_chisel"
    pretty_name = "Cartographer's Chisel"
    stack_size = 20
    regex = "Cartographer's Chisel"
    template_path = "assets/new_currency_templates/cartographer_chisel.png"
    size_x = 1
    size_y = 1


class JewellerOrb(Currency):
    ''' Jeweller's Orb '''

    name = "jeweller_orb"
    pretty_name = "Jeweller's Orb"
    stack_size = 20
    regex = "Jeweller's Orb"
    template_path = "assets/new_currency_templates/jeweller_orb.png"
    size_x = 1
    size_y = 1


class SilverCoin(Currency):
    ''' Silver Coin '''

    name = "silver_coin"
    pretty_name = "Silver Coin"
    stack_size = 30
    regex = "Silver Coin"
    template_path = "assets/new_currency_templates/silver_coin.png"
    size_x = 1
    size_y = 1


class PerandusCoin(Currency):
    ''' Perandus Coin '''

    name = "perandus_coin"
    pretty_name = "Perandus Coin"
    stack_size = 1000
    regex = "Perandus Coin"
    template_path = "assets/new_currency_templates/perandus_coin.png"
    size_x = 1
    size_y = 1


class OrbofScouring(Currency):
    ''' Orb of Scouring '''

    name = "orb_of_scouring"
    pretty_name = "Orb of Scouring"
    stack_size = 30
    regex = "Orb of Scouring"
    template_path = "assets/new_currency_templates/orb_of_scouring.png"
    size_x = 1
    size_y = 1


class GemcutterPrism(Currency):
    ''' Gemcutter's Prism '''

    name = "gemcutter_prism"
    pretty_name = "Gemcutter's Prism"
    stack_size = 20
    regex = "Gemcutter's Prism"
    template_path = "assets/new_currency_templates/gemcutter_prism.png"
    size_x = 1
    size_y = 1


class OrbofChance(Currency):
    ''' Orb of Chance '''

    name = "orb_of_chance"
    pretty_name = "Orb of Chance"
    stack_size = 20
    regex = "Orb of Chance"
    template_path = "assets/new_currency_templates/orb_of_chance.png"
    size_x = 1
    size_y = 1


class ChromaticOrb(Currency):
    ''' Chromatic Orb '''

    name = "chromatic_orb"
    pretty_name = "Chromatic Orb"
    stack_size = 20
    regex = "Chromatic Orb"
    template_path = "assets/new_currency_templates/chromatic_orb.png"
    size_x = 1
    size_y = 1


class BlessedOrb(Currency):
    ''' Blessed Orb '''

    name = "blessed_orb"
    pretty_name = "Blessed Orb"
    stack_size = 20
    regex = "Blessed Orb"
    template_path = "assets/new_currency_templates/blessed_orb.png"
    size_x = 1
    size_y = 1


class GlassblowerBauble(Currency):
    ''' Glassblower's Bauble '''

    name = "glassblower_bauble"
    pretty_name = "Glassblower's Bauble"
    stack_size = 20
    regex = "Glassblower's Bauble"
    template_path = "assets/new_currency_templates/glassblower_bauble.png"
    size_x = 1
    size_y = 1


class OrbofAugmentation(Currency):
    ''' Orb of Augmentation '''

    name = "orb_of_augmentation"
    pretty_name = "Orb of Augmentation"
    stack_size = 30
    regex = "Orb of Augmentation"
    template_path = "assets/new_currency_templates/orb_of_augmentation.png"
    size_x = 1
    size_y = 1


class OrbofTransmutation(Currency):
    ''' Orb of Transmutation '''

    name = "orb_of_transmutation"
    pretty_name = "Orb of Transmutation"
    stack_size = 40
    regex = "Orb of Transmutation"
    template_path = "assets/new_currency_templates/orb_of_transmutation.png"
    size_x = 1
    size_y = 1


class MirrorofKalandra(Currency):
    ''' Mirror of Kalandra '''

    name = "mirror_of_kalandra"
    pretty_name = "Mirror of Kalandra"
    stack_size = 10
    regex = "Mirror of Kalandra"
    template_path = "assets/new_currency_templates/mirror_of_kalandra.png"
    size_x = 1
    size_y = 1


class ScrollofWisdom(Currency):
    ''' Scroll of Wisdom '''

    name = "scroll_of_wisdom"
    pretty_name = "Scroll of Wisdom"
    stack_size = 40
    regex = "Scroll of Wisdom"
    template_path = "assets/new_currency_templates/scroll_of_wisdom.png"
    size_x = 1
    size_y = 1


class PortalScroll(Currency):
    ''' Portal Scroll '''

    name = "portal_scroll"
    pretty_name = "Portal Scroll"
    stack_size = 40
    regex = "Portal Scroll"
    template_path = "assets/new_currency_templates/portal_scroll.png"
    size_x = 1
    size_y = 1


class BlacksmithWhetstone(Currency):
    ''' Blacksmith's Whetstone '''

    name = "blacksmith_whetstone"
    pretty_name = "Blacksmith's Whetstone"
    stack_size = 20
    regex = "Blacksmith's Whetstone"
    template_path = "assets/new_currency_templates/blacksmith_whetstone.png"
    size_x = 1
    size_y = 1


class ArmourerScrap(Currency):
    ''' Armourer's Scrap '''

    name = "armourer_scrap"
    pretty_name = "Armourer's Scrap"
    stack_size = 40
    regex = "Armourer's Scrap"
    template_path = "assets/new_currency_templates/armourer_scrap.png"
    size_x = 1
    size_y = 1


class EternalOrb(Currency):
    ''' Eternal Orb '''

    name = "eternal_orb"
    pretty_name = "Eternal Orb"
    stack_size = 10
    regex = "Eternal Orb"
    template_path = "assets/new_currency_templates/eternal_orb.png"
    size_x = 1
    size_y = 1


class StackedDeck(Currency):
    ''' Stacked Deck '''

    name = "stacked_deck"
    pretty_name = "Stacked Deck"
    stack_size = 10
    regex = "Stacked Deck"
    template_path = "assets/new_currency_templates/stacked_deck.png"
    size_x = 1
    size_y = 1


class SimpleSextant(Currency):
    ''' Simple Sextant '''

    name = "simple_sextant"
    pretty_name = "Simple Sextant"
    stack_size = 10
    regex = "Simple Sextant"
    template_path = "assets/new_currency_templates/simple_sextant.png"
    size_x = 1
    size_y = 1


class PrimeSextant(Currency):
    ''' Prime Sextant '''

    name = "prime_sextant"
    pretty_name = "Prime Sextant"
    stack_size = 10
    regex = "Prime Sextant"
    template_path = "assets/new_currency_templates/prime_sextant.png"
    size_x = 1
    size_y = 1


class AwakenedSextant(Currency):
    ''' Awakened Sextant '''

    name = "awakened_sextant"
    pretty_name = "Awakened Sextant"
    stack_size = 10
    regex = "Awakened Sextant"
    template_path = "assets/new_currency_templates/awakened_sextant.png"
    size_x = 1
    size_y = 1


class ApprenticeCartographerSeal(Currency):
    ''' Apprentice Cartographer's Seal '''

    name = "apprentice_cartographer_seal"
    pretty_name = "Apprentice Cartographer's Seal"
    stack_size = 10
    regex = "Apprentice Cartographer's Seal"
    template_path = "assets/new_currency_templates/apprentice_cartographer_seal.png"
    size_x = 1
    size_y = 1


class JourneymanCartographerSeal(Currency):
    ''' Journeyman Cartographer's Seal '''

    name = "journeyman_cartographer_seal"
    pretty_name = "Journeyman Cartographer's Seal"
    stack_size = 10
    regex = "Journeyman Cartographer's Seal"
    template_path = "assets/new_currency_templates/journeyman_cartographer_seal.png"
    size_x = 1
    size_y = 1


class MasterCartographerSeal(Currency):
    ''' Master Cartographer's Seal '''

    name = "master_cartographer_seal"
    pretty_name = "Master Cartographer's Seal"
    stack_size = 10
    regex = "Master Cartographer's Seal"
    template_path = "assets/new_currency_templates/master_cartographer_seal.png"
    size_x = 1
    size_y = 1


class SplinterofXoph(Currency):
    ''' Splinter of Xoph '''

    name = "splinter_of_xoph"
    pretty_name = "Splinter of Xoph"
    stack_size = 100
    regex = "Splinter of Xoph"
    template_path = "assets/new_currency_templates/splinter_of_xoph.png"
    size_x = 1
    size_y = 1


class SplinterofTul(Currency):
    ''' Splinter of Tul '''

    name = "splinter_of_tul"
    pretty_name = "Splinter of Tul"
    stack_size = 100
    regex = "Splinter of Tul"
    template_path = "assets/new_currency_templates/splinter_of_tul.png"
    size_x = 1
    size_y = 1


class SplinterofEsh(Currency):
    ''' Splinter of Esh '''

    name = "splinter_of_esh"
    pretty_name = "Splinter of Esh"
    stack_size = 100
    regex = "Splinter of Esh"
    template_path = "assets/new_currency_templates/splinter_of_esh.png"
    size_x = 1
    size_y = 1


class SplinterofUulNetol(Currency):
    ''' Splinter of Uul-Netol '''

    name = "splinter_of_uul-netol"
    pretty_name = "Splinter of Uul-Netol"
    stack_size = 100
    regex = "Splinter of Uul-Netol"
    template_path = "assets/new_currency_templates/splinter_of_uul-netol.png"
    size_x = 1
    size_y = 1


class SplinterofChayula(Currency):
    ''' Splinter of Chayula '''

    name = "splinter_of_chayula"
    pretty_name = "Splinter of Chayula"
    stack_size = 100
    regex = "Splinter of Chayula"
    template_path = "assets/new_currency_templates/splinter_of_chayula.png"
    size_x = 1
    size_y = 1


class BlessingofXoph(Currency):
    ''' Blessing of Xoph '''

    name = "blessing_of_xoph"
    pretty_name = "Blessing of Xoph"
    stack_size = 10
    regex = "Blessing of Xoph"
    template_path = "assets/new_currency_templates/blessing_of_xoph.png"
    size_x = 1
    size_y = 1


class BlessingofTul(Currency):
    ''' Blessing of Tul '''

    name = "blessing_of_tul"
    pretty_name = "Blessing of Tul"
    stack_size = 10
    regex = "Blessing of Tul"
    template_path = "assets/new_currency_templates/blessing_of_tul.png"
    size_x = 1
    size_y = 1


class BlessingofEsh(Currency):
    ''' Blessing of Esh '''

    name = "blessing_of_esh"
    pretty_name = "Blessing of Esh"
    stack_size = 10
    regex = "Blessing of Esh"
    template_path = "assets/new_currency_templates/blessing_of_esh.png"
    size_x = 1
    size_y = 1


class BlessingofUulNetol(Currency):
    ''' Blessing of Uul-Netol '''

    name = "blessing_of_uul-netol"
    pretty_name = "Blessing of Uul-Netol"
    stack_size = 10
    regex = "Blessing of Uul-Netol"
    template_path = "assets/new_currency_templates/blessing_of_uul-netol.png"
    size_x = 1
    size_y = 1


class BlessingofChayula(Currency):
    ''' Blessing of Chayula '''

    name = "blessing_of_chayula"
    pretty_name = "Blessing of Chayula"
    stack_size = 10
    regex = "Blessing of Chayula"
    template_path = "assets/new_currency_templates/blessing_of_chayula.png"
    size_x = 1
    size_y = 1


class OrbofAnnulment(Currency):
    ''' Orb of Annulment '''

    name = "orb_of_annulment"
    pretty_name = "Orb of Annulment"
    stack_size = 20
    regex = "Orb of Annulment"
    template_path = "assets/new_currency_templates/orb_of_annulment.png"
    size_x = 1
    size_y = 1


class OrbofBinding(Currency):
    ''' Orb of Binding '''

    name = "orb_of_binding"
    pretty_name = "Orb of Binding"
    stack_size = 20
    regex = "Orb of Binding"
    template_path = "assets/new_currency_templates/orb_of_binding.png"
    size_x = 1
    size_y = 1


class OrbofHorizons(Currency):
    ''' Orb of Horizons '''

    name = "orb_of_horizons"
    pretty_name = "Orb of Horizons"
    stack_size = 20
    regex = "Orb of Horizons"
    template_path = "assets/new_currency_templates/orb_of_horizons.png"
    size_x = 1
    size_y = 1


class HarbingerOrb(Currency):
    ''' Harbinger's Orb '''

    name = "harbinger_orb"
    pretty_name = "Harbinger's Orb"
    stack_size = 20
    regex = "Harbinger's Orb"
    template_path = "assets/new_currency_templates/harbinger_orb.png"
    size_x = 1
    size_y = 1


class EngineerOrb(Currency):
    ''' Engineer's Orb '''

    name = "engineer_orb"
    pretty_name = "Engineer's Orb"
    stack_size = 20
    regex = "Engineer's Orb"
    template_path = "assets/new_currency_templates/engineer_orb.png"
    size_x = 1
    size_y = 1


class AncientOrb(Currency):
    ''' Ancient Orb '''

    name = "ancient_orb"
    pretty_name = "Ancient Orb"
    stack_size = 20
    regex = "Ancient Orb"
    template_path = "assets/new_currency_templates/ancient_orb.png"
    size_x = 1
    size_y = 1


class AnnulmentShard(Currency):
    ''' Annulment Shard '''

    name = "annulment_shard"
    pretty_name = "Annulment Shard"
    stack_size = 20
    regex = "Annulment Shard"
    template_path = "assets/new_currency_templates/annulment_shard.png"
    size_x = 1
    size_y = 1


class ExaltedShard(Currency):
    ''' Exalted Shard '''

    name = "exalted_shard"
    pretty_name = "Exalted Shard"
    stack_size = 20
    regex = "Exalted Shard"
    template_path = "assets/new_currency_templates/exalted_shard.png"
    size_x = 1
    size_y = 1


class MirrorShard(Currency):
    ''' Mirror Shard '''

    name = "mirror_shard"
    pretty_name = "Mirror Shard"
    stack_size = 20
    regex = "Mirror Shard"
    template_path = "assets/new_currency_templates/mirror_shard.png"
    size_x = 1
    size_y = 1


class TimelessKaruiSplinter(Currency):
    ''' Timeless Karui Splinter '''

    name = "timeless_karui_splinter"
    pretty_name = "Timeless Karui Splinter"
    stack_size = 100
    regex = "Timeless Karui Splinter"
    template_path = "assets/new_currency_templates/timeless_karui_splinter.png"
    size_x = 1
    size_y = 1


class TimelessMarakethSplinter(Currency):
    ''' Timeless Maraketh Splinter '''

    name = "timeless_maraketh_splinter"
    pretty_name = "Timeless Maraketh Splinter"
    stack_size = 100
    regex = "Timeless Maraketh Splinter"
    template_path = "assets/new_currency_templates/timeless_maraketh_splinter.png"
    size_x = 1
    size_y = 1


class TimelessEternalEmpireSplinter(Currency):
    ''' Timeless Eternal Empire Splinter '''

    name = "timeless_eternal_empire_splinter"
    pretty_name = "Timeless Eternal Empire Splinter"
    stack_size = 100
    regex = "Timeless Eternal Empire Splinter"
    template_path = "assets/new_currency_templates/timeless_eternal_empire_splinter.png"
    size_x = 1
    size_y = 1


class TimelessTemplarSplinter(Currency):
    ''' Timeless Templar Splinter '''

    name = "timeless_templar_splinter"
    pretty_name = "Timeless Templar Splinter"
    stack_size = 100
    regex = "Timeless Templar Splinter"
    template_path = "assets/new_currency_templates/timeless_templar_splinter.png"
    size_x = 1
    size_y = 1


class TimelessVaalSplinter(Currency):
    ''' Timeless Vaal Splinter '''

    name = "timeless_vaal_splinter"
    pretty_name = "Timeless Vaal Splinter"
    stack_size = 100
    regex = "Timeless Vaal Splinter"
    template_path = "assets/new_currency_templates/timeless_vaal_splinter.png"
    size_x = 1
    size_y = 1


class AwakenerOrb(Currency):
    ''' Awakener's Orb '''

    name = "awakener_orb"
    pretty_name = "Awakener's Orb"
    stack_size = 10
    regex = "Awakener's Orb"
    template_path = "assets/new_currency_templates/awakener_orb.png"
    size_x = 1
    size_y = 1


class CrusaderExaltedOrb(Currency):
    ''' Crusader's Exalted Orb '''

    name = "crusader_exalted_orb"
    pretty_name = "Crusader's Exalted Orb"
    stack_size = 10
    regex = "Crusader's Exalted Orb"
    template_path = "assets/new_currency_templates/crusader_exalted_orb.png"
    size_x = 1
    size_y = 1


class RedeemerExaltedOrb(Currency):
    ''' Redeemer's Exalted Orb '''

    name = "redeemer_exalted_orb"
    pretty_name = "Redeemer's Exalted Orb"
    stack_size = 10
    regex = "Redeemer's Exalted Orb"
    template_path = "assets/new_currency_templates/redeemer_exalted_orb.png"
    size_x = 1
    size_y = 1


class HunterExaltedOrb(Currency):
    ''' Hunter's Exalted Orb '''

    name = "hunter_exalted_orb"
    pretty_name = "Hunter's Exalted Orb"
    stack_size = 10
    regex = "Hunter's Exalted Orb"
    template_path = "assets/new_currency_templates/hunter_exalted_orb.png"
    size_x = 1
    size_y = 1


class WarlordExaltedOrb(Currency):
    ''' Warlord's Exalted Orb '''

    name = "warlord_exalted_orb"
    pretty_name = "Warlord's Exalted Orb"
    stack_size = 10
    regex = "Warlord's Exalted Orb"
    template_path = "assets/new_currency_templates/warlord_exalted_orb.png"
    size_x = 1
    size_y = 1


class TurbulentCatalyst(Currency):
    ''' Turbulent Catalyst '''

    name = "turbulent_catalyst"
    pretty_name = "Turbulent Catalyst"
    stack_size = 10
    regex = "Turbulent Catalyst"
    template_path = "assets/new_currency_templates/turbulent_catalyst.png"
    size_x = 1
    size_y = 1


class ImbuedCatalyst(Currency):
    ''' Imbued Catalyst '''

    name = "imbued_catalyst"
    pretty_name = "Imbued Catalyst"
    stack_size = 10
    regex = "Imbued Catalyst"
    template_path = "assets/new_currency_templates/imbued_catalyst.png"
    size_x = 1
    size_y = 1


class AbrasiveCatalyst(Currency):
    ''' Abrasive Catalyst '''

    name = "abrasive_catalyst"
    pretty_name = "Abrasive Catalyst"
    stack_size = 10
    regex = "Abrasive Catalyst"
    template_path = "assets/new_currency_templates/abrasive_catalyst.png"
    size_x = 1
    size_y = 1


class TemperingCatalyst(Currency):
    ''' Tempering Catalyst '''

    name = "tempering_catalyst"
    pretty_name = "Tempering Catalyst"
    stack_size = 10
    regex = "Tempering Catalyst"
    template_path = "assets/new_currency_templates/tempering_catalyst.png"
    size_x = 1
    size_y = 1


class FertileCatalyst(Currency):
    ''' Fertile Catalyst '''

    name = "fertile_catalyst"
    pretty_name = "Fertile Catalyst"
    stack_size = 10
    regex = "Fertile Catalyst"
    template_path = "assets/new_currency_templates/fertile_catalyst.png"
    size_x = 1
    size_y = 1


class PrismaticCatalyst(Currency):
    ''' Prismatic Catalyst '''

    name = "prismatic_catalyst"
    pretty_name = "Prismatic Catalyst"
    stack_size = 10
    regex = "Prismatic Catalyst"
    template_path = "assets/new_currency_templates/prismatic_catalyst.png"
    size_x = 1
    size_y = 1


class IntrinsicCatalyst(Currency):
    ''' Intrinsic Catalyst '''

    name = "intrinsic_catalyst"
    pretty_name = "Intrinsic Catalyst"
    stack_size = 10
    regex = "Intrinsic Catalyst"
    template_path = "assets/new_currency_templates/intrinsic_catalyst.png"
    size_x = 1
    size_y = 1


class SimulacrumSplinter(Currency):
    ''' Simulacrum Splinter '''

    name = "simulacrum_splinter"
    pretty_name = "Simulacrum Splinter"
    stack_size = 300
    regex = "Simulacrum Splinter"
    template_path = "assets/new_currency_templates/simulacrum_splinter.png"
    size_x = 1
    size_y = 1


CURRENCY_LIST = [
	ChaosOrb,
	ExaltedOrb,
	DivineOrb,
	OrbofAlchemy,
	OrbofFusing,
	OrbofAlteration,
	RegalOrb,
	VaalOrb,
	OrbofRegret,
	CartographerChisel,
	JewellerOrb,
	SilverCoin,
	PerandusCoin,
	OrbofScouring,
	GemcutterPrism,
	OrbofChance,
	ChromaticOrb,
	BlessedOrb,
	GlassblowerBauble,
	OrbofAugmentation,
	OrbofTransmutation,
	MirrorofKalandra,
	ScrollofWisdom,
	PortalScroll,
	BlacksmithWhetstone,
	ArmourerScrap,
	EternalOrb,
	StackedDeck,
	SimpleSextant,
	PrimeSextant,
	AwakenedSextant,
	ApprenticeCartographerSeal,
	JourneymanCartographerSeal,
	MasterCartographerSeal,
	SplinterofXoph,
	SplinterofTul,
	SplinterofEsh,
	SplinterofUulNetol,
	SplinterofChayula,
	BlessingofXoph,
	BlessingofTul,
	BlessingofEsh,
	BlessingofUulNetol,
	BlessingofChayula,
	OrbofAnnulment,
	OrbofBinding,
	OrbofHorizons,
	HarbingerOrb,
	EngineerOrb,
	AncientOrb,
	AnnulmentShard,
	ExaltedShard,
	MirrorShard,
	TimelessKaruiSplinter,
	TimelessMarakethSplinter,
	TimelessEternalEmpireSplinter,
	TimelessTemplarSplinter,
	TimelessVaalSplinter,
	AwakenerOrb,
	CrusaderExaltedOrb,
	RedeemerExaltedOrb,
	HunterExaltedOrb,
	WarlordExaltedOrb,
	TurbulentCatalyst,
	ImbuedCatalyst,
	AbrasiveCatalyst,
	TemperingCatalyst,
	FertileCatalyst,
	PrismaticCatalyst,
	IntrinsicCatalyst,
	SimulacrumSplinter
]
#class SacrificeatDusk(Currency):#
#    ''' Sacrifice at Dusk '''#
#
#    name = "sacrifice_at_dusk"#
#    pretty_name = "Sacrifice at Dusk"#
#    stack_size = #
#    regex = "Sacrifice at Dusk"#
#    template_path = "assets/new_currency_templates/sacrifice_at_dusk.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class SacrificeatMidnight(Currency):#
#    ''' Sacrifice at Midnight '''#
#
#    name = "sacrifice_at_midnight"#
#    pretty_name = "Sacrifice at Midnight"#
#    stack_size = #
#    regex = "Sacrifice at Midnight"#
#    template_path = "assets/new_currency_templates/sacrifice_at_midnight.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class SacrificeatDawn(Currency):#
#    ''' Sacrifice at Dawn '''#
#
#    name = "sacrifice_at_dawn"#
#    pretty_name = "Sacrifice at Dawn"#
#    stack_size = #
#    regex = "Sacrifice at Dawn"#
#    template_path = "assets/new_currency_templates/sacrifice_at_dawn.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class SacrificeatNoon(Currency):#
#    ''' Sacrifice at Noon '''#
#
#    name = "sacrifice_at_noon"#
#    pretty_name = "Sacrifice at Noon"#
#    stack_size = #
#    regex = "Sacrifice at Noon"#
#    template_path = "assets/new_currency_templates/sacrifice_at_noon.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class MortalGrief(Currency):#
#    ''' Mortal Grief '''#
#
#    name = "mortal_grief"#
#    pretty_name = "Mortal Grief"#
#    stack_size = #
#    regex = "Mortal Grief"#
#    template_path = "assets/new_currency_templates/mortal_grief.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class MortalRage(Currency):#
#    ''' Mortal Rage '''#
#
#    name = "mortal_rage"#
#    pretty_name = "Mortal Rage"#
#    stack_size = #
#    regex = "Mortal Rage"#
#    template_path = "assets/new_currency_templates/mortal_rage.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class MortalIgnorance(Currency):#
#    ''' Mortal Ignorance '''#
#
#    name = "mortal_ignorance"#
#    pretty_name = "Mortal Ignorance"#
#    stack_size = #
#    regex = "Mortal Ignorance"#
#    template_path = "assets/new_currency_templates/mortal_ignorance.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class MortalHope(Currency):#
#    ''' Mortal Hope '''#
#
#    name = "mortal_hope"#
#    pretty_name = "Mortal Hope"#
#    stack_size = #
#    regex = "Mortal Hope"#
#    template_path = "assets/new_currency_templates/mortal_hope.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class EberKey(Currency):#
#    ''' Eber's Key '''#
#
#    name = "eber_key"#
#    pretty_name = "Eber's Key"#
#    stack_size = #
#    regex = "Eber's Key"#
#    template_path = "assets/new_currency_templates/eber_key.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class YrielKey(Currency):#
#    ''' Yriel's Key '''#
#
#    name = "yriel_key"#
#    pretty_name = "Yriel's Key"#
#    stack_size = #
#    regex = "Yriel's Key"#
#    template_path = "assets/new_currency_templates/yriel_key.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class InyaKey(Currency):#
#    ''' Inya's Key '''#
#
#    name = "inya_key"#
#    pretty_name = "Inya's Key"#
#    stack_size = #
#    regex = "Inya's Key"#
#    template_path = "assets/new_currency_templates/inya_key.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class VolkuurKey(Currency):#
#    ''' Volkuur's Key '''#
#
#    name = "volkuur_key"#
#    pretty_name = "Volkuur's Key"#
#    stack_size = #
#    regex = "Volkuur's Key"#
#    template_path = "assets/new_currency_templates/volkuur_key.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentoftheHydra(Currency):#
#    ''' Fragment of the Hydra '''#
#
#    name = "fragment_of_the_hydra"#
#    pretty_name = "Fragment of the Hydra"#
#    stack_size = #
#    regex = "Fragment of the Hydra"#
#    template_path = "assets/new_currency_templates/fragment_of_the_hydra.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofthePhoenix(Currency):#
#    ''' Fragment of the Phoenix '''#
#
#    name = "fragment_of_the_phoenix"#
#    pretty_name = "Fragment of the Phoenix"#
#    stack_size = #
#    regex = "Fragment of the Phoenix"#
#    template_path = "assets/new_currency_templates/fragment_of_the_phoenix.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentoftheMinotaur(Currency):#
#    ''' Fragment of the Minotaur '''#
#
#    name = "fragment_of_the_minotaur"#
#    pretty_name = "Fragment of the Minotaur"#
#    stack_size = #
#    regex = "Fragment of the Minotaur"#
#    template_path = "assets/new_currency_templates/fragment_of_the_minotaur.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentoftheChimera(Currency):#
#    ''' Fragment of the Chimera '''#
#
#    name = "fragment_of_the_chimera"#
#    pretty_name = "Fragment of the Chimera"#
#    stack_size = #
#    regex = "Fragment of the Chimera"#
#    template_path = "assets/new_currency_templates/fragment_of_the_chimera.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class OfferingtotheGoddess(Currency):#
#    ''' Offering to the Goddess '''#
#
#    name = "offering_to_the_goddess"#
#    pretty_name = "Offering to the Goddess"#
#    stack_size = #
#    regex = "Offering to the Goddess"#
#    template_path = "assets/new_currency_templates/offering_to_the_goddess.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class SacrificeSet(Currency):#
#    ''' Sacrifice Set '''#
#
#    name = "sacrifice_set"#
#    pretty_name = "Sacrifice Set"#
#    stack_size = #
#    regex = "Sacrifice Set"#
#    template_path = "assets/new_currency_templates/sacrifice_set.png"#
#    size_x = 2#
#    size_y = 2#
#
##
#class MortalSet(Currency):#
#    ''' Mortal Set '''#
#
#    name = "mortal_set"#
#    pretty_name = "Mortal Set"#
#    stack_size = #
#    regex = "Mortal Set"#
#    template_path = "assets/new_currency_templates/mortal_set.png"#
#    size_x = 2#
#    size_y = 2#
#
##
#class PaleCourtSet(Currency):#
#    ''' Pale Court Set '''#
#
#    name = "pale_court_set"#
#    pretty_name = "Pale Court Set"#
#    stack_size = #
#    regex = "Pale Court Set"#
#    template_path = "assets/new_currency_templates/pale_court_set.png"#
#    size_x = 2#
#    size_y = 2#
#
##
#class ShaperSet(Currency):#
#    ''' Shaper Set '''#
#
#    name = "shaper_set"#
#    pretty_name = "Shaper Set"#
#    stack_size = #
#    regex = "Shaper Set"#
#    template_path = "assets/new_currency_templates/shaper_set.png"#
#    size_x = 2#
#    size_y = 2#
#
##
#class XophBreachstone(Currency):#
#    ''' Xoph's Breachstone '''#
#
#    name = "xoph_breachstone"#
#    pretty_name = "Xoph's Breachstone"#
#    stack_size = #
#    regex = "Xoph's Breachstone"#
#    template_path = "assets/new_currency_templates/xoph_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TulBreachstone(Currency):#
#    ''' Tul's Breachstone '''#
#
#    name = "tul_breachstone"#
#    pretty_name = "Tul's Breachstone"#
#    stack_size = #
#    regex = "Tul's Breachstone"#
#    template_path = "assets/new_currency_templates/tul_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class EshBreachstone(Currency):#
#    ''' Esh's Breachstone '''#
#
#    name = "esh_breachstone"#
#    pretty_name = "Esh's Breachstone"#
#    stack_size = #
#    regex = "Esh's Breachstone"#
#    template_path = "assets/new_currency_templates/esh_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class UulNetolBreachstone(Currency):#
#    ''' Uul-Netol's Breachstone '''#
#
#    name = "uul-netol_breachstone"#
#    pretty_name = "Uul-Netol's Breachstone"#
#    stack_size = #
#    regex = "Uul-Netol's Breachstone"#
#    template_path = "assets/new_currency_templates/uul-netol_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class ChayulaBreachstone(Currency):#
#    ''' Chayula's Breachstone '''#
#
#    name = "chayula_breachstone"#
#    pretty_name = "Chayula's Breachstone"#
#    stack_size = #
#    regex = "Chayula's Breachstone"#
#    template_path = "assets/new_currency_templates/chayula_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class AncientReliquaryKey(Currency):#
#    ''' Ancient Reliquary Key '''#
#
#    name = "ancient_reliquary_key"#
#    pretty_name = "Ancient Reliquary Key"#
#    stack_size = #
#    regex = "Ancient Reliquary Key"#
#    template_path = "assets/new_currency_templates/ancient_reliquary_key.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class DivineVessel(Currency):#
#    ''' Divine Vessel '''#
#
#    name = "divine_vessel"#
#    pretty_name = "Divine Vessel"#
#    stack_size = #
#    regex = "Divine Vessel"#
#    template_path = "assets/new_currency_templates/divine_vessel.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TimewornReliquaryKey(Currency):#
#    ''' Timeworn Reliquary Key '''#
#
#    name = "timeworn_reliquary_key"#
#    pretty_name = "Timeworn Reliquary Key"#
#    stack_size = #
#    regex = "Timeworn Reliquary Key"#
#    template_path = "assets/new_currency_templates/timeworn_reliquary_key.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class XophChargedBreachstone(Currency):#
#    ''' Xoph's Charged Breachstone '''#
#
#    name = "xoph_charged_breachstone"#
#    pretty_name = "Xoph's Charged Breachstone"#
#    stack_size = #
#    regex = "Xoph's Charged Breachstone"#
#    template_path = "assets/new_currency_templates/xoph_charged_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TulChargedBreachstone(Currency):#
#    ''' Tul's Charged Breachstone '''#
#
#    name = "tul_charged_breachstone"#
#    pretty_name = "Tul's Charged Breachstone"#
#    stack_size = #
#    regex = "Tul's Charged Breachstone"#
#    template_path = "assets/new_currency_templates/tul_charged_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class EshChargedBreachstone(Currency):#
#    ''' Esh's Charged Breachstone '''#
#
#    name = "esh_charged_breachstone"#
#    pretty_name = "Esh's Charged Breachstone"#
#    stack_size = #
#    regex = "Esh's Charged Breachstone"#
#    template_path = "assets/new_currency_templates/esh_charged_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class UulNetolChargedBreachstone(Currency):#
#    ''' Uul-Netol's Charged Breachstone '''#
#
#    name = "uul-netol_charged_breachstone"#
#    pretty_name = "Uul-Netol's Charged Breachstone"#
#    stack_size = #
#    regex = "Uul-Netol's Charged Breachstone"#
#    template_path = "assets/new_currency_templates/uul-netol_charged_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class ChayulaChargedBreachstone(Currency):#
#    ''' Chayula's Charged Breachstone '''#
#
#    name = "chayula_charged_breachstone"#
#    pretty_name = "Chayula's Charged Breachstone"#
#    stack_size = #
#    regex = "Chayula's Charged Breachstone"#
#    template_path = "assets/new_currency_templates/chayula_charged_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class XophEnrichedBreachstone(Currency):#
#    ''' Xoph's Enriched Breachstone '''#
#
#    name = "xoph_enriched_breachstone"#
#    pretty_name = "Xoph's Enriched Breachstone"#
#    stack_size = #
#    regex = "Xoph's Enriched Breachstone"#
#    template_path = "assets/new_currency_templates/xoph_enriched_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TulEnrichedBreachstone(Currency):#
#    ''' Tul's Enriched Breachstone '''#
#
#    name = "tul_enriched_breachstone"#
#    pretty_name = "Tul's Enriched Breachstone"#
#    stack_size = #
#    regex = "Tul's Enriched Breachstone"#
#    template_path = "assets/new_currency_templates/tul_enriched_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class EshEnrichedBreachstone(Currency):#
#    ''' Esh's Enriched Breachstone '''#
#
#    name = "esh_enriched_breachstone"#
#    pretty_name = "Esh's Enriched Breachstone"#
#    stack_size = #
#    regex = "Esh's Enriched Breachstone"#
#    template_path = "assets/new_currency_templates/esh_enriched_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class UulNetolEnrichedBreachstone(Currency):#
#    ''' Uul-Netol's Enriched Breachstone '''#
#
#    name = "uul-netol_enriched_breachstone"#
#    pretty_name = "Uul-Netol's Enriched Breachstone"#
#    stack_size = #
#    regex = "Uul-Netol's Enriched Breachstone"#
#    template_path = "assets/new_currency_templates/uul-netol_enriched_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class ChayulaEnrichedBreachstone(Currency):#
#    ''' Chayula's Enriched Breachstone '''#
#
#    name = "chayula_enriched_breachstone"#
#    pretty_name = "Chayula's Enriched Breachstone"#
#    stack_size = #
#    regex = "Chayula's Enriched Breachstone"#
#    template_path = "assets/new_currency_templates/chayula_enriched_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class XophPureBreachstone(Currency):#
#    ''' Xoph's Pure Breachstone '''#
#
#    name = "xoph_pure_breachstone"#
#    pretty_name = "Xoph's Pure Breachstone"#
#    stack_size = #
#    regex = "Xoph's Pure Breachstone"#
#    template_path = "assets/new_currency_templates/xoph_pure_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TulPureBreachstone(Currency):#
#    ''' Tul's Pure Breachstone '''#
#
#    name = "tul_pure_breachstone"#
#    pretty_name = "Tul's Pure Breachstone"#
#    stack_size = #
#    regex = "Tul's Pure Breachstone"#
#    template_path = "assets/new_currency_templates/tul_pure_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class EshPureBreachstone(Currency):#
#    ''' Esh's Pure Breachstone '''#
#
#    name = "esh_pure_breachstone"#
#    pretty_name = "Esh's Pure Breachstone"#
#    stack_size = #
#    regex = "Esh's Pure Breachstone"#
#    template_path = "assets/new_currency_templates/esh_pure_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class UulNetolPureBreachstone(Currency):#
#    ''' Uul-Netol's Pure Breachstone '''#
#
#    name = "uul-netol_pure_breachstone"#
#    pretty_name = "Uul-Netol's Pure Breachstone"#
#    stack_size = #
#    regex = "Uul-Netol's Pure Breachstone"#
#    template_path = "assets/new_currency_templates/uul-netol_pure_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class ChayulaPureBreachstone(Currency):#
#    ''' Chayula's Pure Breachstone '''#
#
#    name = "chayula_pure_breachstone"#
#    pretty_name = "Chayula's Pure Breachstone"#
#    stack_size = #
#    regex = "Chayula's Pure Breachstone"#
#    template_path = "assets/new_currency_templates/chayula_pure_breachstone.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TimelessKaruiEmblem(Currency):#
#    ''' Timeless Karui Emblem '''#
#
#    name = "timeless_karui_emblem"#
#    pretty_name = "Timeless Karui Emblem"#
#    stack_size = #
#    regex = "Timeless Karui Emblem"#
#    template_path = "assets/new_currency_templates/timeless_karui_emblem.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TimelessMarakethEmblem(Currency):#
#    ''' Timeless Maraketh Emblem '''#
#
#    name = "timeless_maraketh_emblem"#
#    pretty_name = "Timeless Maraketh Emblem"#
#    stack_size = #
#    regex = "Timeless Maraketh Emblem"#
#    template_path = "assets/new_currency_templates/timeless_maraketh_emblem.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TimelessEternalEmblem(Currency):#
#    ''' Timeless Eternal Emblem '''#
#
#    name = "timeless_eternal_emblem"#
#    pretty_name = "Timeless Eternal Emblem"#
#    stack_size = #
#    regex = "Timeless Eternal Emblem"#
#    template_path = "assets/new_currency_templates/timeless_eternal_emblem.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TimelessTemplarEmblem(Currency):#
#    ''' Timeless Templar Emblem '''#
#
#    name = "timeless_templar_emblem"#
#    pretty_name = "Timeless Templar Emblem"#
#    stack_size = #
#    regex = "Timeless Templar Emblem"#
#    template_path = "assets/new_currency_templates/timeless_templar_emblem.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class TimelessVaalEmblem(Currency):#
#    ''' Timeless Vaal Emblem '''#
#
#    name = "timeless_vaal_emblem"#
#    pretty_name = "Timeless Vaal Emblem"#
#    stack_size = #
#    regex = "Timeless Vaal Emblem"#
#    template_path = "assets/new_currency_templates/timeless_vaal_emblem.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofEnslavement(Currency):#
#    ''' Fragment of Enslavement '''#
#
#    name = "fragment_of_enslavement"#
#    pretty_name = "Fragment of Enslavement"#
#    stack_size = #
#    regex = "Fragment of Enslavement"#
#    template_path = "assets/new_currency_templates/fragment_of_enslavement.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofEradication(Currency):#
#    ''' Fragment of Eradication '''#
#
#    name = "fragment_of_eradication"#
#    pretty_name = "Fragment of Eradication"#
#    stack_size = #
#    regex = "Fragment of Eradication"#
#    template_path = "assets/new_currency_templates/fragment_of_eradication.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofConstriction(Currency):#
#    ''' Fragment of Constriction '''#
#
#    name = "fragment_of_constriction"#
#    pretty_name = "Fragment of Constriction"#
#    stack_size = #
#    regex = "Fragment of Constriction"#
#    template_path = "assets/new_currency_templates/fragment_of_constriction.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofPurification(Currency):#
#    ''' Fragment of Purification '''#
#
#    name = "fragment_of_purification"#
#    pretty_name = "Fragment of Purification"#
#    stack_size = #
#    regex = "Fragment of Purification"#
#    template_path = "assets/new_currency_templates/fragment_of_purification.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofShape(Currency):#
#    ''' Fragment of Shape '''#
#
#    name = "fragment_of_shape"#
#    pretty_name = "Fragment of Shape"#
#    stack_size = #
#    regex = "Fragment of Shape"#
#    template_path = "assets/new_currency_templates/fragment_of_shape.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofKnowledge(Currency):#
#    ''' Fragment of Knowledge '''#
#
#    name = "fragment_of_knowledge"#
#    pretty_name = "Fragment of Knowledge"#
#    stack_size = #
#    regex = "Fragment of Knowledge"#
#    template_path = "assets/new_currency_templates/fragment_of_knowledge.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofTerror(Currency):#
#    ''' Fragment of Terror '''#
#
#    name = "fragment_of_terror"#
#    pretty_name = "Fragment of Terror"#
#    stack_size = #
#    regex = "Fragment of Terror"#
#    template_path = "assets/new_currency_templates/fragment_of_terror.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class FragmentofEmptiness(Currency):#
#    ''' Fragment of Emptiness '''#
#
#    name = "fragment_of_emptiness"#
#    pretty_name = "Fragment of Emptiness"#
#    stack_size = #
#    regex = "Fragment of Emptiness"#
#    template_path = "assets/new_currency_templates/fragment_of_emptiness.png"#
#    size_x = 1#
#    size_y = 1#
#
##
#class Simulacrum(Currency):#
#    ''' Simulacrum '''#
#
#    name = "simulacrum"#
#    pretty_name = "Simulacrum"#
#    stack_size = #
#    regex = "Simulacrum"#
#    template_path = "assets/new_currency_templates/simulacrum.png"#
#    size_x = 1#
#    size_y = 1#
#
#

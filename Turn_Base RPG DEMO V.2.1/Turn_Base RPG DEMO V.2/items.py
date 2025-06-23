# items.py

class Weapon:
    def __init__(self, name, description, stats_boost, effect=None):
        self.name = name
        self.description = description
        self.stats_boost = stats_boost  # Dictionary, e.g., {'atk': 10, 'crit_dmg': 20}
        self.effect = effect # Untuk efek khusus seperti 'double_attack'

class ItemSet:
    def __init__(self, name, bonus_2, bonus_4_desc, bonus_2_stats, bonus_4_effect):
        self.name = name
        self.bonus_2 = bonus_2
        self.bonus_4_desc = bonus_4_desc
        self.bonus_2_stats = bonus_2_stats
        self.bonus_4_effect = bonus_4_effect

# --- Database Senjata ---

# DPS Weapons
CRIMSON_FANG_BLADE = Weapon("Crimson Fang Blade", "+20% Crit Damage, +10% ATK", {'crit_dmg': 20, 'atk': 10})
STORM_PIERCER = Weapon("Storm Piercer", "+15% SPD, serangan biasa bisa menyerang 2x", {'spd': 15}, effect='double_attack')
DRAGONS_WRATH_GAUNTLETS = Weapon("Dragon's Wrath Gauntlets", "+10% ATK, 25% chance serangan menghasilkan burn", {'atk': 10}, effect='chance_burn')

# Sub-DPS Weapons
SHADOW_FANG_DAGGERS = Weapon("Shadow Fang Daggers", "+10% SPD, bonus damage ke musuh lemah", {'spd': 10}, effect='bonus_dmg_weak')
FROSTBOW_ECLIPSE = Weapon("Frostbow Eclipse", "+5% ATK, 30% chance slow", {'atk': 5}, effect='chance_slow')
CHAOS_ORB = Weapon("Chaos Orb", "+10% ATK, skill memiliki 20% chance efek acak", {'atk': 10}, effect='skill_random_effect')

# Tank Weapons
TITAN_SHIELDWALL = Weapon("Titan Shieldwall", "+30% DEF, +10% aggro", {'defe': 30, 'aggro': 10})
IRON_BASTION_HAMMER = Weapon("Iron Bastion Hammer", "+15% DEF, 20% chance stun", {'defe': 15}, effect='chance_stun')
GUARDIAN_CORE_BLADE = Weapon("Guardian Core Blade", "+10% HP, skill aktif memberikan shield", {'max_hp': 10}, effect='skill_shield_self')

# Support Weapons
MELODY_STAFF = Weapon("Melody Staff", "+10% efektivitas buff, buff berdurasi +1 turn", {'buff_effect': 10, 'buff_duration': 1})
AURA_BELL = Weapon("Aura Bell", "+5% SPD, buff ke semua anggota tim", {'spd': 5}, effect='aoe_buff')
SPIRIT_SCROLL = Weapon("Spirit Scroll", "+10% buff ATK/MAG, skill buff tidak bisa di-cancel", {'buff_potency': 10}, effect='unremovable_buff')

# Healer Weapons
BLESSED_WAND = Weapon("Blessed Wand", "+20% efek heal", {'heal_effect': 20})
HERBAL_GRIMOIRE = Weapon("Herbal Grimoire", "Regen 5% HP ke tim HP terendah tiap turn", {}, effect='passive_regen_lowest')
LIFEWELL_CHALICE = Weapon("Lifewell Chalice", "+10% AoE heal, 10% chance remove 1 debuff", {'aoe_heal_effect': 10}, effect='chance_cleanse')

# Debuffer Weapons
CURSED_CHAIN_WHIP = Weapon("Cursed Chain Whip", "+10% chance DEF debuff, +5% debuff duration", {'debuff_chance': 10, 'debuff_duration': 5})
ABYSSAL_DAGGER = Weapon("Abyssal Dagger", "+15% chance apply poison", {'debuff_chance': 15}, effect='apply_poison')
VOID_TOME = Weapon("Void Tome", "+10% AoE debuff, 20% chance confuse", {'aoe_debuff_potency': 10}, effect='chance_confuse')

WEAPONS_BY_ROLE = {
    "DPS": [CRIMSON_FANG_BLADE, STORM_PIERCER, DRAGONS_WRATH_GAUNTLETS],
    "Sub-DPS": [SHADOW_FANG_DAGGERS, FROSTBOW_ECLIPSE, CHAOS_ORB],
    "Tank": [TITAN_SHIELDWALL, IRON_BASTION_HAMMER, GUARDIAN_CORE_BLADE], 
    "Support": [MELODY_STAFF, AURA_BELL, SPIRIT_SCROLL],
    "Healer": [BLESSED_WAND, HERBAL_GRIMOIRE, LIFEWELL_CHALICE],
    "Debuffer": [CURSED_CHAIN_WHIP, ABYSSAL_DAGGER, VOID_TOME]
}

# --- Database Item Set ---

# DPS Sets
BERSERKERS_SOUL = ItemSet("Berserker's Soul", "+10% ATK", "+15% SPD setelah crit", {'atk': 10}, 'speed_on_crit')
INFERNO_BREAKER = ItemSet("Inferno Breaker", "+20% Crit Damage", "25% chance burn", {'crit_dmg': 20}, 'chance_burn_on_hit')

# Sub-DPS Sets
PHANTOM_EDGE = ItemSet("Phantom Edge", "+10% SPD", "+15% damage ke musuh berstatus negatif", {'spd': 10}, 'dmg_on_debuff')
CHAOS_PULSE = ItemSet("Chaos Pulse", "+5% ATK, +5% DEF", "20% chance efek acak", {'atk': 5, 'defe': 5}, 'chance_random_debuff')

# Tank Sets
FORTRESS_WALL = ItemSet("Fortress Wall", "+20% DEF", "30% chance kurangi damage 50%", {'defe': 20}, 'chance_dmg_reduction')
IRON_SENTINEL = ItemSet("Iron Sentinel", "+15% Max HP", "+30% aggro", {'max_hp': 15, 'aggro': 30}, 'increase_aggro')

# Support Sets
HARMONY_BLESSING = ItemSet("Harmony Blessing", "+15% efek buff", "Buff durasi +1 turn", {'buff_effect': 15}, 'extend_buff_duration')
RESONANT_ECHO = ItemSet("Resonant Echo", "+10% SPD", "Dapat +5% ATK/DEF saat memberi buff", {'spd': 10}, 'self_buff_on_cast')

# Healer Sets
SACRED_GRACE = ItemSet("Sacred Grace", "+20% efek penyembuhan", "Target mendapat regen 5% HP", {'heal_effect': 20}, 'regen_on_heal')
SPIRIT_FLOW = ItemSet("Spirit Flow", "+10% MP Recovery", "25% chance hapus 1 debuff", {'mp_regen': 10}, 'chance_cleanse_on_heal')

# Debuffer Sets
CURSE_WEAVER = ItemSet("Curse Weaver", "+15% efek debuff", "20% chance debuff tak bisa dihilangkan", {'debuff_effect': 15}, 'unremovable_debuff')
WITHERING_VEIL = ItemSet("Withering Veil", "+10% SPD", "Musuh terkena debuff -5% ATK", {'spd': 10}, 'atk_down_on_debuff')


ITEM_SETS_BY_ROLE = {
    "DPS": [BERSERKERS_SOUL, INFERNO_BREAKER],
    "Sub-DPS": [PHANTOM_EDGE, CHAOS_PULSE],
    "Tank": [FORTRESS_WALL, IRON_SENTINEL],
    "Support": [HARMONY_BLESSING, RESONANT_ECHO],
    "Healer": [SACRED_GRACE, SPIRIT_FLOW],
    "Debuffer": [CURSE_WEAVER, WITHERING_VEIL]
}
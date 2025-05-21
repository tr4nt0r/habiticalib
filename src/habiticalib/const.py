"""Constants for Habiticalib."""

__version__ = "0.4.0rc1"

DEFAULT_URL = "https://habitica.com/"
ASSETS_URL = "https://habitica-assets.s3.amazonaws.com/mobileApp/images/"

DEVELOPER_ID = "4c4ca53f-c059-4ffa-966e-9d29dd405daf"

# Assets that doesn't follow name conventions like 2019 Kickstarter gear
# https://github.com/HabitRPG/habitica/blob/develop/website/client/src/assets/css/sprites.css
SPECIAL_ASSETS = {
    "armor_special_ks2019": "BackerOnly-Equip-MythicGryphonArmor.gif",
    "back_special_heroicAureole": "back_special_heroicAureole.gif",
    "background_airship": "background_airship.gif",
    "background_clocktower": "background_clocktower.gif",
    "background_steamworks": "background_steamworks.gif",
    "broad_armor_special_0": "BackerOnly-Equip-ShadeArmor.gif",
    "broad_armor_special_1": "ContributorOnly-Equip-CrystalArmor.gif",
    "broad_armor_special_ks2019": "BackerOnly-Equip-MythicGryphonArmor.gif",
    "eyewear_special_ks2019": "BackerOnly-Equip-MythicGryphonVisor.gif",
    "head_special_0": "BackerOnly-Equip-ShadeHelmet.gif",
    "head_special_1": "ContributorOnly-Equip-CrystalHelmet.gif",
    "head_special_ks2019": "BackerOnly-Equip-MythicGryphonHelm.gif",
    "Mount_Body_Gryphon-Gryphatrice": "BackerOnly-Mount-Body-Gryphatrice.gif",
    "Mount_Head_Gryphon-Gryphatrice": "BackerOnly-Mount-Head-Gryphatrice.gif",
    "Pet-Gryphatrice-Jubilant": "Pet-Gryphatrice-Jubilant.gif",
    "Pet-Gryphon-Gryphatrice": "BackerOnly-Pet-Gryphatrice.gif",
    "Pet-Wolf-Cerberus": "BackerOnly-Pet-CerberusPup.gif",
    "shield_special_0": "BackerOnly-Shield-TormentedSkull.gif",
    "shield_special_ks2019": "BackerOnly-Equip-MythicGryphonShield.gif",
    "slim_armor_special_0": "BackerOnly-Equip-ShadeArmor.gif",
    "slim_armor_special_1": "ContributorOnly-Equip-CrystalArmor.gif",
    "slim_armor_special_ks2019": "BackerOnly-Equip-MythicGryphonArmor.gif",
    "weapon_special_0": "BackerOnly-Weapon-DarkSoulsBlade.gif",
    "weapon_special_critical": "weapon_special_critical.gif",
    "weapon_special_ks2019": "BackerOnly-Equip-MythicGryphonGlaive.gif",
}

SPECIAL_ASSETS_OFFSET = {
    "head_special_0": (-3, -18),
    "weapon_special_0": (-3, -18),
    "weapon_special_critical": (-12, 12),
    "weapon_special_1": (-12, 0),
    "head_special_1": (0, 3),
}

PAGE_LIMIT = 60

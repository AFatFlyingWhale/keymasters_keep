from __future__ import annotations

from dataclasses import dataclass
from random import randint

import functools
from Options import Toggle, OptionSet

from typing import List, Dict, Set, Callable

from ..enums import KeymastersKeepGamePlatforms
from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

@dataclass
class HaloMCCArchipelagoOptions:
    mcc_enabled_games: MCCEnabledGames
    #mcc_include_par_time: MCCIncludeParTime
    #mcc_include_par_score: MCCIncludeParScore
    mcc_include_skulls: MCCIncludeSkulls
    mcc_skull_exclusion: MCCExcludeSkulls
    mcc_include_campaigns: MCCIncludeCampaigns
    mcc_include_firefight: MCCIncludeFirefight
    mcc_include_killcount: MCCIncludeKillcount
    mcc_include_weapons: MCCIncludeWeapons

class HaloMCCGame(Game):
    name = "Halo: The Master Chief Collection"
    platform = KeymastersKeepGamePlatforms.PC
    other_platforms = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX
    ]
    is_adult_only_or_unrated = False
    options_cls = HaloMCCArchipelagoOptions

def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
    return[
        GameObjectiveTemplate(
            label="Without dying",
            data=dict(),
        )
    ]

def game_objective_templates(self) -> List[GameObjectiveTemplate]:
    return [
        GameObjectiveTemplate(
            label="Beat MISSION with SKULLS enabled",
            data={
                "MISSION": (self.missions, 1),
                "SKULLS": (self.skulls, 1),
            },
            is_time_consuming=False,
            is_difficult=False,
            weight=2
        ),
        GameObjectiveTemplate(
            label="Beat CAMPAIGN",
            data={
                "CAMPAIGN": (self.campaign, 1),
            },
            is_time_consuming=False,
            is_difficult=False,
            weight=1
        ),
        GameObjectiveTemplate(
            label="Beat a firefight game on FIREFIGHT",
            data={
                "FIREFIGHT": (self.firefight, 1),
            },
            is_time_consuming=False,
            is_difficult=False,
            weight=2
        ),
        GameObjectiveTemplate(
            label="Kill NUMBER ENEMY",
            data={
                "NUMBER": (self.enemy_numbers, 1),
                "ENEMY": (self.enemies, 1),
            },
            is_time_consuming=False,
            is_difficult=False,
            weight=2
        ),
        GameObjectiveTemplate(
            label="Use WEAPON to kill NUMBER of enemies",
            data={
                "WEAPON": (self.weapons, 1),
                "NUMBER": (self.weapon_numbers, 1),
            },
            is_time_consuming=False,
            is_difficult=False,
            weight=2
        ),
        GameObjectiveTemplate(
            label="Beat MISSION on DIFFICULTY",
            data={
                "MISSION": (self.missions, 1),
                "DIFFICULTY": (self.difficulty, 1)
            },
            is_time_consuming=False,
            is_difficult=False,
            weight=4,
        ),
    ]

# Difficulties

@staticmethod
def difficulty() -> List[str]:
    return[
        "Easy",
        "Normal",
        "Heroic",
        "Legendary",
    ]

# Missions

@property
def enabled_games(self) -> List[str]:
    return sorted(self.archipelago_options.mcc_enabled_games.value)

@property
def halo_reach_enabled(self) -> bool:
    return "Halo Reach" in self.enabled_games

@property
def halo_ce_enabled(self) -> bool:
    return "Halo CE" in self.enabled_games

@property
def halo_2_enabled(self) -> bool:
    return "Halo 2" in self.enabled_games

@property
def halo_3_enabled(self) -> bool:
    return "Halo 3" in self.enabled_games

@property
def halo_3_odst_enabled(self) -> bool:
    return "Halo 3 ODST" in self.enabled_games

@property
def halo_4_enabled(self) -> bool:
    return "Halo 4" in self.enabled_games

@staticmethod
def default_missions() -> List[str]:
    return[]

@staticmethod
def reach_missions() -> List[str]:
    return [
        "Winter Contingency (Reach)",
        "ONI: Sword Base (Reach)",
        "Nightfall (Reach)",
        "Tip Of The Spear (Reach)",
        "Long Night Of Solace (Reach)",
        "Exodus (Reach)",
        "New Alexandria (Reach)",
        "The Package (Reach)",
        "The Pillar Of Autumn (Reach)",
        "Lone Wolf (Reach)",
    ]

@staticmethod
def ce_missions() -> List[str]:
    return [
        "The Pillar Of Autumn (CE)",
        "Halo (CE)",
        "The Truth And Reconciliation (CE)",
        "The Silent Cartographer (CE)",
        "Assault On The Control Room (CE)",
        "343 Guilty Spark (CE)",
        "The Library (CE)",
        "Two Betrayals (CE)",
        "Keyes (CE)",
        "The Maw (CE)",
    ]

@staticmethod
def h2_missions() -> List[str]:
    return [
        "Cairo Station (H2)",
        "Outskirts (H2)",
        "Metropolis (H2)",
        "The Arbiter (H2)",
        "The Oracle (H2)",
        "Delta Halo (H2)",
        "Regret (H2)",
        "Sacred Icon (H2)",
        "Quarantine Zone (H2)",
        "Gravemind (H2)",
        "Uprising (H2)",
        "High Charity (H2)",
        "The Great Journey (H2)",
    ]

@staticmethod
def h3_missions() -> List[str]:
    return [
        "Sierra 117 (H3)",
        "Crow's Nest (H3)",
        "Tsavo Highway (H3)",
        "The Storm (H3)",
        "Floodgate (H3)",
        "The Ark (H3)",
        "The Covenant (H3)",
        "Cortana (H3)",
        "Halo (H3)",
    ]

@staticmethod
def odst_missions() -> List[str]:
    return [
        "Tayari Plaza (ODST)",
        "Uplift Reserve (ODST)",
        "Kizingo Boulevard (ODST)",
        "ONI Alpha Site (ODST)",
        "NMPD HQ (ODST)",
        "Kikowani Station (ODST)",
        "Data Hive (ODST)",
        "Coastal Highway (ODST)",
    ]

@staticmethod
def h4_missions() -> List[str]:
    return [
        "Dawn (H4)",
        "Requiem (H4)",
        "Forerunner (H4)",
        "Infinity (H4)",
        "Reclaimer (H4)",
        "Shutdown (H4)",
        "Composer (H4)",
        "Midnight (H4)",
    ]

@property
def missions(self) -> List[str]:
    mission_list = self.default_missions()[:]
    if self.halo_reach_enabled:
        mission_list.extend(self.reach_missions())
    if self.halo_ce_enabled:
        mission_list.extend(self.ce_missions())
    if self.halo_2_enabled:
        mission_list.extend(self.h2_missions())
    if self.halo_3_enabled:
        mission_list.extend(self.h3_missions())
    if self.halo_3_odst_enabled:
        mission_list.extend(self.odst_missions())
    if self.halo_4_enabled:
        mission_list.extend(self.h4_missions())
    return mission_list

# Skulls

@property
def disabled_skulls(self) -> List[str]:
    return sorted(self.archipelago_options.mcc_skull_exclusion.value)

@staticmethod
def default_skulls() -> List[str]:
    return[
        "Black Eye",
        "Blind",
        "Catch",
        "Cowbell",
        "Famine",
        "Fog",
        "Grunt Birthday Party",
        "Iron",
        "IWHBYD",
        "Mythic",
        "Thunderstorm",
        "Tilt",
        "Tough Luck",
    ]

@property
def skulls(self) -> List[str]:
    exclude_set = set(disabled_skulls)
    result = [item for item in default_skulls if item not in exclude_set]
    return result


# Par Times


# Par Scores


# Campaigns
@staticmethod
def default_campaigns() -> List[str]:
    return[]

@staticmethod
def reach_campaigns() -> List[str]:
    return[
        "Self-Preservation (Reach)",
        "Got Your Back (Reach)",
        "Noble Team Doubles (Reach)",
        "Off Your Feet (Reach)",
        "First to the Fight (Reach)",
    ]

@staticmethod
def ce_campaigns() -> List[str]:
    return[
        "Vehicle Playground (CE)",
        "Daring Escapes (CE)",
        "A New Threat (CE)",
    ]

@staticmethod
def h2_campaigns() -> List[str]:
    return[
        "Arbiter's Journey (H2)",
        "Master Chief's Journey (H2)",
        "Fan Favorites (H2)",
        "Boss Fights (H2)",
    ]

@staticmethod
def h3_campaigns() -> List[str]:
    return[
        "Wheels, Wheels and More Wheels (H3)",
        "Mixin' It Up (H3)",
        "Heavy Anticipation (H3)",
    ]

@staticmethod
def odst_campaigns() -> List[str]:
    return[
        "Vehicle Rally (ODST)",
        "Arena Battles (ODST)",
        "Hoofin' It (ODST)",
        "Street Smarts (ODST)",
    ]

@staticmethod
def h4_campaigns() -> List[str]:
    return[
        "The Covenant Threat (H4)",
        "Canyon Combat (H4)",
        "Tight Corridors (H4)",
    ]

@staticmethod
def cross_campaigns() -> List[str]:
    return[
        "Hogs, Jets, Tanks and Mechs (Cross)",
        "Epic Battles (Cross)",
        "Flooded (Cross)",
        "Freedom of Flight (Cross)",
        "Tanks, Tanks, Tanks (Cross)",
        "Final Four (Cross)",
        "Me and My Hog (Cross)",
        "Sniper School (Cross)",
        "Welcome to the Jungle (Cross)",
        "Get in the Ring (Cross)",
        "Guilty Pleasure (Cross)",
        "Fight and Flight (Cross)",
        "Making an Entrance (Cross)",
    ]

@property
def campaigns(self) -> List[str]:
    campaign_list = self.default_campaigns()[:]
    if self.halo_reach_enabled:
        campaign_list.extend(self.reach_campaigns())
    if self.halo_ce_enabled:
        campaign_list.extend(self.ce_campaigns())
    if self.halo_2_enabled:
        campaign_list.extend(self.h2_campaigns())
    if self.halo_3_enabled:
        campaign_list.extend(self.h3_campaigns())
    if self.halo_3_odst_enabled:
        campaign_list.extend(self.odst_campaigns())
    if self.halo_4_enabled:
        campaign_list.extend(self.h4_campaigns())
    if self.halo_reach_enabled and self.halo_ce_enabled and self.halo_2_enabled and self.halo_3_enabled and self.halo_3_odst_enabled and self.halo_4_enabled:
        campaign_list.extend(self.cross_campaigns())
    return campaign_list

# Firefight
@staticmethod
def default_maps() -> List[str]:
    return[]

@staticmethod
def reach_maps() -> List[str]:
    return[
        "Beachhead",
        "Corvette",
        "Courtyard",
        "Glacier",
        "Holdout",
        "Outpost",
        "Overlook",
        "Waterfront",
        "Unearthed",
        "Installation 04"
    ]

@staticmethod
def odst_maps() -> List[str]:
    return[
        "Crater (Night)",
        "Rally (Night)",
        "Crater",
        "Lost Platoon",
        "Rally Point",
        "Security Zone",
        "Alpha Site",
        "Windward",
        "Chasm Ten",
        "Last Exit"
    ]

@property
def firefight(self) -> List[str]:
    firefight_list = self.default_maps()[:]
    if self.halo_3_odst_enabled:
        firefight_list.extend(self.odst_maps())
    if self.halo_reach_enabled:
        firefight_list.extend(self.reach_maps())
    return firefight_list

# Killcount
@staticmethod
def enemies() -> List[str]:
    return[
        "Grunt",
        "Jackal",
        "Skirmisher",
        "Elite",
        "Brute",
        "Hunter",
        "Drone",
        "Engineer",
        "Flood",
        "Crawler",
        "Watcher",
        "Knight",
    ]

@staticmethod
def enemy_numbers() -> range:
    return range(5,50)


# Weapons
@staticmethod
def weapons() -> List[str]:
    return[
        "Magnum",
        "Assault Rifle",
        "Shotgun",
        "Sniper Rifle",
        "Rocket Launcher",
        "Plasma Pistol",
        "Plasma Rifle",
        "Needler",
        "Energy Sword",
        "Fuel Rod Gun",
        "Sentinel Beam",
        "SMG",
        "Battle Rifle",
        "Brute Plasma Rifle",
        "Brute Shot",
        "Beam Rifle",
        "Carbine",
        "Gravity Hammer",
        "Spartan Laser",
        "Brute Spiker",
        "Brute Mauler",
        "DMR",
        "Grenade Launcher",
        "Needle Rifle",
        "Focus Rifle",
        "Plasma Launcher",
        "Plasma Repeater",
        "Concussion Rifle",
        "Sticky Detonator",
        "SAW",
        "Railgun",
        "Storm Rifle",
        "Boltshot",
        "Suppressor",
        "Scattershot",
        "Light Rifle",
        "Incineration Cannon",
        "Binary Rifle",
    ]

@staticmethod
def weapon_numbers() -> range:
    return range(5,40)



# Archipelago Options
class MCCEnabledGames(OptionSet):
    """
    Enables/disables the available games. At least one must be enabled, obviously.
    """
    display_name = "Enabled Games"
    valid_keys = [
        "Halo Reach",
        "Halo CE",
        "Halo 2",
        "Halo 3",
        "Halo 3 ODST",
        "Halo 4"
    ]
    default = valid_keys

class MCCIncludeSkulls(DefaultOnToggle):
    """
    Enables/disables Skull objectives.
    """
    display_name = "Skull Objectives"

class MCCExcludeSkulls(OptionSet):
    """
    Add Skulls to this list to exclude them from the Skull Objectives. Some Skulls are excluded by default as they are not present in all games (Foreign, Sputnik, etc).
    """
    display_name = "Skull Exclusion"
    valid_keys = [
        "Black Eye",
        "Blind",
        "Catch",
        "Cowbell",
        "Famine",
        "Fog",
        "Grunt Birthday Party",
        "Iron",
        "IWHBYD",
        "Mythic",
        "Thunderstorm",
        "Tilt",
        "Tough Luck",
    ]
    default = ""

class MCCIncludeCampaigns(DefaultOnToggle):
    """
    Enables/disables campaign objectives.
    """
    display_name = "Campaign Objectives"

class MCCIncludeFirefight(DefaultOnToggle):
    """
    Enables/disables Firefight objectives. These will only take effect if Halo 3 ODST or Halo Reach are enabled in the games list.
    """
    display_name = "Firefight Objectives"

class MCCIncludeKillcount(DefaultOnToggle):
    """
    Enables/disables Killcount objectives. (Kill a certain number of a specific enemy). Only enable with all games.
    """
    display_name = "Killcount Objectives"

class MCCIncludeWeapons(DefaultOnToggle):
    """
    Enables/disables Weapon objectives. (Kill a certain number of enemies with a specific weapon). Only enable with all games.
    """
    display_name = "Weapon Objectives"
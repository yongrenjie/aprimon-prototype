import json
from pathlib import Path


ALL_BALLS = ["beast",
             "dream",
             "fast",
             "friend",
             "heavy",
             "level",
             "love",
             "lure",
             "moon",
             "safari",
             "sport"]

class Pokemon:
    display_name: str        # name to show the user
    canonical_name: str      # sanitised name, used to retrieve pokesprite
    other_names: [str]       # regional forms, etc.
    national_dex: int        # ND number
    swsh: dict[str, bool]    # Availability in Sword/Shield
    bdsp: dict[str, bool]    # Availability in Brilliant Diamond / Shining Pearl

    def __init__(self,
                 display_name, canonical_name, other_names,
                 national_dex, swsh, bdsp):
        self.display_name = display_name
        self.canonical_name = canonical_name
        self.other_names = other_names
        # All names -- used to match spreadsheet entries
        self.all_names = [self.display_name.lower(), self.canonical_name, *other_names]
        self.national_dex = national_dex
        # Shortcut for indicating availability -- pass True (or False) instead
        # of a dictionary of True/False
        if swsh is True:
            self.swsh = {ball: True for ball in ALL_BALLS}
        elif swsh is False:
            self.swsh = {ball: False for ball in ALL_BALLS}
        else:
            self.swsh = swsh
        if bdsp is True:
            self.bdsp = {ball: True for ball in ALL_BALLS}
        elif bdsp is False:
            self.bdsp = {ball: False for ball in ALL_BALLS}
        else:
            self.bdsp = bdsp

    def to_dict(self):
        return {
            "canonical_name": self.canonical_name,
            "display_name": self.display_name,
            "national_dex": self.national_dex,
            "swsh": self.swsh,
            "bdsp": self.bdsp,
        }


# Read Pokemon data

ALL_POKEMON = {}

with open(Path(__file__).parent / "pokemon.json") as fp:
    all_data = json.load(fp)
    for pokemon_data in all_data.values():
        pokemon = Pokemon(**pokemon_data)
        ALL_POKEMON[pokemon.national_dex] = pokemon


# Read spreadsheet data

with open(Path(__file__).parent / "spreadsheets.json") as fp:
    ALL_SPREADSHEETS = json.load(fp)

# Personal branch - read more spreadsheets
# Note union operator is 3.9+ only

with open(Path(__file__).parent / "more_spreadsheets.json") as fp:
    MORE_SPREADSHEETS = json.load(fp)
ALL_SPREADSHEETS = ALL_SPREADSHEETS | MORE_SPREADSHEETS

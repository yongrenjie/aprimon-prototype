import warnings
from copy import deepcopy
import re

import gspread

from aprimon.data import ALL_BALLS, ALL_SPREADSHEETS, ALL_POKEMON


def col_to_index(col):
    if len(col) == 1:
        return ord(col.lower()) - ord('a')
    elif len(col) == 2:
        return col_to_index(col[1]) + (26 * (col_to_index(col[0]) + 1))
    else:
        raise ValueError("This function can't parse columns beyond ZZ. Why"
                         " even is your spreadsheet so long?")


def get_pokemon(name):
    search_string = re.sub('[^a-z]', '', name.lower())

    for pokemon in ALL_POKEMON.values():
        if search_string in pokemon.all_names:
            return pokemon

    # Not found -- raise a KeyError and let the caller deal with it. Often this
    # is not actually an error because there are things like column headers in
    # spreadsheets, which are not actually Pokemon names.
    raise KeyError(f"A Pokemon entry was not found for: '{search_string}'")


class Entry:
    """An Entry represents one Pokemon in a collection of Aprimon."""
    def __init__(self, pokemon, balls):
        self.pokemon = pokemon   # entries of ALL_POKEMON
        self.balls = set(balls)  # set of string

    def __add__(self, other):
        # check if both Pokemon are the same
        if self.pokemon.canonical_name != other.pokemon.canonical_name:
            raise TypeError("You are trying to add two different entries"
                            f" with names {self.pokemon.canonical_name}"
                            f" and {other.pokemon.canonical_name}.")
        new_balls = self.balls | other.balls
        return Entry(self.pokemon, new_balls)

    def __sub__(self, other):
        # check if both Pokemon are the same
        if self.pokemon.canonical_name != other.pokemon.canonical_name:
            raise TypeError("You are trying to subtract two different entries"
                            f" with names {self.pokemon.canonical_name}"
                            f" and {other.pokemon.canonical_name}.")
        new_balls = self.balls - other.balls
        return Entry(self.pokemon, new_balls)

    def to_dict(self):
        data = self.pokemon.to_dict()
        data['balls'] = list(self.balls)
        return data


class Collection:
    """A Collection represents a set of Aprimon.

    It's essentially a dictionary with some extra methods; however, subclassing
    dict is slightly tricky in Python so it's probably easier to just wrap it
    with a container."""

    def __init__(self, data):
        self.data = data

    def is_empty(self):
        """Checks if a Collection is empty"""
        return not self.data

    def remove_empty(self):
        """Removes empty Entries from the collection"""
        filtered_data = {national_dex: entry
                         for national_dex, entry in self.data.items()
                         if len(entry.balls) > 0}
        return Collection(filtered_data)

    @classmethod
    def read(cls, gc, user_info):
        if user_info['type'] == 'grid':
            return cls.from_grid(gc, user_info)
        elif user_info['type'] == 'list':
            return cls.from_list(gc, user_info)
        else:
            raise ValueError(f'invalid entry for type: {type}')

    @classmethod
    def from_grid(cls, gc, user_info):
        """Read Aprimon data from a grid-like spreadsheet, usually the main tab
        showing the entire collection"""
        # Read data from spreadsheet into a list of lists
        sheet = gc.open_by_key(user_info["key"])
        tab = sheet.worksheet(user_info["tab_name"])
        pokemon_column = user_info["pokemon_column"]
        ball_columns = user_info["ball_columns"]
        verify_method = user_info["verify_method"]
        # Control whether to read in raw formula or whether to evaluate
        # formulae (deals with some spreadsheet edge cases)
        use_formula = user_info.get("use_formula", True)
        if use_formula:
            data = tab.get_values(value_render_option='formula')
        else:
            data = tab.get_values()

        # Function to check whether a spreadsheet value is present
        def is_present(verify_method, spreadsheet_value):
            if verify_method == 'checkbox':
                # Checks for a ticked checkbox
                if use_formula:
                    # value_render_option='formula' directly returns booleans
                    return spreadsheet_value
                else:
                    # the default option returns strings
                    return spreadsheet_value == "TRUE"
            elif verify_method == 'image':
                # Checks for the presence of an image
                return '=image(' in spreadsheet_value.lower()
            elif verify_method == 'nonempty':
                # Checks that the cell isn't empty
                return spreadsheet_value is not None \
                    and len(spreadsheet_value) > 0
            else:
                raise ValueError(f'method {method} not supported')

        # initialise dict of (national dex, [ball availability])
        collection = {}

        # check for commas in ball_columns and split it if so
        COLUMN_DELIMITER = ','
        if COLUMN_DELIMITER in ball_columns:
            ball_columns = ball_columns.split(COLUMN_DELIMITER)

        # Parse the spreadsheet
        for row in data:
            # Grab the name of the Pokemon in the spreadsheet
            name_in_spreadsheet = row[col_to_index(pokemon_column)].lower()
            name_in_spreadsheet = " ".join(name_in_spreadsheet.split())

            # Check it against ALL_POKEMON to see if a match is found
            try:
                pokemon = get_pokemon(name_in_spreadsheet)
            except KeyError:
                warnings.warn(f'pokemon <{name_in_spreadsheet}> was not found')
            else:
                available_balls = []
                for ball, ball_column in zip(ALL_BALLS, ball_columns):
                    if is_present(verify_method, row[col_to_index(ball_column)]):
                        available_balls.append(ball)
                # Create the entry
                entry = Entry(pokemon, available_balls)
                # If the Pokemon is already indexed (e.g. a different regional
                # form was indexed), then merge it with that one
                if pokemon.national_dex in collection:
                    collection[pokemon.national_dex] = entry + collection[pokemon.national_dex]
                else:
                    collection[pokemon.national_dex] = entry

        return Collection(collection).remove_empty()

    @classmethod
    def from_list(cls, gc, user_info):
        """Read Aprimon data from a list-like tab, typically on-hands"""
        sheet = gc.open_by_key(user_info["key"])
        tab = sheet.worksheet(user_info["tab_name"])
        pokemon_column = user_info["pokemon_column"]
        ball_column = user_info["ball_column"]
        # Control whether to read in raw formula or whether to evaluate
        # formulae (deals with some spreadsheet edge cases)
        use_formula = user_info.get("use_formula", True)
        if use_formula:
            data = tab.get_values(value_render_option='formula')
        else:
            data = tab.get_values()

        collection = {}
        for row in data:
            # Grab the name of the Pokemon in the spreadsheet
            name_in_spreadsheet = row[col_to_index(pokemon_column)].lower()
            name_in_spreadsheet = " ".join(name_in_spreadsheet.split())

            # Check it against ALL_POKEMON to see if a match is found
            try:
                pokemon = get_pokemon(name_in_spreadsheet)
            except KeyError:
                warnings.warn(f'pokemon <{name_in_spreadsheet}> was not found')
            else:
                ball = row[col_to_index(ball_column)].lower()
                ball = ball.split()[0]   # cover for e.g. 'Beast Ball'
                if ball in ALL_BALLS:
                    entry = Entry(pokemon, [ball])
                    if pokemon.national_dex in collection:
                        collection[pokemon.national_dex] = entry + collection[pokemon.national_dex]
                    else:
                        collection[pokemon.national_dex] = entry

        return Collection(collection).remove_empty()

    @classmethod
    def from_manual(cls, lines):
        """lines: list of str, each one being of the form <BALL> <SPECIES>"""
        collection = {}

        for line in lines:
            try:
                [ball, name] = line.split(maxsplit=1)
            except ValueError:
                continue

            ball = ball.lower()
            try:
                pokemon = get_pokemon(name)
            except KeyError:
                warnings.warn(f'pokemon <{name}> was not found')
            else:
                if ball in ALL_BALLS:
                    entry = Entry(pokemon, [ball])
                    if pokemon.national_dex in collection:
                        collection[pokemon.national_dex] = entry + collection[pokemon.national_dex]
                    else:
                        collection[pokemon.national_dex] = entry

        return Collection(collection).remove_empty()
        
    def __add__(self, other):
        """c1 + c2 gives you the aprimon which are in either c1 or c2;
        basically a set union."""
        if isinstance(other, Collection):
            sum_data = deepcopy(self.data)
            for national_dex, other_entry in other.data.items():
                if national_dex in sum_data:
                    sum_data[national_dex] = sum_data[national_dex] + other_entry
                else:
                    sum_data[national_dex] = other_entry
            return Collection(sum_data).remove_empty()
        elif isinstance(other, Entry):
            sum_data = deepcopy(self.data)
            nat_dex = other.pokemon.national_dex
            if nat_dex in sum_data:
                sum_data[nat_dex] = sum_data[nat_dex] + entry
            else:
                sum_data[nat_dex] = entry
            return Collection(sum_data).remove_empty()
        else:
            return NotImplemented

    def __sub__(self, other):
        """c1 - c2 gives you the aprimon which are in c1 but not in c2;
        basically a set difference, or the relative complement of c1 with
        respect to c2."""
        if isinstance(other, Collection):
            difference_data = deepcopy(self.data)
            for national_dex, other_entry in other.data.items():
                if national_dex in difference_data:
                    difference_data[national_dex] = difference_data[national_dex] - other_entry
                # No need to do anything if it's not in the original dataset
            return Collection(difference_data).remove_empty()
        elif isinstance(other, Entry):
            difference_data = deepcopy(self.data)
            nat_dex = other.pokemon.national_dex
            if nat_dex in difference_data:
                difference_data[nat_dex] = difference_data[nat_dex] - entry
            else:
                difference_data[nat_dex] = entry
            return Collection(difference_data).remove_empty()
        else:
            return NotImplemented

    def to_list(self):
        """Returns a list of all the Entries, which can be serialised as JSON
        and sent back to the frontend."""
        return [entry.to_dict() for entry in self.data.values()]

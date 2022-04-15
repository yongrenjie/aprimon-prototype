import warnings
from copy import deepcopy
import re

import gspread

from aprimon.data import ALL_BALLS, ALL_SPREADSHEETS, ALL_POKEMON


def uppercase_first(ball):
    return ball[0].upper() + ball[1:]


def col_to_index(col):
    return ord(col.lower()) - ord('a')


def get_pokemon(name):
    search_string = re.sub('[^a-z]', '', name.lower())

    for pokemon in ALL_POKEMON.values():
        if search_string in pokemon.all_names:
            return pokemon
    # If we don't find it, then it should (in principle) be considered an
    # error. For now the function calling this catches the error and re-throws
    # a warning
    raise KeyError(f"A Pokemon entry was not found for: '{search_string}'")


# one row of a Collection
class Entry:
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


# a full Collection
class Collection:
    def __init__(self, data):
        self.data = data
        # dictionary of {int: set(string)} as shown below

    def is_empty(self):
        return not self.data


    def remove_empty(self):
        filtered_data = {national_dex: entry
                         for national_dex, entry in self.data.items()
                         if len(entry.balls) > 0}
        return Collection(filtered_data)

    @classmethod
    def read(cls, gc, username):
        try:
            user_info = ALL_SPREADSHEETS[username]
        except KeyError:
            raise KeyError(f"User /u/{username}'s spreadsheet was not registered")

        if user_info['type'] == 'grid':
            return cls.from_grid(gc, username)
        elif user_info['type'] == 'list':
            return cls.from_list(gc, username)
        else:
            raise ValueError(f'invalid entry for type: {type}')


    @classmethod
    def from_grid(cls, gc, username):
        """Read Aprimon data from a grid-like spreadsheet, usually the main tab
        showing the entire collection"""
        # Read data from spreadsheet into a list of lists
        user_info = ALL_SPREADSHEETS[username]
        sheet = gc.open_by_key(user_info["key"])
        tab = sheet.worksheet(user_info["tab_name"])
        pokemon_column = user_info["pokemon_column"]
        ball_columns = user_info["ball_columns"]
        verify_method = user_info["verify_method"]
        data = tab.get_values(value_render_option='formula')

        # Function to check whether a spreadsheet value is present
        def is_present(verify_method, spreadsheet_value):
            if verify_method == 'checkbox':
                # Checks for a ticked checkbox (which actually comes out as a
                # boolean when we use value_render_option='formula')
                return spreadsheet_value
            elif verify_method == 'image':
                # Checks for the presence of an image
                return '=image(' in spreadsheet_value.lower()
            else:
                raise ValueError(f'method {method} not supported')

        # initialise dict of (national dex, [ball availability])
        collection = {}

        print(user_info)

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
                        # print(f'found in {username}: {pokemon.canonical_name} - {ball}')
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
    def from_list(cls, gc, username):
        """Read Aprimon data from a list-like tab, typically on-hands"""
        user_info = ALL_SPREADSHEETS[username]
        sheet = gc.open_by_key(user_info["key"])
        tab = sheet.worksheet(user_info["tab_name"])
        pokemon_column = user_info["pokemon_column"]
        ball_column = user_info["ball_column"]
        data = tab.get_values(value_render_option='formula')

        print(user_info)

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
                if ball in ALL_BALLS:
                    # print(f'found in {username}: {pokemon.canonical_name} - {ball}')
                    entry = Entry(pokemon, [ball])
                    if pokemon.national_dex in collection:
                        collection[pokemon.national_dex] = entry + collection[pokemon.national_dex]
                    else:
                        collection[pokemon.national_dex] = entry

        return Collection(collection).remove_empty()
        

    # c1 + c2 gives you the aprimon which are in either c1 or c2
    def __add__(self, other):
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


    # c1 - c2 gives you the aprimon which are in c1 but not in c2.
    def __sub__(self, other):
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


    def get_entries(self, sort="name"):
        if sort == "name":
            return list(sorted(self.data.values(), key=(lambda e: e.pokemon.display_name)))
        elif sort == "dex":
            return list(sorted(self.data.values(), key=(lambda e: e.pokemon.national_dex)))
        else:
            raise ValueError('invalid sorting method: supported methods are "name" or "dex"')


    def pretty_print(self):
        # remove empty rows
        stripped = {national_dex: balls for national_dex, balls in self.data.items()
                    if len(balls) != 0}

        # determine longest display name
        longest_name = max(stripped.keys(), key=(lambda nd: len(ALL_POKEMON[nd].display_name)))
        name_width = len(longest_name)

        def print_one_entry(national_dex, available_balls):
            s = ""
            s += f"{ALL_POKEMON[national_dex].display_name:{name_width}}"
            s += " |  "
            for ball in ALL_BALLS:
                ball_width = len(ball)
                if ball in available_balls:
                    s += f"{uppercase_first(ball):{ball_width}} "
                else:
                    s += " " * (ball_width + 1)
            return s

        lines = [print_one_entry(pokemon, available_balls)
                 for pokemon, available_balls in stripped.items()]
        return "\n".join(lines)


    def print_as_text(self):
        for national_dex, available_balls in self.data.items():
            for ball in available_balls:
                print(f'{uppercase_first(ball)} {ALL_POKEMON[national_dex].display_name}')

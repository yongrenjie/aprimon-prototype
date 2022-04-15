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
        # of a list of True/False
        if swsh is True:
            self.swsh = [True for _ in range(len(ALL_BALLS))]
        elif swsh is False:
            self.swsh = [False for _ in range(len(ALL_BALLS))]
        else:
            self.swsh = swsh
        if bdsp is True:
            self.bdsp = [True for _ in range(len(ALL_BALLS))]
        elif bdsp is False:
            self.bdsp = [False for _ in range(len(ALL_BALLS))]
        else:
            self.bdsp = bdsp


ALL_POKEMON = {
    1: Pokemon("Bulbasaur", "bulbasaur", [], 1, swsh=True, bdsp=False),
    4: Pokemon("Charmander", "charmander", [], 4, swsh=True, bdsp=False),
    7: Pokemon("Squirtle", "squirtle", [], 7, swsh=True, bdsp=False),
    10: Pokemon("Caterpie", "caterpie", [], 10, swsh=True, bdsp=False),
    27: Pokemon("Sandshrew", "sandshrew",
                ["sandshrew-a", "sandshrew-alola", "sandshrew (alola)", "sandshrew (kanto)"],
                27, swsh=True, bdsp=False),
    29: Pokemon("Nidoran♀", "nidoran-f",
                ["nidoran-m", "nidoran♀", "nidoran♂"],
                29, swsh=True, bdsp=False),
    37: Pokemon("Vulpix", "vulpix", 
                ["vulpix-a", "vulpix-alola", "vulpix (alola)", "vulpix (kanto)"],
                37, swsh=True, bdsp=False),
    41: Pokemon("Zubat", "zubat", [], 41, swsh=True, bdsp=False),
    43: Pokemon("Oddish", "oddish", [], 43, swsh=True, bdsp=False),
    50: Pokemon("Diglett", "diglett",
                ["diglett-a", "diglett-alola", "diglett (alola)", "diglett (kanto)"],
                50, swsh=True, bdsp=False),
    52: Pokemon("Meowth", "meowth",
                ["meowth-a", "meowth-alola", "meowth (alola)", "meowth-g", "meowth-galar", "meowth (galar)", "meowth (kanto)"],
                52, swsh=True, bdsp=False),
    54: Pokemon("Psyduck", "psyduck", [], 54, swsh=True, bdsp=False),
    58: Pokemon("Growlithe", "growlithe", [], 58, swsh=True, bdsp=False),
    60: Pokemon("Poliwag", "poliwag", [], 60, swsh=True, bdsp=False),
    63: Pokemon("Abra", "abra", [], 63, swsh=True, bdsp=False),
    66: Pokemon("Machop", "machop", [], 66, swsh=True, bdsp=False),
    72: Pokemon("Tentacool", "tentacool", [], 72, swsh=True, bdsp=False),
    77: Pokemon("Ponyta", "ponyta",
                ["ponyta-g", "ponyta-galar", "ponyta (galar)", "ponyta (kanto)"],
                77, swsh=True, bdsp=False),
    79: Pokemon("Slowpoke", "slowpoke",
                ["slowpoke-g", "slowpoke-galar", "slowpoke (galar)", "slowpoke (kanto)"],
                79, swsh=True, bdsp=False),
    81: Pokemon("Magnemite", "magnemite", [], 81, swsh=True, bdsp=False),
    83: Pokemon("Farfetch'd", "farfetchd",
                ["farfetch'd-g", "farfetch'd-galar", "farfetch'd (galar)",
                 "farfetch'd (kanto)"],
                83, swsh=True, bdsp=False),
    90: Pokemon("Shellder", "shellder", [], 90, swsh=True, bdsp=False),
    92: Pokemon("Gastly", "gastly", [], 92, swsh=True, bdsp=False),
    95: Pokemon("Onix", "onix", [], 95, swsh=True, bdsp=False),
    98: Pokemon("Krabby", "krabby", [], 98, swsh=True, bdsp=False),
    102: Pokemon("Exeggcute", "exeggcute", [], 102, swsh=True, bdsp=False),
    104: Pokemon("Cubone", "cubone", [], 104, swsh=True, bdsp=False),
    108: Pokemon("Lickitung", "lickitung", [], 108, swsh=True, bdsp=False),
    109: Pokemon("Koffing", "koffing", [], 109, swsh=True, bdsp=False),
    111: Pokemon("Rhyhorn", "rhyhorn", [], 111, swsh=True, bdsp=False),
    113: Pokemon("Chansey", "chansey", ["happiny"], 113, swsh=True, bdsp=False),
    114: Pokemon("Tangela", "tangela", [], 114, swsh=True, bdsp=False),
    115: Pokemon("Kangaskhan", "kangaskhan", [], 115, swsh=True, bdsp=False),
    116: Pokemon("Horsea", "horsea", [], 116, swsh=True, bdsp=False),
    118: Pokemon("Goldeen", "goldeen", [], 118, swsh=True, bdsp=False),
    120: Pokemon("Staryu", "staryu", [], 120, swsh=True, bdsp=False),
    122: Pokemon("Mr. Mime", "mr-mime",
                 ["mr. mime-g", "mr. mime-galar",
                  "mr. mime (galar)", "mr. mime (kanto)", "mime jr."],
                 122, swsh=True, bdsp=False),
    123: Pokemon("Scyther", "scyther", [], 123, swsh=True, bdsp=False),
    127: Pokemon("Pinsir", "pinsir", [], 127, swsh=True, bdsp=False),
    128: Pokemon("Tauros", "tauros", [], 128, swsh=True, bdsp=False),
    129: Pokemon("Magikarp", "magikarp", [], 129, swsh=True, bdsp=False),
    131: Pokemon("Lapras", "lapras", [], 131, swsh=True, bdsp=False),
    133: Pokemon("Eevee", "eevee", [], 133, swsh=True, bdsp=False),
    137: Pokemon("Porygon", "porygon", [], 137, swsh=True, bdsp=False),
    138: Pokemon("Omanyte", "omanyte", [], 138, swsh=True, bdsp=False),
    140: Pokemon("Kabuto", "kabuto", [], 140, swsh=True, bdsp=False),
    142: Pokemon("Aerodactyl", "aerodactyl", [], 142, swsh=True, bdsp=False),
    143: Pokemon("Snorlax", "snorlax", ["munchlax"], 143, swsh=True, bdsp=False),
    147: Pokemon("Dratini", "dratini", [], 147, swsh=True, bdsp=False),
    163: Pokemon("Hoothoot", "hoothoot", [], 163, swsh=True, bdsp=False),
    170: Pokemon("Chinchou", "chinchou", [], 170, swsh=True, bdsp=False),
    172: Pokemon("Pichu", "pichu", ["pikachu"], 172, swsh=True, bdsp=False),
    173: Pokemon("Cleffa", "cleffa", ["clefairy"], 173, swsh=True, bdsp=False),
    174: Pokemon("Igglybuff", "igglybuff", ["jigglypuff"], 174, swsh=True, bdsp=False),
    175: Pokemon("Togepi", "togepi", [], 175, swsh=True, bdsp=False),
    177: Pokemon("Natu", "natu", [], 177, swsh=True, bdsp=False),
    183: Pokemon("Marill", "marill", ["azurill"], 183, swsh=True, bdsp=False),
    185: Pokemon("Sudowoodo", "sudowoodo", ["bonsly"], 185, swsh=True, bdsp=False),
    194: Pokemon("Wooper", "wooper", [], 194, swsh=True, bdsp=False),
    202: Pokemon("Wobbuffet", "wobbuffet", ["wynaut"], 202, swsh=True, bdsp=False),
    206: Pokemon("Dunsparce", "dunsparce", [], 206, swsh=True, bdsp=False),
    211: Pokemon("Qwilfish", "qwilfish", [], 211, swsh=True, bdsp=False),
    213: Pokemon("Shuckle", "shuckle", [], 213, swsh=True, bdsp=False),
    214: Pokemon("Heracross", "heracross", [], 214, swsh=True, bdsp=False),
    215: Pokemon("Sneasel", "sneasel", [], 215, swsh=True, bdsp=False),
    220: Pokemon("Swinub", "swinub", [], 220, swsh=True, bdsp=False),
    222: Pokemon("Corsola", "corsola",
                 ["corsola-g", "corsola-galar", "corsola (galar)", "corsola (johto)"],
                 222, swsh=True, bdsp=False),
    223: Pokemon("Remoraid", "remoraid", [], 223, swsh=True, bdsp=False),
    225: Pokemon("Delibird", "delibird", [], 225, swsh=True, bdsp=False),
    226: Pokemon("Mantine", "mantine", ["mantyke"], 226, swsh=True, bdsp=False),
    227: Pokemon("Skarmory", "skarmory", [], 227, swsh=True, bdsp=False),
    236: Pokemon("Tyrogue", "tyrogue", ["hitmonchan", "hitmonlee", "hitmontop"], 236, swsh=True, bdsp=False),
    238: Pokemon("Smoochum", "smoochum", ["jynx"], 238, swsh=True, bdsp=False),
    239: Pokemon("Elekid", "elekid", ["electabuzz"], 239, swsh=True, bdsp=False),
    240: Pokemon("Magby", "magby", ["magmar"], 240, swsh=True, bdsp=False),
    241: Pokemon("Miltank", "miltank", [], 241, swsh=True, bdsp=False),
    246: Pokemon("Larvitar", "larvitar", [], 246, swsh=True, bdsp=False),
    252: Pokemon("Treecko", "treecko", [], 252, swsh=True, bdsp=False),
    255: Pokemon("Torchic", "torchic", [], 255, swsh=True, bdsp=False),
    258: Pokemon("Mudkip", "mudkip", [], 258, swsh=True, bdsp=False),
    263: Pokemon("Zigzagoon", "zigzagoon",
                 ["zigzagoon-g", "zigzagoon-galar", "zigzagoon (galar)",
                  "zigzagoon (hoenn)"],
                 263, swsh=True, bdsp=False),
    270: Pokemon("Lotad", "lotad", [], 270, swsh=True, bdsp=False),
    273: Pokemon("Seedot", "seedot", [], 273, swsh=True, bdsp=False),
    278: Pokemon("Wingull", "wingull", [], 278, swsh=True, bdsp=False),
    280: Pokemon("Ralts", "ralts", [], 280, swsh=True, bdsp=False),
    290: Pokemon("Nincada", "nincada", [], 290, swsh=True, bdsp=False),
    293: Pokemon("Whismur", "whismur", [], 293, swsh=True, bdsp=False),
    302: Pokemon("Sableye", "sableye", [], 302, swsh=True, bdsp=False),
    303: Pokemon("Mawile", "mawile", [], 303, swsh=True, bdsp=False),
    304: Pokemon("Aron", "aron", [], 304, swsh=True, bdsp=False),
    309: Pokemon("Electrike", "electrike", [], 309, swsh=True, bdsp=False),
    315: Pokemon("Roselia", "roselia", [], 315, swsh=True, bdsp=False),
    318: Pokemon("Carvanha", "carvanha", [], 318, swsh=True, bdsp=False),
    320: Pokemon("Wailmer", "wailmer", [], 320, swsh=True, bdsp=False),
    324: Pokemon("Torkoal", "torkoal", [], 324, swsh=True, bdsp=False),
    328: Pokemon("Trapinch", "trapinch", [], 328, swsh=True, bdsp=False),
    333: Pokemon("Swablu", "swablu", [], 333, swsh=True, bdsp=False),
    337: Pokemon("Lunatone", "lunatone", [], 337, swsh=True, bdsp=False),
    338: Pokemon("Solrock", "solrock", [], 338, swsh=True, bdsp=False),
    339: Pokemon("Barboach", "barboach", [], 339, swsh=True, bdsp=False),
    341: Pokemon("Corphish", "corphish", [], 341, swsh=True, bdsp=False),
    343: Pokemon("Baltoy", "baltoy", [], 343, swsh=True, bdsp=False),
    345: Pokemon("Lileep", "lileep", [], 345, swsh=True, bdsp=False),
    347: Pokemon("Anorith", "anorith", [], 347, swsh=True, bdsp=False),
    349: Pokemon("Feebas", "feebas", [], 349, swsh=True, bdsp=False),
    355: Pokemon("Duskull", "duskull", [], 355, swsh=True, bdsp=False),
    359: Pokemon("Absol", "absol", [], 359, swsh=True, bdsp=False),
    361: Pokemon("Snorunt", "snorunt", [], 361, swsh=True, bdsp=False),
    363: Pokemon("Spheal", "spheal", [], 363, swsh=True, bdsp=False),
    369: Pokemon("Relicanth", "relicanth", [], 369, swsh=True, bdsp=False),
    371: Pokemon("Bagon", "bagon", [], 371, swsh=True, bdsp=False),
    374: Pokemon("Beldum", "beldum", [], 374, swsh=True, bdsp=False),
    403: Pokemon("Shinx", "shinx", [], 403, swsh=True, bdsp=False),
    415: Pokemon("Combee", "combee", [], 415, swsh=True, bdsp=False),
    420: Pokemon("Cherubi", "cherubi", [], 420, swsh=True, bdsp=False),
    422: Pokemon("Shellos", "shellos",
                 ["shellos-west", "shellos-west-sea", "shellos (west)",
                  "shellos (west sea)", "shellos-east", "shellos-east-sea",
                  "shellos (east)", "shellos (east sea)"],
                 422, swsh=True, bdsp=False),
    425: Pokemon("Drifloon", "drifloon", [], 425, swsh=True, bdsp=False),
    427: Pokemon("Buneary", "buneary", [], 427, swsh=True, bdsp=False),
    434: Pokemon("Stunky", "stunky", [], 434, swsh=True, bdsp=False),
    436: Pokemon("Bronzor", "bronzor", [], 436, swsh=True, bdsp=False),
    442: Pokemon("Spiritomb", "spiritomb", [], 442, swsh=True, bdsp=False),
    443: Pokemon("Gible", "gible", [], 443, swsh=True, bdsp=False),
    447: Pokemon("Riolu", "riolu", [], 447, swsh=True, bdsp=False),
    449: Pokemon("Hippopotas", "hippopotas", [], 449, swsh=True, bdsp=False),
    451: Pokemon("Skorupi", "skorupi", [], 451, swsh=True, bdsp=False),
    453: Pokemon("Croagunk", "croagunk", [], 453, swsh=True, bdsp=False),
    459: Pokemon("Snover", "snover", [], 459, swsh=True, bdsp=False),
    479: Pokemon("Rotom", "rotom", [], 479, swsh=True, bdsp=False),
    506: Pokemon("Lillipup", "lillipup", [], 506, swsh=True, bdsp=False),
    509: Pokemon("Purrloin", "purrloin", [], 509, swsh=True, bdsp=False),
    517: Pokemon("Munna", "munna", [], 517, swsh=True, bdsp=False),
    519: Pokemon("Pidove", "pidove", [], 519, swsh=True, bdsp=False),
    524: Pokemon("Roggenrola", "roggenrola", [], 524, swsh=True, bdsp=False),
    527: Pokemon("Woobat", "woobat", [], 527, swsh=True, bdsp=False),
    529: Pokemon("Drilbur", "drilbur", [], 529, swsh=True, bdsp=False),
    531: Pokemon("Audino", "audino", [], 531, swsh=True, bdsp=False),
    532: Pokemon("Timburr", "timburr", [], 532, swsh=True, bdsp=False),
    535: Pokemon("Tympole", "tympole", [], 535, swsh=True, bdsp=False),
    538: Pokemon("Throh", "throh", [], 538, swsh=True, bdsp=False),
    539: Pokemon("Sawk", "sawk", [], 539, swsh=True, bdsp=False),
    543: Pokemon("Venipede", "venipede", [], 543, swsh=True, bdsp=False),
    546: Pokemon("Cottonee", "cottonee", [], 546, swsh=True, bdsp=False),
    548: Pokemon("Petilil", "petilil", [], 548, swsh=True, bdsp=False),
    550: Pokemon("Basculin", "basculin",
                 ["basculin-blue", "basculin-blue-striped",
                  "basculin (blue)", "basculin (blue striped)",
                  "basculin-red", "basculin-red-striped",
                  "basculin (red)", "basculin (red striped)"],
                 550, swsh=True, bdsp=False),
    551: Pokemon("Sandile", "sandile", [], 551, swsh=True, bdsp=False),
    554: Pokemon("Darumaka", "darumaka",
                 ["darumaka-g", "darumaka-galar", "darumaka (galar)",
                  "darumaka (unova)"],
                 554, swsh=True, bdsp=False),
    556: Pokemon("Maractus", "maractus", [], 556, swsh=True, bdsp=False),
    557: Pokemon("Dwebble", "dwebble", [], 557, swsh=True, bdsp=False),
    559: Pokemon("Scraggy", "scraggy", [], 559, swsh=True, bdsp=False),
    561: Pokemon("Sigilyph", "sigilyph", [], 561, swsh=True, bdsp=False),
    562: Pokemon("Yamask", "yamask",
                 ["yamask-g", "yamask-galar", "yamask (galar)",
                  "yamask (unova)"],
                 562, swsh=True, bdsp=False),
    564: Pokemon("Tirtouga", "tirtouga", [], 564, swsh=True, bdsp=False),
    566: Pokemon("Archen", "archen", [], 566, swsh=True, bdsp=False),
    568: Pokemon("Trubbish", "trubbish", [], 568, swsh=True, bdsp=False),
    570: Pokemon("Zorua", "zorua", [], 570, swsh=True, bdsp=False),
    572: Pokemon("Minccino", "minccino", [], 572, swsh=True, bdsp=False),
    574: Pokemon("Gothita", "gothita", [], 574, swsh=True, bdsp=False),
    577: Pokemon("Solosis", "solosis", [], 577, swsh=True, bdsp=False),
    582: Pokemon("Vanillite", "vanillite", [], 582, swsh=True, bdsp=False),
    587: Pokemon("Emolga", "emolga", [], 587, swsh=True, bdsp=False),
    588: Pokemon("Karrablast", "karrablast", [], 588, swsh=True, bdsp=False),
    590: Pokemon("Foongus", "foongus", [], 590, swsh=True, bdsp=False),
    592: Pokemon("Frillish", "frillish", [], 592, swsh=True, bdsp=False),
    595: Pokemon("Joltik", "joltik", [], 595, swsh=True, bdsp=False),
    597: Pokemon("Ferroseed", "ferroseed", [], 597, swsh=True, bdsp=False),
    599: Pokemon("Klink", "klink", [], 599, swsh=True, bdsp=False),
    605: Pokemon("Elgyem", "elgyem", [], 605, swsh=True, bdsp=False),
    607: Pokemon("Litwick", "litwick", [], 607, swsh=True, bdsp=False),
    610: Pokemon("Axew", "axew", [], 610, swsh=True, bdsp=False),
    613: Pokemon("Cubchoo", "cubchoo", [], 613, swsh=True, bdsp=False),
    615: Pokemon("Cryogonal", "cryogonal", [], 615, swsh=True, bdsp=False),
    616: Pokemon("Shelmet", "shelmet", [], 616, swsh=True, bdsp=False),
    618: Pokemon("Stunfisk", "stunfisk",
                 ["stunfisk-g", "stunfisk-galar", "stunfisk (galar)",
                  "stunfisk (unova)"],
                 618, swsh=True, bdsp=False),
    619: Pokemon("Mienfoo", "mienfoo", [], 619, swsh=True, bdsp=False),
    621: Pokemon("Druddigon", "druddigon", [], 621, swsh=True, bdsp=False),
    622: Pokemon("Golett", "golett", [], 622, swsh=True, bdsp=False),
    624: Pokemon("Pawniard", "pawniard", [], 624, swsh=True, bdsp=False),
    626: Pokemon("Bouffalant", "bouffalant", [], 626, swsh=True, bdsp=False),
    627: Pokemon("Rufflet", "rufflet", [], 627, swsh=True, bdsp=False),
    629: Pokemon("Vullaby", "vullaby", [], 629, swsh=True, bdsp=False),
    631: Pokemon("Heatmor", "heatmor", [], 631, swsh=True, bdsp=False),
    632: Pokemon("Durant", "durant", [], 632, swsh=True, bdsp=False),
    633: Pokemon("Deino", "deino", [], 633, swsh=True, bdsp=False),
    636: Pokemon("Larvesta", "larvesta", [], 636, swsh=True, bdsp=False),
    659: Pokemon("Bunnelby", "bunnelby", [], 659, swsh=True, bdsp=False),
    661: Pokemon("Fletchling", "fletchling", [], 661, swsh=True, bdsp=False),
    674: Pokemon("Pancham", "pancham", [], 674, swsh=True, bdsp=False),
    677: Pokemon("Espurr", "espurr", [], 677, swsh=True, bdsp=False),
    679: Pokemon("Honedge", "honedge", [], 679, swsh=True, bdsp=False),
    682: Pokemon("Spritzee", "spritzee", [], 682, swsh=True, bdsp=False),
    684: Pokemon("Swirlix", "swirlix", [], 684, swsh=True, bdsp=False),
    686: Pokemon("Inkay", "inkay", [], 686, swsh=True, bdsp=False),
    688: Pokemon("Binacle", "binacle", [], 688, swsh=True, bdsp=False),
    690: Pokemon("Skrelp", "skrelp", [], 690, swsh=True, bdsp=False),
    692: Pokemon("Clauncher", "clauncher", [], 692, swsh=True, bdsp=False),
    694: Pokemon("Helioptile", "helioptile", [], 694, swsh=True, bdsp=False),
    696: Pokemon("Tyrunt", "tyrunt", [], 696, swsh=True, bdsp=False),
    698: Pokemon("Amaura", "amaura", [], 698, swsh=True, bdsp=False),
    701: Pokemon("Hawlucha", "hawlucha", [], 701, swsh=True, bdsp=False),
    702: Pokemon("Dedenne", "dedenne", [], 702, swsh=True, bdsp=False),
    703: Pokemon("Carbink", "carbink", [], 703, swsh=True, bdsp=False),
    704: Pokemon("Goomy", "goomy", [], 704, swsh=True, bdsp=False),
    707: Pokemon("Klefki", "klefki", [], 707, swsh=True, bdsp=False),
    708: Pokemon("Phantump", "phantump", [], 708, swsh=True, bdsp=False),
    710: Pokemon("Pumpkaboo", "pumpkaboo",
                 ["pumpkaboo (average)", "pumpkaboo (small)",
                  "pumpkaboo (large)", "pumpkaboo (super)"],
                 710, swsh=True, bdsp=False),
    712: Pokemon("Bergmite", "bergmite", [], 712, swsh=True, bdsp=False),
    714: Pokemon("Noibat", "noibat", [], 714, swsh=True, bdsp=False),
    722: Pokemon("Rowlet", "rowlet", [], 722, swsh=True, bdsp=False),
    725: Pokemon("Litten", "litten", [], 725, swsh=True, bdsp=False),
    728: Pokemon("Popplio", "popplio", [], 728, swsh=True, bdsp=False),
    736: Pokemon("Grubbin", "grubbin", [], 736, swsh=True, bdsp=False),
    742: Pokemon("Cutiefly", "cutiefly", [], 742, swsh=True, bdsp=False),
    744: Pokemon("Rockruff", "rockruff",
                 ["rockruff-dusk", "rockruff (dusk)",
                  "rockruff (own tempo)", "own tempo rockruff",
                  "rockruff-own tempo"],
                 744, swsh=True, bdsp=False),
    746: Pokemon("Wishiwashi", "wishiwashi", [], 746, swsh=True, bdsp=False),
    747: Pokemon("Mareanie", "mareanie", [], 747, swsh=True, bdsp=False),
    749: Pokemon("Mudbray", "mudbray", [], 749, swsh=True, bdsp=False),
    751: Pokemon("Dewpider", "dewpider", [], 751, swsh=True, bdsp=False),
    753: Pokemon("Fomantis", "fomantis", [], 753, swsh=True, bdsp=False),
    755: Pokemon("Morelull", "morelull", [], 755, swsh=True, bdsp=False),
    757: Pokemon("Salandit", "salandit", [], 757, swsh=True, bdsp=False),
    759: Pokemon("Stufful", "stufful", [], 759, swsh=True, bdsp=False),
    761: Pokemon("Bounsweet", "bounsweet", [], 761, swsh=True, bdsp=False),
    764: Pokemon("Comfey", "comfey", [], 764, swsh=True, bdsp=False),
    765: Pokemon("Oranguru", "oranguru", [], 765, swsh=True, bdsp=False),
    766: Pokemon("Passimian", "passimian", [], 766, swsh=True, bdsp=False),
    767: Pokemon("Wimpod", "wimpod", [], 767, swsh=True, bdsp=False),
    769: Pokemon("Sandygast", "sandygast", [], 769, swsh=True, bdsp=False),
    771: Pokemon("Pyukumuku", "pyukumuku", [], 771, swsh=True, bdsp=False),
    776: Pokemon("Turtonator", "turtonator", [], 776, swsh=True, bdsp=False),
    777: Pokemon("Togedemaru", "togedemaru", [], 777, swsh=True, bdsp=False),
    778: Pokemon("Mimikyu", "mimikyu", [], 778, swsh=True, bdsp=False),
    780: Pokemon("Drampa", "drampa", [], 780, swsh=True, bdsp=False),
    781: Pokemon("Dhelmise", "dhelmise", [], 781, swsh=True, bdsp=False),
    782: Pokemon("Jangmo-o", "jangmo-o", [], 782, swsh=True, bdsp=False),
    810: Pokemon("Grookey", "grookey", [], 810, swsh=True, bdsp=False),
    813: Pokemon("Scorbunny", "scorbunny", [], 813, swsh=True, bdsp=False),
    816: Pokemon("Sobble", "sobble", [], 816, swsh=True, bdsp=False),
    819: Pokemon("Skwovet", "skwovet", [], 819, swsh=True, bdsp=False),
    821: Pokemon("Rookidee", "rookidee", [], 821, swsh=True, bdsp=False),
    824: Pokemon("Blipbug", "blipbug", [], 824, swsh=True, bdsp=False),
    827: Pokemon("Nickit", "nickit", [], 827, swsh=True, bdsp=False),
    829: Pokemon("Gossifleur", "gossifleur", [], 829, swsh=True, bdsp=False),
    831: Pokemon("Wooloo", "wooloo", [], 831, swsh=True, bdsp=False),
    833: Pokemon("Chewtle", "chewtle", [], 833, swsh=True, bdsp=False),
    835: Pokemon("Yamper", "yamper", [], 835, swsh=True, bdsp=False),
    837: Pokemon("Rolycoly", "rolycoly", [], 837, swsh=True, bdsp=False),
    840: Pokemon("Applin", "applin", [], 840, swsh=True, bdsp=False),
    843: Pokemon("Silicobra", "silicobra", [], 843, swsh=True, bdsp=False),
    845: Pokemon("Cramorant", "cramorant", [], 845, swsh=True, bdsp=False),
    846: Pokemon("Arrokuda", "arrokuda", [], 846, swsh=True, bdsp=False),
    848: Pokemon("Toxel", "toxel", [], 848, swsh=True, bdsp=False),
    850: Pokemon("Sizzlipede", "sizzlipede", [], 850, swsh=True, bdsp=False),
    852: Pokemon("Clobbopus", "clobbopus", [], 852, swsh=True, bdsp=False),
    854: Pokemon("Sinistea", "sinistea", [], 854, swsh=True, bdsp=False),
    856: Pokemon("Hatenna", "hatenna", [], 856, swsh=True, bdsp=False),
    859: Pokemon("Impidimp", "impidimp", [], 859, swsh=True, bdsp=False),
    868: Pokemon("Milcery", "milcery", [], 868, swsh=True, bdsp=False),
    870: Pokemon("Falinks", "falinks", [], 870, swsh=True, bdsp=False),
    871: Pokemon("Pincurchin", "pincurchin", [], 871, swsh=True, bdsp=False),
    872: Pokemon("Snom", "snom", [], 872, swsh=True, bdsp=False),
    874: Pokemon("Stonjourner", "stonjourner", [], 874, swsh=True, bdsp=False),
    875: Pokemon("Eiscue", "eiscue", [], 875, swsh=True, bdsp=False),
    876: Pokemon("Indeedee", "indeedee",
                 ["indeedee-f", "indeedee-m", "indeedee♀", "indeedee♂"],
                 876, swsh=True, bdsp=False),
    877: Pokemon("Morpeko", "morpeko", [], 877, swsh=True, bdsp=False),
    878: Pokemon("Cufant", "cufant", [], 878, swsh=True, bdsp=False),
    884: Pokemon("Duraludon", "duraludon", [], 884, swsh=True, bdsp=False),
    885: Pokemon("Dreepy", "dreepy", [], 885, swsh=True, bdsp=False),
}


ALL_SPREADSHEETS = {
    "OnePointPi": {
        "key": "1V2uPApY6JDJZln_YwJ7aHG0ITw5d5jqFSdmIMPTmNb4",
        "tab_name": "SwSh/Home",
        "pokemon_column": "C",
        "ball_columns": "NMFGHIJKLOP",
        "verify_method": "checkbox",
    },
    "orthocresol": {
        "key": "1gbRtsdIxN9X43mhyaMw5QTlPQodpwyzaGGyXqvClxho",
        "tab_name": "Aprimon",
        "pokemon_column": "C",
        "ball_columns": "FGHIJKLMNOP",
        "verify_method": "checkbox",
    },
    "orthocresol_FAKE_SPREADSHEET": {
        "key": "1MnAY9sh3MM3Ts9Zrc-a6slPuFn42nsXSFXafMR_FCP0",
        "tab_name": "Aprimon",
        "pokemon_column": "C",
        "ball_columns": "FGHIJKLMNOP",
        "verify_method": "checkbox",
    },
    "torithetaurus": {
        "key": "1A_dV8DsEPnHP6fY8SvFYsHSBjD3RsXgmaK47wG7M3_E",
        "tab_name": "HA Aprimons",
        "pokemon_column": "C",
        "ball_columns": "NMFGHIJKLOP",
        "verify_method": "checkbox",
    },
}

"""Terminal-based Connections game with configurable categories and rendering."""

import random
import re
from colorama import Fore, Style

def print_items(items: list[str], sep: str = ", ", conj: str = "") -> None:
    """Print items as a readable list with an optional conjunction."""
    if not items:
        print()
    elif len(items) == 1:
        print(items[0])
    elif len(items) == 2:
        sep = f" {conj} " if conj else sep
        print(f"{items[0]}{sep}{items[1]}")
    else:
        last_sep = f"{conj} " if conj else ""
        print(f"{sep.join(items[:-1])}{sep}{last_sep}{items[-1]}")

def rpt_print(string: str = "", n: int = 30, end: str = "\n") -> None:
    """Prints "string" "n" times"""
    for i in range(0, n): print(string, end=end)

_TEMPLATE_TOKEN_RE = re.compile(
    r"\$(?:r_word|words|word|cursor|selected|sel|sign|cat|c_[A-Za-z]+|p_[^$\s]+|[cprb])"
)
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")

def _split_template(template: str) -> list[str]:
    """Split template text into literal strings and individual trigger tokens."""
    parts: list[str] = []
    end = 0

    for match in _TEMPLATE_TOKEN_RE.finditer(template):
        if end < match.start():
            parts.append(template[end:match.start()])
        parts.append(match.group())
        end = match.end()

    if end < len(template):
        parts.append(template[end:])

    return parts

class Category:
    """A named category of related words."""

    def __init__(self, name: str, words: list[str], color: str) -> None:
        """Create a category, copying its words and building selectable tiles."""
        self.name = name
        self.words = list(words)
        self.tiles: list[Tile] = [Tile(word, self) for word in self.words]
        self.color = color

class Tile:
    """A selectable word tile belonging to a category."""

    def __init__(self, word: str, category: Category) -> None:
        """Create a tile for a word in a category."""
        self.word = word
        self.category = category
        self.is_selected = False

    def set_selected(self, is_selected: bool) -> None:
        """Set whether this tile is selected."""
        self.is_selected = is_selected

CATEGORIES_BY_DIFFICULTY: dict[str, list[Category]] = {
    "yellow": [
        Category("Shades of Red", ["CHERRY", "RUBY", "CRIMSON", "SCARLET"], Fore.YELLOW),
        Category("Parts of a Book", ["JACKET", "SPINE", "PAGE", "CHAPTER"], Fore.YELLOW),
        Category("Fast Food Chains", ["SUBWAY", "WENDYS", "SONIC", "MCDONALDS"], Fore.YELLOW),
        Category("Kinds of Shoes", ["LOAFER", "SNEAKER", "BOOT", "PUMP"], Fore.YELLOW),
        Category("Basic Geometry Shapes", ["SQUARE", "CIRCLE", "TRIANGLE", "DIAMOND"], Fore.YELLOW),
        Category("Things in a Wallet", ["CASH", "CARD", "RECEIPT", "PHOTO"], Fore.YELLOW),
        Category("Kitchen Appliances", ["TOASTER", "BLENDER", "OVEN", "FRIDGE"], Fore.YELLOW),
        Category("Types of Weather", ["RAIN", "SNOW", "HAIL", "SLEET"], Fore.YELLOW),
        Category("Trees", ["OAK", "PINE", "MAPLE", "BIRCH"], Fore.YELLOW),
        Category("Time Units", ["SECOND", "MINUTE", "HOUR", "CENTURY"], Fore.YELLOW),
        Category("Ways to Walk", ["STRIDE", "PACE", "STROLL", "MARCH"], Fore.YELLOW),
        Category("Parts of a Tree", ["ROOT", "TRUNK", "BRANCH", "LEAF"], Fore.YELLOW),
        Category("Things that are Yellow", ["BANANA", "LEMON", "CORN", "CANARY"], Fore.YELLOW),
        Category("Baking Ingredients", ["FLOUR", "SUGAR", "YEAST", "BUTTER"], Fore.YELLOW),
        Category("Card Suits", ["HEART", "DIAMOND", "CLUB", "SPADE"], Fore.YELLOW),
        Category("Types of Meat", ["BEEF", "PORK", "CHICKEN", "TURKEY"], Fore.YELLOW),
        Category("Office Supplies", ["PEN", "STAPLER", "FOLDER", "CLIP"], Fore.YELLOW),
        Category("Forms of Water", ["STEAM", "ICE", "VAPOR", "LIQUID"], Fore.YELLOW),
        Category("Kinds of Furniture", ["COUCH", "TABLE", "CHAIR", "DESK"], Fore.YELLOW),
        Category("Units of Currency", ["DOLLAR", "EURO", "POUND", "YEN"], Fore.YELLOW),
        Category("Root Vegetables", ["CARROT", "BEET", "TURNIP", "RADISH"], Fore.YELLOW),
        Category("School Subjects", ["MATH", "SCIENCE", "HISTORY", "ENGLISH"], Fore.YELLOW),
        Category("Four-Sided Shapes", ["SQUARE", "RECTANGLE", "RHOMBUS", "TRAPEZOID"], Fore.YELLOW),
        Category("Breakfast Foods", ["OATMEAL", "PANCAKE", "WAFFLE", "CEREAL"], Fore.YELLOW),
        Category("Bathroom Items", ["TOWEL", "SOAP", "SHAMPOO", "TOOTHBRUSH"], Fore.YELLOW),
        Category("Things with Handles", ["MUG", "DOOR", "BROOM", "UMBRELLA"], Fore.YELLOW),
        Category("Types of Bread", ["SOURDOUGH", "RYE", "PITA", "BAGEL"], Fore.YELLOW),
        Category("Dance Styles", ["WALTZ", "TANGO", "SALSA", "FOXTROT"], Fore.YELLOW),
        Category("A Small Amount", ["BIT", "DROP", "DASH", "PINCH"], Fore.YELLOW),
        Category("Things that Fold", ["MAP", "TOWEL", "NAPKIN", "PAPER"], Fore.YELLOW)
    ],
    "green": [
        Category("Things that are Sharp", ["KNIFE", "WIT", "CHEDDAR", "TACK"], Fore.GREEN),
        Category("Palindromes", ["KAYAK", "RACECAR", "RADAR", "MOM"], Fore.GREEN),
        Category("Synonyms for 'Excellent'", ["STELLAR", "SUPERB", "PRIME", "CHOICE"], Fore.GREEN),
        Category("Types of Insurance", ["LIFE", "HEALTH", "AUTO", "HOME"], Fore.GREEN),
        Category("Waterway Features", ["CANAL", "STREAM", "RIVER", "CHANNEL"], Fore.GREEN),
        Category("Slang for Money", ["BREAD", "DOUGH", "CLAMS", "BUCKS"], Fore.GREEN),
        Category("Things that Fly", ["PILOT", "KITE", "SPARROW", "FRISBEE"], Fore.GREEN),
        Category("Internet Browsers", ["CHROME", "SAFARI", "EDGE", "OPERA"], Fore.GREEN),
        Category("Gems and Minerals", ["QUARTZ", "JADE", "DIAMOND", "EMERALD"], Fore.GREEN),
        Category("Ways to Fasten Clothes", ["BUTTON", "ZIPPER", "SNAP", "BUCKLE"], Fore.GREEN),
        Category("Types of Cheese", ["BRIE", "GOUDA", "SWISS", "CHEDDAR"], Fore.GREEN),
        Category("Gym Equipment", ["WEIGHT", "BENCH", "MAT", "TREADMILL"], Fore.GREEN),
        Category("Things with Screens", ["PHONE", "TABLET", "MONITOR", "LAPTOP"], Fore.GREEN),
        Category("Musical Instruments", ["FLUTE", "CELLO", "ORGAN", "HARP"], Fore.GREEN),
        Category("Words Meaning 'Stop'", ["CEASE", "HALT", "QUIT", "DESIST"], Fore.GREEN),
        Category("Types of Footwear", ["SLIPPER", "SNEAKER", "CLOG", "SANDAL"], Fore.GREEN),
        Category("Found in a Laboratory", ["BEAKER", "FLASK", "SCOPE", "VIAL"], Fore.GREEN),
        Category("Types of Fabric", ["SILK", "COTTON", "WOOL", "SATIN"], Fore.GREEN),
        Category("Parts of a Car", ["HOOD", "TRUNK", "WHEEL", "BRAKE"], Fore.GREEN),
        Category("Synonyms for 'Happy'", ["GLAD", "JOYFUL", "MERRY", "ELATED"], Fore.GREEN),
        Category("Synonyms for 'Brief'", ["TERSE", "CONCISE", "SUCCINCT", "LACONIC"], Fore.GREEN),
        Category("Words Meaning 'Praise'", ["LAUD", "EXTOL", "ACCLAIM", "COMMEND"], Fore.GREEN),
        Category("Poetic Forms", ["SONNET", "HAIKU", "ODE", "ELEGY"], Fore.GREEN),
        Category("Types of Clouds", ["CIRRUS", "CUMULUS", "STRATUS", "NIMBUS"], Fore.GREEN),
        Category("Words before 'Stone'", ["STEPPING", "MILE", "CORNER", "TOUCH"], Fore.GREEN),
        Category("Rhetorical Devices", ["IRONY", "HYPERBOLE", "ALLUSION", "OXYMORON"], Fore.GREEN),
        Category("A Difficult Situation", ["QUANDARY", "DILEMMA", "PREDICAMENT", "PICKLE"], Fore.GREEN),
        Category("Synonyms for 'Avoid'", ["EVADE", "ELUDE", "DODGE", "SHUN"], Fore.GREEN),
        Category("Words Ending in '-ology'", ["BIOLOGY", "GEOLOGY", "ZOOLOGY", "ECOLOGY"], Fore.GREEN),
        Category("Words Meaning 'Inspect'", ["EXAMINE", "SCRUTINIZE", "SURVEY", "REVIEW"], Fore.GREEN)
    ],
    "blue": [
        Category("Words that can follow 'Apple'", ["CORE", "SAUCE", "JACKS", "PIE"], Fore.BLUE),
        Category("Homophones for Animals", ["BARE", "DEER", "HARE", "NIGHTINGALE"], Fore.BLUE),
        Category("Things with Wings", ["AIRPLANE", "ANGEL", "BUTTERFLY", "STAGE"], Fore.BLUE),
        Category("Words meaning 'Fake'", ["SHAM", "PHONY", "BOGUS", "ARTIFICIAL"], Fore.BLUE),
        Category("Rhymes with 'Blue'", ["GREW", "THROUGH", "SHOE", "QUEUE"], Fore.BLUE),
        Category("Things you 'Strike'", ["MATCH", "POSE", "DEAL", "BALANCE"], Fore.BLUE),
        Category("Found in a Casino", ["CHIPS", "DEALER", "SLOTS", "WHEEL"], Fore.BLUE),
        Category("Celestial Bodies", ["SATURN", "COMET", "MARS", "ASTEROID"], Fore.BLUE),
        Category("Anatomical Homophones", ["EYE", "HAIR", "HEEL", "SOLE"], Fore.BLUE),
        Category("Units of Measurement", ["FOOT", "GRAIN", "STONE", "YARD"], Fore.BLUE),
        Category("Words before 'Card'", ["CREDIT", "GIFT", "WILD", "FLASH"], Fore.BLUE),
        Category("Things with Teeth", ["COMB", "GEAR", "SAW", "SHARK"], Fore.BLUE),
        Category("Can follow 'Rain'", ["BOW", "COAT", "DROP", "FALL"], Fore.BLUE),
        Category("Famous Painters", ["MONET", "MANET", "RENOIR", "DEGAS"], Fore.BLUE),
        Category("Slang for 'Excellent'", ["WILD", "SWEET", "COOL", "RAD"], Fore.BLUE),
        Category("Things that Spin", ["TOP", "WHEEL", "EARTH", "RECORD"], Fore.BLUE),
        Category("Things you 'Catch'", ["COLD", "DRIFT", "BREATH", "WAVE"], Fore.BLUE),
        Category("Palindromic Names", ["ANNA", "BOB", "OTTO", "NATHAN"], Fore.BLUE),
        Category("Homophones for Clothes", ["COAT", "SUIT", "PANTS", "JEANS"], Fore.BLUE),
        Category("Things that are Green", ["ENVY", "LIME", "MINT", "JADE"], Fore.BLUE),
        Category("Homographs with Different Pronunciations", ["BASS", "BOW", "LEAD", "TEAR"], Fore.BLUE),
        Category("Kinds of Berry", ["STRAWBERRY", "BLUEBERRY", "CRANBERRY", "RASPBERRY"], Fore.BLUE),
        Category("Shakespearean Characters", ["HAMLET", "OPHELIA", "IAGO", "MACBETH"], Fore.BLUE),
        Category("Words before 'Court'", ["SUPREME", "TENNIS", "FOOD", "NIGHT"], Fore.BLUE),
        Category("Collective Animal Nouns", ["MURDER", "PRIDE", "SCHOOL", "PARLIAMENT"], Fore.BLUE),
        Category("Words Ending in '-ate'", ["LOCATE", "NARRATE", "VACATE", "DONATE"], Fore.BLUE),
        Category("Greek Gods and Goddesses", ["ATHENA", "ARES", "HERA", "HERMES"], Fore.BLUE),
        Category("Words before 'Time'", ["OVER", "DOWN", "PAST", "LIFE"], Fore.BLUE),
        Category("Silent Initial Letters", ["GNOME", "PSALM", "KNIFE", "WRECK"], Fore.BLUE),
        Category("Words Meaning 'Withdraw'", ["RETRACT", "RENEGE", "RECOIL", "BACKPEDAL"], Fore.BLUE)
    ],
    "purple": [
        Category("Words that start with US States", ["MAINSPRING", "MASSIVE", "INDIAN", "OREGONIAN"], Fore.MAGENTA),
        Category("Anagrams of 'LEAST'", ["STALE", "TALES", "SLATE", "TEALS"], Fore.MAGENTA),
        Category("Double Letters in the Middle", ["SPOON", "COFFEE", "BUBBLE", "EGGPLANT"], Fore.MAGENTA),
        Category("Ending in Greek Letters", ["ALPHABET", "MICROBETA", "CHEVRONDELTA", "PI"], Fore.MAGENTA),
        Category("Synonyms for 'Complain' that are also animals", ["CRAB", "GROUSE", "BEEF", "CARP"], Fore.MAGENTA),
        Category("Words containing hidden numbers", ["ATTENTION", "OZONE", "WEIGHT", "FORTRESS"], Fore.MAGENTA),
        Category("Homophones for units of time", ["OUR", "MINUET", "SECONDO", "DAZE"], Fore.MAGENTA),
        Category("Slang for 'Head'", ["NOGGIN", "MELON", "DOME", "BEAN"], Fore.MAGENTA),
        Category("Words before 'Jack'", ["BLACK", "LUMBER", "FLAP", "APPLE"], Fore.MAGENTA),
        Category("Palindromic words when reversed", ["STAR", "LIVE", "DIAPER", "KNITS"], Fore.MAGENTA),
        Category("Words that contain elements", ["IRONIC", "LEADERSHIP", "GOLDEN", "CARBON"], Fore.MAGENTA),
        Category("Anagrams of 'SPARE'", ["PEARS", "REAPS", "SPEAR", "PARSE"], Fore.MAGENTA),
        Category("Ending in body parts", ["BEFOREHAND", "FOOTNOTE", "HEADSTRONG", "ARMCHAIR"], Fore.MAGENTA),
        Category("Words that sound like letters", ["QUEUE", "BEE", "SEA", "WHY"], Fore.MAGENTA),
        Category("Homophones for numbers", ["WON", "TOO", "FOR", "ATE"], Fore.MAGENTA),
        Category("Words containing calendar months", ["MAYHEM", "DECEASED", "MARCHING", "AUGMENT"], Fore.MAGENTA),
        Category("Slang for 'Money' that are also food", ["BREAD", "DOUGH", "CHIPS", "CHEDDAR"], Fore.MAGENTA),
        Category("Words before 'Fish'", ["JELLY", "STAR", "GOLDFISH", "CAT"], Fore.MAGENTA),
        Category("Words with three double letters", ["BOOKKEEPER", "COMMITTEE", "WOOLLIEST", "TATOOEE"], Fore.MAGENTA),
        Category("Words that read backward as other words", ["PART", "REWARD", "SNAP", "STRAW"], Fore.MAGENTA),
        Category("Anagrams of 'STONE'", ["TONES", "NOTES", "ONSET", "STONE"], Fore.MAGENTA),
        Category("Words Made Only of Roman Numerals", ["CIVIC", "CIVIL", "MIX", "MIMIC"], Fore.MAGENTA),
        Category("Words with Alphabetical Letters", ["ALMOST", "BIOPSY", "CHINTZ", "EFFORT"], Fore.MAGENTA),
        Category("Words with 'OUGH'", ["THOUGH", "THROUGH", "ROUGH", "COUGH"], Fore.MAGENTA),
        Category("Words with Multiple Double Letters", ["BOOKKEEPER", "COMMITTEE", "BALLOON", "SUCCESS"], Fore.MAGENTA),
        Category("Anagrams of 'CARES'", ["ACRES", "SCARE", "RACES", "CARES"], Fore.MAGENTA),
        Category("Words with Stress-Shift Homographs", ["RECORD", "PRESENT", "OBJECT", "PERMIT"], Fore.MAGENTA),
        Category("Words with Silent Letters", ["AISLE", "SUBTLE", "HYMN", "AUTUMN"], Fore.MAGENTA),
        Category("Words with Silent 'GH'", ["THOUGHT", "EIGHT", "LIGHT", "KNIGHT"], Fore.MAGENTA),
        Category("Words Containing 'one' Hidden", ["PHONE", "STONE", "ALONE", "CLONE"], Fore.MAGENTA)
    ]
}

WORDS_PER_CATEGORY: int = 4
# Preserve the original public name for existing imports.
SELECT_COUNT: int = WORDS_PER_CATEGORY
# Preserve the original category collection name for existing imports.
CATS_BY_DIFFICULTY: dict[str, list[Category]] = CATEGORIES_BY_DIFFICULTY

def trig_to_str(
    trigger: str,
    tile: Tile,
    num_pad: int = 0,
    cursor: bool = False,
    selected: bool = False,
) -> str:
    """Resolve a template trigger into display text for a tile."""
    TRIG_DICT: dict[str, str] = {
        "$sign": "$",
        "$words": " ".join(
            tile.category.words if tile.category is not None else []
        ),
        "$cat": tile.category.name if tile.category is not None else "",
        "$cursor": (
            f"{Style.BRIGHT}{Fore.WHITE}▲{Style.RESET_ALL}" if cursor else " "
        ),
        "$selected": Style.BRIGHT if selected else "",
        "$sel": Style.BRIGHT if selected else "",
        "$r_word": tile.word * num_pad,
        "$p": " " * num_pad,
        "$word": tile.word,
        "$c": tile.category.color if tile.category is not None else "",
        "$r": Style.RESET_ALL,
        "$b": Style.BRIGHT,
    }
    if trigger in TRIG_DICT:
        return TRIG_DICT[trigger]
    if trigger.startswith("$c_"):
        color_name = trigger[3:].upper()
        return getattr(Fore, color_name, Fore.RESET)
    if trigger.startswith("$p_"):
        filler = trigger[3:]
        if not filler:
            return ""
        return (filler * ((num_pad + len(filler) - 1) // len(filler)))[:num_pad]
    return trigger

class GameBoard:
    """Manage a Connections board, cursor, tile selections, and solved categories."""

    MOVES: dict[str, tuple[int, int]] = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
    }

    CATEGORY_BAR_VISUAL: str = "| $p$b$c$cat$r$p |"
    WORDS_VISUAL: str = "$p$words$p"
    TILE_BOX_VISUAL: str = "$sel[$p $word $p]$r"
    CURSOR_LINE_VISUAL: str = "$p$cursor$p"
    BOX_VISUAL: str = TILE_BOX_VISUAL

    def __init__(
        self,
        tiles: list[Tile] | None = None,
        cats: list[Category] | None = None,
        cols: int = 4,
        rows: int = 4,
        lives: int | None = None,
        *,
        num_moves: int | None = None,
    ) -> None:
        """Create a board from categories, tiles, or randomly chosen categories.

        ``rows`` is the maximum board height; used rows shrink as groups are solved.
        ``num_moves`` remains as a compatibility alias for ``lives``.
        """
        if cols <= 0 or rows <= 0:
            raise ValueError("Board width and height must be positive.")
        if tiles is not None and cats is not None:
            raise ValueError("Provide either tiles or categories, not both.")
        if lives is not None and num_moves is not None:
            raise ValueError("Specify either lives or num_moves, not both.")
        if num_moves is not None:
            lives = num_moves
        if lives is not None and lives < 0:
            raise ValueError("The number of lives cannot be negative.")

        self.cols = cols
        self.max_rows = rows
        self.rows = rows
        self.tiles: list[Tile] = []
        self.cats: list[Category] = []
        self.cursor_pos: tuple[int, int] = (0, 0)
        self.selected_tiles: list[Tile] = []
        self.solved_cats: list[Category] = []
        self.lives_remaining = lives
        self.max_lives = lives

        if cats is not None:
            self.set_categories(cats)
        elif tiles is not None:
            self.set_tiles(tiles)
        else:
            self.generate_board()

    @property
    def num_moves(self) -> int | None:
        """Compatibility alias for the number of remaining lives."""
        return self.lives_remaining

    @num_moves.setter
    def num_moves(self, value: int | None) -> None:
        """Set remaining lives using the legacy property name."""
        if value is not None and value < 0:
            raise ValueError("The number of lives cannot be negative.")
        self.lives_remaining = value

    @property
    def all_words(self) -> list[str]:
        """Return every word belonging to the board's categories."""
        return [word for cat in self.cats for word in cat.words]

    @property
    def cursor_tile(self) -> Tile:
        """Return the tile currently under the cursor."""
        return self.get_tile_at(self.cursor_pos)

    @property
    def rendered_board(self) -> str:
        """Render solved groups above the unsolved tiles and their cursor markers."""
        examples = [tile for category in self.cats for tile in category.tiles]
        if not examples:
            examples = list(self.tiles)
        if not examples:
            return ""

        max_cell_width = max(
            len(
                _ANSI_ESCAPE_RE.sub(
                    "",
                    self.fill_template(self.TILE_BOX_VISUAL, tile),
                )
            )
            for tile in examples
        )
        max_full_line_width = max_cell_width
        for category in self.cats:
            sample = category.tiles[0] if category.tiles else Tile("", category)
            for template in (self.CATEGORY_BAR_VISUAL, self.WORDS_VISUAL):
                rendered = self.fill_template(template, sample)
                max_full_line_width = max(
                    max_full_line_width,
                    len(_ANSI_ESCAPE_RE.sub("", rendered)),
                )

        life_line = ""
        if self.max_lives is not None:
            lives_left = min(
                max(self.lives_remaining or 0, 0), self.max_lives
            )
            life_line = "   ".join(
                ["●"] * lives_left
                + ["○"] * (self.max_lives - lives_left)
            )
            max_full_line_width = max(max_full_line_width, len(life_line))

        # Choose a cell width that lets the longest category line fit the grid.
        cell_width = max(
            max_cell_width,
            (max_full_line_width + self.cols - 1) // self.cols,
        )
        board_width = self.cols * cell_width + self.cols - 1
        lines: list[str] = []

        # Solved groups stay at the top, with their words directly below each label.
        for category in self.solved_cats:
            sample = category.tiles[0] if category.tiles else Tile("", category)
            lines.append(
                self.fill_template(
                    self.CATEGORY_BAR_VISUAL, sample, board_width
                )
            )
            lines.append(
                self.fill_template(self.WORDS_VISUAL, sample, board_width)
            )
            lines.append(" " * board_width)

        cursor_index = (
            min(max(self.pos_to_idx(self.cursor_pos), 0), len(self.tiles) - 1)
            if self.tiles
            else -1
        )

        # Each unsolved row gets a second line with an arrow under the active tile.
        for start in range(0, len(self.tiles), self.cols):
            row_tiles = self.tiles[start:start + self.cols]
            tile_line: list[str] = []
            cursor_line: list[str] = []
            for col in range(self.cols):
                index = start + col
                if col < len(row_tiles):
                    tile = row_tiles[col]
                    tile_line.append(
                        self.fill_template(
                            self.TILE_BOX_VISUAL, tile, cell_width
                        )
                    )
                    cursor_line.append(
                        self.fill_template(
                            self.CURSOR_LINE_VISUAL,
                            tile,
                            cell_width,
                            cursor=index == cursor_index,
                        )
                    )
                else:
                    tile_line.append(" " * cell_width)
                    cursor_line.append(" " * cell_width)
            lines.append(" ".join(tile_line))
            lines.append(" ".join(cursor_line))

        if self.max_lives is not None:
            # Show the life counter below the board, centered to its full width.
            lines.append(life_line.center(board_width))

        return "\n".join(lines)

    def fill_template(
        self,
        template: str,
        tile: Tile,
        target_length: int | None = None,
        *,
        cursor: bool = False,
    ) -> str:
        """Render a tile template and distribute padding to reach a visible width."""
        parts = _split_template(template)
        padding_indices = [
            index for index, part in enumerate(parts) if part.startswith("$p")
        ]

        def render(padding: dict[int, int]) -> str:
            """Resolve the template parts using the requested padding."""
            rendered_parts: list[str] = []
            for index, part in enumerate(parts):
                if part.startswith("$p"):
                    rendered_parts.append(
                        trig_to_str(
                            part,
                            tile,
                            padding.get(index, 0),
                            cursor=cursor,
                            selected=tile.is_selected,
                        )
                    )
                elif part.startswith("$"):
                    rendered_parts.append(
                        trig_to_str(
                            part,
                            tile,
                            cursor=cursor,
                            selected=tile.is_selected,
                        )
                    )
                else:
                    rendered_parts.append(part)
            return "".join(rendered_parts)

        unpadded = render({})
        if target_length is None or not padding_indices:
            return unpadded
        if target_length < 0:
            raise ValueError("target_length must be non-negative.")

        visible_length = len(_ANSI_ESCAPE_RE.sub("", unpadded))
        extra_padding = max(0, target_length - visible_length)
        padding_each, remainder = divmod(extra_padding, len(padding_indices))
        padding = {
            index: padding_each + (position < remainder)
            for position, index in enumerate(padding_indices)
        }
        return render(padding)

    def set_categories(self, cats: list[Category]) -> None:
        """Set active categories and reset their tile selection state."""
        categories = list(cats)
        tiles = [tile for category in categories for tile in category.tiles]
        self.set_tiles(tiles)
        self.cats = categories

    def set_tiles(self, tiles: list[Tile]) -> None:
        """Set the active tiles after checking they fit the configured board."""
        if len(tiles) > self.cols * self.max_rows:
            raise ValueError(
                f"{len(tiles)} tiles do not fit on a {self.max_rows}-row, "
                f"{self.cols}-column board."
            )
        active_tiles = list(tiles)
        self.tiles = active_tiles
        self.cats = list(dict.fromkeys(tile.category for tile in active_tiles))
        for tile in active_tiles:
            tile.set_selected(False)
        self._update_row_count()
        self.cursor_pos = (0, 0)
        self.selected_tiles.clear()

    def _update_row_count(self) -> None:
        """Recalculate used rows while keeping within the configured row limit."""
        rows_needed = max(1, (len(self.tiles) + self.cols - 1) // self.cols)
        self.rows = min(rows_needed, self.max_rows)

    def generate_board(self) -> None:
        """Choose one category from each difficulty and create its tiles."""
        # Each game gets fresh tile objects rather than shared global selection state.
        categories: list[Category] = []
        for choices in CATEGORIES_BY_DIFFICULTY.values():
            chosen = random.choice(choices)
            categories.append(Category(chosen.name, chosen.words, chosen.color))
        self.set_categories(categories)

    def debug_tiles(self) -> None:
        """Print the current unsolved words for debugging."""
        print_items([tile.word for tile in self.tiles], sep=", ", conj="and")

    def play(self) -> bool:
        """Run until all categories are solved or the player runs out of lives."""
        self.shuffle()
        while self.tiles:
            rpt_print()
            print(self.rendered_board)

            if self.lives_remaining is not None:
                if self.lives_remaining <= 0:
                    print("No lives remaining. Game over.")
                    return False

            print(
                f"Selected: {len(self.selected_tiles)} / {WORDS_PER_CATEGORY}"
            )
            if not self.handle_input():
                print(self.rendered_board)
                print("No lives remaining. Game over.")
                return False

        # Render once more so the final solved category is visible before exit.
        rpt_print()
        print(self.rendered_board)
        print("You solved all the categories!")
        return True

    def handle_input(
        self,
        moves: dict[str, tuple[int, int]] | None = None,
        select_key: str = "q",
        submit_key: str = "e",
        shuffle_key: str = "r",
    ) -> bool:
        """Read and process one command, retrying only unrecognized input."""
        if self.lives_remaining is not None and self.lives_remaining <= 0:
            return False

        moves = self.MOVES if moves is None else moves
        print(
                f"{Fore.GREEN + Style.BRIGHT}w/a/s/d{Style.RESET_ALL} to move\n"
                f"{Fore.GREEN + Style.BRIGHT}{select_key}{Style.RESET_ALL} to select\n"
                f"{Fore.GREEN + Style.BRIGHT}{submit_key}{Style.RESET_ALL} to submit\n"
                f"{Fore.GREEN + Style.BRIGHT}{shuffle_key}{Style.RESET_ALL} to shuffle\n"
                f"Action: ",
                end=f"{Fore.BLUE + Style.BRIGHT}",
            )
        while True:
            command = input().strip().lower()
            # The action prompt leaves the terminal bright blue; reset it before rendering.
            print(Style.RESET_ALL, end="")
            if command in moves:
                self.move_cursor(command, moves)

            elif command == select_key:
                self.toggle_selection()

            elif command == submit_key and len(self.selected_tiles) == WORDS_PER_CATEGORY:
                solved, one_away = self.submit()
                if solved:
                    print(
                        f"{Style.BRIGHT}{Fore.GREEN}Correct group!{Style.RESET_ALL}"
                    )
                elif one_away:
                    print(
                        f"{Style.BRIGHT}{Fore.YELLOW}One away!{Style.RESET_ALL}"
                    )
                else:
                    print(
                        f"{Style.BRIGHT}{Fore.RED}Not a group.{Style.RESET_ALL}"
                    )

                if self.lives_remaining is not None and not solved:
                    self.lives_remaining -= 1
                    if self.lives_remaining <= 0:
                        return False
            elif command == shuffle_key:
                self.shuffle()
            else:
                print(f"{Style.BRIGHT}{Fore.RED}<Invalid action>{Style.RESET_ALL}")
                continue

            return True

    def move_cursor(
        self,
        move_key: str,
        moves: dict[str, tuple[int, int]] | None = None,
    ) -> None:
        """Move the cursor by one cell if the destination is on the board."""
        moves = self.MOVES if moves is None else moves
        if not self.tiles:
            self.cursor_pos = (0, 0)
            return

        idx = min(self.pos_to_idx(self.cursor_pos), len(self.tiles) - 1)
        row, col = self.idx_to_pos(idx)
        self.cursor_pos = (row, col)
        row_change, col_change = moves[move_key]
        if row_change:
            # Wrap vertically and clamp to the last real tile in a partial row.
            next_row = (row + row_change) % self.rows
            row_start = next_row * self.cols
            row_length = min(self.cols, len(self.tiles) - row_start)
            next_col = min(col, row_length - 1)
        elif col_change:
            # Horizontal movement wraps within the current row's existing tiles.
            row_start = row * self.cols
            row_length = min(self.cols, len(self.tiles) - row_start)
            next_row = row
            next_col = (col + col_change) % row_length
        else:
            return

        self.cursor_pos = (next_row, next_col)

    def toggle_selection(self, max_select: int = WORDS_PER_CATEGORY) -> None:
        """Toggle the cursor tile in the selection, up to the selection limit."""
        if max_select < 1:
            raise ValueError("max_select must be positive.")
        if not self.tiles:
            return
        tile = self.cursor_tile
        if tile.is_selected:
            tile.set_selected(False)
            self.selected_tiles.remove(tile)
        elif len(self.selected_tiles) < max_select:
            tile.set_selected(True)
            self.selected_tiles.append(tile)

    def submit(self) -> tuple[bool, bool | None]:
        """Submit a full selection; return whether it solved or was one away."""
        if len(self.selected_tiles) != WORDS_PER_CATEGORY:
            return False, False

        selected_cat = self.selected_tiles[0].category
        if all(tile.category is selected_cat for tile in self.selected_tiles):
            self.complete_category(selected_cat)
            return True, None

        tile_counts: dict[Category, int] = {}
        for tile in self.selected_tiles:
            tile_counts[tile.category] = tile_counts.get(tile.category, 0) + 1
        return False, max(tile_counts.values()) == WORDS_PER_CATEGORY - 1

    def complete_category(self, cat: Category) -> None:
        """Remove a solved category and update the cursor position."""
        if cat not in self.cats or cat in self.solved_cats:
            raise ValueError("Cannot complete an inactive or already-solved category.")
        if any(tile not in self.tiles for tile in cat.tiles):
            raise ValueError("Cannot complete a category with missing board tiles.")

        cursor_idx = min(self.pos_to_idx(self.cursor_pos), len(self.tiles) - 1)
        cursor_tile = self.tiles[cursor_idx] if self.tiles else None
        self.solved_cats.append(cat)
        solved_tiles = set(cat.tiles)
        self.tiles = [tile for tile in self.tiles if tile not in solved_tiles]

        for tile in cat.tiles:
            tile.set_selected(False)
        self.selected_tiles.clear()

        self._update_row_count()
        if cursor_tile is None or cursor_tile in solved_tiles:
            cursor_idx = min(cursor_idx, len(self.tiles) - 1)
        else:
            cursor_idx = self.tiles.index(cursor_tile)
        self.cursor_pos = self.idx_to_pos(cursor_idx) if self.tiles else (0, 0)

    def shuffle(self) -> None:
        """Shuffle tiles while keeping the cursor at the same grid position."""
        if not self.tiles:
            return
        random.shuffle(self.tiles)

    def get_tile_at(self, pos: tuple[int, int]) -> Tile:
        """Return the tile at a row-and-column position."""
        row, col = pos
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(f"Board position {pos} is outside the active grid.")
        index = self.pos_to_idx(pos)
        if index >= len(self.tiles):
            raise IndexError(f"Board position {pos} does not contain a tile.")
        return self.tiles[index]

    def pos_to_idx(self, pos: tuple[int, int]) -> int:
        """Convert a row-and-column position to a flat tile index."""
        return self.cols * pos[0] + pos[1]

    def idx_to_pos(self, idx: int) -> tuple[int, int]:
        """Convert a flat tile index to a row-and-column position."""
        return divmod(idx, self.cols)

if __name__ == "__main__":
    GameBoard(lives=4).play()
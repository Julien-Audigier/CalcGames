import random
from colorama import Fore, Style


def prt_list(items: list[str], middle: str = ", ", end: str = "") -> None:
    """Print the items with a separator and optional final conjunction."""
    if len(items) == 0:
        print()
    elif len(items) == 1:
        print(items[0])
    elif len(items) == 2:
        separator = f" {end} " if end else middle
        print(f"{items[0]}{separator}{items[1]}")
    else:
        last_separator = f"{end} " if end else ""
        print(f"{middle.join(items[:-1])}{middle}{last_separator}{items[-1]}")


class group:
    """A category and the four words that belong to it."""

    def __init__(self, category: str, words: list[str], rank: str) -> None:
        """Create a group and its word tiles."""
        self.category = category
        self.words = words
        self.tiles: list[tile] = [tile(word, self) for word in words]
        self.rank = rank


class tile:
    """A selectable word tile tied to its source group."""

    def __init__(self, text: str, group: group) -> None:
        """Create a tile for a word in a group."""
        self.text = text
        self.group = group
        self.selected = False
        self.grouped = False

    def select(self, selected: bool | None = None) -> None:
        """Set selection state, or toggle it when no state is supplied."""
        if selected is None:
            self.selected = not self.selected
        else:
            self.selected = selected


CONNECTIONS_DATA: dict[str, list[group]] = {
    "yellow": [
        group("Shades of Red", ["CHERRY", "RUBY", "CRIMSON", "SCARLET"], Fore.YELLOW),
        group("Parts of a Book", ["JACKET", "SPINE", "PAGE", "CHAPTER"], Fore.YELLOW),
        group("Fast Food Chains", ["SUBWAY", "WENDYS", "SONIC", "MCDONALDS"], Fore.YELLOW),
        group("Kinds of Shoes", ["LOAFER", "SNEAKER", "BOOT", "PUMP"], Fore.YELLOW),
        group("Basic Geometry Shapes", ["SQUARE", "CIRCLE", "TRIANGLE", "DIAMOND"], Fore.YELLOW),
        group("Things in a Wallet", ["CASH", "CARD", "RECEIPT", "PHOTO"], Fore.YELLOW),
        group("Kitchen Appliances", ["TOASTER", "BLENDER", "OVEN", "FRIDGE"], Fore.YELLOW),
        group("Types of Weather", ["RAIN", "SNOW", "HAIL", "SLEET"], Fore.YELLOW),
        group("Trees", ["OAK", "PINE", "MAPLE", "BIRCH"], Fore.YELLOW),
        group("Time Units", ["SECOND", "MINUTE", "HOUR", "CENTURY"], Fore.YELLOW),
        group("Ways to Walk", ["STRIDE", "PACE", "STROLL", "MARCH"], Fore.YELLOW),
        group("Parts of a Tree", ["ROOT", "TRUNK", "BRANCH", "LEAF"], Fore.YELLOW),
        group("Things that are Yellow", ["BANANA", "LEMON", "CORN", "CANARY"], Fore.YELLOW),
        group("Baking Ingredients", ["FLOUR", "SUGAR", "YEAST", "BUTTER"], Fore.YELLOW),
        group("Card Suits", ["HEART", "DIAMOND", "CLUB", "SPADE"], Fore.YELLOW),
        group("Types of Meat", ["BEEF", "PORK", "CHICKEN", "TURKEY"], Fore.YELLOW),
        group("Office Supplies", ["PEN", "STAPLER", "FOLDER", "CLIP"], Fore.YELLOW),
        group("Forms of Water", ["STEAM", "ICE", "VAPOR", "LIQUID"], Fore.YELLOW),
        group("Kinds of Furniture", ["COUCH", "TABLE", "CHAIR", "DESK"], Fore.YELLOW),
        group("Units of Currency", ["DOLLAR", "EURO", "POUND", "YEN"], Fore.YELLOW)
    ],
    "green": [
        group("Things that are Sharp", ["KNIFE", "WIT", "CHEDDAR", "TACK"], Fore.GREEN),
        group("Palindromes", ["KAYAK", "RACECAR", "RADAR", "MOM"], Fore.GREEN),
        group("Synonyms for 'Excellent'", ["STELLAR", "SUPERB", "PRIME", "CHOICE"], Fore.GREEN),
        group("Types of Insurance", ["LIFE", "HEALTH", "AUTO", "HOME"], Fore.GREEN),
        group("Waterway Features", ["CANAL", "STREAM", "RIVER", "CHANNEL"], Fore.GREEN),
        group("Slang for Money", ["BREAD", "DOUGH", "CLAMS", "BUCKS"], Fore.GREEN),
        group("Things that Fly", ["PILOT", "KITE", "SPARROW", "FRISBEE"], Fore.GREEN),
        group("Internet Browsers", ["CHROME", "SAFARI", "EDGE", "OPERA"], Fore.GREEN),
        group("Gems and Minerals", ["QUARTZ", "JADE", "DIAMOND", "EMERALD"], Fore.GREEN),
        group("Ways to Fasten Clothes", ["BUTTON", "ZIPPER", "SNAP", "BUCKLE"], Fore.GREEN),
        group("Types of Cheese", ["BRIE", "GOUDA", "SWISS", "CHEDDAR"], Fore.GREEN),
        group("Gym Equipment", ["WEIGHT", "BENCH", "MAT", "TREADMILL"], Fore.GREEN),
        group("Things with Screens", ["PHONE", "TABLET", "MONITOR", "LAPTOP"], Fore.GREEN),
        group("Musical Instruments", ["FLUTE", "CELLO", "ORGAN", "HARP"], Fore.GREEN),
        group("Words Meaning 'Stop'", ["CEASE", "HALT", "QUIT", "DESIST"], Fore.GREEN),
        group("Types of Footwear", ["SLIPPER", "SNEAKER", "CLOG", "SANDAL"], Fore.GREEN),
        group("Found in a Laboratory", ["BEAKER", "FLASK", "SCOPE", "VIAL"], Fore.GREEN),
        group("Types of Fabric", ["SILK", "COTTON", "WOOL", "SATIN"], Fore.GREEN),
        group("Parts of a Car", ["HOOD", "TRUNK", "WHEEL", "BRAKE"], Fore.GREEN),
        group("Synonyms for 'Happy'", ["GLAD", "JOYFUL", "MERRY", "ELATED"], Fore.GREEN)
    ],
    "blue": [
        group("Words that can follow 'Apple'", ["CORE", "SAUCE", "JACKS", "PIE"], Fore.BLUE),
        group("Homophones for Animals", ["BARE", "DEER", "HARE", "NIGHTINGALE"], Fore.BLUE),
        group("Things with Wings", ["AIRPLANE", "ANGEL", "BUTTERFLY", "STAGE"], Fore.BLUE),
        group("Words meaning 'Fake'", ["SHAM", "PHONY", "BOGUS", "ARTIFICIAL"], Fore.BLUE),
        group("Rhymes with 'Blue'", ["GREW", "THROUGH", "SHOE", "QUEUE"], Fore.BLUE),
        group("Things you 'Strike'", ["MATCH", "POSE", "DEAL", "BALANCE"], Fore.BLUE),
        group("Found in a Casino", ["CHIPS", "DEALER", "SLOTS", "WHEEL"], Fore.BLUE),
        group("Celestial Bodies", ["SATURN", "COMET", "MARS", "ASTEROID"], Fore.BLUE),
        group("Anatomical Homophones", ["EYE", "HAIR", "HEEL", "SOLE"], Fore.BLUE),
        group("Units of Measurement", ["FOOT", "GRAIN", "STONE", "YARD"], Fore.BLUE),
        group("Words before 'Card'", ["CREDIT", "GIFT", "WILD", "FLASH"], Fore.BLUE),
        group("Things with Teeth", ["COMB", "GEAR", "SAW", "SHARK"], Fore.BLUE),
        group("Can follow 'Rain'", ["BOW", "COAT", "DROP", "FALL"], Fore.BLUE),
        group("Famous Painters", ["MONET", "MANET", "RENOIR", "DEGAS"], Fore.BLUE),
        group("Slang for 'Excellent'", ["WILD", "SWEET", "COOL", "RAD"], Fore.BLUE),
        group("Things that Spin", ["TOP", "WHEEL", "EARTH", "RECORD"], Fore.BLUE),
        group("Things you 'Catch'", ["COLD", "DRIFT", "BREATH", "WAVE"], Fore.BLUE),
        group("Palindromic Names", ["ANNA", "BOB", "OTTO", "NATHAN"], Fore.BLUE),
        group("Homophones for Clothes", ["COAT", "SUIT", "PANTS", "JEANS"], Fore.BLUE),
        group("Things that are Green", ["ENVY", "LIME", "MINT", "JADE"], Fore.BLUE)
    ],
    "purple": [
        group("Words that start with US States", ["MAINSPRING", "MASSIVE", "INDIAN", "OREGONIAN"], Fore.MAGENTA),
        group("Anagrams of 'LEAST'", ["STALE", "TALES", "SLATE", "TEALS"], Fore.MAGENTA),
        group("Double Letters in the Middle", ["SPOON", "COFFEE", "BUBBLE", "EGGPLANT"], Fore.MAGENTA),
        group("Ending in Greek Letters", ["ALPHABET", "MICROBETA", "CHEVRONDELTA", "PI"], Fore.MAGENTA),
        group("Synonyms for 'Complain' that are also animals", ["CRAB", "GROUSE", "BEEF", "CARP"], Fore.MAGENTA),
        group("Words containing hidden numbers", ["ATTENTION", "OZONE", "WEIGHT", "FORTRESS"], Fore.MAGENTA),
        group("Homophones for units of time", ["OUR", "MINUET", "SECONDO", "DAZE"], Fore.MAGENTA),
        group("Slang for 'Head'", ["NOGGIN", "MELON", "DOME", "BEAN"], Fore.MAGENTA),
        group("Words before 'Jack'", ["BLACK", "LUMBER", "FLAP", "APPLE"], Fore.MAGENTA),
        group("Palindromic words when reversed", ["STAR", "LIVE", "DIAPER", "KNITS"], Fore.MAGENTA),
        group("Words that contain elements", ["IRONIC", "LEADERSHIP", "GOLDEN", "CARBON"], Fore.MAGENTA),
        group("Anagrams of 'SPARE'", ["PEARS", "REAPS", "SPEAR", "PARSE"], Fore.MAGENTA),
        group("Ending in body parts", ["BEFOREHAND", "FOOTNOTE", "HEADSTRONG", "ARMCHAIR"], Fore.MAGENTA),
        group("Words that sound like letters", ["QUEUE", "BEE", "SEA", "WHY"], Fore.MAGENTA),
        group("Homophones for numbers", ["WON", "TOO", "FOR", "ATE"], Fore.MAGENTA),
        group("Words containing calendar months", ["MAYHEM", "DECEASED", "MARCHING", "AUGMENT"], Fore.MAGENTA),
        group("Slang for 'Money' that are also food", ["BREAD", "DOUGH", "CHIPS", "CHEDDAR"], Fore.MAGENTA),
        group("Words before 'Fish'", ["JELLY", "STAR", "GOLDFISH", "CAT"], Fore.MAGENTA),
        group("Words with three double letters", ["BOOKKEEPER", "COMMITTEE", "WOOLLIEST", "TATOOEE"], Fore.MAGENTA),
        group("Words that read backward as other words", ["PART", "REWARD", "SNAP", "STRAW"], Fore.MAGENTA)
    ]
}

MAX_SELECT: int = 4


class board:
    """Manage a Connections board, cursor, selections, and solved groups."""

    DEFAULT_MOVES: dict[str, tuple[int, int]] = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
    }

    def __init__(
        self,
        board: list[tile] | None = None,
        groups: list[group] | None = None,
        length: int = 4,
        height: int = 4,
    ) -> None:
        """Create a board from groups, existing tiles, or random data."""
        if length <= 0 or height <= 0:
            raise ValueError("Board length and height must be positive.")

        self.length = length
        self.height = height
        self.board: list[tile] = []
        self.groups: list[group] = []
        self.cursorPOS: tuple[int, int] = (0, 0)
        self.selected: list[tile] = []
        self.winGroups: list[list[tile]] = []

        if groups is not None:
            self.create(groups)
        elif board is not None:
            self.board = list(board)
            self.groups = list(dict.fromkeys(item.group for item in self.board))
            self.height = max(1, (len(self.board) + self.length - 1) // self.length)
        else:
            self.generate()

    @property
    def words(self) -> list[str]:
        """Return every word in the board's source groups."""
        return [word for category in self.groups for word in category.words]

    @property
    def cursor(self) -> tile:
        """Return the tile currently under the cursor."""
        return self.tile(self.cursorPOS)

    def create(self, groups: list[group]) -> None:
        """Build the playable tile list from the supplied groups."""
        self.groups = list(groups)
        self.board = [item for category in self.groups for item in category.tiles]
        self.height = max(1, (len(self.board) + self.length - 1) // self.length)
        self.cursorPOS = (0, 0)
        self.selected.clear()

    def generate(self) -> None:
        """Choose one category from each difficulty and create its tiles."""
        self.create([random.choice(rank) for rank in CONNECTIONS_DATA.values()])

    def debug(self) -> None:
        """Print the current unsolved tile words."""
        prt_list([item.text for item in self.board], middle=", ", end="and")

    def input(
        self,
        move: dict[str, tuple[int, int]] | None = None,
        select: str = "q",
        submit: str = "e",
        shuffle: str = "r",
    ) -> None:
        """Read and process one command, retrying only unrecognized input."""
        moves = self.DEFAULT_MOVES if move is None else move
        while True:
            print(
                f"{Fore.GREEN + Style.BRIGHT}w/a/s/d{Style.RESET_ALL} to move\n"
                f"{Fore.GREEN + Style.BRIGHT}{select}{Style.RESET_ALL} to select\n"
                f"{Fore.GREEN + Style.BRIGHT}{submit}{Style.RESET_ALL} to submit\n"
                f"{Fore.GREEN + Style.BRIGHT}{shuffle}{Style.RESET_ALL} to shuffle\n"
                f"Action: ",
                end=f"{Fore.BLUE + Style.BRIGHT}",
            )
            key = input().strip().lower()
            if key in moves:
                self.move(key, moves)
            elif key == select:
                self.select()
            elif key == submit:
                won, one_away = self.submit()
                if won:
                    print("Group found!")
                elif one_away:
                    print("One Away!")
                else:
                    print("Not a group.")
            elif key == shuffle:
                self.shuffle()
            else:
                print("Unknown action.")
                continue
            return

    def move(
        self,
        key: str,
        move: dict[str, tuple[int, int]] | None = None,
    ) -> None:
        """Move the cursor by one cell if the destination is on the board."""
        moves = self.DEFAULT_MOVES if move is None else move
        if not self.board:
            self.cursorPOS = (0, 0)
            return

        current_index = min(self.pos_to_index(self.cursorPOS), len(self.board) - 1)
        row, column = self.index_to_pos(current_index)
        self.cursorPOS = (row, column)
        row_change, column_change = moves[key]
        next_row = row + row_change
        next_column = column + column_change
        next_index = self.pos_to_index((next_row, next_column))
        if (
            0 <= next_row < self.height
            and 0 <= next_column < self.length
            and next_index < len(self.board)
        ):
            self.cursorPOS = (next_row, next_column)

    def select(self, max_select: int = MAX_SELECT) -> None:
        """Toggle the cursor tile in the selection, up to the selection limit."""
        current = self.cursor
        if current.selected:
            current.select(False)
            self.selected.remove(current)
        elif len(self.selected) < max_select:
            current.select(True)
            self.selected.append(current)

    def submit(self) -> tuple[bool, bool | None]:
        """Submit four selected tiles; return (solved, one_away)."""
        if len(self.selected) != MAX_SELECT:
            return False, False

        selected_group = self.selected[0].group
        if all(item.group is selected_group for item in self.selected):
            self.add_win_group(self.selected)
            return True, None

        group_counts: dict[group, int] = {}
        for item in self.selected:
            group_counts[item.group] = group_counts.get(item.group, 0) + 1
        return False, max(group_counts.values()) == MAX_SELECT - 1

    def add_win_group(self, winning_tiles: list[tile]) -> None:
        """Remove a solved group and keep the cursor at its tile or replacement."""
        if not winning_tiles:
            return

        old_cursor_index = min(self.pos_to_index(self.cursorPOS), len(self.board) - 1)
        cursor_tile = self.board[old_cursor_index] if self.board else None
        winning_set = set(winning_tiles)
        self.winGroups.append(winning_tiles.copy())
        self.board = [item for item in self.board if item not in winning_set]

        for item in winning_tiles:
            item.select(False)
        winning_tiles.clear()
        self.selected.clear()

        self.height = max(1, (len(self.board) + self.length - 1) // self.length)
        if cursor_tile is None or cursor_tile in winning_set:
            new_cursor_index = min(old_cursor_index, len(self.board) - 1)
        else:
            new_cursor_index = self.board.index(cursor_tile)
        self.cursorPOS = self.index_to_pos(new_cursor_index) if self.board else (0, 0)

    def shuffle(self) -> None:
        """Shuffle unsolved tiles without moving the cursor to a new tile."""
        if not self.board:
            return
        cursor_tile = self.cursor
        random.shuffle(self.board)
        self.cursorPOS = self.index_to_pos(self.board.index(cursor_tile))

    def tile(self, pos: tuple[int, int]) -> tile:
        """Return the tile at a row-and-column position."""
        return self.board[self.pos_to_index(pos)]

    def pos_to_index(self, pos: tuple[int, int]) -> int:
        """Convert a row-and-column position to a flat tile index."""
        return self.length * pos[0] + pos[1]

    def index_to_pos(self, index: int) -> tuple[int, int]:
        """Convert a flat tile index to a row-and-column position."""
        return divmod(index, self.length)


def main() -> None:
    """Run the text-based game loop."""
    game = board()
    while game.board:
        game.debug()
        game.input()
    print("You found all the groups!")


if __name__ == "__main__":
    main()

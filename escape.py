
WALL = "#"
NON_EXISTING = "~"
MAX_MOVE = 2

class Obj:
    """Base class for anything that can appear on the game board."""

    def __init__(self, pos, symbol, collidable = False, static = False):
            """Store the object's position, display symbol, and movement rules."""
            self.collidable = collidable
            self.pos = pos
            self.symbol = symbol
            self.static = static

    def move(self, offset, board:list[list] = None, objects = None, amount_moved = None):
        """Move this object and push a collidable object in front of it."""
        if board == None: self.pos = (self.x+offset[0], self.y+offset[1])
        else:
            match self.moveable(board,offset,objects,amount_moved):
                case True:
                    self.pos = self.wrap(board,offset)
                case False:
                    return
                case Obj() as obj:
                    if obj.collidable: obj.move(offset,board,objects)
                    self.pos = self.wrap(board,offset)

    def wrap(self, board, offset):
        """Return the next valid position, including movement around map edges."""
        def exists(x, y):
            return (
                0 <= y < len(board)
                and 0 <= x < len(board[y])
                and board[y][x] != NON_EXISTING
            )

        candidate = (self.x + offset[0], self.y + offset[1])
        reverse = (-offset[0], -offset[1])

        if exists(*candidate):
            return candidate

        result = self.pos
        while True:
            if reverse[0] != 0:
                next_position = (result[0] + reverse[0], result[1])
            else:
                next_position = (result[0], result[1] + reverse[1])

            if not exists(*next_position):
                break
            result = next_position

        while board[result[1]][result[0]] == WALL:
            if reverse[0] != 0:
                next_position = (result[0] + reverse[0], result[1])
            else:
                next_position = (result[0], result[1] + reverse[1])

            if not exists(*next_position):
                return self.pos
            result = next_position

        return result

    def pressed(self, board, objects=None):
        """Return whether another object is currently covering this object."""
        return load_board(board, objects)[self.y][self.x] != self.symbol

    def moveable(self, board, offset, objects = None,amount_moved = None):
        """Check whether this object and any pushed objects can move."""
        if self.collidable is False: return True
        if self.static is True: return False
        if amount_moved is not None:
            if amount_moved <= 0: return False
            amount_moved -= 1
        
        newPos= self.wrap(board,offset)
        if board[newPos[1]][newPos[0]] == "#":
            return False
        
        if objects is None:
            objects = globals().get("objects", ())
        for obj in objects:
            if obj is self or not obj.collidable or obj.pos != newPos:
                continue
            if obj.moveable(board, offset, objects, amount_moved):
                return obj
            return False
        return True

    @property
    def x(self):
        """Return the object's horizontal coordinate."""
        return self.pos[0]

    @property
    def y(self):
        """Return the object's vertical coordinate."""
        return self.pos[1] 
    
class Player(Obj):
    """The object controlled by keyboard input."""

    def __init__(self, pos = (1,1)):
        """Initializes the player with a position and a symbol."""
        super().__init__(pos, "&")
        self.collidable = True

    def movement(self, board, objects=None, xKey = ("a","d"), yKey = ("w","s"), maxMove = MAX_MOVE):
        """Moves the player based on the input keys: _Key = (-1,1)."""

        inputKey = ""
        keys = {
            xKey[0]: (-1, 0),
            xKey[1]: (1, 0),
            yKey[0]: (0, -1),
            yKey[1]: (0, 1)
        }

        while inputKey not in keys:
            inputKey = input("Enter key to move: ")
        offset = keys[inputKey]
        self.move(offset, board, objects, amount_moved=maxMove+1)

class Pressureplate(Obj):
    """Preset for a non-collidable object intended to act as a trigger."""

    def __init__(self, pos = (1,1),id=0, symbol = "*",): #⍟
        super().__init__(pos, symbol)
        self.collidable = False
        self.id = id

class Box(Obj):
    """Preset for a movable object that can be pushed by the player."""

    def __init__(self,pos=(1,1),symbol="☒"):
        super().__init__(pos, symbol)
        self.collidable = True   

class Door(Obj):
    """A static obstacle controlled by one or more pressure plates."""

    def __init__(self, pos,triggers:list[Obj],id=None,gate = 0, instance = 0, symbols = ["│"," ","—"]):
        """Initialize a door; gate 0 means OR and gate 1 means AND."""
        super().__init__(pos, symbols[instance], [True,False][instance],static=True)
        self.triggers = triggers
        self.id = id
        self.symbols = symbols
        self.instance = instance
        self.gate = gate
        self.intsStart = instance

    def update(self, board, objects=None):
        """Update the door state from its pressure plates."""
        # OR opens after the first pressed plate; AND requires every plate.
        for obj in self.triggers:
            if obj.pressed(board, objects):
                self.instance = (self.intsStart + 1) % 2
                if self.gate == 0: break
            else:
                self.instance = self.intsStart
                if self.gate == 1: break
        self.symbol = self.symbols[self.instance]
        self.collidable = [True,False][self.instance]
        
def load_board(board, objects=None):
    """Return a copy of the board with objects drawn in display priority order."""
    if objects is None:
        objects = globals().get("objects", ())
    board = [row.copy() for row in board]
    # Draw higher-priority objects last so they remain visible when positions overlap.
    def priority(obj):
        if isinstance(obj, Player):
            return 0
        if isinstance(obj, Box):
            return 1
        if isinstance(obj, Pressureplate):
            return 3
        return 2
    sorted_objects = sorted(objects, key=priority)

    for obj in reversed(sorted_objects):
        board[obj.y][obj.x] = obj.symbol
    return board

def prt_board(board:list[list], objects=None):
    """Print the current board to the terminal."""
    for row in load_board(board, objects):
        print(" ".join(row))

def play_level(level:list[list], player:Player = None):
    """If plater is None then first object in objects is assumed to be the player."""
    board,objects = level
    for door in objects:
        if isinstance(door, Door):
            door.triggers = [
                plate for plate in objects
                if isinstance(plate, Pressureplate) and plate.id == door.id
            ]
    numMoves = 0
    running = True
    while running:
        prt_board(board, objects)
        objects[0].movement(board, objects)
        numMoves += 1
        for obj in objects:
            if isinstance(obj, Door):
                obj.update(board, objects)
        for obj in objects:
            if isinstance(obj, Pressureplate):
                if obj.pressed(board, objects) and obj.symbol == "E":
                    running = False
                    print("You win with " + str(numMoves) + " moves!")

def askList(prompt:str,options:list[str]):
    while True:
        print(prompt)
        for i,option in enumerate(options):
            print(str(i+1)+". "+option)
        answer = int(input())
        if answer > 0 and answer-1 < len(options):
            return answer
    
#Vars
level1 = [
    [
        ["#","#","#","#","#","#","#"],
        ["#"," "," "," ","#"," ","#"],
        ["#"," "," "," ","#"," ","#"],
        ["#"," "," ","#","#"," ","#"],
        [" "," "," ","#","#"," "," "],
        [" "," "," ","#"," "," "," "],
        ["#"," ","#","#","#"," ","#"],
        ["#"," "," "," "," "," ","#"],
        ["#"," "," "," "," "," ","#"],
        ["#","#","#","#","#","#","#"]
    ],
    [
    Player(),
    Pressureplate((1, 2),1),
    Pressureplate((4, 5),1),
    Pressureplate((5, 1),"E", "E"),
    Box((2, 2)),
    Box((2, 3)),
    Door((5, 3), [], 1, gate=1, symbols=["—", " "])
    ]
]

play_level(level1)
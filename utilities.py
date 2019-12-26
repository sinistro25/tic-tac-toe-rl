
from enum import Enum,auto
EPSILON = 0.0001
DSURF = None

def epsilon_equal(x,y):
    return abs(x-y) < EPSILON
def epsilon_greater(x,y):
    return x > y +EPSILON
def list_to_tuple2d(l):
    return tuple(tuple(x for x in row) for row in l)
def tuple_to_list2d(t):
    return [[x for x in row] for row in t]
# Represents player's side
class Player(Enum):
    X = auto()
    O = auto()
    def __repr__(self):
        if self is Player.X:
            return "<X>"
        return "<O>"
    def __str__(self):
        if self is Player.X:
            return "X"
        return "O"
    def __invert__(self):
        if self is Player.X:
            return Player.O
        return Player.X
        

# Define rewards values
class Reward(Enum):
    VICTORY = 1
    LOSS = -1
    DRAW = 0
    BASE = 0

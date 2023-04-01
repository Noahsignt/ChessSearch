from enum import Enum

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

#max/min notation for AI context
class Team(Enum):
    MAX = 0
    MIN = 1

class Piece: 
    def __init__(self, piecetype, team, x, y) -> None:
        self.piecetype = piecetype
        self.team = team
        self.x = x
        self.y = y
    
    #return true if successful move, false otherwise
    def pawn_move(self, new_x, new_y):
        #check if pawn is on first move
        if (self.team == Team.MIN and self.y == 6) or (self.team == Team.MAX and self.y == 1):
            first_move = True
        else:
            first_move = False

        #check no deviation in x
        if (abs(self.x - new_x) > 0):
            return False
        #check correct y movement
        if (abs(self.y - new_y) > 1 and not(first_move)):
            return False
        if (abs(self.y - new_y) > 2):
            return False
        
        self.y = new_y
        return True
    
    #checks piece type and calls correct position modifying function. 
    #returns true if move successfully made, false otherwise
    def move(self, new_x, new_y):
        match self.piecetype:
            case PieceType.PAWN:
                self.pawn_move(new_x, new_y)


class Chessboard:
    pieces = [ [0]*8 for i in range(8)]

    def print(self):
        return str(self.pieces)


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
    
    #all x_move functions check if a move is valid.
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

        return True
    
    def knight_move(self, new_x, new_y):
        change_x = abs(self.x - new_x)
        change_y = abs(self.y - new_y)
        is_valid = (change_x == 1 and change_y == 2) or (change_x == 2 and change_y == 1)

        if(is_valid):
            self.x = new_x
            self.y = new_y
        return is_valid
    
    def bishop_move(self, new_x, new_y):
        change_x = abs(self.x - new_x)
        change_y = abs(self.y - new_y)
        is_valid = change_x == change_y
        return is_valid
    
    def rook_move(self, new_x, new_y):
        change_x = abs(self.x - new_x)
        change_y = abs(self.y - new_y)
        is_valid = change_x == 0 or change_y == 0
        return is_valid
    
    def queen_move(self, new_x, new_y):
        is_valid = self.bishop_move(new_x, new_y) or self.rook_move(new_x, new_y)
        return is_valid
    
    def king_move(self, new_x, new_y):
        change_x = abs(self.x - new_x)
        change_y = abs(self.y - new_y)
        is_valid = change_x <= 1 and change_y <= 1
        return is_valid


    #checks piece type and calls correct position modifying function. 
    #returns true if move successfully made, false otherwise
    def move(self, new_x, new_y):
        match self.piecetype:
            case PieceType.PAWN:
                is_valid = self.pawn_move(new_x, new_y)
            case PieceType.KNIGHT:
                is_valid = self.knight_move(new_x, new_y)
            case PieceType.BISHOP:
                is_valid = self.bishop_move(new_x, new_y)
            case PieceType.ROOK:
                is_valid = self.rook_move(new_x, new_y)
            case PieceType.QUEEN:
                is_valid = self.queen_move(new_x, new_y)
            case PieceType.KING:
                is_valid = self.king_move(new_x, new_y)
        
        if(is_valid):
            self.x = new_x
            self.y = new_y
            return True
        else:
            return False
            


class Chessboard:
    pieces = [ [0]*8 for i in range(8)]

    def print(self):
        return str(self.pieces)


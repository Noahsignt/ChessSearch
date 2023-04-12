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

    def __str__(self):
        return self.piecetype.name + " " + self.team.name + " " + str(self.x) + " " + str(self.y)
    
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

#tile holds a piece and a flag indicating whether there is a piece on it or not        
class Tile:
    def __init__(self, piece):
        if(piece == None):
            self.empty = True
        else:
            self.empty = False
        
        self.piece = piece

    def __repr__(self):

        if(self.empty):
            return "Empty"
        
        return str(self.piece)

    def setPiece(self, piece):
        self.piece = piece
        self.empty = False

class Chessboard:
    tiles = [[Tile(None) for i in range(8)] for j in range(8)]

    #creates pieces and assigns correct tiles for the board
    def __init__(self) -> None:
        for x in range(8):
            for y in range(8):
                #pawn initializing
                if(y == 1):
                    self.tiles[y][x].setPiece(Piece(PieceType.PAWN, Team.MAX, x, y))
                if(y == 6):
                    self.tiles[y][x].setPiece(Piece(PieceType.PAWN, Team.MIN, x, y))

                #rook initializing
                if(y == 0 and (x == 0 or x == 7)):
                    self.tiles[y][x].setPiece(Piece(PieceType.ROOK, Team.MAX, x, y))
                if(y == 7 and (x == 0 or x == 7)):
                    self.tiles[y][x].setPiece(Piece(PieceType.ROOK, Team.MIN, x, y))

                #knight initializing
                if(y == 0 and (x == 1 or x == 6)):
                    self.tiles[y][x].setPiece(Piece(PieceType.KNIGHT, Team.MAX, x, y))
                if(y == 7 and (x == 1 or x == 6)):
                    self.tiles[y][x].setPiece(Piece(PieceType.KNIGHT, Team.MIN, x, y))

                #bishop initializing
                if(y == 0 and (x == 2 or x == 5)):
                    self.tiles[y][x].setPiece(Piece(PieceType.BISHOP, Team.MAX, x, y))
                if(y == 7 and (x == 2 or x == 5)):
                    self.tiles[y][x].setPiece(Piece(PieceType.BISHOP, Team.MIN, x, y))

                #queen initializing
                if(y == 0 and x == 3):
                    self.tiles[y][x].setPiece(Piece(PieceType.QUEEN, Team.MAX, x, y))
                if(y == 7 and x == 3):
                    self.tiles[y][x].setPiece(Piece(PieceType.QUEEN, Team.MIN, x, y))

                #king initializing
                if(y == 0 and x == 4):
                    self.tiles[y][x].setPiece(Piece(PieceType.KING, Team.MAX, x, y))
                if(y == 7 and x == 4):
                    self.tiles[y][x].setPiece(Piece(PieceType.KING, Team.MIN, x, y))
                
                

    def __str__(self):
        return str(self.tiles)


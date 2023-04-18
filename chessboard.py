from enum import Enum
import pygame
import math

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
    def __init__(self, piecetype, team, x, y, chessboard) -> None:
        self.chessboard = chessboard
        self.piecetype = piecetype
        self.team = team
        self.x = x
        self.y = y
        self.img = pygame.image.load(self.path()).convert_alpha()

    def __str__(self):
        return self.piecetype.name + " " + self.team.name + " " + str(self.x) + " " + str(self.y)
    
    #constructs image path based on team and type
    def path(self):
        if self.team.name == 'MIN':
            team = 'black'
        else:
            team = 'white'
        
        return 'Assets/' + team + self.piecetype.name.lower() + '.png'
        
    #all x_move functions check if a move is valid.
    def pawn_move(self, new_x, new_y):
        #check if pawn is on first move
        if (self.team == Team.MIN and self.y == 6) or (self.team == Team.MAX and self.y == 1):
            first_move = True
        else:
            first_move = False
       
        #check correct y magnitude
        if (abs(self.y - new_y) > 1 and not(first_move)):
            return False
        if (abs(self.y - new_y) > 2):
            return False
        #check correct y direction
        if((self.team == Team.MIN and new_y - self.y > 0) or (self.team == Team.MAX and new_y - self.y < 0)):
            return False 
        #check no deviation in x
        if (abs(self.x - new_x) > 0):
            #check if we can capture a piece
            if(abs(self.x - new_x) == 1 and abs(self.y - new_y) == 1):
                piece = self.chessboard.tiles[new_y][new_x].piece

                if(piece == None):
                    return False
                elif(piece.team != self.team):
                    return True
                
            return False
        #check didn't land on a piece
        piece = self.chessboard.tiles[new_y][new_x].piece
        if(piece != None):
            return False

        return True
    
    def knight_move(self, new_x, new_y):
        change_x = abs(self.x - new_x)
        change_y = abs(self.y - new_y)
        is_valid = (change_x == 1 and change_y == 2) or (change_x == 2 and change_y == 1)

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
        if(piece == None):
            self.piece = None
            self.empty = True
        else:
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
                    self.tiles[y][x].setPiece(Piece(PieceType.PAWN, Team.MAX, x, y, self))
                if(y == 6):
                    self.tiles[y][x].setPiece(Piece(PieceType.PAWN, Team.MIN, x, y, self))

                #rook initializing
                if(y == 0 and (x == 0 or x == 7)):
                    self.tiles[y][x].setPiece(Piece(PieceType.ROOK, Team.MAX, x, y, self))
                if(y == 7 and (x == 0 or x == 7)):
                    self.tiles[y][x].setPiece(Piece(PieceType.ROOK, Team.MIN, x, y, self))

                #knight initializing
                if(y == 0 and (x == 1 or x == 6)):
                    self.tiles[y][x].setPiece(Piece(PieceType.KNIGHT, Team.MAX, x, y, self))
                if(y == 7 and (x == 1 or x == 6)):
                    self.tiles[y][x].setPiece(Piece(PieceType.KNIGHT, Team.MIN, x, y, self))

                #bishop initializing
                if(y == 0 and (x == 2 or x == 5)):
                    self.tiles[y][x].setPiece(Piece(PieceType.BISHOP, Team.MAX, x, y, self))
                if(y == 7 and (x == 2 or x == 5)):
                    self.tiles[y][x].setPiece(Piece(PieceType.BISHOP, Team.MIN, x, y, self))

                #queen initializing
                if(y == 0 and x == 3):
                    self.tiles[y][x].setPiece(Piece(PieceType.QUEEN, Team.MAX, x, y, self))
                if(y == 7 and x == 3):
                    self.tiles[y][x].setPiece(Piece(PieceType.QUEEN, Team.MIN, x, y, self))

                #king initializing
                if(y == 0 and x == 4):
                    self.tiles[y][x].setPiece(Piece(PieceType.KING, Team.MAX, x, y, self))
                if(y == 7 and x == 4):
                    self.tiles[y][x].setPiece(Piece(PieceType.KING, Team.MIN, x, y, self))       

    #high-level idea is that this draws the vector between the old and new positions. It moves along each point of the vector, checking
    #if a piece exists there.
    def check_no_collide(self, old_x, old_y, new_x, new_y):
        collided = False

        while old_x != new_x or old_y != new_y:
            if(old_x < new_x):
                old_x += 1
            elif(old_x > new_x):
                old_x -= 1
            if(old_y < new_y):
                old_y += 1
            elif(old_y > new_y):
                old_y -= 1

            if(old_x == new_x and old_y == new_y):
                break

            if(not(self.tiles[old_y][old_x].empty)):
                collided = True
                break
        
        return not(collided)
    
    #uses x coords 
    def find_piece(self, x, y, x_offset, y_offset):
        relative_x = x - x_offset
        relative_y = y - y_offset
        
        x = math.floor(relative_x / 80)
        y = math.floor(relative_y / 80)

        return self.tiles[y][x].piece
    
    #checks all requirements to see if move is legal
    def legal_move(self, piece, x, y):
        #same team tile
        if(not(self.tiles[y][x].empty) and piece.team == self.tiles[y][x].piece.team):
            return False
        
        old_x = piece.x
        old_y = piece.y
        
        #return true if knight lands in valid tile or other piece can trace clear vector to tile
        return (piece.piecetype == PieceType.KNIGHT or self.check_no_collide(old_x, old_y, x, y)) and piece.move(x, y)
    
    #finds all legal moves - very slow bc we iterate through all tiles. Will make faster by only checking possible vectors
    def find_legal_moves(self, piece):
        valid = []

        for x in range(8):
            for y in range(8):
                if(self.legal_move(piece, x, y)):
                    valid.append((x, y))

        return valid
    
    def move_piece(self, piece, x, y, x_offset, y_offset):
        x = math.floor((x - x_offset) / 80)
        y = math.floor((y - y_offset) / 80)

        old_x = piece.x
        old_y = piece.y

        if(self.legal_move( piece, x, y)):
            piece.x = x
            piece.y = y
            self.tiles[old_y][old_x].setPiece(None)
            self.tiles[y][x].setPiece(piece)

    

    def __str__(self):
        return str(self.tiles)


import pygame
import chessboard

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.font.init() 
my_font = pygame.font.SysFont('Arial Bold Italic', 30)

#initialize chessboard data structure
chessboard = chessboard.Chessboard()

#initialize chessboard graphic
board_img = pygame.image.load("Assets/chessboard.png").convert_alpha()
x_offset = 320
y_offset = 0


while running:
    #poll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                active_piece = chessboard.find_piece(event.pos[0], event.pos[1], 320, 0)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                #try and move active piece
                chessboard.move_piece(active_piece, event.pos[0], event.pos[1], 320, 0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER
    # chessboard
    screen.blit(board_img, (x_offset, y_offset))

    # pieces
    for x in range(8):
        for y in range(8):
            if not(chessboard.tiles[y][x].empty):
                #render if not empty
                screen.blit(chessboard.tiles[y][x].piece.img, (x_offset + 80 * x, y_offset + 80 * y))

    
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
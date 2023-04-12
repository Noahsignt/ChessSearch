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
chess = chessboard.Chessboard()
print(chess)

#initialize chessboard graphic
board_img = pygame.image.load("Assets/chessboard.png").convert()
x_offset = 320
y_offset = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    screen.blit(board_img, (x_offset, y_offset))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
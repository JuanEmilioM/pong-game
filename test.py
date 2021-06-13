# Módulos
import sys
import pygame
from pygame.locals import *
 
# Constantes
WIDTH = 640
HEIGHT = 480
 
# Clases
# ---------------------------------------------------------------------
class Ball (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.5, -0.5]

    def get_image (self): return self.image

    def get_rect (self): return self.rect
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
def load_image (filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit

    image = image.convert_alpha() # more suitable for .png images

    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)

    return image

# ---------------------------------------------------------------------
 
def main():
    # sets the main screen with its background image
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test")
    background_image = load_image("images/fondo_pong.png")
    
    # creates the pong ball
    ball = Ball()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        
        screen.blit(background_image, (0, 0))
        screen.blit(ball.get_image(), ball.get_rect())
        pygame.display.flip()

    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()

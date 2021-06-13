# Módulos
import sys, os
import pygame
from pygame.locals import *
 
# Constantes
WIDTH = 640
HEIGHT = 480
 
# Clases
# ---------------------------------------------------------------------
 
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test")
    background_image = load_image("images/fondo_pong.png")
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        
        screen.blit(background_image, (0, 0))
        pygame.display.flip()

    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()

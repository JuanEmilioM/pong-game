# Modules
import sys, enum
import pygame
from pygame.locals import *

# Constants
WIDTH = 640
HEIGHT = 480
FRAMERATE = 60
X = 0
Y = 1

# Classes
# ---------------------------------------------------------------------
class Positions (enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
class Ball (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.25, -0.25]

    def get_image (self): return self.image
    def get_rect (self): return self.rect
    def speed_up (self, speed): self.speed = speed

    # updates the position of the ball on the screen
    def update (self, time):
        self.rect.centerx += self.speed[X] * time
        self.rect.centery += self.speed[Y] * time

        if (self.rect.left <= 0 or self.rect.right >= WIDTH):
            self.speed[X] = -self.speed[X]  # changes of x momentum component
            self.rect.centerx += self.speed[X] * time

        if (self.rect.top <= 0 or self.rect.bottom >= HEIGHT):
            self.speed[Y] = -self.speed[Y]  # changes of y momentum component
            self.rect.centery += self.speed[Y] * time

class Racket (pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/racket.png", True)
        self.rect = self.image.get_rect()
        self.speed = .5

        if (pos == Positions.LEFT):
            self.rect.midleft = (0,HEIGHT/2)
        elif (pos == Positions.RIGHT):
            self.rect.midright = (WIDTH,HEIGHT/2)
        else:
            raise ("Error, position invalid")

    def get_image (self): return self.image
    def get_rect (self): return self.rect

    def move (self, time, keys):
        if (self.rect.top >= 0 and keys[K_UP]):
            self.rect.centery -= self.speed * time
        
        if (self.rect.bottom <= HEIGHT and keys[K_DOWN]):
            self.rect.centery += self.speed * time
# ---------------------------------------------------------------------

# Procedures
# ---------------------------------------------------------------------
def load_image (filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit

    image = image.convert_alpha()   # more suitable for png images

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

    # creates a clock to control the game time
    clock = pygame.time.Clock()

    # creates the pong ball
    ball = Ball()

    # creates the two rackets
    racket_player = Racket(Positions.LEFT)
    racket_cpu = Racket(Positions.RIGHT)

    while True:
        time = clock.tick(FRAMERATE)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        # updates the position of the sprites on the screen
        ball.update(time)
        racket_player.move(time, pygame.key.get_pressed())
        screen.blit(background_image, (0, 0))
        screen.blit(ball.get_image(), ball.get_rect())
        screen.blit(racket_player.get_image(), racket_player.get_rect())
        screen.blit(racket_cpu.get_image(), racket_cpu.get_rect())
        pygame.display.flip()

    return 0

if __name__ == '__main__':
    pygame.init()
    main()

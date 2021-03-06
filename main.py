# Modules
import sys, enum
import pygame
from pygame.locals import *
from pygame.key import get_pressed
from pygame.sprite import collide_rect
from numpy.random import normal, randint

# Constants
WIDTH = 640
HEIGHT = 480
FRAMERATE = 60
X = 0
Y = 1
POINTS_TO_WIN = 10

# Classes
# ---------------------------------------------------------------------
class Positions (enum.Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Ball (pygame.sprite.Sprite):
    def __init__(self, speed=[.25, -.25]):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = speed

    def get_image (self): return self.image
    def get_rect (self): return self.rect
    def speed_up (self, speed): self.speed = speed
    def get_speed (self): return self.speed

    # updates the position of the ball on the screen
    def update (self, time, racket):
        self.rect.centerx += self.speed[X] * time
        self.rect.centery += self.speed[Y] * time
        
        # looks for colisions with the left wall
        if (self.rect.left <= 0): return Positions.LEFT
        
        # looks for colisions with the right wall
        if (self.rect.right >= WIDTH): return Positions.RIGHT

        if (self.rect.top <= 0 or self.rect.bottom >= HEIGHT):
            self.speed[Y] = -self.speed[Y]  # changes of y momentum component
            self.rect.centery += self.speed[Y] * time

        if (collide_rect(self, racket)):
            self.speed[X] = -self.speed[X]
            self.rect.centerx += self.speed[X] * time

        return Positions.NONE
        
class Racket (pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("racket.png", True)
        self.rect = self.image.get_rect()
        self.speed = speed

        if (pos == Positions.LEFT):
            self.rect.midleft = (0,HEIGHT/2)
        elif (pos == Positions.RIGHT):
            self.rect.midright = (WIDTH,HEIGHT/2)
        else:
            raise ("Error, position invalid")

    def get_image (self): return self.image
    def get_rect (self): return self.rect

    def move (self, time, keys=None, ball=None):
        if (keys is not None):
            if (self.rect.top >= 0 and keys[K_UP]):
                self.rect.centery -= self.speed * time
            
            if (self.rect.bottom <= HEIGHT and keys[K_DOWN]):
                self.rect.centery += self.speed * time
        
        elif(ball is not None):
            ball_speed = ball.get_speed()
            ball_rect = ball.get_rect()
            
            if (ball_speed[X] >= 0 and ball_rect.centerx >= WIDTH/2):
                if (self.rect.centery < ball_rect.centery):
                    self.rect.centery += self.speed * time
                if (self.rect.centery > ball_rect.centery):
                    self.rect.centery -= self.speed * time
# ---------------------------------------------------------------------

# Procedures
# ---------------------------------------------------------------------
def winner_message (screen, message):
    # sets the colors 
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    red = (255, 0, 0)

    # sets the font used to print messages 
    font = pygame.font.Font('freesansbold.ttf', 36)
    text = font.render(message, True, green, white)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
 
    # set the center of the rectangular object.
    textRect.center = (WIDTH/2, HEIGHT/2)

    screen.blit(text, textRect)

def load_image (filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit

    image = image.convert_alpha()   # more suitable for png images

    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)

    return image

def print_points (screen, player_points, cpu_points):
    # sets the colors 
    white = (255, 255, 255)
    black = (0, 0, 0)

    # sets the font used to print messages 
    font = pygame.font.Font('freesansbold.ttf', 36)
    text_1 = font.render(str(player_points), True, white, black)
    text_2 = font.render(str(cpu_points), True, white, black)

    # create a rectangular object for the
    # text surface object
    textRect_1 = text_1.get_rect()
    textRect_2 = text_2.get_rect()
 
    # set the center of the rectangular object.
    textRect_1.center = (WIDTH/2 - 50, 50)
    textRect_2.center = (WIDTH/2 + 50, 50)

    screen.blit(text_1, textRect_1)
    screen.blit(text_2, textRect_2)
# ---------------------------------------------------------------------

def main():
    # sets the main screen with its background image
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    background_image = load_image("fondo_pong.png")

    # creates a clock to control the game time
    clock = pygame.time.Clock()

    # initalizes the scorers
    player_points = cpu_points = 0

    # a flag to control if someone has won
    winner = False

    while not winner:
        # creates the pong ball with the given velocity vector
        v_x = (-1)**randint(0,100) * normal(loc=.45, scale=.006)
        v_y = (-1)**randint(0,100) * normal(loc=-.085, scale=.008)
        ball = Ball([v_x, v_y])

        # creates the two rackets
        racket_player = Racket(Positions.LEFT, .5)
        racket_cpu = Racket(Positions.RIGHT, .7)
        
        while True:
            time = clock.tick(FRAMERATE)

            # checks if exit button was pressed
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            if(ball.update(time, racket_player) == Positions.LEFT):
                cpu_points += 1
                break

            elif(ball.update(time, racket_cpu) == Positions.RIGHT):
                player_points += 1
                break

            else:
                racket_player.move(time, keys=get_pressed())
                racket_cpu.move(time, ball=ball)
                screen.blit(background_image, (0, 0))
                screen.blit(ball.get_image(), ball.get_rect())
                screen.blit(racket_player.get_image(), racket_player.get_rect())
                screen.blit(racket_cpu.get_image(), racket_cpu.get_rect())
                print_points(screen, player_points, cpu_points)
                pygame.display.flip()       

        if (player_points == POINTS_TO_WIN):
            winner_message(screen, "You won!")
            winner = True

        elif(cpu_points == POINTS_TO_WIN):
            winner_message(screen, "CPU won!")
            winner = True

        print_points(screen, player_points, cpu_points)
        pygame.display.flip()

    # waits until the window is closed
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

if __name__ == '__main__':
    pygame.init()
    main()

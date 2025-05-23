import pygame
from pygame.rect import Rect

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400

SPEED = 7

SCORE = 0
ball_speed_y = 4
ball_speed_x = 4
HIGHSCORE = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Single Pong')

font = pygame.font.SysFont('Calibri', 40, bold = False)

class Player:
    def __init__(self):
        self.paddle = Rect(0, 0, 90, 10)
        self.paddle.bottomright = (SCREEN_WIDTH / 1.7, SCREEN_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, 'white', self.paddle)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.move_ip(-SPEED, 0)

        if key[pygame.K_RIGHT] and self.paddle.right < SCREEN_WIDTH:
            self.paddle.move_ip(SPEED, 0)

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    def draw(self):
        pygame.draw.ellipse(screen, 'white', self.rect)

    def move(self):
        global ball_speed_x
        global SCORE
        global ball_speed_y
        # Checking for collisions
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            ball_speed_x *= -1
        
        if self.rect.top <= 0:
            ball_speed_y *= -1

        if self.rect.colliderect(player.paddle):
            ball_speed_y *= -1
            SCORE += 1
            self.set_highscore()

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Updating Speed
        self.rect.x += ball_speed_x
        self.rect.y += ball_speed_y

    def reset(self, x, y):
        global SCORE
        self.x = x
        self.y = y
        self.ball_rad = 20
        self.rect = Rect(x, y, self.ball_rad, self.ball_rad)
        SCORE = 0
        self.get_highscore()

    def set_highscore(self):
        global HIGHSCORE
        if SCORE > HIGHSCORE:
            HIGHSCORE = SCORE

            with open('records', 'w') as w:
                w.write(str(SCORE))

    def get_highscore(self):
        global HIGHSCORE
        try:
            with open('records', 'r') as r:
                HIGHSCORE = int(r.read())
        except FileNotFoundError:
            HIGHSCORE = 0

clock = pygame.time.Clock()
player = Player()
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        # Quit the Game
        if event.type == pygame.QUIT:
            running = False
    
    # Drawing and Updating
    player.move()
    ball.move()

    screen.fill('black')
    score_text = font.render(f'Score: {str(SCORE)}', 1, 'white')
    screen.blit(score_text, (5, 5))
    player.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
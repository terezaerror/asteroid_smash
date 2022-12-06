import pygame
from pygame.draw import *
from random import randint

pygame.init()

WIDTH = 1300
HEIGHT = 700
Rmin = 30
Rmax = 60
Vmin = 7
Vmax = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 80
n = 5 #количество кружков на экране
background = pygame.image.load('background.jpg')
background_rect = background.get_rect(
    bottomright=(WIDTH, HEIGHT))


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

'''class SpaceShip(self):
    def __init__(self):
class Bullet(self):
    sdjhg'''


class Asteroid:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = []
        self.y = []
        self.r = []
        self.vx = []
        self.vy = []
        self.color = []
    def create(self):
        for i in range(n):
            self.x += [randint(Rmax, WIDTH-Rmax)]
            self.y += [randint(Rmax, HEIGHT - Rmax)]
            self.r += [randint(Rmin, Rmax)]
            self.vx += [randint(Vmin, Vmax)*(2*randint(0, 1)-1)]
            self.vy += [randint(Vmin, Vmax)*(2*randint(0, 1)-1)]
            self.color += [COLORS[randint(0, 5)]]
            circle(screen, self.color[i], (self.x[i], self.y[i]), self.r[i])

    def catch_check(self, event):
        '''п'''
        for i in range(n):
            if (event.pos[0]-self.x[i])**2 + (event.pos[1]-self.y[i])**2 <= self.r[i]**2:
                self.x.remove(self.x[i])
                self.y.remove(self.y[i])
                self.r.remove(self.r[i])
                self.vx.remove(self.vx[i])
                self.vy.remove(self.vy[i])
                self.color.remove(self.self.color[i])
                return True
        return False

    def new(self):
        '''с'''
        self.x += [randint(Rmax, WIDTH - Rmax)]
        self.y += [randint(Rmax, HEIGHT - Rmax)]
        self.r += [randint(Rmin, Rmax)]
        self.vx += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
        self.vy += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
        self.color += [COLORS[randint(0, 5)]]
        circle(screen, self.color[n-1], (self.x[n-1], self.y[n-1]), self.r[n-1])

    def move(self):
        '''с'''
        for i in range(n):
            self.x[i] += self.vx[i]
            self.y[i] += self.vy[i]

    def wall_check(self):
        '''проверяет необходимость отскока и отражает скорости астероидов если нужно'''
        for i in range(n):
            if min(WIDTH-self.x[i], self.x[i]) <= self.r[i]:
                self.vx[i] = -self.vx[i]
            if min(HEIGHT - self.y[i], self.y[i]) <= self.r[i]:
                self.vy[i] = -self.vy[i]

    def draw(self):
        '''в'''
        for i in range(n):
            circle(screen, self.color[i], (self.x[i], self.y[i]), self.r[i])

score = 0
asteroid = Asteroid(screen)
shrift = pygame.font.SysFont('Times New Roman', 30)
text_color = RED
clock = pygame.time.Clock()
finished = False

asteroid.create()
while not finished:
    clock.tick(FPS)
    screen.blit(background, background_rect)
    asteroid.move()
    asteroid.wall_check()
    asteroid.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if asteroid.catch_check(event):
                asteroid.new()
                score += 1
    pygame.display.update()
    screen.fill(BLACK)

print("Ваш счёт: ", score)



pygame.init()
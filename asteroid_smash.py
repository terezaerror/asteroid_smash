import math
import pygame
from pygame.draw import *
from random import randint
from random import choice

WIDTH = 1300
HEIGHT = 700
FPS = 60

background = pygame.image.load('background-1.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 102, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.n = 0
        self.x = []
        self.y = []
        self.r = []
        self.r0 = 5
        self.angle = []
        self.v0 = 10
        self.color = WHITE
        self.delay = 5

    def new(self, obj):
        self.n += 1
        self.x.append(obj.x)
        self.y.append(obj.y)
        self.r.append(self.r0)
        self.angle.append(obj.angle)

    def move_and_draw(self):
        for i in range(self.n):
            self.x[i] += self.v0 * math.sin(-math.radians(self.angle[i]))
            self.y[i] -= self.v0 * math.cos(math.radians(self.angle[i]))
            circle(self.screen, self.color, (self.x[i], self.y[i]), self.r[i])

    def wall_check(self):
        for i in range(self.n):
            if self.y[i] >= HEIGHT + 100 or self.y[i] <= - 100 or self.x[i] >= WIDTH + 100 or self.x[i] <= - 100:
                self.delete(i)
                return True
        return False

    def delete(self, i):
        self.x.pop(i)
        self.y.pop(i)
        self.r.pop(i)
        self.angle.pop(i)
        self.n -= 1


class SpaceShip:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('spaceship.png')
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.r = 30
        self.speed = 8
        self.angle = 0
        self.maneuverability = 5

    def move(self):
        self.x += self.speed * math.sin(-math.radians(self.angle))
        self.y -= self.speed * math.cos(math.radians(self.angle))

    def move_back(self):
        self.x -= self.speed * math.sin(-math.radians(self.angle))
        self.y += self.speed * math.cos(math.radians(self.angle))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        self.angle += self.maneuverability * sign

    def draw(self):
        self.screen.blit(pygame.transform.rotate(
            pygame.transform.scale(self.image, (self.r * 2, self.r * 2)), self.angle),
            pygame.transform.rotate(pygame.transform.scale(
                self.image, (self.r * 2, self.r * 2)),
                self.angle).get_rect(center=(self.x, self.y)))


class Asteroid:
    def __init__(self, screen):
        self.n = 0
        self.Rmin = 20
        self.Rmax = 50
        self.Vmin = 2
        self.Vmax = 3
        self.Wmax = 2
        self.screen = screen
        self.x = []
        self.y = []
        self.r = []
        self.vx = []
        self.vy = []
        self.image = []
        self.angle = []
        self.w = []
        self.rect = []
        self.image_1 = pygame.image.load('asteroid-1.png')
        self.image_2 = pygame.image.load('asteroid-2.png')
        # self.image_3 = ...
        # self.smash_image = ...
        self.choices = [self.image_1, self.image_2]
        self.delay = 200

    def catch_check(self, event):
        for i in range(self.n):
            if (event.pos[0] - self.x[i]) ** 2 + (event.pos[1] - self.y[i]) ** 2 <= self.r[i] ** 2:
                self.delete(i)
                return True
        return False

    def new(self):
        self.n += 1
        self.x.append(randint(*choice([(WIDTH + self.Rmax, WIDTH + 100 + self.Rmax),
                                       (-self.Rmax - 100, -self.Rmax)])))
        self.y.append(randint(*choice([(HEIGHT + self.Rmax, HEIGHT + 100 + self.Rmax),
                                       (-self.Rmax - 100, -self.Rmax)])))
        self.r.append(randint(self.Rmin, self.Rmax))
        self.vx.append(randint(*choice([(-self.Vmax, -self.Vmin), (self.Vmin, self.Vmax)])))
        self.vy.append(randint(*choice([(-self.Vmax, -self.Vmin), (self.Vmin, self.Vmax)])))
        self.image.append(choice(self.choices))
        self.angle.append(0)
        self.w.append(randint(*choice([(-self.Wmax, -1), (1, self.Wmax)])))

    def move_and_draw(self):
        for i in range(self.n):
            self.x[i] += self.vx[i]
            self.y[i] += self.vy[i]
            self.angle[i] += self.w[i]
            self.screen.blit(pygame.transform.rotate(
                pygame.transform.scale(self.image[i], (self.r[i] * 2, self.r[i] * 2)), self.angle[i]),
                pygame.transform.rotate(pygame.transform.scale(
                    self.image[i], (self.r[i] * 2, self.r[i] * 2)),
                    self.angle[i]).get_rect(center=(self.x[i], self.y[i])))

    def wall_check(self):
        for i in range(self.n):
            if (self.vx[i] > 0 and WIDTH + 300 - self.x[i] <= self.r[i]) or \
                    (self.vx[i] < 0 and 300 + self.x[i] <= self.r[i]):
                self.vx[i] = -self.vx[i]
            if (self.vy[i] > 0 and HEIGHT + 300 - self.y[i] <= self.r[i]) or \
                    (self.vy[i] < 0 and 300 + self.y[i] <= self.r[i]):
                self.vy[i] = -self.vy[i]

    def crash_check(self, obj):
        for i in range(self.n):
            if (obj.x - self.x[i]) ** 2 + (obj.y - self.y[i]) ** 2 <= (obj.r + self.r[i]) ** 2:
                return True
        return False

    def delete(self, i):
        self.x.pop(i)
        self.y.pop(i)
        self.r.pop(i)
        self.vx.pop(i)
        self.vy.pop(i)
        self.image.pop(i)
        self.angle.pop(i)
        self.w.pop(i)
        self.n -= 1
    '''def smash(self):
        self.screen.blit(pygame.transform.scale(self.image[i], (self.r[i] * 2, self.r[i] * 2)),
                         (self.x[i] - self.r[i], self.y[i] - self.r[i]))'''


class Energy:
    def __init__(self, screen):
        self.screen = screen
        self.x = 1
        self.y = 1
        self.length = 300
        self.height = 25
        self.fuel = 0
        self.delay = False

    def draw(self):
        if self.fuel < self.length:
            self.fuel += 1
        if 0 < self.fuel <= self.length // 4:
            rect(self.screen, RED, (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif self.length // 4 < self.fuel <= self.length // 2:
            rect(self.screen, ORANGE, (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif self.length // 2 < self.fuel <= 3 * self.length // 4:
            rect(self.screen, YELLOW, (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif 3 * self.length // 4 < self.fuel <= self.length:
            rect(self.screen, GREEN, (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        if self.fuel == self.length:
            self.delay = False

    def charge(self):
        if self.fuel > 0:
            self.fuel -= 20
            return True
        else:
            self.delay = True
            return False


def hit_check(obj1, obj2):
    for i in range(obj1.n):
        for j in range(obj2.n):
            if (obj1.x[i] - obj2.x[j]) ** 2 + (obj1.y[i] - obj2.y[j]) ** 2 <= (obj1.r[i] + obj2.r[j]) ** 2:
                obj1.delete(i)
                obj2.delete(j)
                return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 1
    asteroid = Asteroid(screen)
    spaceship = SpaceShip(screen)
    ball = Ball(screen)
    energy = Energy(screen)
    shrift = pygame.font.SysFont('Times New Roman', 30)
    ending_shrift = pygame.font.SysFont('Times New Roman', 100)
    delay1 = asteroid.delay
    delay2 = ball.delay
    clock = pygame.time.Clock()
    finished = False

    asteroid.new()
    while not finished:
        clock.tick(FPS)
        screen.blit(background, background_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.new(spaceship)'''

        if hit_check(ball, asteroid):
            # asteroid.smash()
            asteroid.new()
            score += 10

        asteroid.wall_check()
        asteroid.move_and_draw()
        spaceship.draw()
        ball.wall_check()
        ball.move_and_draw()

        print(ball.x, ball.y, ball.angle)

        delay1 -= 1
        if delay1 == 0:
            score += 1
            asteroid.new()
            delay1 = asteroid.delay

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            spaceship.rotate(clockwise=False)
        elif keys[pygame.K_LEFT]:
            spaceship.rotate(clockwise=True)
        if keys[pygame.K_UP]:
            spaceship.move()
        elif keys[pygame.K_DOWN]:
            spaceship.move_back()
        if keys[pygame.K_SPACE]:
            delay2 -= 1
            if delay2 <= 0 and not energy.delay:
                score += 1
                delay2 = ball.delay
                ball.new(spaceship)
                energy.charge()
        energy.draw()

        text = shrift.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (1, 1))
        pygame.display.update()
        screen.fill(BLACK)

        if asteroid.crash_check(spaceship):
            while not finished:
                text = shrift.render("Ваш счёт: " + str(score), True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                ending_text = ending_shrift.render("Game over", True, (255, 0, 0))
                ending_text_rect = ending_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(ending_text, ending_text_rect)
                screen.blit(text, text_rect)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished = True

    print("Ваш счёт: ", score)
    pygame.init()


if __name__ == '__main__':
    main()

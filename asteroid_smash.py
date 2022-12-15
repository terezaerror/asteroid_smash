import math
import pygame
from random import randint
from random import choice

WIDTH = 1300
HEIGHT = 700
Rmin = 30
Rmax = 60
Vmin = 2
Vmax = 4
FPS = 80

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = COLORS[randint(0, 5)]
        self.live = 45

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        g = 0.7
        k = 0.02
        self.x += self.vx
        self.y -= self.vy
        self.vx -= k * self.vx
        if (self.y >= HEIGHT - self.r - 1) or (self.y <= 10):
            self.vy = -self.vy
        else:
            self.vy -= g
            self.vy -= k * self.vy
        if (self.x >= WIDTH - self.r - 1) or (self.x <= 10): self.vx = -self.vx
        self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class SpaceShip:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = CYAN
        self.x = 200
        self.y = 450
        self.width = 5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x=self.x, y=self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def draw(self):
        x2 = self.x - self.width * math.sin(self.an)
        y2 = self.y + self.width * math.cos(self.an)
        x1 = self.x + math.cos(self.an) * self.f2_power
        y1 = self.y + math.sin(self.an) * self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.polygon(self.screen, self.color, ((self.x, self.y), (x1, y1), (x3, y3), (x2, y2)))


class Asteroid:
    def __init__(self, screen):
        self.n = 20
        self.screen = screen
        self.x = []
        self.y = []
        self.r = []
        self.vx = []
        self.vy = []
        self.image = []
        self.image_1 = pygame.image.load('asteroid-1.png')
        self.image_2 = pygame.image.load('asteroid-2.png')
        self.choices = [self.image_1, self.image_2]

    def create(self):
        for i in range(self.n):
            self.x += [randint(*choice([(WIDTH + Rmax, WIDTH + 100 + Rmax), (-Rmax - 100, -Rmax)]))]
            self.y += [randint(*choice([(HEIGHT + Rmax, HEIGHT + 100 + Rmax), (-Rmax - 100, -Rmax)]))]
            self.r += [randint(Rmin, Rmax)]
            self.vx += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
            self.vy += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
            self.image += [choice(self.choices)]
            self.screen.blit(pygame.transform.scale(self.image[i], (self.r[i] * 2, self.r[i] * 2)),
                             (self.x[i] - self.r[i], self.y[i] - self.r[i]))

    def catch_check(self, event):
        for i in range(self.n):
            if (event.pos[0] - self.x[i]) ** 2 + (event.pos[1] - self.y[i]) ** 2 <= self.r[i] ** 2:
                self.x.remove(self.x[i])
                self.y.remove(self.y[i])
                self.r.remove(self.r[i])
                self.vx.remove(self.vx[i])
                self.vy.remove(self.vy[i])
                self.image.remove(self.image[i])
                return True
        return False

    def new(self):
        self.x += [randint(*choice([(WIDTH + Rmax, WIDTH + 100 + Rmax), (-Rmax - 100, -Rmax)]))]
        self.y += [randint(*choice([(HEIGHT + Rmax, HEIGHT + 100 + Rmax), (-Rmax - 100, -Rmax)]))]
        self.r += [randint(Rmin, Rmax)]
        self.vx += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
        self.vy += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
        self.image += [choice(self.choices)]
        self.screen.blit(pygame.transform.scale(self.image[self.n - 1],
                                                (self.r[self.n - 1] * 2, self.r[self.n - 1] * 2)),
                         (self.x[self.n - 1] - self.r[self.n - 1],
                          self.y[self.n - 1] - self.r[self.n - 1]))

    def move(self):
        for i in range(self.n):
            self.x[i] += self.vx[i]
            self.y[i] += self.vy[i]

    def draw(self):
        for i in range(self.n):
            self.screen.blit(pygame.transform.scale(self.image[i], (self.r[i] * 2, self.r[i] * 2)),
                             (self.x[i] - self.r[i], self.y[i] - self.r[i]))

    def wall_check(self):
        for i in range(self.n):
            if WIDTH + 300 - self.x[i] <= self.r[i] or 200 + self.x[i] <= self.r[i]:
                self.vx[i] = -self.vx[i]
            if HEIGHT + 300 - self.y[i] <= self.r[i] or 200 + self.y[i] <= self.r[i]:
                self.vy[i] = -self.vy[i]


class Timer:
    def __init__(self, delay, callback):
        self.delay = delay
        self.callback = callback

    def tick(self):
        self.delay -= 1
        if self.delay == 0:
            self.callback()
            self.delay += 100


def do_smth():
    print("12345")


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 0
    asteroid = Asteroid(screen)
    # shrift = pygame.font.SysFont('Times New Roman', 30)
    # text_color = RED
    clock = pygame.time.Clock()
    finished = False
    pygame.init()

    asteroid.create()

    timer = Timer(100, do_smth())
    while not finished:
        clock.tick(FPS)
        screen.blit(background, background_rect)
        asteroid.move()
        # timer.tick()
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

    print("Game over: ", score)

    pygame.init()


if __name__ == '__main__':
    main()

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
        self.color = choice(COLORS)
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
        if (self.y >= HEIGHT-self.r - 1) or (self.y <= 10): self.vy = -self.vy
        else:
            self.vy -= g
            self.vy -= k * self.vy
        if (self.x >= WIDTH-self.r - 1) or (self.x <= 10): self.vx = -self.vx
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
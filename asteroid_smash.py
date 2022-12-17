import math
import pygame
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
        if (self.x >= WIDTH - self.r - 1) or (self.x <= 10):
            self.vx = -self.vx
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
        self.image = pygame.image.load('spaceship.png')
        self.x = 200
        self.y = 450
        self.r = 30
        self.speed = 8
        self.angle = 0
        self.maneuverability = 4
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = CYAN
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

    def move(self):
        self.x += self.speed * math.sin(-math.radians(self.angle))
        self.y -= self.speed * math.cos(math.radians(self.angle))

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
        self.Vmin = 1
        self.Vmax = 7
        self.Wmax = 5
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
                self.x.pop(i)
                self.y.pop(i)
                self.r.pop(i)
                self.vx.pop(i)
                self.vy.pop(i)
                self.image.pop(i)
                self.angle.pop(i)
                self.w.pop(i)
                self.n -= 1
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

    def hit_check(self, obj):
        for i in range(self.n):
            if (obj.x - self.x[i]) ** 2 + (obj.y - self.y[i]) ** 2 <= (obj.r + self.r[i]) ** 2:
                return True
        return False

    '''def smash(self):
        self.screen.blit(pygame.transform.scale(self.image[i], (self.r[i] * 2, self.r[i] * 2)),
                         (self.x[i] - self.r[i], self.y[i] - self.r[i]))'''


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 1
    asteroid = Asteroid(screen)
    spaceship = SpaceShip(screen)
    shrift = pygame.font.SysFont('Times New Roman', 30)
    ending_shrift = pygame.font.SysFont('Times New Roman', 100)
    delay = asteroid.delay
    clock = pygame.time.Clock()
    finished = False
    asteroid.new()
    while not finished:
        clock.tick(FPS)
        screen.blit(background, background_rect)
        delay -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if asteroid.catch_check(event):  # if a bullet gets into an asteroid
                    # asteroid.smash()
                    asteroid.new()
                    score += 10

        asteroid.wall_check()
        asteroid.move_and_draw()

        if delay == 0:
            score += 1
            asteroid.new()
            delay = asteroid.delay

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            spaceship.rotate(clockwise=False)
        elif keys[pygame.K_LEFT]:
            spaceship.rotate(clockwise=True)
        if keys[pygame.K_UP]:
            spaceship.move()
        spaceship.draw()

        text = shrift.render("Ваш счёт: " + str(score), True, (255, 255, 255))
        screen.blit(text, (1, 1))
        pygame.display.update()
        screen.fill(BLACK)

        if asteroid.hit_check(spaceship):
            text = shrift.render("Ваш счёт: " + str(score), True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            ending_text = ending_shrift.render("Game over", True, (255, 0, 0))
            ending_text_rect = ending_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(ending_text, ending_text_rect)
            pygame.display.update()
            clock.tick(1)
            screen.fill(BLACK)
            screen.blit(text, text_rect)
            pygame.display.update()
            clock.tick(1)
            finished = True

    print("Ваш счёт: ", score)
    pygame.init()


if __name__ == '__main__':
    main()

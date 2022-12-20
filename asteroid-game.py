import math
import pygame
import sys
from pygame.draw import *
from random import randint
from random import choice
from pygame import mixer

WIDTH = 1300
HEIGHT = 700
FPS = 80

data = open('table.txt', 'r')
table_old = data.read()
data.close()
mixer.init()
global name

background = pygame.image.load('Sounds&Images/background_pixel.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
main_menu = pygame.image.load('Sounds&Images/start.jpg')
main_menu = pygame.transform.scale(main_menu, (WIDTH, HEIGHT))
main_menu_rect = main_menu.get_rect()
DEFAULT_IMAGE_SIZE = (100, 100)
space_base = pygame.image.load('Sounds&Images/end.jpg')
space_base = pygame.transform.scale(space_base, (WIDTH, HEIGHT))
space_base_rect = space_base.get_rect()


def load_sound(file):
    sound = mixer.Sound(file)
    return sound


hit_sound = load_sound('Sounds&Images/laser.mp3')
chewbacca = load_sound('Sounds&Images/Chewbacca roar.mp3')
explosion_sound = load_sound('Sounds&Images/boom1.wav')


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.n = 0
        self.x = []
        self.y = []
        self.r = []
        self.r0 = 5
        self.angle = []
        self.v0 = 20
        self.color = (255, 255, 255)
        self.delay = 4

    def new(self, obj):
        hit_sound.play()
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
        self.image = pygame.image.load('Sounds&Images/spaceship.png')
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

    def is_outside(self):
        if self.x < - 10 or self.x > WIDTH + 10 or self.y < - 10 or self.y > HEIGHT + 10:
            return True
        return False


class Asteroid:
    def __init__(self, screen):
        self.n = 0
        self.R1 = 20
        self.R2 = 35
        self.R3 = 50
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
        self.image_1 = pygame.image.load('Sounds&Images/asteroid-1.png')
        self.image_2 = pygame.image.load('Sounds&Images/asteroid-2.png')
        # self.smash_image = ...
        self.choices = [self.image_1, self.image_2]
        self.delay = 70

    def catch_check(self, event):
        for i in range(self.n):
            if (event.pos[0] - self.x[i]) ** 2 + (event.pos[1] - self.y[i]) ** 2 <= self.r[i] ** 2:
                self.delete(i)
                return True
        return False

    def new(self):
        self.n += 1
        self.x.append(randint(*choice([(WIDTH + 100, WIDTH + 200), (- 200, - 100)])))
        self.y.append(randint(*choice([(HEIGHT + 100, HEIGHT + 200), (- 200, - 100)])))
        self.r.append(choice([self.R1, self.R2, self.R3]))
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


class Power:
    def __init__(self, screen):
        self.screen = screen
        self.x = 1
        self.y = 27
        self.length = 300
        self.height = 17
        self.fuel = 0
        self.delay = False
        self.color = (240, 0, 0)

    def draw(self):
        if self.fuel < self.length:
            self.fuel += 1
        if 0 < self.fuel <= self.length:
            rect(self.screen, self.color, (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        if self.fuel == self.length:
            self.color = (240, 0, 0)
            self.delay = False

    def charge(self):
        if self.fuel > 0:
            self.fuel -= 15
            return True
        else:
            self.delay = True
            self.color = (132, 0, 0)
            return False


class Health:
    def __init__(self, screen):
        self.screen = screen
        self.x = 1
        self.y = 1
        self.length = 300
        self.height = 25
        self.fuel = 300
        self.heal = 60
        self.heal_delay = 400
        self.hit_delay = 30

    def draw(self):
        if 0 < self.fuel <= self.length // 5:
            rect(self.screen, (200, 0, 0), (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif self.length // 5 < self.fuel <= 2 * self.length // 5:
            rect(self.screen, (255, 100, 0), (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif 2 * self.length // 5 < self.fuel <= 3 * self.length // 5:
            rect(self.screen, (220, 200, 0), (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif 3 * self.length // 5 < self.fuel <= 4 * self.length // 5:
            rect(self.screen, (150, 200, 0), (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))
        elif 4 * self.length // 5 < self.fuel <= self.length:
            rect(self.screen, (0, 230, 0), (WIDTH - self.x - self.fuel, self.y, self.fuel, self.height))


def hit_check(obj1, obj2):
    for i in range(obj1.n):
        for j in range(obj2.n):
            if (obj1.x[i] - obj2.x[j]) ** 2 + (obj1.y[i] - obj2.y[j]) ** 2 <= (obj1.r[i] + obj2.r[j]) ** 2:
                obj1.delete(i)
                obj2.delete(j)
                return True
    return False


def main():
    global name
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    font1 = pygame.font.Font("font.ttf", 35)
    text1 = font1.render('Enter name:', True, (255, 255, 255))
    text2 = font1.render('A long time ago in a galaxy far,', True, (14, 246, 255))
    text3 = font1.render('far away. . .', True, (14, 246, 255))
    font = pygame.font.Font("font.ttf", 40)
    input_box = pygame.Rect(450, 38, 200, 55)
    color_inactive = pygame.Color((255, 255, 255))
    color_active = pygame.Color((14, 246, 255))
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        mixer.music.load('Sounds&Images/open.mp3')
        mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        name = text
                        print(text)
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        screen.fill((0, 0, 0))
        # Render the current text.
        text_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, text_surface.get_width() + 10)
        input_box.w = width
        screen.blit(text1, (30, 50))
        screen.blit(text2, (80, 340))
        screen.blit(text3, (80, 390))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    end = False
    while not end:
        screen.blit(main_menu, main_menu_rect)
        font = pygame.font.Font("font.ttf", 25)
        font_buttons = pygame.font.Font("font.ttf", 40)
        label = font.render(name + ", welcome to Millennium Falcon!", True, (255, 255, 255))

        menu_mouse_pos = pygame.mouse.get_pos()

        play_button = Button(image=None, pos=(325, 350),
                             text_input="PLAY", font=font_buttons, base_color=(209, 17, 74), hovering_color="White")
        quit_button = Button(image=None, pos=(975, 350),
                             text_input="QUIT", font=font_buttons, base_color=(209, 17, 74), hovering_color="White")

        for button in [play_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    end = True
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(label, (150, 110))
        pygame.display.update()

    score = 1
    asteroid = Asteroid(screen)
    spaceship = SpaceShip(screen)
    ball = Ball(screen)
    power = Power(screen)
    health = Health(screen)
    asteroid_delay = asteroid.delay
    ball_delay = ball.delay
    heal_delay = health.heal_delay
    hit_delay = health.hit_delay
    clock = pygame.time.Clock()
    finished = False
    asteroid.new()
    while not finished:
        mixer.music.load('Sounds&Images/imperial.mp3')
        mixer.music.play(-1)
        clock.tick(FPS)
        screen.blit(background, background_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        if hit_check(ball, asteroid):
            # asteroid.smash()
            asteroid.new()
            score += 10

        asteroid.wall_check()
        asteroid.move_and_draw()
        spaceship.draw()
        ball.wall_check()
        ball.move_and_draw()
        power.draw()
        health.draw()

        asteroid_delay -= 1
        if asteroid_delay == 0:
            score += 1
            asteroid.new()
            asteroid_delay = asteroid.delay

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
            ball_delay -= 1
            if ball_delay <= 0 and not power.delay:
                ball_delay = ball.delay
                ball.new(spaceship)
                power.charge()

        score_text = pygame.font.Font("font.ttf", 20).render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (1, 1))
        power_text = pygame.font.Font("font.ttf", 13).render("Power", True, (255, 255, 255))
        screen.blit(power_text, (WIDTH - 290, 30))
        health_text = pygame.font.Font("font.ttf", 20).render("Health", True, (255, 255, 255))
        screen.blit(health_text, (WIDTH - 290, 4))
        pygame.display.update()
        screen.fill((0, 0, 0))

        if 0 < health.fuel < health.length:
            if heal_delay == 0:
                health.fuel += health.heal
                heal_delay = health.heal_delay
            else:
                heal_delay -= 1
        if hit_delay:
            hit_delay -= 1

        if asteroid.crash_check(spaceship) or spaceship.is_outside():
            explosion_sound.play()
            # !!! hit sound !!!
            heal_delay = health.heal_delay
            if health.fuel > 0 and hit_delay == 0:
                health.fuel -= health.heal
                hit_delay = health.hit_delay
            if health.fuel <= 0:
                mixer.music.load('Sounds&Images/Dont fail me again.mp3')
                mixer.music.play()
                while not finished:
                    text1 = pygame.font.Font("font.ttf", 20).render("Your score: " + str(score), True, (255, 255, 255))
                    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    text2 = pygame.font.Font("font.ttf", 30).render("Game over", True, (209, 17, 74))
                    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                    screen.blit(text1, text1_rect)
                    screen.blit(text2, text2_rect)
                    pygame.display.update()
                    screen.fill((0, 0, 0))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            finished = True

    table = open('table.txt', 'w')
    print(table_old, file=table)
    print(name, score, file=table)
    table.close()

    table = open('table.txt', 'r')
    a_data = table.readlines()
    a_data = [a_line.rstrip() for a_line in a_data]
    table.close()

    complete = False
    screen.blit(space_base, space_base_rect)
    text = []
    for a_line in a_data:
        text.append(font.render(a_line, True, (255, 255, 255)))
    while not complete:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                complete = True
        for i in range(len(text)):
            screen.blit(text[i], (40, 30 + 25 * i))

        pygame.display.update()

    pygame.init()


if __name__ == '__main__':
    main()

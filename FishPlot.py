import pygame
import math
from varname import nameof
from pygame.locals import *
from pygame.version import ver

pygame.init()

clock = pygame.time.Clock()
fps = 30

screen_width = 1900
screen_height = 1000

playable_width = screen_width - 300
playable_height = screen_height

columns = int((playable_width * 20) / 1000)
rows = int((playable_height * 20) / 1000)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fish Jumping Simulator')
icon = pygame.image.load('Sprites/banano.png')
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

# define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Generate matrix
WORLD = []
for i in range(rows):
    WORLD.append([])
    for j in range(columns):
        if i == 0 or i == rows - 1 or j == 0 or j == columns - 1:
            WORLD[i].append(99)
        elif i < 10:
            WORLD[i].append(1)
        else:
            WORLD[i].append(0)

# define game variables
tile_size = 50

# define colours
white = (255, 255, 255)
blue = (0, 0, 255)
red = (204, 0, 0)

# load images
bg_img = pygame.image.load('Sprites/background.png')


class Player:
    def __init__(self, x, y):
        self.counter = 0
        self.img_right = pygame.image.load("Sprites/fish.png")
        self.img_right = pygame.transform.scale(self.img_right, (80, 40))
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.image = self.img_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.vel_x = 0
        self.direction = 0
        self.in_air = False
        self.re_entry = [False, 0]
        self.re_entryX = 0
        self.last_pressed = 'None'
        self.water_to_air = False
        self.frames = 0

    def update(self):
        horizontal_speed = 0.2
        vertical_speed = 0.4
        if self.frames > 0:
            self.frames -= 1
        else:
            self.frames = 0

        if self.re_entry[1] > 0 or self.in_air:  # For x
            dx = self.re_entryX
        else:
            dx = self.vel_x

        dy = 0

        walk_cooldown = 5

        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.in_air and not self.re_entry[0]:
            self.vel_y -= vertical_speed

        if key[pygame.K_DOWN] and not self.in_air:
            self.vel_y += vertical_speed

        if key[pygame.K_LEFT] and not self.in_air:
            self.last_pressed = 'LEFT'
            dx -= horizontal_speed
            self.counter += 1
            self.direction = -1

        if key[pygame.K_RIGHT] and not self.in_air:
            self.last_pressed = 'RIGHT'
            dx += horizontal_speed
            self.counter += 1
            self.direction = 1

        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] or self.in_air:
            self.last_pressed = 'None'
            self.counter = 0

            if self.direction == 1:
                self.image = self.img_right
            if self.direction == -1:
                self.image = self.img_left

        if not key[pygame.K_UP] and not key[pygame.K_DOWN] and not self.in_air and not self.re_entry[0]:
            self.vel_y = 0

        if self.re_entry[1] > 0:
            self.re_entry[1] -= 1
        else:
            self.re_entry[0] = False
            self.re_entry[1] = 0

        # handle animation
        if self.counter > walk_cooldown:
            self.counter = 0

            if self.direction == 1:
                self.image = self.img_right
            if self.direction == -1:
                self.image = self.img_left

        # add gravity
        if self.in_air:
            self.vel_y += 0.8
            if self.vel_y > 8:
                self.vel_y = 8
        dy += self.vel_y

        # check for collision

        self.in_air = False
        self.water_to_air = False
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):  # Right now
                # pygame.draw.rect(screen, blue, tile[1], 2)
                if tile[2] == "air":
                    self.in_air = True
                elif tile[2] == "water":
                    pass

            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):  # X
                # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
                if tile[2] == "air":
                    dx = dx
                elif tile[2] == "water":
                    if self.in_air:
                        dx = self.vel_x
                        self.re_entryX = self.vel_x
                else:
                    dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):  # Y
                # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
                if tile[2] == "air":
                    if not self.in_air:
                        if self.frames == 0:
                            self.water_to_air = True
                            self.frames = 20

                elif tile[2] == "water":
                    if self.in_air:
                        self.re_entry = [True, 20]
                        if self.vel_y < 0:
                            pass
                        elif self.vel_y >= 0:
                            self.vel_y = 10
                    else:
                        self.vel_y += self.vel_y

                else:
                    if self.vel_y < 0:
                        dy = 0
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = 0
                        self.vel_y = 0

        # update player coordinates
        lastx = self.rect.x
        lasty = self.rect.y
        if self.rect.x + dx >= playable_width - 50:
            self.rect.x = playable_width - 50
        elif self.rect.x + dx <= 50:
            self.rect.x = 50
        else:
            self.rect.x += dx
        self.vel_x = dx

        if self.rect.y + dy >= 950:
            self.rect.y = 900
        elif self.rect.y + dy <= 50:
            self.rect.y = 100
        else:
            self.rect.y += dy
        self.vel_y = dy

        return lastx, lasty, self.in_air, [self.rect.x, self.rect.y], self.vel_x, self.vel_y, self.water_to_air

    def draw(self):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


# TODO: VECTORES, BANANO, BOTONES (gravedad, Hitbox)

class World:
    def __init__(self, data):
        self.tile_list = []

        # load images
        water_img = pygame.image.load('Sprites/water0.png')
        air_img = pygame.image.load('Sprites/air1.png')
        border_img = pygame.image.load('Sprites/border.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                img = None
                name = ""
                if tile == 0:  # Water
                    img = pygame.transform.scale(
                        water_img, (tile_size, tile_size))
                    name = "water"

                if tile == 1:  # Air
                    img = pygame.transform.scale(
                        air_img, (tile_size, tile_size))
                    name = "air"

                if tile == 99:  # Border
                    img = pygame.transform.scale(
                        border_img, (tile_size, tile_size))
                    name = "border"

                img_rect = img.get_rect()
                img_rect.x = col_count * tile_size
                img_rect.y = row_count * tile_size
                tile = (img, img_rect, name)
                self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 1) # Draw Hitbox


chipi = Player(700, 600)
world = World(WORLD)

# trail
border_img = pygame.image.load('Sprites/border.png')
trail_img = pygame.transform.scale(border_img, (10, 10))
trail = []

# Vector
x_vec_pos = pygame.image.load('Sprites/right.png')
x_vec_neg = pygame.image.load('Sprites/left.png')
y_vec_pos = pygame.image.load('Sprites/up.png')
y_vec_neg = pygame.image.load('Sprites/down.png')

XMax = 0
lastXmax = 0
YMax = 0
Xlinex = 0
Xliney = 0
orientation = -1
vxi = 0
vyi = 0


def draw_text(text, var, text_col, x, y, offset):
    t = font.render(text, True, text_col)
    var = font.render(var, True, text_col)
    screen.blit(var, (x + offset, y))
    screen.blit(t, (x, y))


text_pos = screen_width - 320
leave_trail = False

run = True
while run:
    clock.tick(fps)

    world.draw()
    x, y, air, actual, velx, vely, wta = chipi.update()

    if air:
        fps = 15
    else:
        fps = 30

    pygame.draw.rect(screen, [0, 0, 0], pygame.Rect(
        (screen_width - 300, 0), (1000, 1000)))
    draw_text("Vel x:", str(velx), white, text_pos, 100, 200)
    draw_text("Vel y:", str(vely), white, text_pos, 200, 200)
    draw_text("X:", str(actual[0]), white, text_pos, 300, 100)
    draw_text("Y:", str(actual[1]), white, text_pos, 400, 100)

    # print("wta", wta)

    if wta:
        trail = []
        vxi = abs(velx)
        vyi = abs(vely)
        print(vxi, vyi)
        print((vxi + vyi) / 2)

    if wta:
        vi = ((vxi ** 2 + vyi ** 2) ** (1 / 2))
        theta_i = math.atan(vyi / vxi) if velx != 0 else 0
        XMax = ((2 * (vi ** 2)) * (math.sin(theta_i)) * (math.cos(theta_i))) / 5
        flight_duration = (2*vi*math.sin(theta_i))/5
        print(flight_duration)
        orientation = 1 if velx >= 0 else -1
        if int(lastXmax) != int(XMax):
            Xlinex = actual[0]
        Xliney = actual[1]

        lastXmax = XMax
        YMax = ((vi ** 2) * ((math.sin(theta_i)) ** 2)) / 10

    factor = 7.3
    if orientation >= 0:
        pygame.draw.line(screen, red, (Xlinex, Xliney), (Xlinex + XMax * factor, Xliney), 3)
        pygame.draw.line(screen, red, (Xlinex + (XMax * factor) / 2, Xliney),
                         (Xlinex + (XMax * factor) / 2, Xliney + YMax * -7.5), 3)
    else:
        pygame.draw.line(screen, red, (Xlinex, Xliney), (Xlinex - XMax * 7.5, Xliney), 3)
        pygame.draw.line(screen, red, (Xlinex - (XMax * factor) / 2, Xliney),
                         (Xlinex - (XMax * factor) / 2, Xliney + YMax * -7.5), 3)

    # R Vector
    draw_text("R:", str((vely ** 2 + velx ** 2) ** (1 / 2)), white, text_pos, 500, 100)
    draw_text("Theta:", str(math.atan(vely / (velx + 0.1))), white, text_pos, 600, 200)
    draw_text("XMax:", str(XMax), white, text_pos, 700, 200)
    draw_text("YMax:", str(YMax), white, text_pos, 800, 200)

    op_factor = 0
    if air:
        img_rect = trail_img.get_rect()
        img_rect.x = x
        img_rect.y = y
        # trail_block = (trail_img, img_rect)
        # trail.append(trail_block)
        trail.append(pygame.Rect((x, y), (10, 10)))

        op_factor = 255 / len(trail)

    if op_factor == 0:
        opacity = 0
    else:
        opacity = 255 + op_factor
    for tr in trail:
        opacity -= op_factor
        # screen.blit(tr[0], tr[1])
        if air:
            pygame.draw.rect(screen, [222, 235, 242], pygame.Rect((x, y), (10, 10)))
        pygame.draw.rect(screen, [opacity, opacity, opacity], tr)

    ''' Always trail
    if air:
        img_rect = trail_img.get_rect()
        img_rect.x = x
        img_rect.y = y
        trail_block = (trail_img, img_rect)
        trail.append(trail_block)

        print(len(trail))

    for tr in trail:
        screen.blit(tr[0], tr[1])
    '''

    chipi.draw()

    x_offset = int(abs(velx))

    if velx >= 0:
        img_x = x_vec_pos
    else:
        x_offset = int(abs(velx)) + 10
        img_x = x_vec_neg

    y_offset = int(abs(vely))
    if vely >= 0:
        y_offset = int(abs(vely))
        img_y = y_vec_neg
    else:
        img_y = y_vec_pos

    # Vector x
    img_x = pygame.transform.scale(img_x, (int(abs(velx * 10)), 50))
    img_x_rect = img_x.get_rect()
    img_x_rect.x = actual[0] - 3 * x_offset if velx < 0 else actual[0] + 3 * x_offset
    img_x_rect.y = actual[1]

    # Vector y
    img_y = pygame.transform.scale(img_y, (50, int(abs(vely * 10))))
    img_y_rect = img_y.get_rect()
    img_y_rect.x = actual[0]
    img_y_rect.y = actual[1] - 3 * y_offset if vely < 0 else actual[1] + 3 * y_offset

    screen.blit(img_x, img_x_rect)  # Vector x
    screen.blit(img_y, img_y_rect)  # Vector y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

# XMAX =
# YMAX =
# TITA =
# DIBUJAR VECTOR RESULTANTE = sqrt(

import pygame
import random
pygame.init()

screen_width = 1200
screen_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(tile_textures)  # Zufällige Tile-Textur auswählen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_frames = []
        self.jump_frames = []
        self.running_right_frames = []
        self.running_left_frames = []
        self.current_frame_index = 0
        self.animation_speed = 10
        self.is_jumping = False
        self.is_running_right = False
        self.is_running_left = False

        for i in range(4):
            frame = pygame.image.load(f"Individual Sprites/adventurer-idle-2-0{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (200, 200))
            self.idle_frames.append(frame)

        for i in range(4):
            frame = pygame.image.load(f"Individual Sprites/adventurer-run-0{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (200, 200))
            self.running_right_frames.append(frame)

        for i in range(4):
            frame = pygame.image.load(f"Individual Sprites/adventurer-run-0{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (200, 200))
            frame = pygame.transform.flip(frame, True, False)
            self.running_left_frames.append(frame)

        for i in range(4):
            frame = pygame.image.load(f"Individual Sprites/adventurer-jump-0{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (200, 200))
            self.jump_frames.append(frame)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.width = 80
        self.rect.height = 190
        self.rect.x = 50
        self.rect.y = screen_height - self.rect.height
        self.vel_x = 0
        self.vel_y = 0
        self.jump_power = -19

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= screen_height and not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True

        elif keys[pygame.K_a]:
            self.vel_x = -5
            self.is_running_left = True

        elif keys[pygame.K_d]:
            self.vel_x = 5
            self.is_running_right = True

        else:
            self.vel_x = 0

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += 1

        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.is_jumping = False

        if not keys[pygame.K_d]:
            self.is_running_right = False

        if not keys[pygame.K_a]:
            self.is_running_left = False

        if self.is_jumping:
            self.animate(self.jump_frames)

        elif self.is_running_right:
            self.animate(self.running_right_frames)

        elif self.is_running_left:
            self.animate(self.running_left_frames)

        else:
            self.animate(self.idle_frames)

    def animate(self, frames):
        self.current_frame_index += 1
        if self.current_frame_index >= len(frames) * self.animation_speed:
            self.current_frame_index = 0

        frame_index = self.current_frame_index // self.animation_speed
        self.image = frames[frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.current_frame_index = 0
        self.running_frames = []
        self.animation_speed = 10

        for i in range(4):
            frame = pygame.image.load(f"demonTextures/big_demon_run_anim_f{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (100, 100))
            self.running_frames.append(frame)

        self.image = self.running_frames[0]
        self.rect = self.image.get_rect()
        self.rect.width = 30
        self.rect.height = 90
        self.rect.x = screen_width
        self.rect.y = screen_height - self.rect.height
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        self.animate(self.running_frames)

    def animate(self, frames):
        self.current_frame_index += 1
        if self.current_frame_index >= len(frames) * self.animation_speed:
            self.current_frame_index = 0

        frame_index = self.current_frame_index // self.animation_speed
        self.image = frames[frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def show_text(screen, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

tiles = pygame.sprite.Group()
tile_textures = []
for i in range(1, 9):
    texture = pygame.image.load(f"tiles/floor_{i}.png").convert_alpha()
    texture = pygame.transform.scale(texture, (100, 100))
    tile_textures.append(texture)

tile_width = 64
tile_height = 64

for x in range(0, screen_width, tile_width):
    for y in range(0, screen_height, tile_height):
        tile = Tile(x, y)
        tiles.add(tile)

player = Player()
all_sprites.add(player)

enemy_speed = 3
enemy_spawn_delay = 4000
last_enemy_spawn_time = pygame.time.get_ticks()

game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:

        all_sprites.update()

        if pygame.sprite.spritecollide(player, enemies, False):
            game_over = True

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_delay:
            last_enemy_spawn_time = current_time
            enemy = Enemy(enemy_speed)
            all_sprites.add(enemy)
            enemies.add(enemy)

        screen.fill(black)
        tiles.draw(screen)
        all_sprites.draw(screen)
    else:

        show_text(screen, "Game Over", 64, screen_width // 2, screen_height // 2 + 50)
        show_text(screen, "Drücke R zum Neustarten", 22, screen_width // 2, screen_height // 2 + 100)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            all_sprites.empty()
            enemies.empty()
            player = Player()
            all_sprites.add(player)
            enemy_speed = 3
            enemy_spawn_delay = 4000
            game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

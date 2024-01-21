from config import BULLET_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, FPS
import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("pygame")

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        speed = 5

        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= speed
        if keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += speed

    def create_bullet(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        return Bullet(self.rect.center, angle)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_center, angle):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(red)
        self.rect = self.image.get_rect(center=player_center)
        self.speed = BULLET_SPEED
        self.angle = angle

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

        if self.rect.x not in range(-200, WINDOW_WIDTH + 200) or self.rect.y not in range(-200, WINDOW_HEIGHT + 200):
            self.kill()


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(green)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()


bullet_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
cursor = Cursor()
player = Player()
all_sprites.add(player, cursor)

# Hide the normal cursor
pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())

    screen.fill((0, 0, 0))

    bullet_group.draw(screen)
    bullet_group.update()

    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()

    pygame.time.Clock().tick(FPS)

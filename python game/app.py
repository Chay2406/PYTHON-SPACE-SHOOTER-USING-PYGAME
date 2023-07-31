import pygame
import sys
import random

pygame.init()

# Constants
window_width, window_height = 800, 600
BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    ("X", (0, 0, 255)),  # Blue
    ("O", (0, 128, 0)),  # Green
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))  # White rectangle as a placeholder
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_height - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width:
            self.rect.right = window_width

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red rectangle as a placeholder
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > window_height:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, window_width)

def show_start_screen(screen):
    font = pygame.font.Font(None, 36)
    title_text = font.render("Space Shooter", True, (255, 255, 255))
    start_text = font.render("Press SPACE to start", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    start_rect = start_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.flip()

def game_over(screen):
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemy_group = pygame.sprite.Group()
    for _ in range(5):  # Add 5 initial enemy ships
        enemy = Enemy(random.randint(0, window_width), random.randint(0, window_height))
        enemy_group.add(enemy)
        all_sprites.add(enemy)

    show_start_screen(screen)

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_game = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        all_sprites.update()
        enemy_group.update()

        # Check for collisions
        if pygame.sprite.spritecollide(player, enemy_group, dokill=True):
            game_over(screen)
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()

        # Draw
        screen.fill((0, 0, 0))  # Fill the screen with black
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
 
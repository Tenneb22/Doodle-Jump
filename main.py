import pygame
import random
import time
pygame.font.init()

# Fenstergröße
WIDTH = 720
HEIGHT = 1600

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Spielergröße und Geschwindigkeit
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Plattformgröße und Geschwindigkeit
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 3

# Zeitverzögerung zwischen dem Spawnen von Plattformen (in Millisekunden)
PLATFORM_SPAWN_DELAY = 2000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")
FONT = pygame.font.SysFont("comicsans", 30)

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.y = -HEIGHT
        self.vel_y = 0
        self.on_platform = False  # Variable zum Überprüfen, ob der Spieler auf einer Plattform steht

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        self.rect.y += self.vel_y
        self.vel_y = 5  # Schwerkraft

        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH

        # Überprüfe Kollision mit Plattformen
        platform_collision = pygame.sprite.spritecollide(self, platforms, False)
        if platform_collision:
            for platform in platform_collision:
                if self.vel_y > 0 and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = -500  # Nach oben springen
                    platform.kill()  # Entferne die Plattform

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += PLATFORM_SPEED

        if self.rect.top > HEIGHT:
          all_sprites.remove(self)

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

last_platform_spawn_time = time.time()  # Zeitpunkt des letzten Plattform-Spawns
platform_spawn_delay = 1  # Verzögerung in Sekunden zwischen dem Spawnen von Plattformen

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Überprüfe, ob genug Zeit vergangen ist, um eine neue Plattform zu spawnen
    current_time = time.time()
    if current_time - last_platform_spawn_time > platform_spawn_delay:
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = -PLATFORM_HEIGHT
        platform = Platform(x, y)
        all_sprites.add(platform)
        platforms.add(platform)
        last_platform_spawn_time = current_time

    for platform in platforms.copy():  # Kopie der Plattformen, um während des Iterierens zu löschen
        if platform.rect.bottom > HEIGHT:
            platform.kill()
    
    if player.rect.bottom > HEIGHT:
        player.kill()
        lost_text = FONT.render("You Lost!", 1, "white")
        screen.fill(BLACK)
        screen.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
        pygame.display.update()
        print("Player lost")
        pygame.time.delay(4000)
        print("Leaving the game.")
        break

    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

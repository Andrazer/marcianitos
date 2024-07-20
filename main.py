import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configurar la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Juego de Marcianitos')

# Configurar reloj
clock = pygame.time.Clock()
FPS = 60

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/explosion.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño según sea necesario
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.lifetime = 0  # Para controlar el tiempo de vida de la explosión

    def update(self):
        self.lifetime += 1
        if self.lifetime > 10:  # Ajusta el número según la duración deseada
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load('assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < pygame.display.get_surface().get_width():
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load('assets/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= pygame.display.get_surface().get_width() or self.rect.left <= 0:
            self.speed *= -1
            self.rect.y += 10

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def check_collisions(bullets, enemies, explosions):
    for bullet in bullets:
        for enemy in enemies:
            if pygame.sprite.collide_rect(bullet, enemy):
                bullet.kill()  # Elimina la bala
                enemy.kill()  # Elimina el enemigo

                # Crear explosión en la posición del enemigo
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                all_sprites.add(explosion)
                explosions.add(explosion)

def check_win_condition(enemies):
    return len(enemies) == 0

def display_message(text, color, position):
    font = pygame.font.SysFont(None, 55)
    message = font.render(text, True, color)
    screen.blit(message, position)

def reset_game():
    global player, enemies, bullets, explosions, all_sprites, game_won

    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    explosions.empty()

    # Crear jugador
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    all_sprites.add(player)

    # Crear enemigos
    for x in range(10):
        for y in range(5):
            enemy = Enemy(x * 60, y * 40)
            all_sprites.add(enemy)
            enemies.add(enemy)

    game_won = False

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()  # Nuevo grupo para explosiones

# Crear jugador
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
all_sprites.add(player)

# Crear enemigos
for x in range(10):
    for y in range(5):
        enemy = Enemy(x * 60, y * 40)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Bucle principal del juego
running = True
game_won = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if event.key == pygame.K_r and game_won:
                reset_game()
    
    if not game_won:
        # Actualizar todos los sprites
        all_sprites.update()
        explosions.update()  # Actualizar explosiones

        # Comprobar colisiones
        check_collisions(bullets, enemies, explosions)

        # Comprobar si el juego ha ganado
        if check_win_condition(enemies):
            game_won = True
    
    # Dibujar todo en la pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    if game_won:
        display_message("¡Felicidades! Ganaste", WHITE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        display_message("Presiona R para reiniciar", WHITE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 60))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Mantener la velocidad del juego
    clock.tick(FPS)

pygame.quit()
sys.exit()

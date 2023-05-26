import pygame
import random

# 初期化
pygame.init()

# ゲームウィンドウの作成
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# カラー定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# プレイヤーシップの作成
player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5

player = pygame.Rect(player_x, player_y, player_width, player_height)

# スペースインベーダーの作成
invader_width = 40
invader_height = 40
invader_speed = 2
invader_direction = 1

invaders = []
for row in range(5):
    for col in range(10):
        invader_x = col * (invader_width + 10) + 50
        invader_y = row * (invader_height + 10) + 50
        invader = pygame.Rect(invader_x, invader_y, invader_width, invader_height)
        invaders.append(invader)

# 弾の作成
bullet_width = 5
bullet_height = 10
bullet_speed = 5

bullet = None
bullet_state = "ready"  # "ready" or "fired"

# 敵の攻撃
enemy_bullet_width = 3
enemy_bullet_height = 10
enemy_bullet_speed = 3

enemy_bullets = []

# スコア
score = 0
font = pygame.font.Font(None, 36)

# ゲームオーバーメッセージ
game_over_font = pygame.font.Font(None, 72)

# ゲームループ
running = True
clock = pygame.time.Clock()

def draw_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, game_over_rect)

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_state = "fired"
                bullet_x = player.x + player.width // 2 - bullet_width // 2
                bullet_y = player.y
                bullet = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < width - player_width:
        player.x += player_speed
    
    if bullet_state == "fired":
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullet_state = "ready"
    
    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += enemy_bullet_speed
        if enemy_bullet.colliderect(player):
            running = False
        if enemy_bullet.y > height:
            enemy_bullets.remove(enemy_bullet)
    
    for invader in invaders:
        invader.x += invader_speed * invader_direction
        if invader.x < 0 or invader.x > width - invader_width:
            invader_direction *= -1
            for invader in invaders:
                invader.y += 20
        
        if invader.colliderect(player):
            running = False
        
        if random.randint(0, 1000) < 5 and len(enemy_bullets) < 5:
            enemy_bullet_x = invader.x + invader.width // 2 - enemy_bullet_width // 2
            enemy_bullet_y = invader.y + invader.height
            enemy_bullet = pygame.Rect(enemy_bullet_x, enemy_bullet_y, enemy_bullet_width, enemy_bullet_height)
            enemy_bullets.append(enemy_bullet)
    
    if bullet_state == "fired":
        for invader in invaders:
            if bullet.colliderect(invader):
                invaders.remove(invader)
                bullet_state = "ready"
                score += 10
    
    screen.fill(BLACK)
    
    pygame.draw.rect(screen, WHITE, player)
    
    for invader in invaders:
        pygame.draw.rect(screen, WHITE, invader)
    
    if bullet_state == "fired":
        pygame.draw.rect(screen, WHITE, bullet)
    
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, WHITE, enemy_bullet)
    
    draw_score()
    
    if len(invaders) == 0:
        draw_game_over()
    
    pygame.display.update()

# 終了
pygame.quit()
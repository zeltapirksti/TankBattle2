import pygame
import os

pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("Tank Battle")  # Setting the window caption

WIDTH, HEIGHT = 900, 500;  # Width and Height of my display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Setting the game display

WHITE = (255, 255, 255)  # Setting the display color (RGB)
GRAY = (80, 80, 80)  # Setting the border color (RGB)
BLACK = (0, 0, 0)  # Setting the black color (RGB)
GREEN = (0, 255, 0)  # Setting the green color (RGB)
DARK_BLUE = (0, 0, 128)  # Setting the dark blue color (RGB)

BORDER = pygame.Rect((WIDTH // 2 - 5), 0, 2, HEIGHT)  # X, Y, WIDTH, HEIGHT

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/tank-hit.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/tank-fire.wav')

HEALTH_FONT = pygame.font.SysFont('modern warfare', 30)
WINNER_FONT = pygame.font.SysFont('modern warfare', 50)

FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 3
TANK_WDT, TANK_HGT = 100, 100

BLACK_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

BLACK_TANK_IMAGE = pygame.image.load(os.path.join('Assets/black-tank.png'))
BLACK_TANK = pygame.transform.rotate(pygame.transform.scale(BLACK_TANK_IMAGE, (TANK_WDT, TANK_HGT)), 0)

GREEN_TANK_IMAGE = pygame.image.load(os.path.join('Assets/green-tank.png'))
GREEN_TANK = pygame.transform.rotate(pygame.transform.scale(GREEN_TANK_IMAGE, (TANK_WDT, TANK_HGT)), 90)

DESERT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'desert.jpeg')), (WIDTH, HEIGHT))


def draw_window(green, black, green_bullets, black_bullets, green_health, black_health):
    WIN.blit(DESERT_IMAGE, (0, 0))
    pygame.draw.rect(WIN, GRAY, BORDER)

    green_health_text = HEALTH_FONT.render('Health: ' + str(green_health), 1, DARK_BLUE)
    black_health_text = HEALTH_FONT.render('Health: ' + str(black_health), 1, DARK_BLUE)
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))
    WIN.blit(black_health_text, (10, 10))

    WIN.blit(BLACK_TANK, (black.x, black.y))
    WIN.blit(GREEN_TANK, (green.x, green.y))

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    for bullet in black_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    pygame.display.update()


def black_handle_movement(keys_pressed, black):
    # Black tank is placed on the left-handle side of the screen
    if keys_pressed[pygame.K_a] and black.x - VEL > 0:  # LEFT KEY
        black.x -= VEL
    if keys_pressed[pygame.K_d] and black.x + VEL + black.width < BORDER.x:  # RIGHT KEY
        black.x += VEL
    if keys_pressed[pygame.K_w] and black.y - VEL > 0:  # UP KEY
        black.y -= VEL
    if keys_pressed[pygame.K_s] and black.y + VEL + black.height < HEIGHT - 15:  # DOWN KEY
        black.y += VEL


def green_handle_movement(keys_pressed, green):
    # Green tank is placed on the right-handle side of the screen
    if keys_pressed[pygame.K_LEFT] and green.x - VEL > BORDER.x + 25:  # LEFT KEY
        green.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and green.x + VEL + green.width - 10 < WIDTH:  # RIGHT KEY
        green.x += VEL
    if keys_pressed[pygame.K_UP] and green.y - VEL > 0:  # UP KEY
        green.y -= VEL
    if keys_pressed[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT - 15:  # DOWN KEY
        green.y += VEL


def handle_bullets(black_bullets, green_bullets, black, green):
    for bullet in black_bullets:
        bullet.x += BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            black_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            black_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VEL
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)


def draw_winner(text, color):
    winner_msg = WINNER_FONT.render(text, 1, color)
    WIN.blit(winner_msg, (WIDTH // 2 - winner_msg.get_width() // 2, HEIGHT // 2 - winner_msg.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    green = pygame.Rect(700, 300, TANK_WDT, TANK_HGT)  # Rectangle that catch the green_tank position
    black = pygame.Rect(100, 300, TANK_WDT, TANK_HGT)  # Rectangle that catch the black_tank position

    green_bullets = []
    black_bullets = []

    green_health = 10
    black_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(black_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(black.x + black.width, black.y + black.height // 2 - 2, 10, 5)
                    black_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height // 2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BLACK_HIT:
                black_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if green_health <= 0:
            winner_text = 'Black Tank Wins!'
            color = BLACK
        if black_health <= 0:
            winner_text = 'Green Tank Wins!'
            color = GREEN

        if winner_text != '':
            draw_winner(winner_text, color)
            break

        keys_pressed = pygame.key.get_pressed()
        black_handle_movement(keys_pressed, black)  # BLACK TANK MOVEMENTS
        green_handle_movement(keys_pressed, green)  # GREEN TANK MOVEMENTS

        handle_bullets(black_bullets, green_bullets, black, green)
        draw_window(green, black, green_bullets, black_bullets, green_health, black_health)

    main()


# The program is just executed if this file be run
if __name__ == "__main__":
    main()
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

#  set up
fps = 30

black_blue = (0, 0, 50)
white = (255, 240, 220)

screen_width = 800
screen_height = 600

paddle_width = 5
paddle_height = 90

line_start = (int(screen_width/2), 0)
line_end = (int(screen_width/2), screen_height)

ball_radius = 10
ball_init_x = int(screen_width / 2)
ball_init_y = int(screen_height / 2)
ball_velocity_x = 10
ball_velocity_y = 10

score_1 = 0
score_2 = 0
font_size = 40
font = pygame.font.SysFont('comicsansms', font_size)  # create font object
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')


#  players
def p1(rect1):
    pygame.draw.rect(game_display, white, rect1)


def p2(rect2):
    pygame.draw.rect(game_display, white, rect2)


#  ball handlers
ball = pygame.Rect(ball_init_x - ball_radius, ball_init_y - ball_radius, ball_radius * 2, ball_radius * 2)


def score(p1, p2):
    message = str(p1) + ' ' + str(p2)
    screen_message(message, white, -40)


def screen_message(text, color, y_displace=0):
    screen_text = font.render(text, True, color)  # creating the idea of the font
    text_rect = screen_text.get_rect()
    text_rect.center = [screen_width/2, screen_height/2 + y_displace]
    game_display.blit(screen_text, text_rect)


def restart():
    global ball_velocity_x, ball_velocity_y, score_1, score_2
    score_1 = 0
    score_2 = 0
    ball.center = (int(screen_width / 2), int(screen_height / 2))
    ball_velocity_x = 10
    ball_velocity_y = 10
    ball_velocity_x *= random.choice((-1, 1))
    ball_velocity_y *= random.choice((-1, 1))


def ball_anime(rect1, rect2):
    global ball_velocity_x, ball_velocity_y, ball_init_x, ball_init_y, score_1, score_2
    ball.x += ball_velocity_x
    ball.y += ball_velocity_y
    if ball.left < -paddle_width + 1 or ball.right > screen_width + paddle_width:
        restart()
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_velocity_y = ball_velocity_y * -1
    if ball.colliderect(rect1) or ball.colliderect(rect2):
        ball_velocity_x = ball_velocity_x * -1
        if ball_velocity_x < 20:
            ball_velocity_x = ball_velocity_x * 1.05
        if ball_velocity_y < 20:
            ball_velocity_y = ball_velocity_y * 1.05
        if ball_velocity_x >= 20:
            ball_velocity_x *= 1
        if ball_velocity_y >= 20:
            ball_velocity_y *= 1
    if ball.colliderect(rect1):
        score_1 += 1
    if ball.colliderect(rect2):
        score_2 += 1
    pygame.draw.ellipse(game_display, white, ball)


def game_loop():
    game_over = False
    global ball_init_x, ball_init_y, ball_velocity_x, ball_velocity_y

    paddle_speed_1 = 0
    paddle_speed_2 = 0

    p1_position = [0, int(screen_height / 2 - paddle_height / 2)]
    p2_position = [int(screen_width - paddle_width), int(screen_height / 2 - paddle_height / 2)]

    while not game_over:

        player_1 = pygame.Rect(p1_position[0], p1_position[1], paddle_width, paddle_height)
        player_2 = pygame.Rect(p2_position[0], p2_position[1], paddle_width, paddle_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_speed_1 = -15
                if event.key == pygame.K_s:
                    paddle_speed_1 = 15
                if event.key == pygame.K_UP:
                    paddle_speed_2 = -15
                if event.key == pygame.K_DOWN:
                    paddle_speed_2 = 15

            if event.type == pygame.KEYUP:
                paddle_speed_1 = 0
                paddle_speed_2 = 0


        #  moving objects
        p1_position[1] += paddle_speed_1
        p2_position[1] += paddle_speed_2

        if p1_position[1] <= 0:
            p1_position[1] = 0
        if p1_position[1] >= (screen_height - paddle_height):
            p1_position[1] = (screen_height - paddle_height)

        if p2_position[1] <= 0:
            p2_position[1] = 0
        if p2_position[1] >= (screen_height - paddle_height):
            p2_position[1] = (screen_height - paddle_height)

        #  draw stuff
        game_display.fill(black_blue)
        pygame.draw.aaline(game_display, white, line_start, line_end)
        ball_anime(player_1, player_2)
        p1(player_1)
        p2(player_2)
        score(score_1, score_2)
        pygame.display.update()
        clock.tick(fps)


game_loop()

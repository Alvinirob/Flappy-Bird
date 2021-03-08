import pygame
import sys
import random


def draw_floor():
    screen.blit(floor, (floor_pos, 750))
    screen.blit(floor, (floor_pos + 500, 750))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_sur.get_rect(midtop=(600, random_pipe_pos))
    top_pipe = pipe_sur.get_rect(midbottom=(600, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 900:
            screen.blit(pipe_sur, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_sur, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):  # collision with pipe
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 710:  # collision with top-bottom
        return False
    return True


def score_display(game_state):
    if game_state == 'Main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'Game_over':

        score_surface = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score : {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 600))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()  # Main section 1/4 initialize all function

# Main section 2/4 start making display surface
screen = pygame.display.set_mode((500, 900))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# background image load
background = pygame.image.load('File/uni_back.png').convert()
# background = pygame.transform.scale2x(background)

# floor image load
floor = pygame.image.load('File/uni_floor.png').convert()
# floor = pygame.transform.scale2x(floor)
floor_pos = 0

# bird image load
bird = pygame.image.load('File/uni_bird.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 450))  # create a rectangular outside the bird

# pipe image load
pipe_sur = pygame.image.load('File/uni_pipe.png')
# pipe_sur = pygame.transform.scale2x(pipe_sur)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 500, 600]

# game over surface load
game_over_surface = pygame.image.load('File/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(250, 350))


# Main section 3/4 start game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # for movement of bird
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 450)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        # background image in loop

    screen.blit(background, (0, 0))
    if game_active:
        # bird image in loop
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        # check collision
        game_active = check_collision(pipe_list)
        # pipe image in loop
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        # score display in loop
        score += 0.01
        score_display('Main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('Game_over')
    # floor image in loop
    floor_pos -= 5
    draw_floor()
    if floor_pos <= -500:
        floor_pos = 0

    pygame.display.update()
    clock.tick(100)

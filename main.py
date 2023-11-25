from random import randint
import pygame as pg
pg.init()
pg.font.init()

FPS = 60

WHITE = (255, 255, 255)

END_GAME_FONT = pg.font.SysFont('cascadia code', 100)
SCORE_FONT = pg.font.SysFont('cascadia coid', 40)

SPAWN_POINTS = {
    'first': (20, 10),
    'second': (220, 10),
    'third': (440, 10),
    'fourth': (660, 10)
}

SAFE_AREA = 880
SAFE_AREA_MOVE = 220
WIDTH = 900
HEIGHT = 700
PLAYER_DIMENSIONS = (100, 100)
BACKGROUND_DIMENSIONS = (900, 700)
OBSTACLE_DIMENSIONS = (WIDTH//4, 80)

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Cubethon')

PLAYER_IMAGE = pg.image.load('Player.png')
PLAYER = pg.transform.scale(PLAYER_IMAGE, PLAYER_DIMENSIONS)
PLAYER_POS = [60, HEIGHT - 100]

BACKGROUND_IMAGE = pg.image.load('BackGround.png')
BACKGROUND = pg.transform.scale(BACKGROUND_IMAGE, BACKGROUND_DIMENSIONS)

OBSTACLE_IMAGE = pg.image.load('Obstacle.png')
OBSTACLE = pg.transform.scale(OBSTACLE_IMAGE, OBSTACLE_DIMENSIONS)


def main():

    obstacle_vel = 7
    score = 0

    clock = pg.time.Clock()
    run = True

    obs1 = pg.Rect(SPAWN_POINTS['first'], OBSTACLE_DIMENSIONS)
    obs2 = pg.Rect(SPAWN_POINTS['second'], OBSTACLE_DIMENSIONS)
    obs3 = pg.Rect(SPAWN_POINTS['third'], OBSTACLE_DIMENSIONS)

    while run:
        player = pg.Rect(PLAYER_POS, PLAYER_DIMENSIONS)
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if PLAYER_POS[0] != 60:
                    if event.key == pg.K_a or event.key == pg.K_LEFT:
                        PLAYER_POS[0] -= 220
                if PLAYER_POS[0] != 720:
                    if event.key == pg.K_d or event.key == pg.K_RIGHT:
                        PLAYER_POS[0] += 220

        if obs1.y >= HEIGHT - obs1.height:
            spawn = spawn_obstacles(obs1, obs2, obs3, score, obstacle_vel)
            score = spawn[1]
            obstacle_vel = spawn[2]

        if detect_collision(player, [obs1, obs2, obs3]):
            end_game()
            pg.time.delay(5000)
            run = False

        draw_window(obs1, obs2, obs3)
        move_obstacles([obs1, obs2, obs3], obstacle_vel)
        show_score(score)
        pg.display.update()

    restart = False
    while not restart:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and (event.key == pg.K_RETURN or event.key == pg.K_SPACE):
                main()  # Restart the game
            if event.type == pg.QUIT:
                restart = True
                pg.quit()
        if restart:
            break    

    main()


def add_score_vel(obstacle, score, vel):
    if obstacle.y >= HEIGHT - obstacle.height - 5:
        score += 1
        print(f'Score: {score}')
        if score != 0 and score % 10 == 0:
            vel += 2
    return [score, vel]


def spawn_obstacles(obs1, obs2, obs3, score, vel):

    if obs1.y >= HEIGHT - obs1.height:
        score += 1
        print(f'Score: {score}')
        if score != 0 and score % 10 == 0:
            vel += 2

    spawn_positions = [SPAWN_POINTS['first'], SPAWN_POINTS['second'],
                       SPAWN_POINTS['third'], SPAWN_POINTS['fourth']]
    scrambled = []
    while len(scrambled) < len(spawn_positions) - 1:
        index = randint(0, len(spawn_positions) - 1)
        curr_pos = spawn_positions[index]
        if curr_pos in scrambled:
            while curr_pos in scrambled:
                index = randint(0, len(spawn_positions) - 1)
                curr_pos = spawn_positions[index]
        else:
            scrambled.append(curr_pos)
    obs1.x = scrambled[0][0]
    obs1.y = scrambled[0][1]
    obs2.x = scrambled[1][0]
    obs2.y = scrambled[1][1]
    obs3.x = scrambled[2][0]
    obs3.y = scrambled[2][1]
    return [scrambled, score, vel]


def show_score(score):
    score_text = SCORE_FONT.render(f'Score: {score}', 1, WHITE)
    WIN.blit(score_text, (20, 20))


def end_game():
    you_lost_text = END_GAME_FONT.render('You lost!', 1, WHITE)
    WIN.blit(you_lost_text, (WIDTH/2 - you_lost_text.get_width() /
                             2, HEIGHT/2 - you_lost_text.get_height()/2))
    pg.display.update()


def detect_collision(player, obss):
    for obstacle in obss:
        if player.colliderect(obstacle):
            return True
    return False


def move_obstacles(obss, vel):
    spawn = []
    for obstacle in obss:
        if obstacle.y >= HEIGHT - obstacle.height:
            spawn = spawn_obstacles()
            for x in spawn:
                obstacle.y = x[1]
        else:
            obstacle.y += vel
    return spawn


def draw_window(obs1, obs2, obs3):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(PLAYER, (PLAYER_POS[0], PLAYER_POS[1]))
    WIN.blit(OBSTACLE, (obs1.x, obs1.y))
    WIN.blit(OBSTACLE, (obs2.x, obs2.y))
    WIN.blit(OBSTACLE, (obs3.x, obs3.y))


if __name__ == '__main__':
    main()

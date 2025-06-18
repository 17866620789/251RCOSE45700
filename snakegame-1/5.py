import pygame, sys, time, random, os



food_img = pygame.image.load('food.webp')
food_img = pygame.transform.scale(food_img, (10, 10))
background_img = pygame.image.load('background.png')
# head_img = pygame.image.load('head.png')
# head_img = pygame.transform.scale(head_img, (10, 10))  # 缩放为蛇格大小


pygame.init()
frame_size_x, frame_size_y = 600,600
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

pygame.display.set_caption('Snake Game')

# 颜色
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

fps_controller = pygame.time.Clock()
difficulty = 10  # 默认

score = 0

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score: {score}', True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

def game_over():
    global score
    font = pygame.font.SysFont('marker felt', 60)
    msg_surface = font.render('GAME OVER', True, red)
    msg_rect = msg_surface.get_rect(center=(frame_size_x/2, frame_size_y/3))
    game_window.blit(background_img, (0, 0))
    game_window.blit(msg_surface, msg_rect)
    show_score(0, black, 'marker felt', 30)
    pygame.display.flip()
    time.sleep(2)
    main_menu()

def run_game():
    global score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, frame_size_x//10) * 10, random.randrange(1, frame_size_y//10) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, ord('w')]: change_to = 'UP'
                elif event.key in [pygame.K_DOWN, ord('s')]: change_to = 'DOWN'
                elif event.key in [pygame.K_LEFT, ord('a')]: change_to = 'LEFT'
                elif event.key in [pygame.K_RIGHT, ord('d')]: change_to = 'RIGHT'
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

        if direction == 'UP': snake_pos[1] -= 10
        elif direction == 'DOWN': snake_pos[1] += 10
        elif direction == 'LEFT': snake_pos[0] -= 10
        elif direction == 'RIGHT': snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, frame_size_x//10) * 10, random.randrange(1, frame_size_y//10) * 10]
        food_spawn = True

        game_window.blit(background_img, (0, 0))
        for block in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(block[0], block[1], 10, 10))
        game_window.blit(food_img, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or \
           snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            game_over()
        for part in snake_body[1:]:
            if snake_pos == part:
                game_over()

        show_score(1, white, 'marker felt', 20)
        pygame.display.update()
        fps_controller.tick(difficulty)

def select_difficulty():
    global difficulty
    options = [("Easy", 10), ("Medium", 25), ("Hard", 40), ("Impossible", 80)]
    selected = 0
    font = pygame.font.SysFont('marker felt', 36)
    title_font = pygame.font.SysFont('marker felt', 48)

    while True:
        game_window.blit(background_img, (0, 0))
        title = title_font.render("Select Difficulty", True, black)
        title_rect = title.get_rect(center=(frame_size_x / 2, 80))
        game_window.blit(title, title_rect)

        for idx, (name, _) in enumerate(options):
            color = black if idx == selected else white
            option_text = font.render(name, True, color)
            option_rect = option_text.get_rect(center=(frame_size_x / 2, 160 + idx * 50))
            game_window.blit(option_text, option_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0: selected -= 1
                elif event.key == pygame.K_DOWN and selected < len(options) - 1: selected += 1
                elif event.key == pygame.K_RETURN:
                    difficulty = options[selected][1]
                    return

def main_menu():
    font = pygame.font.SysFont('marker felt', 36)
    title_font = pygame.font.SysFont('marker felt', 60)
    options = ["Start Game", ]
    selected = 0

    while True:
        game_window.blit(background_img, (0, 0))
        title = title_font.render("Snake Game", True, black)
        title_rect = title.get_rect(center=(frame_size_x / 2, 80))
        game_window.blit(title, title_rect)

        for i, option in enumerate(options):
            color = black if i == selected else white
            text = font.render(option, True, color)
            rect = text.get_rect(center=(frame_size_x / 2, 180 + i * 60))
            game_window.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0: selected -= 1
                elif event.key == pygame.K_DOWN and selected < len(options) - 1: selected += 1
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        select_difficulty()
                        run_game()
                    elif selected == 1:
                        pygame.quit(); sys.exit()

if __name__ == '__main__':
    main_menu()

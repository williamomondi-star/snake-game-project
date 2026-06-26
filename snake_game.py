import pygame
import random
import sys

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH   
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT  
FPS_START = 8
HIGH_SCORE_FILE = "high_score.txt"

BLACK = (15, 15, 15)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 140, 0)
RED = (220, 50, 50)
GOLD = (255, 200, 0)
WHITE = (255, 255, 255)
GREY = (40, 40, 40)

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake - CNS 1102 Group Project")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    return screen, clock, font

snake_body = [(15, 10)]   # starts as just the head in the middle

def random_food_position(snake_body):
    while True:
        position = (random.randint(0, GRID_WIDTH - 1),
                    random.randint(0, GRID_HEIGHT - 1))
        if position not in snake_body:
            return position
        
def draw_cell(screen, position, color):
    rect = pygame.Rect(
        position[0] * CELL_SIZE,   # x in pixels
        position[1] * CELL_SIZE,   # y in pixels
        CELL_SIZE,                  # width
        CELL_SIZE                   # height
    )
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)  # thin black border

def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GREY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GREY, (0, y), (SCREEN_WIDTH, y))

def draw_hud(screen, font, score, high_score):
    text = font.render(f"Score: {score}   High Score: {high_score}", True, WHITE)
    screen.blit(text, (10, 5))

def move_snake(snake_body, direction):
    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    return [new_head] + snake_body[:-1]  # add new head, drop tail

def grow_snake(snake_body, direction):
    head_x, head_y = snake_body[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    return [new_head] + snake_body  # add new head, keep tail

def check_wall_collision(position):
    x, y = position
    return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

def check_self_collision(snake_body):
    head = snake_body[0]
    return head in snake_body[1:]

def handle_input(direction):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
    return direction

def run_round(screen, clock, font, high_score):
    # Setup
    snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food_position = random_food_position(snake_body)
    score = 0
    speed = FPS_START

    while True:
        # 1. Handle input
        direction = handle_input(direction)

        # 2. Calculate next head position
        head_x, head_y = snake_body[0]
        dx, dy = direction
        next_head = (head_x + dx, head_y + dy)

        # 3. Did we eat the food?
        if next_head == food_position:
            snake_body = grow_snake(snake_body, direction)
            food_position = random_food_position(snake_body)
            score += 1
            if score % 5 == 0:       # BONUS FEATURE: speed up every 5 points
                speed += 1
        else:
            snake_body = move_snake(snake_body, direction)

        # 4. Check for death
        if check_wall_collision(snake_body[0]) or check_self_collision(snake_body):
            return score             # round is over, return final score

        # 5. Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        for index, segment in enumerate(snake_body):
            color = DARK_GREEN if index == 0 else GREEN   # head is darker
            draw_cell(screen, segment, color)
        draw_cell(screen, food_position, GOLD)
        draw_hud(screen, font, score, high_score)

        # 6. Push the frame to the screen and wait
        pygame.display.flip()
        clock.tick(speed)
    
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def show_game_over(screen, font, score, high_score):
    screen.fill(BLACK)
    line1 = font.render("GAME OVER - Press R to Restart or Q to Quit", True, RED)
    line2 = font.render(f"Final Score: {score}   High Score: {high_score}", True, WHITE)
    screen.blit(line1, (SCREEN_WIDTH//2 - line1.get_width()//2, SCREEN_HEIGHT//2 - 20))
    screen.blit(line2, (SCREEN_WIDTH//2 - line2.get_width()//2, SCREEN_HEIGHT//2 + 20))
    pygame.display.flip()

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return      # restart
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()           # quit

def main():
    screen, clock, font = init_game()
    high_score = load_high_score()

    while True:                            # outer loop = multiple rounds
        score = run_round(screen, clock, font, high_score)
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        show_game_over(screen, font, score, high_score)
        wait_for_restart()

if __name__ == "__main__":
    main()
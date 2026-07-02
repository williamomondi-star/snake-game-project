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

def show loading_screen(screen, clock, font):
        """Colorful animated loading screen shown once before the game starts."""
        screen.fill(BLACK)
        Loading_text = font.render("Loading...", True, WHITE)
        screen.blit(Loading_text, (SCREEN_WIDTH//2 - Loading_text.get_width()//2, SCREEN_HEIGHT //2 - 20))
        pygame.display.flip()
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]
        for i in range(6):
           pygame.draw.rect(screen, colors[i], (SCREEN_WIDTH//2 - 150 + i*50, SCREEN_HEIGHT//2 + 20, 40, 40))
           Pygame.disply.flip()
  # --- Animated rainbow title ---
  title_text = font.render("SNAKE GAME", True, WHITE)
  for i in range(6):
      color = colors[i]
      title_surface = font.render("SNAKE GAME", True, color)
      screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, SCREEN_HEIGHT//2 - 80))
      pygame.display.flip()
        
def run_round(screen, clock, font, high_score):
    # Setup
    snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food_position = random_food_position(snake_body) 
    food_shape =  random.choice(SHAPES) 
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
            food_shape = random.choice(SHAPES) # Change food shape after eating
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
        draw_cell(screen, food_position,  food_ shape,  YELLOW) 
        draw_hud(screen, font, score, high_score)
        # 6. Push the frame to the screen and wait
        while pygame.time.get_ticks() - start_time < duration_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS_START)
    
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

def main ():
    screen, clock, font = init_game()
    show_loading_screen(screen, clock, font)
    high_score = load_high_score()

    while True:                             # outer loop = multiple rounds
        score= run_round(screen, clock, font, high_score)
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            show_game_over(screen, font, score, high_score)
            wait_for_restart()

if __name__ == "__main__":
    main()
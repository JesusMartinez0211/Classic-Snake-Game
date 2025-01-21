import pygame, sys, time, random

speed = 15

# Window sizes
frame_size_x = 720
frame_size_y = 480

check_errors = pygame.init()

if(check_errors[1]>0):
    print("Error " + check_errors[1])
else:
    print("Game Successfully Initialized")

# Initialise game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
snake_color = pygame.Color(50, 205, 50) 
snake_head_color = pygame.Color(34, 139, 34)  
background_color = pygame.Color(0, 0, 0)  
line_color = pygame.Color(0, 255, 255)  

fps_controller = pygame.time.Clock()
square_size = 30

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("arcade.mp3") 
pygame.mixer.music.play(-1, 0.0)  

def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True
    score = 0

init_vars()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    
    game_window.blit(score_surface, score_rect)

def game_over():
    # Pause the music when game over
    pygame.mixer.music.pause()

    game_over_font = pygame.font.SysFont('consolas', 50)
    game_over_surface = game_over_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    
    restart_font = pygame.font.SysFont('consolas', 20)
    restart_surface = restart_font.render('Press any key to Restart', True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (frame_size_x / 2, frame_size_y / 1.5)
    game_window.blit(restart_surface, restart_rect)

    pygame.display.update()

# Function to create dynamic background with lines aligned to the snake
def draw_guidelines():
    head_x, head_y = head_pos
    
    # Create grid lines that move with the snake
    for x in range(0, frame_size_x, square_size):
        pygame.draw.line(game_window, line_color, (x, 0), (x, frame_size_y), 1)
    for y in range(0, frame_size_y, square_size):
        pygame.draw.line(game_window, line_color, (0, y), (frame_size_x, y), 1)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord("w")
                and direction != "DOWN"):
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == ord("s")
                and direction != "UP"):
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == ord("a")
                and direction != "RIGHT"):
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == ord("d")
                and direction != "LEFT"):
                direction = "RIGHT"
            
            # Restart the game if any key is pressed after Game Over
            if event.type == pygame.KEYDOWN and pygame.mixer.music.get_busy() == False:
                init_vars()  # Restart the game
                pygame.mixer.music.unpause()  # Resume the music

    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size
    
    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y - square_size:
        head_pos[1] = 0
    
    # Eating apple
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
    
    # Spawn food
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                    random.randrange(1, (frame_size_y // square_size)) * square_size]
        food_spawn = True
    
    # GFX
    game_window.fill(background_color)  # Set the background color
    draw_guidelines()  # Draw grid lines that guide the snake
    
    # Draw the snake with a styled design
    for i, pos in enumerate(snake_body):
        if i == 0:  # Head of the snake
            pygame.draw.circle(game_window, snake_head_color, (pos[0] + square_size // 2, pos[1] + square_size // 2), square_size // 2)
        else:  # Body of the snake
            pygame.draw.rect(game_window, snake_color, pygame.Rect(
                pos[0] + 2, pos[1] + 2,
                square_size - 2, square_size - 2))
        
    # Draw the food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0],
                    food_pos[1], square_size, square_size))
    
    # Game over conditions
    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            game_over()
            pygame.display.update()
            time.sleep(2)  # Show game over message for 2 seconds
            init_vars()  # Restart the game
    
    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(speed)

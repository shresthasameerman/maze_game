import pygame
import random
import sys

# Constants
CELL_SIZE = 20
MAZE_WIDTH = 25
MAZE_HEIGHT = 25
WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE  # Increase the screen width
WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 100  # Increase the screen height for the text panel
FPS = 30
LEVELS = 10
BASE_TRAP_COUNT = 5  # Reduced base trap count
INITIAL_TIME_LIMIT = 60  # Initial seconds per level
TIME_DECREASE = 5  # Decrease time by 5 seconds each level
TIME_LIMIT_MIN = 10  # Minimum time limit (seconds)
LIVES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TRANSPARENT_TRAP = (0, 0, 255, 100)
BACKGROUND_COLOR = (30, 30, 30)
TEXT_PANEL_COLOR = (20, 20, 20)  # Dark background for the text panel
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Directions for maze generation
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Initialize Pygame
pygame.init()

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Function to generate the maze
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(0, 0)]
    maze[0][0] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[ny - (ny - y) // 2][nx - (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

# Function to place traps
def place_traps(maze, trap_count):
    path_positions = [
        (x, y)
        for y in range(MAZE_HEIGHT)
        for x in range(MAZE_WIDTH)
        if maze[y][x] == 0 and (x, y) != (0, 0) and (x, y) != (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)
    ]
    return random.sample(path_positions, min(trap_count, len(path_positions)))

# Function to draw maze
def draw_maze(screen, maze, traps, show_traps):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = WHITE if cell == 1 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for trap in traps:
        if show_traps:
            pygame.draw.rect(screen, RED, (trap[0] * CELL_SIZE, trap[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to display text
def display_text(screen, text, color, x, y, font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw a button
def draw_button(screen, text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Main menu screen
def menu_screen(screen):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Display Title
        display_text(screen, "Maze Game", WHITE, WINDOW_WIDTH // 3, WINDOW_HEIGHT // 4, big_font)

        # Draw buttons
        draw_button(screen, "Start Game", WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        draw_button(screen, "Instructions", WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2 + 60, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        draw_button(screen, "Exit", WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2 + 120, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if WINDOW_WIDTH // 3 < mouse_x < WINDOW_WIDTH // 3 + 200 and WINDOW_HEIGHT // 2 < mouse_y < WINDOW_HEIGHT // 2 + 50:
                    return "start"  # Start game
                elif WINDOW_WIDTH // 3 < mouse_x < WINDOW_WIDTH // 3 + 200 and WINDOW_HEIGHT // 2 + 60 < mouse_y < WINDOW_HEIGHT // 2 + 110:
                    return "instructions"  # Show instructions
                elif WINDOW_WIDTH // 3 < mouse_x < WINDOW_WIDTH // 3 + 200 and WINDOW_HEIGHT // 2 + 120 < mouse_y < WINDOW_HEIGHT // 2 + 170:
                    pygame.quit()
                    sys.exit()  # Exit game

# Instructions screen
def instructions_screen(screen):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        display_text(screen, "Use WASD keys to move.", WHITE, 50, 50, font)
        display_text(screen, "Avoid traps and reach the goal.", WHITE, 50, 100, font)
        display_text(screen, "Press ESC to quit at any time.", WHITE, 50, 200, font)
        draw_button(screen, "Back to Menu", WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2 + 180, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if WINDOW_WIDTH // 3 < mouse_x < WINDOW_WIDTH // 3 + 200 and WINDOW_HEIGHT // 2 + 180 < mouse_y < WINDOW_HEIGHT // 2 + 230:
                    return "menu"  # Back to menu screen

# Function to reset the maze and traps
def reset_maze_and_traps(level):
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    traps = place_traps(maze, BASE_TRAP_COUNT + (level - 1) * 3)  # Scale traps more gently
    return maze, traps

# Game screen function
def game_screen(screen, clock):
    level = 1
    player_pos = [0, 0]
    goal_pos = [MAZE_WIDTH - 1, MAZE_HEIGHT - 1]
    maze, traps = reset_maze_and_traps(level)

    show_traps = False
    player_alive = True
    shield = 1
    lives = LIVES
    time_limit = INITIAL_TIME_LIMIT

    while level <= LEVELS and lives > 0:
        running = True
        level_start_time = pygame.time.get_ticks()

        while running:
            elapsed_time = (pygame.time.get_ticks() - level_start_time) // 1000
            time_left = max(0, time_limit - elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_h:
                        show_traps = not show_traps

                    if player_alive:
                        dx, dy = 0, 0
                        if event.key == pygame.K_a:
                            dx = -1
                        elif event.key == pygame.K_d:
                            dx = 1
                        elif event.key == pygame.K_w:
                            dy = -1
                        elif event.key == pygame.K_s:
                            dy = 1

                        new_pos = [player_pos[0] + dx, player_pos[1] + dy]
                        if 0 <= new_pos[0] < MAZE_WIDTH and 0 <= new_pos[1] < MAZE_HEIGHT and maze[new_pos[1]][new_pos[0]] == 0:
                            player_pos = new_pos

                        if tuple(player_pos) in traps:  # Convert player_pos to tuple for comparison
                            if shield > 0:
                                shield -= 1
                                traps.remove(tuple(player_pos))
                            else:
                                lives -= 1
                                player_pos = [0, 0]
                                if lives > 0:
                                    maze, traps = reset_maze_and_traps(level)  # Reset maze and traps on death
                                running = False

                        if player_pos == goal_pos:
                            level += 1
                            player_pos = [0, 0]
                            maze, traps = reset_maze_and_traps(level)
                            shield = 1
                            # Decrease the time limit for the next level
                            time_limit = max(TIME_LIMIT_MIN, INITIAL_TIME_LIMIT - (level - 1) * TIME_DECREASE)
                            running = False

            if time_left == 0:
                lives -= 1
                player_pos = [0, 0]
                if lives > 0:
                    maze, traps = reset_maze_and_traps(level)  # Reset maze and traps on timeout
                running = False

            screen.fill(BACKGROUND_COLOR)
            draw_maze(screen, maze, traps, show_traps)
            pygame.draw.rect(screen, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, RED, (goal_pos[0] * CELL_SIZE, goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw the text panel at the bottom
            pygame.draw.rect(screen, TEXT_PANEL_COLOR, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
            display_text(screen, f"Level: {level}", WHITE, 10, WINDOW_HEIGHT - 90, font)
            display_text(screen, f"Lives: {lives}", WHITE, 10, WINDOW_HEIGHT - 60, font)
            display_text(screen, f"Time: {time_left}s", WHITE, 10, WINDOW_HEIGHT - 30, font)

            pygame.display.flip()
            clock.tick(FPS)

    if lives == 0:
        display_text(screen, "Game Over!", RED, WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3, big_font)
    else:
        display_text(screen, "You Win!", GREEN, WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3, big_font)

    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    while True:
        result = menu_screen(screen)
        
        if result == "start":
            game_screen(screen, clock)
        elif result == "instructions":
            instructions_screen(screen)

if __name__ == "__main__":
    main()
from button import Button
import pygame
import sys
pygame.mixer.init()
import os

pygame.init()

MENU_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'menu_music.mp3'))

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/tbb.jpg")

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():


    GRAY = (128, 128, 128)
    YELLOW = (255 ,255, 0)
    ORANGE = (139, 69, 19)
    FPS = 10


    cell_size = 90
    rows, columns = 8, 8
    WIDTH, HEIGHT = columns * cell_size, rows * cell_size
    BOT_WIDTH, BOT_HEIGHT = cell_size - 5, cell_size
    TREASURE_WIDTH, TREASURE_HEIGHT = cell_size - 5, cell_size
    WALL_WIDTH, WALL_HEIGHT = cell_size - 5, cell_size - 5
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BOT_IMAGE = pygame.image.load(os.path.join('Assets','bot.png'))
    BOT = pygame.transform.scale(BOT_IMAGE, (BOT_WIDTH, BOT_HEIGHT))
    TREASURE_IMAGE = pygame.image.load(os.path.join('Assets','treasure.png'))
    TREASURE = pygame.transform.scale(TREASURE_IMAGE, (TREASURE_WIDTH, TREASURE_HEIGHT))

    WALL_IMAGE = pygame.image.load(os.path.join('Assets','wall_image.jpg'))
    WALL_IMAGE = pygame.transform.scale(WALL_IMAGE, (cell_size, cell_size))

    TROPHY_WIDTH, TROPHY_HEIGHT = 40, 60
    TROPHY_IMAGE = pygame.image.load(os.path.join('Assets','treasure.png'))
    TROPHY = pygame.transform.scale(TROPHY_IMAGE, (TROPHY_WIDTH, TROPHY_HEIGHT))

    FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'burn.mp3'))
    COIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'coin.mp3'))
    BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'background_music.mp3'))

    def count_stuck_squares(rows, columns, wall_vals):
        blocked_cells = []
        all_walls = add_walls(wall_vals)
        for wall in wall_vals:
            x1, y1, x2, y2 = wall
            if columns - 1 == x2:
                blocked_cells += [[i, j] for i in range(x1, columns) for j in range(y2)]
            if rows - 1 == y2:
                blocked_cells += [[i, j] for i in range(y1, rows) for j in range(x2)]
        return blocked_cells

    def add_walls(wall_vals):
        all_walls = []
        for wall in wall_vals:
            x1, y1, x2, y2 = wall
            if x1 == x2:
                for i in range(y1, y2 + 1):
                    all_walls.append([x1, i])
            if y1 == y2:
                for i in range(x1, x2 + 1):
                    all_walls.append([i, y1])
        return all_walls

    def draw_grid(rows, columns):
        for i in range(rows):
            for j in range(columns):
                pygame.draw.rect(screen, ORANGE, (j * cell_size, i * cell_size, cell_size, cell_size), 1)

    def bot_movement(grid, keys_pressed, bot, wall_vals):
        new_bot = bot.copy()

        if keys_pressed[pygame.K_RIGHT] and bot.x + 40 + bot.width < WIDTH:
            new_bot.x += cell_size
        if keys_pressed[pygame.K_UP] and bot.y - 1 > 0:
            new_bot.y -= cell_size
        if bot.x >= WIDTH - BOT_WIDTH - 5 and bot.y == 0:
            MENU_MUSIC.stop()
            COIN_SOUND.play()
            end() 

        
        for wall in wall_vals:
            wall_rect = pygame.Rect(wall[0] * cell_size, (rows - wall[3] - 1) * cell_size, (wall[2] - wall[0] + 1) * cell_size, cell_size)
            if new_bot.colliderect(wall_rect):
                return

        bot.x = new_bot.x
        bot.y = new_bot.y

    def draw_walls(wall_vals):
        all_walls = add_walls(wall_vals)
        for wall in all_walls:
            j, i = wall
            screen.blit(WALL_IMAGE, (j * cell_size, (rows - i - 1) * cell_size))

    




    def highlight_stuck_squares(stuck_squares):
        for square in stuck_squares:
            j, i = square
            pygame.draw.rect(screen, YELLOW, (j * cell_size, (rows - 1 - i) * cell_size, cell_size, cell_size), 1)

    def create_grid(rows, columns):
        grid = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(0)
            grid.append(row)
        return grid
    
    def end():

        WIDTH, HEIGHT = 1280, 720
        trophy = pygame.Rect(20, 100, TROPHY_WIDTH, TROPHY_HEIGHT)
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.fill("black")

            OPTIONS_TEXT = get_font(60).render("You win!", True, "White")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(900, 460), 
                                text_input="BACK", font=get_font(60), base_color="White", hovering_color="Green")
            OPTIONS_REPLAY = Button(image=None, pos=(400, 460), 
                                text_input="REPLAY", font=get_font(60), base_color="White", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)
            OPTIONS_REPLAY.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_REPLAY.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
                    if OPTIONS_REPLAY.checkForInput(OPTIONS_MOUSE_POS):
                        play()

            pygame.display.update()

        

# Create a display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Load images (you need to have these loaded)
BOT = pygame.Surface((BOT_WIDTH, BOT_HEIGHT))
TREASURE = pygame.Surface((TREASURE_WIDTH, TREASURE_HEIGHT))
# Load other assets like MENU_MUSIC, etc.

def main():
    global screen

    cell_size = 90
    rows = 8
    columns = 8
    wall_vals = [[1, 6, 3, 6], [2, 4, 2, 4], [4, 2, 7, 2]]
    bot = pygame.Rect(1, cell_size * rows - cell_size, BOT_WIDTH, BOT_HEIGHT)
    treasure = pygame.Rect(cell_size * columns - cell_size, 0, TREASURE_WIDTH, TREASURE_HEIGHT)

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  # Get the initial time in milliseconds
    timer_interval = 1000  # Timer interval in milliseconds (1 second)

    running = True
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rest of your game loop code

        screen.fill((0, 0, 0))
        # Draw game elements
        pygame.draw.rect(screen, (255, 0, 0), bot)  # Just a placeholder for bot
        pygame.draw.rect(screen, (0, 255, 0), treasure)  # Just a placeholder for treasure

        # Check and handle timer expiration
        if current_time - start_time >= timer_interval:
            print("Timer expired!")
            # Reset the timer
            start_time = current_time

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

    
def options():
     while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MUSIC.play()
        MENU_TEXT = get_font(72).render("Tracking Bio-Bots", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
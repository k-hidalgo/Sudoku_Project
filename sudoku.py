import sys, pygame
from turtle import Screen
from sudoku_generator import *
from colors_and_values import *

#Initialize Pygame
pygame.init()
Screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welcome to Sudoku")

#Initialize fonts
num_font = pygame.font.Font(None, 50)
start_title_font = pygame.font.Font(None, 85)
subtitle_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 50)

difficulty_settings = {
    "easy": 30,
    "medium": 40,
    "hard": 50
}

#Cell Class
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0  # sketching temp numbers
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.is_fixed = value != 0  # if the cell is fixed, it cannot be changed

    def set_cell_value(self, value):
        if not self.is_fixed:
            self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value #fix: value was set to value not sketched_value

    #Draw method for one sudoku cell
    def draw(self):
        gap = WIDTH // 9
        x = self.col * gap
        y = self.row * gap

        if self.selected:
            pygame.draw.rect(self.screen, LINE_COLOR, (x, y, gap, gap), 3)

        if self.value != 0:
            text = num_font.render(str(self.value), True, TITLE_COLOR)
            self.screen.blit(text, (x + gap // 2 - text.get_width() / 2, y + gap // 2 - text.get_height() / 2))
        elif self.sketched_value != 0:
            text = num_font.render(str(self.sketched_value), True, SKETCH_COLOR)
            self.screen.blit(text, (x + 5, y + 5))
        if self.is_fixed:
            pygame.draw.rect(self.screen, LINE_COLOR, (x, y, gap, gap), 2)

#Board Class
class Board:
    def __init__(self, width, height, screen, difficulty):
        # just initializes the board and sets the difficulty
        self.width = width
        self.height = height
        self.screen = screen
        self.selected_cell = None
        # setting the opening screen
        self.cells = [[Cell(0, i, j, screen) for j in range(9)] for i in range(9)]
        self.sudoku_generator = SudokuGenerator(difficulty_settings[difficulty], 9)
        self.sudoku_generator.fill_values()
        self.sudoku_generator.remove_cells()
        self.load_board(self.sudoku_generator.get_board())
        # Store a deep copy of the initial board state
        self.initial_board = [row[:] for row in self.sudoku_generator.get_board()]

    def draw(self):
        #draws sudoku board
        gap = self.width // 9
        #Draws each cell in row
        for row in self.cells:
            for cell in row:
                cell.draw()

        for i in range(9+1):
            line_width = 4 if i % 3 == 0  else 1
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * gap), (9 * gap, i * gap), line_width)
            pygame.draw.line(self.screen, LINE_COLOR, (i * gap, 0), (i * gap, 9 * gap), line_width)

    def load_board(self, board):
        for i in range(9):
            for j in range(9):
                svalue = board[i][j]
                self.cells[i][j].value = svalue
                self.cells[i][j].is_fixed = svalue != 0  # if the cell is fixed, it cannot be changed

    def select(self, row, col):
        for r in self.cells:
            for cell in r:
                cell.selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if not self.cells[row][col].is_fixed:
                self.cells[row][col].set_sketched_value(value)

    def submit_guess(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].sketched_value != 0:
                self.cells[row][col].set_cell_value(self.cells[row][col].sketched_value)
                self.cells[row][col].sketched_value = 0

    def reset_to_original(self):
        self.load_board(self.initial_board)

    def check_is_full(self):
        for row in self.cells:
            for j in row:
                if j.value == 0:
                    return False
        return True

    def check_is_correct(self):
        for row in self.cells:
            if sorted([cell.value for cell in row]) != list(range(1, 10)):
                return False
        for col in range(9):
            if sorted([self.cells[row][col].value for row in range(9)]) != list(range(1, 10)):
                return False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                grid_values = []
                for r in range(3):
                    for c in range(3):
                        grid_values.append(self.cells[box_row + r][box_col + c].value)

                if sorted(grid_values) != list(range(1, 10)):
                    return False
        return True

class SudokuGame:
    def __init__(self):
        self.running = True
        self.state = 'start'
        self.board = None
        self.difficulty = None

    def start_screen(self):
        Screen.fill(BACKGROUND)

        # Initialize and Draw Title
        title_text = start_title_font.render("Welcome to Sudoku", True, TITLE_COLOR)
        Screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150)))

        subtitle_text= subtitle_font.render("Select Game Mode:", True, TITLE_COLOR)
        Screen.blit(subtitle_text, subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))

        # Initialize Text For Buttons
        easy_text = button_font.render("Easy", True, BACKGROUND)
        medium_text = button_font.render("Medium", True, BACKGROUND)
        hard_text = button_font.render("Hard", True, BACKGROUND)

        # Initialize Buttons
        button_width = 150
        button_height = 50
        button_y = HEIGHT // 2 + 60
        button_spacing = 40
        total_width = button_width * 3 + button_spacing * 2
        start_x = (WIDTH - total_width) // 2

        easy_button = pygame.Rect(start_x, button_y, button_width, button_height)
        medium_button = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, button_height)
        hard_button = pygame.Rect(start_x + 2 * (button_width + button_spacing), button_y, button_width, button_height)

        pygame.draw.rect(Screen, TITLE_COLOR, easy_button)
        pygame.draw.rect(Screen, TITLE_COLOR, medium_button)
        pygame.draw.rect(Screen, TITLE_COLOR, hard_button)

        #Draw Buttons
        Screen.blit(easy_text, (easy_button.x + (easy_button.width - easy_text.get_width()) // 2,
                                easy_button.y + (easy_button.height - easy_text.get_height()) // 2))
        Screen.blit(medium_text, (medium_button.x + (medium_button.width - medium_text.get_width()) // 2,
                                  medium_button.y + (medium_button.height - medium_text.get_height()) // 2))
        Screen.blit(hard_text, (hard_button.x + (hard_button.width - hard_text.get_width()) // 2,
                                hard_button.y + (hard_button.height - hard_text.get_height()) // 2))

        pygame.display.update()
        return easy_button, medium_button, hard_button

    def in_game_buttons(self):
        button_width = 150
        button_height = 50
        button_spacing = 20
        total_width = button_width * 3 + button_spacing * 2

        # Center the buttons horizontally
        x_offset = (WIDTH - total_width) / 2

        # Position buttons just below the Sudoku board
        button_y = self.board.height + 10
        reset_button = pygame.Rect(x_offset, button_y, button_width, button_height)
        restart_button = pygame.Rect(x_offset + button_width + button_spacing, button_y, button_width, button_height)
        exit_button = pygame.Rect(x_offset + (button_width + button_spacing) * 2, button_y, button_width, button_height)

        pygame.draw.rect(Screen, BACKGROUND, reset_button)
        pygame.draw.rect(Screen, BACKGROUND, restart_button)
        pygame.draw.rect(Screen, BACKGROUND, exit_button)

        reset_text = button_font.render("Reset", True, TITLE_COLOR)
        restart_text = button_font.render("Restart", True, TITLE_COLOR)
        exit_text = button_font.render("Exit", True, TITLE_COLOR)

        Screen.blit(reset_text, (reset_button.x + (button_width - reset_text.get_width()) // 2,
                                 reset_button.y + (button_height - reset_text.get_height()) // 2))
        Screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2,
                                   restart_button.y + (button_height - restart_text.get_height()) // 2))
        Screen.blit(exit_text, (exit_button.x + (button_width - exit_text.get_width()) // 2,
                                exit_button.y + (button_height - exit_text.get_height()) // 2))
        pygame.display.update()

        return reset_button, restart_button, exit_button

    def game_win_screen(self):
        # Fill background
        Screen.fill(BACKGROUND)

        win_text = start_title_font.render("Game Won!", True, TITLE_COLOR)
        Screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))

        #Exit Button
        exit_button = pygame.Rect(WIDTH / 2 - 75, HEIGHT/2 + 50, 150, 50)
        pygame.draw.rect(Screen, TITLE_COLOR, exit_button)
        exit_text = button_font.render("Exit", True, BACKGROUND)
        Screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2,
                                exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if exit_button.collidepoint(pos):
                        pygame.quit()
                        sys.exit()

    def game_lose_screen(self):
        # Fill background
        Screen.fill(BACKGROUND)

        lose_text = start_title_font.render("Game Over :(", True, TITLE_COLOR)
        Screen.blit(lose_text, lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))

        #Restart Button
        restart_button = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 + 51, 150, 50)
        pygame.draw.rect(Screen, BACKGROUND, restart_button)
        restart_text = button_font.render("Restart", True, TITLE_COLOR)
        # Center the "Restart" text inside the button
        Screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                                   restart_button.y + (restart_button.height - restart_text.get_height()) // 2))

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(pos):
                        self.state = 'start'
                        waiting = False

    #Functions that handle if the in game buttons are clicked while the game is in progress
    def is_button_clicked(self, button_name, pos):
        button_width = 150
        button_height = 50
        button_spacing = 20
        total_width = button_width * 3 + button_spacing * 2
        x_offset = (WIDTH - total_width) / 2
        button_y = self.board.height + 10

        if button_name == 'Reset':
            return pygame.Rect(x_offset, button_y, button_width, button_height).collidepoint(pos)
        elif button_name == 'Restart':
            return pygame.Rect(x_offset + button_width + button_spacing, button_y, button_width,
                               button_height).collidepoint(pos)
        elif button_name == 'Exit':
            return pygame.Rect(x_offset + (button_width + button_spacing) * 2, button_y, button_width,
                               button_height).collidepoint(pos)
        return False


    def run_game(self, difficulty):
        self.difficulty = difficulty
        self.board = Board(WIDTH, GRID_HEIGHT, Screen, difficulty)
        self.state = 'playing'

        while self.state == 'playing':
            # Board and buttons
            Screen.fill(BACKGROUND)
            self.board.draw()
            self.in_game_buttons()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = 'exit'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    grid_height = HEIGHT - 100
                    row, col = pos[1] // (grid_height // 9), pos[0] // (WIDTH // 9)
                    # check if click is within the grid
                    if pos[1] < grid_height and row < 9 and col < 9:
                        self.board.select(row, col)

                    # Check if the in game buttons are clicked
                    if self.is_button_clicked('Reset', pos):
                        self.board.reset_to_original()
                    elif self.is_button_clicked('Exit', pos):
                        self.running = False
                        self.state = 'exit'
                    elif self.is_button_clicked('Restart', pos):
                        self.state = 'start'
                elif event.type == pygame.KEYDOWN:
                    if self.board.selected_cell and event.key == pygame.K_UP:
                        if self.board.selected_cell[0] > 0:
                            self.board.select(self.board.selected_cell[0] - 1, self.board.selected_cell[1])
                    elif self.board.selected_cell and event.key == pygame.K_DOWN:
                        if self.board.selected_cell[0] < 8:
                            self.board.select(self.board.selected_cell[0] + 1, self.board.selected_cell[1])
                    elif self.board.selected_cell and event.key == pygame.K_LEFT:
                        if self.board.selected_cell[1] > 0:
                            self.board.select(self.board.selected_cell[0], self.board.selected_cell[1] - 1)
                    elif self.board.selected_cell and event.key == pygame.K_RIGHT:
                        if self.board.selected_cell[1] < 8:
                            self.board.select(self.board.selected_cell[0], self.board.selected_cell[1] + 1)
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        value = event.key - pygame.K_0
                        self.board.sketch(value)
                    elif event.key == pygame.K_RETURN:
                        self.board.submit_guess()

            # checks if the board is full and if it is correct
            if self.board.check_is_full():
                if self.board.check_is_correct():
                    self.game_win_screen()
                    self.state = 'start'
                else:
                    self.game_lose_screen()
                    self.state = 'start'

    def run(self):
        while self.running:
            if self.state == 'start':
                # Pass screen explicitly to start_screen
                easy_button, medium_button, hard_button = self.start_screen()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            waiting = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if easy_button.collidepoint(pos):
                                self.difficulty = 'easy'
                                waiting = False
                            elif medium_button.collidepoint(pos):
                                self.difficulty = 'medium'
                                waiting = False
                            elif hard_button.collidepoint(pos):
                                self.difficulty = 'hard'
                                waiting = False

                if self.difficulty:
                    self.run_game(self.difficulty)

if __name__ == "__main__":
    game = SudokuGame()
    game.run()

import pygame
from config.constants import (
    CELL_SIZE, MARGIN, BG_COLOR,
    CELL_COLOR, TEXT_COLOR,
    FONT_SIZE, SCORE_FONT_SIZE,
    NEXT_FONT_SIZE, GRID_LENGTH,
    GRID_WIDTH
)


class GameUI:
    COLORS = {
        0: (60, 58, 50),         # dark base for empty
        2: (255, 255, 153),      # bright yellow
        4: (255, 204, 102),      # orange-yellow
        8: (255, 153, 51),       # vivid orange
        16: (255, 102, 102),     # red-orange
        32: (255, 51, 51),       # bright red
        64: (204, 0, 0),         # deep red
        128: (102, 255, 102),    # bright green
        256: (51, 204, 51),      # green
        512: (0, 153, 0),        # dark green
        1024: (102, 178, 255),   # sky blue
        2048: (0, 102, 255),     # vivid blue
    }

    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.window_width = GRID_WIDTH * (CELL_SIZE + MARGIN) + MARGIN
        self.window_height = GRID_LENGTH * (CELL_SIZE + MARGIN) + MARGIN + 80

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("2D Array Game")
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.score_font = pygame.font.SysFont("Arial", SCORE_FONT_SIZE)
        self.next_font = pygame.font.SysFont("Arial", NEXT_FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.input_column = None
        self.next_value = self.game_logic.random_value()
        self.temp_message = None
        self.temp_message_time = 0
        self.temp_message_duration = 1500

    def show_temp_message(self, text):
        self.temp_message = text
        self.temp_message_time = pygame.time.get_ticks()

    def draw_matrix(self):
        self.screen.fill(BG_COLOR)
        matrix = self.game_logic._matrix

        for row in range(GRID_LENGTH):
            for col in range(GRID_WIDTH):
                value = matrix[row][col]
                rect = pygame.Rect(
                    MARGIN + col * (CELL_SIZE + MARGIN),
                    MARGIN + row * (CELL_SIZE + MARGIN) + 40,
                    CELL_SIZE,
                    CELL_SIZE
                )
                cell_color = self.COLORS.get(value, CELL_COLOR)
                pygame.draw.rect(self.screen, cell_color, rect)

                if value != 0:
                    text_surface = self.font.render(
                        str(value), True, TEXT_COLOR
                    )
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

        score_surface = self.score_font.render(
            f"Score: {self.game_logic.get_score()}", True, (0, 0, 0)
        )
        self.screen.blit(
            score_surface, (10, GRID_LENGTH * (CELL_SIZE + MARGIN) + 45)
        )
        next_surface = self.next_font.render(
            f"Next: {self.next_value}", True, (255, 0, 0)
        )
        self.screen.blit(next_surface, (10, 5))
        self.draw_temp_message()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                for i in range(GRID_WIDTH):
                    if event.key == getattr(pygame, f'K_{i}'):
                        self.input_column = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if y >= 40:
                        col = (x - MARGIN) // (CELL_SIZE + MARGIN)
                        if 0 <= col < GRID_WIDTH:
                            self.input_column = col

    def draw_game_over(self):
        overlay = pygame.Surface(
            (self.window_width, self.window_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.SysFont("Arial", 60, bold=True)
        text_surface = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def draw_temp_message(self):
        if not self.temp_message:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.temp_message_time > self.temp_message_duration:
            self.temp_message = None
            return

        msg_surface = self.font.render(self.temp_message, True, (255, 80, 80))
        msg_rect = msg_surface.get_rect(
            center=(
                self.window_width // 2,
                self.window_height - 25
            )
        )

        self.screen.blit(msg_surface, msg_rect)

    def run(self):
        game_is_over = False

        while True:
            self.handle_events()
            show_message = False
            if not game_is_over and self.input_column is not None:
                try:
                    if not self.game_logic.add_to_column(
                        self.next_value, self.input_column
                    ):
                        show_message = True
                    if not show_message:
                        self.next_value = self.game_logic.random_value()
                        self.input_column = None
                except Exception as e:
                    print("Invalid move:", e)

            if show_message:
                self.show_temp_message("Column is full")

            if self.game_logic.game_over(self.next_value):
                self.draw_game_over()
            self.draw_matrix()
            self.clock.tick(30)

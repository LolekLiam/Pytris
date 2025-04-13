import threading
import pygame
import random
import time

from typing import List, Literal
from srs.rotation import TetrominoI, TetrominoJ, TetrominoL, TetrominoO, TetrominoS, TetrominoT, TetrominoZ

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_MARGIN = 1
SIDEBAR_WIDTH = 200

SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

move_delay = 150
move_interval = 50
last_move_time = 0


def play(sound, start, end):
    pygame.mixer.music.play(0, start)
    time.sleep(end - start)
    # pygame.mixer.music.stop()
    return True


from typing import List, Literal

TetrominGrid = List[List[Literal[0, 1]]]


class Tetromino:
    def __init__(self, grid_rotations: List[TetrominGrid], color: str):
        self.grid_rotations = grid_rotations
        self.rotation = 0
        self.color = color
        self.width = len(self.current_grid()[0])
        self.height = len(self.current_grid())

    def width(self) -> int:
        return len(self.current_grid()[0])

    def height(self) -> int:
        return len(self.current_grid())

    def defined_rotations(self) -> int:
        return len(self.grid_rotations)

    def current_rotation_i(self) -> int:
        return self.rotation % len(self.grid_rotations)

    def current_grid(self) -> TetrominGrid:
        return self.grid_rotations[self.rotation % len(self.grid_rotations)]

    def peek_next_grid(self, backward=False) -> TetrominGrid:
        self.rotate(backward)
        next_grid = self.current_grid()
        self.rotate(not backward)
        return next_grid

    def rotate(self, backward=False) -> None:
        self.rotation += 1 if not backward else -1

    def debug_print(self) -> None:
        for row in self.current_grid():
            print(row)


class TetrisGame:
    def __init__(self):
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except FileNotFoundError:
            self.high_score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.lvlup_sound = pygame.mixer.Sound("lvlup.wav")
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 0.5
        self.soft_drop_speed = 0.05
        self.lock_delay = 0.5
        self.last_move_time = time.time()

    def main_menu(self):
        selected_option = 0
        options = ["Start Game", "Help", "About", "Quit"]

        while True:
            self.screen.fill(BLACK)

            title = self.font.render("Pytris (Pygame Tetris clone)", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            for i, option in enumerate(options):
                color = WHITE if i == selected_option else GRAY
                text = self.font.render(option, True, color)
                self.screen.blit(
                    text,
                    (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 60)
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        choice = options[selected_option]
                        if choice == "Start Game":
                            return
                        elif choice == "Help":
                            self.help_screen()
                        elif choice == "About":
                            self.about_screen()
                        elif choice == "Quit":
                            pygame.quit()
                            exit()

            self.clock.tick(60)

    def help_screen(self):
        lines = [
            "Controls:",
            "Left/Right: Move",
            "Up: Rotate",
            "Down: Soft Drop",
            "Space: Hard Drop",
            "P: Pause",
            "R: Restart",
            "",
            "Press ESC to return"
        ]
        self.draw_text_screen("HELP", lines)

    def about_screen(self):
        lines = [
            "TETRIS Clone by Liam",
            "Inspired by the original Game Boy version.",
            "Using Pygame + Python",
            "",
            "Music: Korobeiniki (Tetris Theme)",
            "Rotation System: SRS",
            "",
            "Press ESC to return"
        ]
        self.draw_text_screen("ABOUT", lines)

    def draw_text_screen(self, title, lines):
        while True:
            self.screen.fill(BLACK)

            title_text = self.font.render(title, True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

            for i, line in enumerate(lines):
                rendered = self.small_font.render(line, True, GRAY)
                self.screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, 150 + i * 30))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.clock.tick(60)

    def new_piece(self):
        tetromino_classes = [TetrominoI, TetrominoJ, TetrominoL, TetrominoO, TetrominoS, TetrominoT, TetrominoZ]
        tetromino_class = random.choice(tetromino_classes)
        color = SHAPE_COLORS[tetromino_classes.index(tetromino_class)]  # Assign color based on class index
        return tetromino_class(GRID_WIDTH // 2 - 2, 0)  # Pass color to constructor

    def valid_move(self, piece, x, y, shape=None):
        if shape is None:
            shape = piece.current_grid()

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if not (0 <= x + j < GRID_WIDTH and y + i < GRID_HEIGHT):
                        return False
                    if y + i >= 0 and self.grid[y + i][x + j]:
                        return False
        return True

    def has_landed(self):
        return not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1)

    def add_to_grid(self):
        for i, row in enumerate(self.current_piece.current_grid()):
            for j, cell in enumerate(row):
                if cell:
                    if self.current_piece.y + i < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]

        if not lines_to_clear:
            return 0

        # Flash animation (white-out effect)
        flash_duration = 0.3
        flash_interval = 0.05
        flash_times = int(flash_duration / flash_interval)

        original_colors = [[self.grid[y][x] for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

        for _ in range(flash_times):
            for line in lines_to_clear:
                for x in range(GRID_WIDTH):
                    self.grid[line][x] = WHITE  # Flash white
            self.draw_frame()
            time.sleep(flash_interval)

            for line in lines_to_clear:
                for x in range(GRID_WIDTH):
                    self.grid[line][x] = original_colors[line][x]  # Restore original
            self.draw_frame()
            time.sleep(flash_interval)

        # Remove the lines
        for line in sorted(lines_to_clear, reverse=True):
            del self.grid[line]
        for _ in lines_to_clear:
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

        line_scores = [40, 100, 300, 1200]
        self.score += line_scores[min(len(lines_to_clear) - 1, 3)] * self.level
        self.lines_cleared += len(lines_to_clear)

        old_level = self.level
        self.level = self.lines_cleared // 10 + 1

        if self.level > old_level:
            self.lvlup_sound.play()

        self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)

        return len(lines_to_clear)

    def get_ghost_piece_position(self):
        ghost_y = self.current_piece.y
        while self.valid_move(self.current_piece, self.current_piece.x, ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def draw_ghost_piece(self):
        ghost_y = self.get_ghost_piece_position()
        for i, row in enumerate(self.current_piece.current_grid()):
            for j, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (self.current_piece.x + j) * BLOCK_SIZE,
                        (ghost_y + i) * BLOCK_SIZE,
                        BLOCK_SIZE - GRID_MARGIN,
                        BLOCK_SIZE - GRID_MARGIN
                    )
                    pygame.draw.rect(self.screen, self.current_piece.color, rect, 2)  # Outline only

    def move(self, dx, dy):
        if self.valid_move(self.current_piece, self.current_piece.x + dx, self.current_piece.y + dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            self.last_move_time = time.time()
            return True
        return False

    def rotate_piece(self):
        self.current_piece.rotate()
        rotated_shape = self.current_piece.current_grid()
        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y, rotated_shape):
            self.last_move_time = time.time()
            return True

        # Wall kick attempts
        for dx in [-1, 1, -2, 2]:
            if self.valid_move(self.current_piece, self.current_piece.x + dx, self.current_piece.y, rotated_shape):
                self.current_piece.x += dx
                self.last_move_time = time.time()
                return True

        # Revert rotation if no valid move found
        self.current_piece.rotate(backward=True)
        return False

    def drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()

    def lock_piece(self):
        self.add_to_grid()
        lines_cleared = self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.last_move_time = time.time()
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x] if self.grid[y][x] else BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    [(BLOCK_SIZE) * x,
                     (BLOCK_SIZE) * y,
                     BLOCK_SIZE - GRID_MARGIN,
                     BLOCK_SIZE - GRID_MARGIN]
                )

        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                GRAY,
                (x * BLOCK_SIZE, 0),
                (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE),
                1
            )
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                GRAY,
                (0, y * BLOCK_SIZE),
                (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE),
                1
            )

    def draw_frame(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_current_piece()
        self.draw_sidebar()
        pygame.display.flip()

    def draw_current_piece(self):
        for i, row in enumerate(self.current_piece.current_grid()):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece.color,
                        [(BLOCK_SIZE) * (self.current_piece.x + j),
                         (BLOCK_SIZE) * (self.current_piece.y + i),
                         BLOCK_SIZE - GRID_MARGIN,
                         BLOCK_SIZE - GRID_MARGIN]
                    )

    def draw_sidebar(self):
        pygame.draw.rect(
            self.screen,
            BLACK,
            [GRID_WIDTH * BLOCK_SIZE, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT]
        )

        next_label = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_label, (GRID_WIDTH * BLOCK_SIZE + 20, 20))

        preview_x = GRID_WIDTH * BLOCK_SIZE + SIDEBAR_WIDTH // 2 - len(
            self.next_piece.current_grid()[0]) * BLOCK_SIZE // 2
        preview_y = 70

        for i, row in enumerate(self.next_piece.current_grid()):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.next_piece.color,
                        [preview_x + j * BLOCK_SIZE,
                         preview_y + i * BLOCK_SIZE,
                         BLOCK_SIZE - GRID_MARGIN,
                         BLOCK_SIZE - GRID_MARGIN]
                    )

        score_label = self.font.render("Score:", True, WHITE)
        score_value = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(score_label, (GRID_WIDTH * BLOCK_SIZE + 20, 160))
        self.screen.blit(score_value, (GRID_WIDTH * BLOCK_SIZE + 20, 200))

        level_label = self.font.render("Level:", True, WHITE)
        level_value = self.font.render(str(self.level), True, WHITE)
        self.screen.blit(level_label, (GRID_WIDTH * BLOCK_SIZE + 20, 240))
        self.screen.blit(level_value, (GRID_WIDTH * BLOCK_SIZE + 20, 280))

        highscore_label = self.font.render("High Score:", True, WHITE)
        highscore_value = self.font.render(str(self.high_score), True, WHITE)
        self.screen.blit(highscore_label, (GRID_WIDTH * BLOCK_SIZE + 20, 320))
        self.screen.blit(highscore_value, (GRID_WIDTH * BLOCK_SIZE + 20, 360))

        lines_label = self.font.render("Lines:", True, WHITE)
        lines_value = self.font.render(str(self.lines_cleared), True, WHITE)
        self.screen.blit(lines_label, (GRID_WIDTH * BLOCK_SIZE + 20, 400))
        self.screen.blit(lines_value, (GRID_WIDTH * BLOCK_SIZE + 20, 440))

        """
        controls = [
            "Controls:",
            "Left/Right: Move",
            "Up: Rotate",
            "Down: Soft Drop",
            "Space: Hard Drop",
            "P: Pause",
            "R: Restart"
        ]

        y_pos = 450
        for text in controls:
            control_text = self.small_font.render(text, True, WHITE)
            self.screen.blit(control_text, (GRID_WIDTH * BLOCK_SIZE + 20, y_pos))
            y_pos += 25"""

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, WHITE)
        restart_text = self.small_font.render("Press R to restart", True, WHITE)

        self.screen.blit(
            game_over_text,
            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
             SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2)
        )
        self.screen.blit(
            restart_text,
            (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
             SCREEN_HEIGHT // 2 + 40)
        )

    def run(self):
        self.main_menu()
        last_fall_time = time.time()
        paused = False

        running = True
        while running:
            current_time = time.time()
            current_time_ticks = pygame.time.get_ticks()

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    if event.key == pygame.K_r:
                        self.reset_game()

                    if not self.game_over and not paused:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.move(-1 if event.key == pygame.K_LEFT else 1, 0)
                            last_move_time = current_time_ticks + move_delay
                        if event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            self.drop()

            if not self.game_over and not paused:
                if keys[pygame.K_LEFT] and current_time_ticks > last_move_time:
                    self.move(-1, 0)
                    last_move_time = current_time_ticks + move_interval
                elif keys[pygame.K_RIGHT] and current_time_ticks > last_move_time:
                    self.move(1, 0)
                    last_move_time = current_time_ticks + move_interval

                if keys[pygame.K_DOWN]:
                    if current_time - last_fall_time > self.soft_drop_speed:
                        if not self.move(0, 1) and current_time - self.last_move_time > self.lock_delay:
                            self.lock_piece()
                        last_fall_time = current_time

                elif current_time - last_fall_time > self.fall_speed:
                    if not self.move(0, 1):
                        if current_time - self.last_move_time > self.lock_delay:
                            self.lock_piece()
                    last_fall_time = current_time

            self.screen.fill(BLACK)

            self.draw_grid()
            if not self.game_over:
                self.draw_ghost_piece()
                self.draw_current_piece()
            self.draw_sidebar()

            if paused:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))

                pause_text = self.font.render("PAUSED", True, WHITE)
                resume_text = self.small_font.render("Press P to resume", True, WHITE)

                self.screen.blit(
                    pause_text,
                    (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                     SCREEN_HEIGHT // 2 - pause_text.get_height() // 2)
                )
                self.screen.blit(
                    resume_text,
                    (SCREEN_WIDTH // 2 - resume_text.get_width() // 2,
                     SCREEN_HEIGHT // 2 + 40)
                )

            if self.game_over:
                self.draw_game_over()
                if self.score > self.high_score:
                    self.high_score = self.score
                    with open("highscore.txt", "w") as f:
                        f.write(str(self.high_score))

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    # music = pygame.mixer.music
    # sound = music.load("tetris_songs.wav")
    # sound_thread = threading.Thread(target=play, args=([sound, 1, 2]))
    # sound_thread.start()
    game = TetrisGame()
    game.run()

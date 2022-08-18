# Project 5
# Katy Huang
# 59698946
# katyh1@uci.edu
import pygame
import columns

_BACKGROUND_COLOR = pygame.Color(0, 0, 0)
_INITIAL_WIDTH = 300
_INITIAL_HEIGHT = 650
_WHITE = pygame.Color(255, 255, 255)
_RED = pygame.Color(255, 51, 51)
_BROWN = pygame.Color(153, 76, 0)
_YELLOW = pygame.Color(255, 255, 51)
_BLUE = pygame.Color(51, 153, 255)
_ORANGE = pygame.Color(255, 153, 51)
_GREEN = pygame.Color(51, 255, 51)
_PURPLE = pygame.Color(153, 51, 255)


class ColumnsGame:
    def __init__(self) -> None:
        self._running = True
        self._gamestate = columns.GameState()
        self._gameboard = None

    def run(self):
        """Run the program"""
        pygame.init()
        try:
            ENTER_EVENT = pygame.event.custom_type()
            pygame.time.set_timer(ENTER_EVENT, 1000)
            self._gameboard = self._gamestate.create_empty_board(13, 6)
            self._create_display((_INITIAL_WIDTH, _INITIAL_HEIGHT))
            self._draw_current_board(_WHITE)
            while self._running:
                if self._gamestate.faller_on_gameboard() or self._gamestate.there_is_a_match():
                    self._update_game(faller, ENTER_EVENT)
                    self._draw_current_board(_WHITE)
                elif self._gamestate.game_is_over():
                    self._draw_current_board(_RED)
                else:
                    faller = self._gamestate.create_new_faller()
                    self._gamestate.add_faller(faller)
                    self._draw_current_board(_WHITE)
        finally:
            pygame.quit()

    def _create_display(self, size: (int, int)) -> None:
        """Create display and make it resizeable"""
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _update_game(self, faller, ENTER_EVENT) -> None:
        """Update the game events, also handle user inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end()
            elif event.type == ENTER_EVENT:
                self._gamestate.enter_action(faller)
            elif event.type == pygame.KEYDOWN:
                self._handle_keys(faller)

    def _handle_keys(self, faller) -> None:
        """Handle user inputs"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self._gamestate.can_move(faller, -1):
            self._gamestate.move_action(faller, -1)
        elif keys[pygame.K_RIGHT] and self._gamestate.can_move(faller, 1):
            self._gamestate.move_action(faller, 1)
        elif keys[pygame.K_SPACE]:
            self._gamestate.rotate_action(faller)

    def _get_grid_size(self):
        """Get the size of the grid base on the board size"""
        board_size_x, board_size_y = pygame.display.get_surface().get_size()
        grid_size_x = board_size_x / 6
        grid_size_y = board_size_y / 13
        return grid_size_x, grid_size_y

    def _draw_current_board(self, color):
        """Draw the current game board with visual effect when matching and landing"""
        self._draw_grid_board(color)
        displayed_game_board = self._gamestate.current_game_board()[2:]
        grid_size_x, grid_size_y = self._get_grid_size()
        top_left_y = -grid_size_y
        for i in displayed_game_board:
            top_left_y += grid_size_y
            top_left_x = -grid_size_x
            for j in i:
                top_left_x += grid_size_x
                color = self.find_color_to_fill(j)
                surface = pygame.display.get_surface()
                pygame.draw.rect(surface, color, [
                    top_left_x, top_left_y, grid_size_x, grid_size_y])
                if '*' in j:
                    self._draw_grid_board(color)
                    pygame.draw.rect(surface, _BACKGROUND_COLOR, [
                        top_left_x, top_left_y, grid_size_x, grid_size_y], 100)
                elif '|' in j:
                    self._draw_grid_board(color)
                    pygame.draw.rect(surface, _WHITE, [
                        top_left_x, top_left_y, grid_size_x, grid_size_y])
                    pygame.display.flip()
                    pygame.draw.rect(surface, color, [
                        top_left_x, top_left_y, grid_size_x, grid_size_y])

    def _end(self) -> None:
        """Make self._running = False"""
        self._running = False

    def _draw_grid_board(self, color):
        """Draw the grid board"""
        grid_size_x, grid_size_y = self._get_grid_size()
        for x in range(_INITIAL_WIDTH):
            for y in range(_INITIAL_HEIGHT):
                rect = pygame.Rect(x*grid_size_x, y*grid_size_y,
                                   grid_size_x, grid_size_y)
                surface = pygame.display.get_surface()
                pygame.draw.rect(surface, color, rect, 1)
        pygame.display.flip()

    def find_color_to_fill(self, element):
        """Find color to fill for rectangle based on element"""
        if element == ' ':
            return _BACKGROUND_COLOR
        elif element == 'R' or (len(element) == 3 and element[1] == 'R'):
            return _RED
        elif element == 'W' or (len(element) == 3 and element[1] == 'W'):
            return _BROWN
        elif element == 'Y' or (len(element) == 3 and element[1] == 'Y'):
            return _YELLOW
        elif element == 'B' or (len(element) == 3 and element[1] == 'B'):
            return _BLUE
        elif element == 'O' or (len(element) == 3 and element[1] == 'O'):
            return _ORANGE
        elif element == 'G' or (len(element) == 3 and element[1] == 'G'):
            return _GREEN
        elif element == 'P' or (len(element) == 3 and element[1] == 'P'):
            return _PURPLE


if __name__ == '__main__':
    ColumnsGame().run()

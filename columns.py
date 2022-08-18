from copy import deepcopy
from random import randint
from project5 import *


class InvalidColorError(Exception):
    '''Raised whenever an invalid color is input as faller'''
    pass


class Faller():
    def __init__(self, color_list, position, freeze=False, land=False) -> None:
        self._color_list = color_list
        self._position = position
        self._freeze = freeze
        self._land = land

    def change_faller_status_to_land(self) -> None:
        """Change self._land to True"""
        self._land = True

    def change_faller_status_to_freeze(self) -> None:
        """Change self._freeze to True"""
        self._freeze = True

    def change_faller_status_to_falling(self) -> None:
        """Change self._land to False"""
        self._land = False

    def color_list(self) -> list:
        """Return the color list of the faller"""
        return self._color_list

    def faller_is_land(self) -> bool:
        """Return True if faller is land, return False otherwise"""
        return self._land

    def faller_is_freeze(self) -> bool:
        """Return True if faller is freeze, return False otherwise"""
        return self._freeze

    def rotate_color_list(self) -> list:
        """Change the color_list to the rotated color list, and return the rotated color list"""
        rotated_color = [self._color_list[-1]]+self._color_list[: -1]
        self._color_list = rotated_color
        return self._color_list

    def falling_color_list(self) -> list:
        """Change the symbol of color in color list to falling state"""
        color_list = self._color_list
        for i in range(len(color_list)):
            if len(color_list[i]) != 1:
                color_list[i] = f'[{color_list[i][1]}]'
            else:
                color_list[i] = f'[{color_list[i]}]'
        self._color_list = color_list
        return self._color_list

    def land_color_list(self) -> None:
        """Change the symbol of color in color list to land state"""
        color_list = self._color_list
        for i in range(len(color_list)):
            if len(color_list[i]) != 1:
                color_list[i] = f'|{color_list[i][1]}|'
            else:
                color_list[i] = f'|{color_list[i]}|'
        self._color_list = color_list

    def freeze_color_list(self) -> None:
        """Change the symbol of color in color list to freeze state"""
        color_list = self._color_list
        for i in range(len(color_list)):
            color_list[i] = f' {color_list[i][1]} '
        self._color_list = color_list

    def position(self) -> list:
        """Return the position of the faller"""
        return self._position

    def update_position(self, new_pos: tuple) -> None:
        """Update the position of the faller with new position"""
        self._position = new_pos


class GameState():
    def __init__(self) -> None:
        self._game_board = None
        self._game_running = True
        self._faller = False
        self._matching = False
        self._row = 13
        self._col = 6
        self._color_reference = {
            1: 'R', 2: 'W', 3: 'Y', 4: 'B', 5: 'O', 6: 'G', 7: 'P'}

    def choose_col_num_for_faller(self) -> int:
        """
        Randomly choose a col number for faller
        Make sure adding the faller wont cause the game over"""
        game_board = self.current_game_board()
        while True:
            col = randint(0, 5)
            if game_board[3][col] == ' ':
                return col

    def create_new_faller(self) -> Faller:
        """Create a new faller with random color in random column number"""
        color = []
        col = self.choose_col_num_for_faller()
        for i in range(3):
            random_num = randint(1, 7)
            color.append(self._color_reference[random_num])
        return Faller(color, col)

    def faller_on_gameboard(self) -> bool:
        """Return True if there is currently a faller falling down, return False otherwise"""
        return self._faller

    def a_faller_is_falling(self) -> None:
        """Set self_faller to True"""
        self._faller = True

    def reset_faller_status_on_gameboard(self) -> None:
        """Set self._faller to False"""
        self._faller = False

    def there_is_a_match(self) -> bool:
        """Return the matching status"""
        return self._matching

    def change_matching_status_to_True(self) -> bool:
        """Change self._matching to True"""
        self._matching = True

    def change_matching_status_to_False(self) -> bool:
        """Change self._matching to False"""
        self._matching = False

    def is_valid_column_number(self, col: int) -> bool:
        """Given a column number, return True if it is a valid column number"""
        return 0 <= col < self._col

    def is_valid_row_number(self, row: int) -> bool:
        """Given a row number, return True if it is a valid row number"""
        return 0 <= row < self._row

    def update_game_board(self, new_board: list[list[str]]) -> None:
        """Update the game board with the new board"""
        self._game_board = new_board

    def current_game_board(self) -> list[list[str]]:
        """Return the current game board"""
        return self._game_board

    def game_is_running(self) -> bool:
        """Return the game status, return True if the game is running, return False otherwise"""
        return self._game_running

    def stop_running(self) -> None:
        """Change the game status to False"""
        self._game_running = False

    def check_valid_column_number(self, column_number: int) -> None:
        '''Raises a ValueError if its parameter is not a valid column number'''
        if type(column_number) != int or not self.is_valid_column_number(column_number):
            raise ValueError

    def check_valid_row_number(self, row_number: int) -> None:
        '''Raises a ValueError if its parameter is not a valid column number'''
        if type(row_number) != int or not self.is_valid_row_number(row_number):
            raise ValueError

    def create_empty_board(self, row: int, column: int):
        """Given row and column, create and return a empty board"""
        game_board = []
        lst = []
        for j in range(column):
            lst.append(' ')
        for i in range(row+2):
            game_board.append(deepcopy(lst))
        self._game_board = game_board

    def three_in_a_row(self, board: list[list[str]], row: int, col: int, rowdelta: int,  coldelta: int) -> bool:
        """
        Given board, row number, col number, rowdelta, and coldelta, check if three same character matching.
        If there is matching, it will mark the character with *
        This function check one row at a time
        """
        start_cell = board[row][col]
        match = []
        if start_cell == ' ':
            match.append(False)
        else:
            for i in range(0, 3):
                if self.is_valid_column_number(col+coldelta*i) and self.is_valid_row_number(row+rowdelta*i) and (board[row + rowdelta * i][col + coldelta * i] == start_cell or (len(str(board[row+rowdelta*i][col+coldelta*i])) == 3 and str(board[row+rowdelta*i][col+coldelta*i][1]) == str(start_cell))):
                    match.append(True)
                else:
                    match.append(False)

        if False not in match:
            for i in range(0, 1000):
                try:
                    if '*' not in str(board[row+rowdelta*i][col+coldelta*i]) and board[row+rowdelta*i][col+coldelta*i] == start_cell:
                        board[row+rowdelta*i][col +
                                              coldelta*i] = f'*{start_cell}*'
                        self.update_game_board(board)
                except IndexError:
                    break
            return True
        else:
            return False

    def matching_sequence_begin_at(self, row: int, col: int) -> bool:
        """Given row number and col number, check if matching sequence appear"""
        board = self.current_game_board()
        return (self.three_in_a_row(board, row, col, 0, 1)
                or self.three_in_a_row(board, row, col, 1, 1)
                or self.three_in_a_row(board, row, col, 1, 0)
                or self.three_in_a_row(board, row, col, 1, -1)
                or self.three_in_a_row(board, row, col, 0, -1)
                or self.three_in_a_row(board, row, col, -1, -1)
                or self.three_in_a_row(board, row, col, -1, 0)
                or self.three_in_a_row(board, row, col, -1, 1))

    def matching(self) -> None:
        """
        Check the entire board and if there is matching it will mark the matching character with *
        """
        self.make_element_in_board_down()
        rows = self._row
        columns = self._col
        change = []
        for row in range(rows):
            for col in range(columns):
                if self.matching_sequence_begin_at(row, col):
                    change.append(True)
                    self.update_game_board(self.current_game_board())
        self.update_game_board(self.current_game_board())
        if True in change:
            self.change_matching_status_to_True()

    def draw_game_board(self) -> None:
        """Draw the current game board"""
        game_board = self.current_game_board()[2:]
        result = ''
        for row in game_board:
            result += '|'
            for col in row:
                if len(col) == 1:
                    result += f' {col} '
                else:
                    result += col
            result += '|\n'
        result += f" {'-' * 3 * len(game_board[0])} "
        print(result)

    def make_element_in_board_down(self) -> None:
        """Make all element in the board down"""
        board = self.current_game_board()
        for i in range(len(board)):
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if r != len(board)-1 and board[r][c] != ' ' and board[r+1][c] == ' ':
                        board[r+1][c] = board[r][c]
                        board[r][c] = ' '
        self.update_game_board(board)

    def update_matching_game_board(self) -> list[list[str]]:
        """
        Replace characters that are matching from the board with empty space.
        """
        game_board = self.current_game_board()
        while any('*' in ele for row in self.current_game_board() for ele in row):
            for r in range(len(game_board)):
                for c in range(len(game_board[r])):
                    if '*' in game_board[r][c]:
                        game_board[r][c] = ' '
        self.make_element_in_board_down()
        self.update_game_board(game_board)

    def add_faller(self, faller: Faller) -> None:
        """
        Given a Faller object, check if the colors are valid.
        If the faller colors are valid, it will add faller to the board
        """
        self.a_faller_is_falling()
        if not(self.new_faller_will_land(faller)):
            color_list = faller.falling_color_list()
        else:
            faller.change_faller_status_to_land()
            faller.land_color_list()
            color_list = faller.color_list()
        col_num = faller.position()
        game_board = self.current_game_board()
        new_position = []
        for r in range(len(color_list)):
            game_board[r][col_num] = color_list[r]
            new_position.append((r, col_num))
        faller.update_position(new_position)

    def new_faller_will_land(self, faller: Faller) -> bool:
        """Given a Faller object, check if new faller will land immediately after add"""
        col_num = faller.position()
        game_board = self.current_game_board()
        if game_board[3][col_num] != ' ':
            return True
        else:
            return False

    def game_over_action(self) -> None:
        """
        When determine that the game is over, it will draw the current gameboard,
        change the status to stop running and print GAME OVER
        """
        self.draw_game_board()
        self.stop_running()
        print("GAME OVER")

    def freeze_faller_action(self, faller: Faller) -> None:
        """
        Given a Faller object, change the faller state
        to freeze, and update faller status on gameboard.
        Check matching and draw the gameboard
        """
        faller.change_faller_status_to_freeze()
        faller.freeze_color_list()
        self.freeze_board()
        self.reset_faller_status_on_gameboard()
        self.matching()

    def land_faller_action(self, faller: Faller) -> None:
        """Given a Faller object, change the faller state to land, update the board"""
        faller.change_faller_status_to_land()
        faller.land_color_list()
        self.land_board()

    def enter_action(self, faller=None) -> None:
        """
        Perform enter action, move every element in the faller down
        The function also check the status of the faller and update it if necessary
        If the faller freeze it will also check if the game is over
        """
        game_board = self.current_game_board()
        if self.there_is_a_match():
            self.update_matching_game_board()
            self.change_matching_status_to_False()
        elif faller is not None:
            game_board = self.current_game_board()
            faller_position = faller.position()
            faller_list = faller.color_list()
            new_position = []
            if (faller_position[-1][0] == len(game_board)-1 or faller.faller_is_land()):
                self.freeze_faller_action(faller)
                if self.game_is_over() and not(self.there_is_a_match()):
                    self.game_over_action()
            else:
                for index in range(len(faller_list)):
                    row = faller_position[index][0]
                    col = faller_position[index][1]
                    if index == 0:
                        game_board[row][col] = ' '
                    if row+1 <= len(game_board)-1:
                        game_board[row+1][col] = faller_list[index]
                        new_position.append((row+1, col))
                    if faller_position[-1][0]+1 == len(game_board)-1 or (faller_position[-1][0]+2 < len(game_board) and game_board[faller_position[-1][0]+2][faller_position[-1][1]] != ' '):
                        self.land_faller_action(faller)
            if len(new_position) == 3:
                faller.update_position(new_position)
            self.update_game_board(game_board)

    def rotate_action(self, faller: Faller) -> None:
        """Given a Faller object, rotate the faller and update the gameboard"""
        game_board = self.current_game_board()
        faller_position = faller.position()
        new_faller_list = faller.rotate_color_list()
        for index in range(len(new_faller_list)):
            row = faller_position[index][0]
            col = faller_position[index][1]
            game_board[row][col] = new_faller_list[index]
        self.update_game_board(game_board)

    def move_action(self, faller: Faller, col_delta: int) -> None:
        """
        Given a Faller object and change in column, move the faller and update the gameboard
        The function also handle cases such as change state of faller to falling when the faller move to
        somewhere that there is nothing underneath. Change state of faller to land when the faller move to
        somewhere that there is thing underneath.
        """
        game_board = self.current_game_board()
        faller_position = faller.position()
        faller_list = faller.color_list()
        new_position = []
        largest_row = faller_position[2][0]
        col = faller_position[0][1]
        if largest_row + 1 < len(game_board) and game_board[largest_row+1][col+col_delta] == ' ' and faller.faller_is_land():
            faller.change_faller_status_to_falling()
            faller.falling_color_list()
        if largest_row + 1 < len(game_board) and game_board[largest_row+1][col+col_delta] != ' ' and not(faller.faller_is_land()):
            faller.change_faller_status_to_land()
            faller.land_color_list()
        for index in range(len(faller_list)):
            largest_row = faller_position[index][0]
            col = faller_position[index][1]
            game_board[largest_row][col+col_delta] = faller_list[index]
            game_board[largest_row][col] = ' '
            new_position.append((largest_row, col+col_delta))
        faller.update_position(new_position)
        self.update_game_board(game_board)

    def can_move(self, faller: Faller, col_delta: int) -> bool:
        """Return True if the faller can move, return False otherwise"""
        game_board = self.current_game_board()
        faller_position = faller.position()
        faller_list = faller.color_list()
        for index in range(len(faller_list)):
            row = faller_position[index][0]
            col = faller_position[index][1]
            if col+col_delta >= len(game_board[row]) or game_board[row][col+col_delta] != ' ':
                return False
            elif col_delta == 1 and col+col_delta == 0:
                return False
            elif col_delta == -1 and col+col_delta == -1:
                return False
        return True

    def freeze_board(self) -> None:
        """Change the format of the faller to freeze"""
        board = self.current_game_board()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if '|' in board[i][j]:
                    board[i][j] = board[i][j][1]
        self.update_game_board(board)

    def land_board(self) -> None:
        """Change the format of the faller to land"""
        board = self.current_game_board()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if '[' in board[i][j]:
                    board[i][j] = f'|{board[i][j][1]}|'
        self.update_game_board(board)

    def count_empty_space_in_col(self, col: int) -> int:
        """Count how many empty space in the provide col"""
        self.check_valid_column_number(col)
        game_board = self.current_game_board()
        count = 0
        for r in range(len(game_board)):
            if game_board[r][col] == ' ':
                count += 1
        return count

    def game_is_over(self) -> bool:
        """Return True if the game is over, return False otherwise"""
        num_col = self._col
        for i in range(num_col):
            empty_space = self.count_empty_space_in_col(i)
            if empty_space <= 1:
                return True
        return False

from set import SetType, Set
from square import Square
from number import Number

from colorama import Fore, Style

class InvalidPuzzleInitStringException(Exception):
    pass

class Puzzle(object):
    def __init__(self, initial_state_str):
        if len(initial_state_str) != 81:
            raise InvalidPuzzleInitStringException('Supplied Puzzle init string is not 81 characters long and is thus invalid')

        self._puzzle = []
        self._boxes = [Set(SetType.BOX) for i in range(9)]
        self._rows = [Set(SetType.ROW) for i in range(9)]
        self._columns = [Set(SetType.COLUMN) for i in range(9)]
        self._empty_squares = set()
        self._errors_visible = True

        for index, value in enumerate(initial_state_str):
            row = int(index / 9)
            if row >= len(self._puzzle):
                self._puzzle.append([])
            column = index % 9

            square = Square(value)
            
            self._puzzle[row].append(square)
            square._set_puzzle(self)

            self._box_for(row, column).add_square(square)
            self._rows[row].add_square(square)
            self._columns[column].add_square(square)

            if square.is_empty():
                self._empty_squares.add(square)

        if not self.is_valid():
            raise InvalidPuzzleInitStringException('Supplied Puzzle init string has conflicts and is invalid: \n' + str(self))

    def is_valid(self):
        return all([s.is_valid() for s in (self._boxes + self._rows + self._columns)])

    def is_solved(self):
        return all([s.is_solved() for s in (self._boxes + self._rows + self._columns)])

    def _box_for(self, row_index, col_index):
        box_index = int(row_index / 3) * 3 + int(col_index / 3)
        return self._boxes[box_index]

    def _square_for(self, row_index, col_index):
        return self._puzzle[row_index][col_index]

    def set_square_to(self, row_index, col_index, value):
        square = self._square_for(row_index, col_index)
        square.set(value)

    def solve(self):
        pass_number = 1
        while not self.is_solved():
            squares_solved_this_pass = set()
            for square in self._empty_squares:
                options = square.options
                if len(options) == 1:
                    square.set(options.pop())
                    squares_solved_this_pass.add(square)
            for square in squares_solved_this_pass:
                self._empty_squares.remove(square)
            pass_number += 1
        print(f'Number of passes required: {pass_number}')
        self.display()

    def errors_visible(self):
        return self._errors_visible

    def hide_errors(self):
        self._errors_visible = False

    def show_errors(self):
        self._errors_visible = True

    def display(self):
        print(self)

    def __str__(self):
        s = f'{Style.BRIGHT}┌───────────┬───────────┬───────────┐{Style.RESET_ALL}\n'
        for row_index, row in enumerate(self._puzzle):
            if row_index in [3, 6]:
                s += f'{Style.BRIGHT}├───────────┼───────────┼───────────┤{Style.RESET_ALL}\n'
            s += f'{Style.BRIGHT}│{Style.RESET_ALL} '
            for col_index, square in enumerate(self._puzzle[row_index]):
                if col_index in [3, 6]:
                    s += '│ '
                s += str(square)
                if col_index not in [2, 5, 8]:
                    s += f'{Style.DIM}|{Style.RESET_ALL} '
            s += f'{Style.BRIGHT}│{Style.RESET_ALL}\n'
            if row_index not in [2, 5, 8]:
                s += f'{Style.BRIGHT}├{Style.RESET_ALL} - + - + - ┼ - + - + - ┼ - + - + - {Style.BRIGHT}┤{Style.RESET_ALL}\n'
        s += f'{Style.BRIGHT}└───────────┴───────────┴───────────┘{Style.RESET_ALL}\n'
        return s

from colorama import Fore, Style

from number import Number

class InvalidSquareValueException(Exception):
    pass

class SquareLockedException(Exception):
    pass

class Square(object):
    def __init__(self, value = None):
        if value == ' ':
            value = None
        if not Number.is_valid(value):
            raise InvalidSquareValueException('Invalid initial value for square: ' + str(value))
        self._value = value
        self.locked = value is not None
        self._box = None
        self._row = None
        self._column = None
        self._puzzle = None

    def set(self, value):
        if self.locked:
            raise SquareLockedException('Square is locked and value cannot be set')
        if not Number.is_valid(value):
            raise InvalidSquareValueException('Invalid value for square: ' + str(value))
        self._value = str(value)

    def reset(self):
        if not self.locked:
            self._value = None

    def _set_puzzle(self, puzzle):
        self._puzzle = puzzle

    def _set_box(self, box):
        self._box = box

    def _set_row(self, row):
        self._row = row

    def _set_column(self, column):
        self._column = column

    @property
    def value(self):
        return self._value

    @property
    def linked_squares(self):
        return self._box.squares + \
                self._row.squares + \
                self._column.squares

    @property
    def options(self):
        if self.locked:
            return [self.value]

        options = set(Number.VALID_NUMBERS)
        for square in self.linked_squares:
            options.discard(square.value)

        return options

    def is_valid(self):
        return all(s.is_valid() for s in [self._box, self._row, self._column])

    def is_empty(self):
        return self.value is None

    def __str__(self):
        s = str(self._value or ' ') + ' '
        if self._puzzle.errors_visible() and not self.is_valid():
            s = f'{Fore.RED}{s}'
        if self.locked:
            s = f'{Style.BRIGHT}{Fore.YELLOW}{s}'
        s = f'{s}{Style.RESET_ALL}'
        return s

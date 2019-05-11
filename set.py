import enum

from square import Square

class InvalidSetValuesException(Exception):
    pass

class InvalidSetTypeException(Exception):
    pass

class SetType(enum.Enum):
    BOX = 'Box'
    ROW = 'Row'
    COLUMN = 'Column'

class Set(object):
    def __init__(self, set_type):
        if not isinstance(set_type, SetType):
            raise InvalidSetTypeException('Received invalid value for set_type. Must be of type SetType')

        self._squares = []
        self.set_type = set_type

    def add_square(self, square):
        if not isinstance(square, Square):
            raise InvalidSetValuesException('Received object that is not of type Square')
        if square in self._squares:
            raise InvalidSetValuesException('Received square that was already in set')
        self._squares.append(square)
        if self.set_type == SetType.BOX:
            square._set_box(self)
        elif self.set_type == SetType.ROW:
            square._set_row(self)
        elif self.set_type == SetType.COLUMN:
            square._set_column(self)

    def is_valid(self):
        if len(self._squares) != 9:
            return False

        return len(self.values) == len(set(self.values))

    @property
    def squares(self):
        return self._squares

    @property
    def values(self):
        values = []
        for square in self._squares:
            if square.value:
                values.append(square.value)
        return values

    def is_solved(self):
        for square in self._squares:
            if square.value is None:
                return False

        return self.is_valid()

    def __str__(self):
        s = ''
        if self.set_type == SetType.BOX:
            for index, square in enumerate(self._squares):
                if index in [3, 6]:
                    s += '\n'
                s += str(square)
        elif self.set_type == SetType.COLUMN:
            for square in self._squares:
                s += str(square) + '\n'
        elif self.set_type == SetType.ROW:
            s = ''.join([str(square) for square in self._squares])

        return s

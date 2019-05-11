class InvalidNumberException(Exception):
    pass

class Number(object):
    VALID_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    instance = None

    def __init__(self, value):
        value = str(value)
        if value is None or not Number.is_valid(value):
            raise InvalidNumberException('Number passed in is not valid ' + value)

        self._value = value
        self.count = 0

    @classmethod
    def is_valid(cls, value):
        return value is None or str(value) in cls.VALID_NUMBERS

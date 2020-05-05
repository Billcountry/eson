from datetime import date
from eson.config import EsonExtension


class EsonDate(EsonExtension):
    def should_encode(self, value) -> bool:
        return type(value) == date

    def encode(self, value):
        return dict(year=value.year, month=value.month, day=value.day)

    def decode(self, encoded_value):
        return date(**encoded_value)

#!/usr/bin/env python3
from collections.abc import Mapping
from functools import singledispatch
from itertools import zip_longest
from math import ceil
from more_itertools import sliced
from shutil import get_terminal_size


class Item:
    def __init__(self, string, width):
        self.string = string
        self.width = width

    def __str__(self):
        string = self.string[:self.width]
        return string.ljust(self.width)

    def get_wrapped(self):
        for chunk in sliced(self.string, self.width):
            yield Item(chunk, self.width)


class Column:
    def __init__(self, strings):
        self.strings = strings

    def __iter__(self):
        return self.get_items()

    def get_items(self, width=None):
        if width is None:
            width = self.get_width()
        for string in self.strings:
            yield Item(string, width)

    def get_wrapped_items(self, width):
        for item in self.get_items(width):
            for chunk in item.get_wrapped():
                yield chunk

    def get_width(self):
        return max(map(len, self.strings), default=0)

    @classmethod
    def from_iterable(cls, values):
        strings = map(str, values)
        return cls(list(strings))


class ColumnCalculator:
    def __init__(self, strings, spacing):
        self.strings = strings
        self.spacing = spacing

    def build_columns(self, num_columns):
        num_lines = ceil(len(self.strings) / num_columns)
        return list(map(Column, sliced(self.strings, num_lines)))

    def fits_in_line(self, columns, line_width):
        total_column_widths = sum(col.get_width() for col in columns)
        total_spacing = (len(columns) - 1) * self.spacing
        total_width = total_column_widths + total_spacing + 1
        return total_width <= line_width

    def get_fitting_columns(self, line_width):
        columns = self.build_columns(min(line_width, len(self.strings)))
        while len(columns) > 1 and not self.fits_in_line(columns, line_width):
            columns = self.build_columns(len(columns) - 1)
        return columns


@singledispatch
def get_columns(values, spacing, line_width):
    return ColumnCalculator(
        list(map(str, values)), spacing
    ).get_fitting_columns(line_width)

@get_columns.register(Mapping)
def get_mapping_columns(mapping, spacing, line_width):
    return [
        Column.from_iterable(mapping.keys()),
        Column.from_iterable(mapping.values())
    ]

def iter_lines(columns, spacer):
    for line_items in zip_longest(*columns, fillvalue=""):
        yield spacer.join(map(str, line_items)).rstrip()

def columnize(values, spacer="  ", line_width=None):
    if line_width is None:
        line_width = get_terminal_size().columns
    columns = get_columns(values, len(spacer), line_width)
    return "\n".join(iter_lines(columns, spacer))

def cprint(values, spacer="  ", line_width=None):
    print(columnize(values, spacer, line_width))

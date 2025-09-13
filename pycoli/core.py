#!/usr/bin/env python3
"""Core functionality for pycoli: columns, alignment, screen rendering, and arrangement."""

import math
import shutil
from enum import StrEnum
from itertools import zip_longest


class Alignment(StrEnum):
    LEFT = "<"
    RIGHT = ">"
    CENTER = "^"


class Column:
    """Represents a column with optional fixed width and alignment.
    
    Stores the original items and provides their string representations via iteration.
    """

    def __init__(self, items, width=None, align=Alignment.LEFT):
        """Initialize the column.

        Args:
            items (iterable): The original values for the column.
            width (int or None): Fixed width for the column (must be > 0),
                or None for automatic width.
            align (Alignment): Alignment for the column content.

        Raises:
            ValueError: If width is not None and is not a positive integer.
        """
        self.items = list(items)
        if width is not None:
            if not (isinstance(width, int) and width > 0):
                raise ValueError("width must be a positive integer or None")
        self.width = width
        self.align = align

    def __iter__(self):
        """Iterate over the items as their string representations.

        Yields:
            str: String representation of each item.
        """
        return map(str, self.items)

    def __len__(self):
        """Return the width of the column.

        Returns:
            int: Fixed width if specified, otherwise the maximum string
                length of items.
        """
        if self.width is not None:
            return self.width
        return max(map(len, self), default=0)

    @property
    def template(self):
        """Create a formatting template for this column.

        Returns:
            str: A format string template based on the column width and alignment.
        """
        return f"{{:{self.align}{len(self)}}}"

    def __str__(self):
        """Return the column items as a string, one item per line.

        Returns:
            str: All column items joined with newlines.
        """
        return "\n”.join(self)


class Screen:
    """Render Column instances or mixed data in rows using a specified spacer and width."""

    def __init__(self, model, spacer="  ", width=None):
        """Initialize the screen.

        Args:
            model (iterable): A list containing Column instances, iterables, or
                mixed combinations. Non-Column items will be converted to
                Column instances automatically.
            spacer (str): String used to separate columns.
            width (int or None): Total width for the output (defaults to
                terminal width).
        """
        self.model = model
        self.spacer = spacer
        if width is not None:
            self.width = width
        else:
            self.width = shutil.get_terminal_size((80, 20)).columns

    @property
    def columns(self):
        """Convert model items to Column instances where needed.

        Returns:
            list: List of Column instances.
        """
        columns = []
        for item in self.model:
            if isinstance(item, Column):
                columns.append(item)
            else:
                # Convert any iterable to Column
                columns.append(Column(item))
        return columns

    @property
    def template(self):
        """Create a formatting template by combining column templates.

        Returns:
            str: A format string template combining all column templates with spacer.
        """
        return self.spacer.join(col.template for col in self.columns)

    def __iter__(self):
        """Iterate over the formatted output lines.

        Yields:
            str: Each formatted line.
        """
        if not self.columns:
            return
        
        template = self.template
        
        # Use zip_longest to handle columns of different lengths
        for row_values in zip_longest(*self.columns, fillvalue=""):
            line = template.format(*row_values)
            yield line.rstrip()

    def __str__(self):
        """Return the formatted output as a string.

        Returns:
            str: All formatted lines joined with newlines.
        """
        return "\n".join(self)


def arrange_columns(items, spacer, width, col_widths=None):
    """Arrange items into columns according to the given spacer and width.

    Args:
        items (list): List of items to display.
        spacer (str): String used to separate columns.
        width (int): Total width for the output.
        col_widths (list or None): Optional fixed widths per column.

    Returns:
        list of Column: List of Column instances arranged for display.
    """
    n_items = len(items)
    if n_items == 0:
        return []
    
    for cols in range(n_items, 0, -1):
        rows = math.ceil(n_items / cols)
        columns = [[] for _ in range(cols)]
        for idx, item in enumerate(items):
            col = idx // rows
            columns[col].append(item)
        
        if col_widths is not None:
            col_objs = [
                Column(col, width=col_widths[i] if i < len(col_widths) else None)
                for i, col in enumerate(columns)
            ]
        else:
            col_objs = [Column(col) for col in columns]
        
        col_actual_widths = [len(col) for col in col_objs]
        total_width = sum(col_actual_widths) + len(spacer) * (cols - 1)
        if total_width <= width:
            return col_objs
    
    return [Column(items, width=col_widths[0] if col_widths else None)]


__all__ = [
    "Alignment",
    "Column",
    "Screen",
    "arrange_columns",
]
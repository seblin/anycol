#!/usr/bin/env python3
"""Tests for the pycoli module."""

import unittest
from pycoli import Column, Screen, Alignment, arrange_columns


class TestAlignment(unittest.TestCase):
    """Test the Alignment enum."""

    def test_alignment_values(self):
        """Test that Alignment enum has correct values."""
        self.assertEqual(Alignment.LEFT, "<")
        self.assertEqual(Alignment.RIGHT, ">")
        self.assertEqual(Alignment.CENTER, "^")

    def test_alignment_is_str(self):
        """Test that Alignment values can be used as strings."""
        self.assertEqual(str(Alignment.LEFT), "<")
        self.assertEqual(str(Alignment.RIGHT), ">")
        self.assertEqual(str(Alignment.CENTER), "^")


class TestColumn(unittest.TestCase):
    """Test the Column class."""

    def test_default_alignment(self):
        """Test that default alignment is LEFT."""
        col = Column(["test"])
        self.assertEqual(col.align, Alignment.LEFT)

    def test_custom_alignment(self):
        """Test setting custom alignment."""
        col = Column(["test"], align=Alignment.RIGHT)
        self.assertEqual(col.align, Alignment.RIGHT)

    def test_template_with_left_alignment(self):
        """Test template generation with left alignment."""
        col = Column(["hello", "world"], width=10, align=Alignment.LEFT)
        self.assertEqual(col.template, "{:<10}")

    def test_template_with_right_alignment(self):
        """Test template generation with right alignment."""
        col = Column(["hello", "world"], width=10, align=Alignment.RIGHT)
        self.assertEqual(col.template, "{:>10}")

    def test_template_with_center_alignment(self):
        """Test template generation with center alignment."""
        col = Column(["hello", "world"], width=10, align=Alignment.CENTER)
        self.assertEqual(col.template, "{:^10}")

    def test_template_with_auto_width(self):
        """Test template generation with automatic width calculation."""
        col = Column(["hello", "world"], align=Alignment.RIGHT)
        # Length should be 5 (length of "hello" and "world")
        self.assertEqual(col.template, "{:>5}")

    def test_template_with_zero_width(self):
        """Test template generation with empty column."""
        col = Column([], align=Alignment.CENTER)
        self.assertEqual(col.template, "{:^0}")

    def test_formatting_with_alignments(self):
        """Test actual formatting with different alignments."""
        # Left alignment
        col_left = Column(["hi"], width=5, align=Alignment.LEFT)
        template = col_left.template
        result = template.format("hi")
        self.assertEqual(result, "hi   ")

        # Right alignment
        col_right = Column(["hi"], width=5, align=Alignment.RIGHT)
        template = col_right.template
        result = template.format("hi")
        self.assertEqual(result, "   hi")

        # Center alignment
        col_center = Column(["hi"], width=5, align=Alignment.CENTER)
        template = col_center.template
        result = template.format("hi")
        self.assertEqual(result, " hi  ")


class TestScreen(unittest.TestCase):
    """Test the Screen class with alignment."""

    def test_screen_with_mixed_alignments(self):
        """Test screen rendering with different column alignments."""
        col1 = Column(["A", "BB"], width=4, align=Alignment.LEFT)
        col2 = Column(["1", "22"], width=4, align=Alignment.RIGHT)
        col3 = Column(["X", "YY"], width=4, align=Alignment.CENTER)
        
        screen = Screen([col1, col2, col3], spacer=" | ")
        lines = list(screen)
        
        # Detailed breakdown:
        # col1: "A" -> "A   ", "BB" -> "BB  " (left aligned, width 4)
        # col2: "1" -> "   1", "22" -> "  22" (right aligned, width 4)  
        # col3: "X" -> " X  ", "YY" -> " YY " (center aligned, width 4)
        # Line 1: "A   " + " | " + "   1" + " | " + " X  " = "A    |    1 |  X  " -> rstrip() -> "A    |    1 |  X"
        # Line 2: "BB  " + " | " + "  22" + " | " + " YY " = "BB   |   22 |  YY " -> rstrip() -> "BB   |   22 |  YY"
        expected = [
            "A    |    1 |  X",
            "BB   |   22 |  YY"
        ]
        self.assertEqual(lines, expected)

    def test_screen_template_generation(self):
        """Test that screen template combines column templates correctly."""
        col1 = Column(["test"], width=5, align=Alignment.LEFT)
        col2 = Column(["test"], width=3, align=Alignment.RIGHT)
        
        screen = Screen([col1, col2], spacer=" ")
        expected_template = "{:<5} {:>3}"
        self.assertEqual(screen.template, expected_template)

    def test_screen_with_alignment_not_affected_by_rstrip(self):
        """Test that alignment works correctly when not in the last column."""
        col1 = Column(["X", "YY"], width=4, align=Alignment.CENTER)
        col2 = Column(["A", "BB"], width=4, align=Alignment.LEFT)
        
        screen = Screen([col1, col2], spacer=" | ")
        lines = list(screen)
        
        # First column alignment is preserved because it's not the last column
        expected = [
            " X   | A",
            " YY  | BB"
        ]
        self.assertEqual(lines, expected)


class TestArrangeColumns(unittest.TestCase):
    """Test the arrange_columns function."""

    def test_arrange_columns_preserves_default_alignment(self):
        """Test that arrange_columns creates columns with default alignment."""
        items = ["a", "b", "c", "d"]
        columns = arrange_columns(items, "  ", 20)
        
        for col in columns:
            self.assertEqual(col.align, Alignment.LEFT)


if __name__ == "__main__":
    unittest.main()
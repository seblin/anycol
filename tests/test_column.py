#!/usr/bin/env python3
"""Tests for the Column class of pycoli."""

import unittest
from pycoli import Column, Alignment


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

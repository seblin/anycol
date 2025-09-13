#!/usr/bin/env python3
"""Tests for the Screen class of pycoli."""

import unittest
from pycoli import Column, Screen, Alignment


class TestScreen(unittest.TestCase):
    """Test the Screen class with alignment."""

    def test_screen_with_mixed_alignments(self):
        """Test screen rendering with different column alignments."""
        col1 = Column(["A", "BB"], width=4, align=Alignment.LEFT)
        col2 = Column(["1", "22"], width=4, align=Alignment.RIGHT)
        col3 = Column(["X", "YY"], width=4, align=Alignment.CENTER)
        
        screen = Screen([col1, col2, col3], spacer=" | ")
        lines = list(screen)
        
        # Note: line.rstrip() removes trailing spaces from the last column
        expected = [
            "A    |    1 |  X",      # " X  " becomes " X" after rstrip()
            "BB   |   22 |  YY"       # " YY " becomes " YY" after rstrip()
        ]
        self.assertEqual(lines, expected)

    def test_screen_template_generation(self):
        """Test that screen template combines column templates correctly."""
        col1 = Column(["test"], width=5, align=Alignment.LEFT)
        col2 = Column(["test"], width=3, align=Alignment.RIGHT)
        
        screen = Screen([col1, col2], spacer=" ")
        expected_template = "{: <5} {: >3}"
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

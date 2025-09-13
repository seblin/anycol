#!/usr/bin/env python3
"""Tests for the Alignment enum of pycoli."""

import unittest
from pycoli import Alignment


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

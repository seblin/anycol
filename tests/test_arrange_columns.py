#!/usr/bin/env python3
"""Tests for the arrange_columns function of pycoli."""

import unittest
from pycoli import arrange_columns, Alignment


class TestArrangeColumns(unittest.TestCase):
    """Test the arrange_columns function."""

    def test_arrange_columns_preserves_default_alignment(self):
        """Test that arrange_columns creates columns with default alignment."""
        items = ["a", "b", "c", "d"]
        columns = arrange_columns(items, "  ", 20)
        
        for col in columns:
            self.assertEqual(col.align, Alignment.LEFT)

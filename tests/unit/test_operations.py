from __future__ import annotations

import unittest

from django_migration_linter import IgnoreMigration


class IgnoreMigrationTestCase(unittest.TestCase):
    def test_ignore_migration_with_valid_reason(self):
        """Test that IgnoreMigration accepts a valid reason."""
        reason = "This is a valid reason"
        operation = IgnoreMigration(reason)
        self.assertEqual(operation.reason, reason)

    def test_ignore_migration_strips_whitespace(self):
        """Test that IgnoreMigration strips leading and trailing whitespace."""
        reason = "  Valid reason with whitespace  "
        operation = IgnoreMigration(reason)
        self.assertEqual(operation.reason, "Valid reason with whitespace")

    def test_ignore_migration_without_reason_raises_error(self):
        """Test that IgnoreMigration raises ValueError when no reason is provided."""
        with self.assertRaises(TypeError) as _:
            IgnoreMigration()

    def test_ignore_migration_with_empty_string_raises_error(self):
        """Test that IgnoreMigration raises ValueError for empty string."""
        with self.assertRaises(ValueError) as context:
            IgnoreMigration("")
        self.assertIn("non-empty reason", str(context.exception))

    def test_ignore_migration_with_whitespace_only_raises_error(self):
        """Test that IgnoreMigration raises ValueError for whitespace-only string."""
        with self.assertRaises(ValueError) as context:
            IgnoreMigration("   ")
        self.assertIn("non-empty reason", str(context.exception))

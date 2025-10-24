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

    def test_ignore_migration_without_reason_allowed(self):
        """Test that IgnoreMigration can be instantiated without a reason for backward compatibility."""
        operation = IgnoreMigration()
        self.assertIsNone(operation.reason)

    def test_ignore_migration_with_empty_string(self):
        """Test that IgnoreMigration with empty string sets reason to None."""
        operation = IgnoreMigration("")
        self.assertIsNone(operation.reason)

    def test_ignore_migration_with_whitespace_only(self):
        """Test that IgnoreMigration with whitespace-only string sets reason to None."""
        operation = IgnoreMigration("   ")
        self.assertIsNone(operation.reason)

    def test_ignore_migration_describe_with_reason(self):
        """Test that describe() includes reason when provided."""
        reason = "Test reason"
        operation = IgnoreMigration(reason)
        description = operation.describe()
        self.assertIn(reason, description)
        self.assertIn("Reason:", description)

    def test_ignore_migration_describe_without_reason(self):
        """Test that describe() handles missing reason gracefully."""
        operation = IgnoreMigration()
        description = operation.describe()
        self.assertEqual(
            description, "The Django migration linter will ignore this migration"
        )

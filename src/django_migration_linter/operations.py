from __future__ import annotations

from django.db.migrations.operations.base import Operation


class IgnoreMigration(Operation):
    """
    No-op migration operation that will enable the Django Migration Linter
    to detect if the entire migration should be ignored (through code).

    A reason must be provided to document why this migration is being ignored.
    """

    reversible = True
    reduces_to_sql = False
    elidable = True

    def __init__(self, reason: str):
        """
        Initialize IgnoreMigration with a required reason.

        Args:
            reason: A non-empty string explaining why this migration is being ignored.

        Raises:
            ValueError: If reason is empty or contains only whitespace.
        """
        if not reason or not reason.strip():
            raise ValueError("IgnoreMigration requires a non-empty reason")
        self.reason = reason.strip()

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        return (
            f"The Django migration linter will ignore this migration - "
            f"Reason: {self.reason}"
        )

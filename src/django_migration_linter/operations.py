from __future__ import annotations

from django.db.migrations.operations.base import Operation


class IgnoreMigration(Operation):
    """
    No-op migration operation that will enable the Django Migration Linter
    to detect if the entire migration should be ignored (through code).
    """

    reversible = True
    reduces_to_sql = False
    elidable = True

    def __init__(self, reason: str | None = None):
        """
        Initialize IgnoreMigration with an optional reason.

        Args:
            reason: Optional string explaining why this migration is being ignored.
                   For backward compatibility, this parameter is optional, but providing
                   a reason is strongly encouraged and will be enforced during linting
                   for new migrations.
        """
        self.reason = reason.strip() if reason and reason.strip() else None

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        if self.reason:
            return (
                f"The Django migration linter will ignore this migration - "
                f"Reason: {self.reason}"
            )
        return "The Django migration linter will ignore this migration"

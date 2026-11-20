from __future__ import annotations

import re

from .base import BaseAnalyser, Check, CheckMode, CheckType


def has_create_index_in_transaction(sql_statements: list[str], **kwargs) -> bool:
    """Return if a migration opens a transaction, acquires EXCLUSIVE lock, then indexes.

    Any locks that are obtained after a transaction is opened will not be released
    until that transaction either commits or rolls back.

    Accordingly, it's extremely important that a migration avoid any long-running
    queries while exclusive locks are held.

    Building an index is generally a long-running operation. A standard index
    creation (that is, avoiding use of `CONCURRENTLY`) can be safe to run on
    tables which are small in size and/or read-heavy. (`CREATE INDEX` only
    prevents writes to a table; reads are allowed during index creation).

    This check is a stricter version of `CREATE_INDEX` -- if a team wishes
    to build indices nonconcurrently, it's imperative to be mindful of locks.
    """
    if not (sql_statements and sql_statements[0].startswith("BEGIN")):
        return False

    for i, sql in enumerate(sql_statements):
        # If any statements acquire an exclusive lock, complain about index creation
        # later.
        # Nearly every single `ALTER TABLE` command requires an exclusive lock:
        #     https://www.postgresql.org/docs/current/sql-altertable.html
        # (Most common example is `ALTER TABLE... ADD COLUMN`, then later
        # `CREATE INDEX`)
        if sql.startswith("ALTER TABLE"):
            return has_create_index(sql_statements, ignore_concurrently=False)
    return False


def has_create_index(
    sql_statements: list[str], ignore_concurrently: bool = True, **kwargs
) -> bool:
    regex_result = None
    for i, sql in enumerate(sql_statements):
        regex_result = re.search(r"CREATE (UNIQUE )?INDEX.*ON (.*) \(", sql)
        if ignore_concurrently and re.search("INDEX CONCURRENTLY", sql):
            regex_result = None
        if regex_result:
            break
    if not regex_result:
        return False

    preceding_sql_statements = sql_statements[:i]
    concerned_table = regex_result.group(2)
    table_is_added_in_transaction = any(
        sql.startswith(f"CREATE TABLE {concerned_table}")
        for sql in preceding_sql_statements
    )
    return not table_is_added_in_transaction


def has_alter_multiple_tables_in_transaction(
    sql_statements: list[str], **kwargs
) -> bool:
    """Return if a transaction takes ACCESS EXCLUSIVE locks on several tables.

    The locks are taken one statement at a time and all held until commit.
    A live transaction that already holds a lock on a later table and then
    needs an earlier one deadlocks with the migration, and every query on the
    earlier tables queues up behind it in the meantime.
    """
    if not (sql_statements and sql_statements[0].startswith("BEGIN")):
        return False

    created_tables = set()
    altered_tables = set()
    for sql in sql_statements:
        if created := re.match(r"CREATE TABLE (\S+)", sql):
            created_tables.add(created.group(1))
        elif altered := re.match(r"ALTER TABLE (\S+)", sql):
            altered_tables.add(altered.group(1))
    return len(altered_tables - created_tables) > 1


class PostgresqlAnalyser(BaseAnalyser):
    migration_checks: list[Check] = [
        Check(
            code="ALTER_MULTIPLE_TABLES",
            fn=has_alter_multiple_tables_in_transaction,
            message=(
                "ALTERING multiple tables in one transaction can deadlock "
                "(use one migration per table)"
            ),
            mode=CheckMode.TRANSACTION,
            type=CheckType.ERROR,
        ),
        Check(
            code="CREATE_INDEX",
            fn=has_create_index,
            message="CREATE INDEX locks table",
            mode=CheckMode.TRANSACTION,
            type=CheckType.WARNING,
        ),
        Check(
            code="CREATE_INDEX_EXCLUSIVE",
            fn=has_create_index_in_transaction,
            message="CREATE INDEX prolongs transaction, delaying lock release",
            mode=CheckMode.TRANSACTION,
            type=CheckType.WARNING,
        ),
        Check(
            code="DROP_INDEX",
            fn=lambda sql, **kw: re.search("DROP INDEX", sql)
            and not re.search("INDEX CONCURRENTLY", sql),
            message="DROP INDEX locks table",
            mode=CheckMode.ONE_LINER,
            type=CheckType.WARNING,
        ),
        Check(
            code="REINDEX",
            fn=lambda sql, **kw: sql.startswith("REINDEX"),
            message="REINDEX locks table",
            mode=CheckMode.ONE_LINER,
            type=CheckType.WARNING,
        ),
    ]

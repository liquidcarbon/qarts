__doc__ = """qarts/query.py
Query strings - with methods on them.
"""

import typing as t

import duckdb


class Q(str):
    """A SQL query string."""

    def run(
        self, max_rows: int | None = None
    ) -> "tuple[list[str], list[tuple[t.Any, ...]], bool]":
        """Execute and return (columns, rows, truncated).

        The connection is always closed, so rows are materialized before
        returning. If max_rows is given, the returned rows list is truncated
        and truncated=True signals that more rows exist.
        """
        con = duckdb.connect()
        try:
            rel = con.sql(self)
            columns = list(rel.columns)
            rows = rel.fetchall()
        finally:
            con.close()

        truncated = max_rows is not None and len(rows) > max_rows
        return columns, rows[:max_rows], truncated

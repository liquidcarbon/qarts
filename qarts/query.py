__doc__ = """qarts/query.py
Query strings - with methods on them.
"""

import typing as t

import duckdb


class Q(str):
    """A SQL query string."""

    def run(self) -> "duckdb.DuckDBPyRelation":
        con = duckdb.connect()
        return con.sql(self)

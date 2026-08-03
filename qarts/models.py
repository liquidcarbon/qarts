__doc__ = """qarts/models.py
Data models for the qarts server.
"""

import typing as t
from dataclasses import dataclass

from .query import Q


@dataclass
class QueryRequest:
    """A request to execute a SQL query."""

    q: Q
    query_type: t.Literal["sql", "other"] = "sql"


@dataclass
class QueryResponse:
    """The result of executing a query."""

    columns: list[str]
    rows: list[tuple[t.Any, ...]]
    row_count: int
    error: str | None = None

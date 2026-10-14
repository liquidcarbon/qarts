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
    max_rows: int | None = 1000


@dataclass
class QueryResponse:
    """The result of executing a query."""

    columns: list[str]
    rows: list[tuple[t.Any, ...]]
    row_count: int
    truncated: bool = False
    error: str | None = None

__doc__ = """tests/test_qarts.py
Tests for the qarts models.
"""

import duckdb
import pytest

import qarts


def test_q_request_model():
    q = qarts.Q("SELECT 1")
    req = qarts.QueryRequest(q=q)
    assert req.q == q
    assert isinstance(req.q, qarts.Q)


def test_q_run_csv():
    q = qarts.Q(
        "SELECT Symbol, Mass FROM read_csv_auto('tests/test_data/isotopes.csv') "
        "WHERE Symbol = 'H' ORDER BY Mass"
    )
    result = q.run()
    assert result.columns == ["Symbol", "Mass"]
    rows = result.fetchall()
    assert len(rows) == 3
    assert [row[1] for row in rows] == [1.007825, 2.014102, 3.016049]


def test_q_bad_sql():
    q = qarts.Q("SELECT * FROM")
    with pytest.raises(duckdb.ParserException):
        q.run()

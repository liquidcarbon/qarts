__doc__ = """tests/test_server.py
Tests for the qarts server.
"""

import asyncio
import json

from microdot.test_client import TestClient

from qarts.server import app

client = TestClient(app)


def test_root_endpoint():
    resp = asyncio.run(client.post("/"))
    assert resp.status_code == 200
    assert resp.json is not None
    assert resp.json["message"] == "Qarts HTTP server is running."


def test_query_valid_sql():
    resp = asyncio.run(
        client.post(
            "/query",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "q": "SELECT Symbol, Mass FROM read_csv_auto('tests/test_data/isotopes.csv') "
                    "WHERE Symbol = 'H' ORDER BY Mass"
                }
            ),
        )
    )
    assert resp.status_code == 200
    assert resp.json is not None
    assert resp.json["columns"] == ["Symbol", "Mass"]
    assert resp.json["row_count"] == 3
    assert [row[1] for row in resp.json["rows"]] == [1.007825, 2.014102, 3.016049]


def test_query_invalid_sql():
    resp = asyncio.run(
        client.post(
            "/query",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"q": "SELECT * FROM"}),
        )
    )
    assert resp.status_code == 400
    assert resp.json is not None
    assert "error" in resp.json


def test_query_max_rows_truncates():
    resp = asyncio.run(
        client.post(
            "/query",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "q": "SELECT Symbol FROM read_csv_auto('tests/test_data/isotopes.csv')",
                    "max_rows": 5,
                }
            ),
        )
    )
    assert resp.status_code == 200
    assert resp.json is not None
    assert resp.json["truncated"] is True
    assert resp.json["row_count"] == 5
    assert len(resp.json["rows"]) == 5


def test_query_max_rows_none_returns_all():
    resp = asyncio.run(
        client.post(
            "/query",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "q": "SELECT Symbol FROM read_csv_auto('tests/test_data/isotopes.csv')",
                    "max_rows": None,
                }
            ),
        )
    )
    assert resp.status_code == 200
    assert resp.json is not None
    assert resp.json["truncated"] is False
    assert resp.json["row_count"] == 354


def test_query_bad_max_rows_type():
    resp = asyncio.run(
        client.post(
            "/query",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"q": "SELECT 1", "max_rows": "lots"}),
        )
    )
    assert resp.status_code == 400
    assert "max_rows" in resp.json["error"]


def test_shutdown():
    resp = asyncio.run(client.post("/shutdown"))
    assert resp.status_code == 200
    assert resp.json == {"status": "shutting down"}

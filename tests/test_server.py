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

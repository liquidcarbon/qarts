__doc__ = """qarts/server.py
Qarts HTTP server using Microdot.  Bring your own for production use.
"""

import typing as t
from dataclasses import asdict

from microdot import Microdot

from .models import QueryRequest, QueryResponse
from .query import Q

app = Microdot()

DEFAULT_MAX_ROWS = 1000


@app.post("/")
def root(request) -> t.Tuple[dict, int]:
    return {"message": "Qarts HTTP server is running."}, 200


@app.post("/shutdown")
def shutdown(request) -> t.Tuple[dict, int]:
    try:
        request.app.shutdown()
    except AttributeError:
        pass  # server is not running (e.g. from TestClient)
    return {"status": "shutting down"}, 200


@app.post("/query")
def query(request) -> t.Tuple[dict, int]:
    payload: dict = request.json
    if not isinstance(payload, dict):
        return {"error": "request body must be a JSON object"}, 400

    q = Q(str(payload.get("q", "")))
    max_rows = payload.get("max_rows", DEFAULT_MAX_ROWS)
    if max_rows is not None and not isinstance(max_rows, int):
        return {"error": "max_rows must be an int or null"}, 400

    req = QueryRequest(q=q, max_rows=max_rows)

    try:
        columns, rows, truncated = req.q.run(req.max_rows)
        resp = QueryResponse(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            truncated=truncated,
        )
        return asdict(resp), 200
    except Exception as e:
        resp = QueryResponse(
            columns=[],
            rows=[],
            row_count=0,
            error=str(e),
        )
        return asdict(resp), 400

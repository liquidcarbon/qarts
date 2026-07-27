import typing as t
from dataclasses import asdict

from microdot import Microdot

from .models import QueryRequest, QueryResponse
from .query import Q

app = Microdot()


@app.post("/query")
def query(request) -> t.Tuple[dict, int]:
    payload: dict = request.json
    req = QueryRequest(q=Q(payload.get("q", "")))

    try:
        relation = req.q.run()
        rows = relation.fetchall()
        resp = QueryResponse(
            columns=relation.columns,
            rows=rows,
            row_count=len(rows),
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

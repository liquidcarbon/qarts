## 2026-07-27

- Wrote `AGENTS.md`, `DECISIONS.md`, `WORKLOG.md`.

## 2026-07-27

- Created `qarts/models.py` with `QueryRequest` and `QueryResponse` dataclasses.
- Created `qarts/query.py` with `Q(str)` and `execute(path)` backed by DuckDB.
- Created `tests/test_qarts.py` with 4 passing tests (models, CSV execution, error handling).
- Updated `qarts/__init__.py` to expose `Q`, `QueryRequest`, `QueryResponse`.
- Updated `tests/__init__.py`.

## 2026-07-27

- Simplified `QueryRequest` to a single `sql` attribute typed as `Q`, using `t.Annotated` for metadata.
- Simplified `Q` into `Q.run()` with no arguments and no exception handling; returns raw DuckDB relation.
- Updated tests to use `read_csv_auto` inline in SQL and `pytest.raises` for invalid SQL.

## 2026-07-27

- Added `import typing as t` and return-type annotations to `qarts/query.py`.
- Removed `t.TYPE_CHECKING` guard in `models.py`; imported `Q` directly.
- Removed the `rows` field from `QueryResponse` (lists-of-lists are inefficient).
- Removed `test_q_response_model` — the `QueryResponse` shape will be revisited later.

## 2026-07-27

- Implemented `POST /query` endpoint in `qarts/server.py` using Microdot.
- Created `tests/test_server.py` with tests for valid and invalid SQL.
- No TODOs remain in source code.

## 2026-07-27

- Added `rows` back to `QueryResponse` as `list[tuple[t.Any, ...]]`.
- Rewrote server endpoint to strictly use `QueryRequest` and `QueryResponse`.
- Updated `DECISIONS.md` with "Query Execution Engine" and "HTTP Endpoint Types" decisions.

## 2026-07-27

- Created `qarts/cli.py` as the server entry point, keeping `server.py` side-effect-free.
- Added `qarts-server` console script in `pyproject.toml` pointing to `qarts.cli:main`.
- Started server from CLI and verified functionality with a curl command:
    ```bash
    curl -s -X POST http://0.0.0.0:5000/query \
        -H "Content-Type: application/json" \
        -d '{"q": "SELECT COUNT(*) AS count FROM read_csv_auto('\''tests/test_data/isotopes.csv'\'')"}'
    ```

## 2026-08-03

- Implemented `-D`/`--daemon` CLI flag in `qarts/cli.py`.
- Added Unix-only double-fork daemonization (`_daemonize`) with stdio redirection to `/dev/null`.
- Added `tests/test_cli.py` with 5 passing tests covering argument parsing, fork behavior, stdio redirection, and platform guard.

## 2026-08-03

- Implemented `POST /shutdown` endpoint in `qarts/server.py` that calls `request.app.shutdown()`.
- Endpoint gracefully handles `AttributeError` when the server is not running (e.g. from TestClient).
- Added `test_shutdown` to `tests/test_server.py`.

## 2026-10-14

- Compact results: reworked `Q.run(max_rows)` to close its DuckDB connection and return `(columns, rows, truncated)` instead of a lazy relation.
- Added `max_rows` (default 1000) to `QueryRequest` and `truncated` flag to `QueryResponse`.
- `POST /query` now validates `max_rows` type and returns the new shape.
- Added server and model tests for truncation, no-truncation, and bad `max_rows`.
- CLI: added `--host` (default `0.0.0.0`) and `--port` (default `7890`) flags, passed through to `app.run()`.
- Added CLI tests for defaults and custom host/port.
- Verified end-to-end: 19 tests pass; smoke-tested server on `127.0.0.1:7999` with curl (query with `max_rows: 2` returns `truncated: true`; `/shutdown` works).

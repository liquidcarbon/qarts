# This Package

We are building an HTTP interface for SQL and LLM queries on filesystems.

## Consider Arrow Flight

**Decision:** Use ordinary HTTP for the initial API.  Queries can go into GET POST bodies and dare naturally expressed as URLs/POST bodies and responses need only compressed serialized data. 
**Rationale:** HTTP methods fully satisfy current needs.  Arrow Flight is not needed for most use cases and would add protocol complexity.


## Web Framework

**Decision:** [Microdot](https://github.com/miguelgrinberg/microdot)
**Rationale:** Microdot provides the core HTTP framework functionality needed by this package with zero dependencies (as of today). Its route-decorator syntax is similar to the conventions in Flask and FastAPI.


## Data Models

**Decision:** Python `dataclasses` over Pydantic.
**Rationale:** The package needs lightweight structures for representing HTTP requests, query parameters, configuration, and results, but does not currently require Pydantic's validation, serialization, or schema-generation machinery. Standard-library dataclasses keep the dependency footprint minimal and make the data model explicit without introducing infrastructure that is not yet needed. If external input validation becomes sufficiently complex, Pydantic can be reconsidered at that point.


## Client Query Type

**Decision:** `Q` is a subclass of `str`.
**Rationale:** The primary user-facing value is a SQL string; subclassing `str` makes `Q` interchangeable with normal strings while allowing methods like `execute()` to be attached.  This avoids a wrapper object with a `.sql` attribute and keeps the API lightweight.


## Query Execution Engine

**Decision:** DuckDB in an in-memory connection drives query execution.  Queries reference files directly via DuckDB functions such as `read_csv_auto('path')`.
**Rationale:** DuckDB already reads CSV, Parquet, and other formats directly.  Embedding the path in the SQL keeps the API simple and avoids hidden state (temporary views) inside the connection.


## HTTP Endpoint Types

**Decision:** The `POST /query` endpoint consumes `QueryRequest` and produces `QueryResponse` strictly.
**Rationale:** Using the same dataclass types across client and server gives a single source of truth for the request/response contract.  The payload is deserialized into `QueryRequest` (with `Q` wrapping the incoming string), and the response is built as a `QueryResponse` then serialized via `dataclasses.asdict()`.  This enforces shape consistency without adding Pydantic or custom JSON schema machinery.


## Daemon Flag

**Decision:** Support `-D`/`--daemon` via a Unix-only double-fork in the CLI, and do not write PID files.
**Rationale:** Daemonization is a common server need and is easy to implement with `os.fork()` on POSIX systems. PID files add file-system bookkeeping that we decided to skip; users who need PID files already have tools like `pidfile` or can layer that on externally.

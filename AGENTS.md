# This Package

We are building an HTTP interface for SQL and LLM queries on filesystems.


## Running Commands

Folders for python and pytest executables:
- Linux: `./.venv/bin/`
- Windows: `./.venv/Scripts/`

## Development Rules

1. Build incrementally. Implement exactly one feature at a time.
2. Never work on multiple subsystems in the same iteration.
3. Every iteration must leave the repository runnable, internally consistent, and with all tests passing.
4. Write tests before considering a feature complete.
5. Stop after each completed feature and wait for approval before continuing.
6. Keep each change as small and reviewable as possible.
7. Do not introduce infrastructure, abstractions, dependencies, or extension points solely for anticipated future features.
8. Before adding machinery, search the existing codebase for functionality that already serves the purpose.
9. Do not add a dependency without explaining why existing dependencies or the standard library are insufficient.


## At the Beginning of Every Step

Before editing any files:

1. Scan for TODOs and unresolved design notes relevant to the feature under consideration. Start with module docstrings, then class/function docstrings, followed by inline comments.
2. Report relevant TODOs with their location and a brief description. Do not modify or resolve them yet.
3. Identify the next feature and explain why it is the logical next step.  Consult `DECISIONS.md` when historical context is relevant.
4. Identify files that will be created or modified.
5. Stop and wait for approval.


## At the End of Every Step

1. Summarize what was implemented.
2. Report new tests and existing tests that could have been affected.
3. Report assumptions and intentional deviations.
4. Remove completed TODOs from the code.
5. Record durable decisions in `DECISIONS.md` and noteworthy work in
   `WORKLOG.md`.
6. Stop and wait for approval.


## Project Memory

- `DECISIONS.md` records durable architectural/design decisions and their rationale.
- `WORKLOG.md` records noteworthy chronological work and discoveries.
- Completed TODOs do not remain in source code merely as historical records.
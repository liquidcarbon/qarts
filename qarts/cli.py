"""CLI entry point for the qarts server."""

from .server import app


def main() -> None:
    app.run(debug=True)

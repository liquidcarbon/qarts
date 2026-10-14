__doc__ = """qarts/cli.py
CLI entry point for the qarts server.
"""

import argparse
import os
import sys

from .server import app


def _daemonize() -> None:
    """Detach the process into a background daemon (Unix only).

    Similar to gunicorn's `utils.daemonsize`.
    """
    try:
        pid = os.fork()
    except OSError as e:
        raise RuntimeError(f"First fork failed: {e}") from e

    if pid > 0:
        sys.exit(0)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
    except OSError as e:
        raise RuntimeError(f"Second fork failed: {e}") from e

    if pid > 0:
        sys.exit(0)

    # Grandchild continues as the daemon. Redirect stdio to /dev/null.
    for stream in (sys.stdout, sys.stderr):
        stream.flush()
    devnull = os.open(os.devnull, os.O_RDWR)
    for fd in range(3):
        os.dup2(devnull, fd)
    if devnull > 2:
        os.close(devnull)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Qarts HTTP server")
    parser.add_argument(
        "-D",
        "--daemon",
        action="store_true",
        help="Run as a background daemon (Unix only)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host/IP to bind (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7890,
        help="Port to bind (default: 7890)",
    )
    args = parser.parse_args(argv)

    if args.daemon:
        if os.name != "posix":
            parser.error("--daemon is not supported on this platform")
        _daemonize()

    app.run(host=args.host, port=args.port)

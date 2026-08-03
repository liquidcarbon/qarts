__doc__ = """tests/test_cli.py
Tests for the qarts CLI.
"""

import os
from unittest.mock import patch

import pytest

from qarts import cli


def test_cli_daemon_flag():
    with (
        patch("qarts.cli.app.run") as mock_run,
        patch("qarts.cli._daemonize") as mock_daemon,
    ):
        cli.main(["--daemon"])
        mock_daemon.assert_called_once_with()
        mock_run.assert_called_once()


def test_daemonize_first_parent_exits():
    with patch("os.fork", return_value=1):
        with pytest.raises(SystemExit) as exc_info:
            cli._daemonize()
        assert exc_info.value.code == 0


def test_daemonize_second_parent_exits():
    with (
        patch("os.fork", side_effect=[0, 1]) as mock_fork,
        patch("os.chdir"),
        patch("os.setsid"),
        patch("os.umask"),
    ):
        with pytest.raises(SystemExit) as exc_info:
            cli._daemonize()
        assert exc_info.value.code == 0
        assert mock_fork.call_count == 2


def test_daemonize_grandchild_redirects_stdio():
    with (
        patch("os.fork", side_effect=[0, 0]),
        patch("os.chdir"),
        patch("os.setsid"),
        patch("os.umask"),
        patch("os.open", return_value=99) as mock_open,
        patch("os.dup2") as mock_dup2,
        patch("os.close") as mock_close,
        patch("os.getpid", return_value=12345),
    ):
        cli._daemonize()
        mock_open.assert_called_once_with("/dev/null", os.O_RDWR)
        assert mock_dup2.call_count == 3
        mock_close.assert_called_once_with(99)


def test_daemon_not_supported_on_non_posix(capsys):
    with patch("qarts.cli.os.name", "nt"):
        with pytest.raises(SystemExit) as exc_info:
            cli.main(["--daemon"])
        assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "not supported" in captured.err

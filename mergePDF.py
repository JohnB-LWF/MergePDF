#!/usr/bin/env python3
"""Backward-compatible launcher for the MergePDF CLI."""

from cli.main import main


if __name__ == "__main__":
    raise SystemExit(main())

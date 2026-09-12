#!/usr/bin/env python3
"""verify_setup.py - check your environment for Applied AI for Law.

You run this file in Week 1, after you install the tools. It checks that each
tool is installed and prints a green or red result for each one. When every
required line is green, your environment is ready.

Running this file is itself the final test: it is a Python program, so if it
runs and prints a checklist, Python works.

How to run it:
    On macOS:    python3 verify_setup.py
    On Windows:  python verify_setup.py

Standard library only. No internet needed except for the last check.
"""
from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys

# Colours for the terminal. Older Windows terminals do not show them, so we
# turn them off there and use plain text instead.
GREEN = "\033[32m"
RED = "\033[31m"
AMBER = "\033[33m"
RESET = "\033[0m"
if os.name == "nt" and not os.environ.get("WT_SESSION"):
    GREEN = RED = AMBER = RESET = ""

OK = f"{GREEN}[ OK ]{RESET}"
NO = f"{RED}[ -- ]{RESET}"
WARN = f"{AMBER}[ ? ]{RESET}"


def line(symbol: str, name: str, detail: str) -> None:
    print(f"{symbol}  {name:<28} {detail}")


def check_python() -> bool:
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 12)
    detail = f"found {v.major}.{v.minor}.{v.micro}"
    if not ok:
        detail += "  - you need 3.12 or newer"
    line(OK if ok else NO, "Python 3.12 or newer", detail)
    return ok


def check_module(name: str, label: str) -> bool:
    try:
        __import__(name)
        line(OK, label, "available")
        return True
    except Exception:
        line(NO, label, "not found")
        return False


def check_tool(exe: str, label: str, hint: str) -> bool:
    path = shutil.which(exe)
    if path:
        version = ""
        r = _run([exe, "--version"])
        if r and r.stdout:
            version = r.stdout.strip().splitlines()[0]
        line(OK, label, version or f"found ({path})")
        return True
    line(NO, label, f"not found - {hint}")
    return False


def check_internet() -> bool:
    try:
        with socket.create_connection(("github.com", 443), timeout=5):
            line(OK, "Internet (github.com)", "reachable")
            return True
    except OSError:
        line(WARN, "Internet (github.com)", "could not reach github.com - check your network")
        return False


def _run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except Exception:
        return None


def main() -> int:
    print("Applied AI for Law - environment check")
    print("=" * 44)

    results = [
        check_python(),
        check_module("pip", "pip (installs packages)"),
        check_module("venv", "venv (project environments)"),
        check_tool("git", "Git", "install Git, then open a new terminal"),
    ]
    internet_ok = check_internet()  # a warning, not a failure

    print("=" * 44)

    if all(results):
        print(f"\n{GREEN}Your environment is ready.{RESET}")
        print("You just ran a Python program, so Python works. Tell the facilitator you are green.")
        if not internet_ok:
            print("Note: the internet check did not pass. You need it for GitHub later today.")
        return 0

    print(f"\n{RED}Some required checks did not pass.{RESET}")
    print("Fix each red line above, then run this file again.")
    print("If a line stays red after two attempts, ask the facilitator.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

from pathlib import Path

from agent_runner import run_demo


if __name__ == "__main__":
    run_demo(Path(__file__).resolve().parent)

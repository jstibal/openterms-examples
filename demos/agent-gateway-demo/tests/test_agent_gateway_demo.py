from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_runner import run_demo
from policy_engine import LocalOpenTermsPolicy
from report_builder import build_report
from timeline import ActionTrace

BASE = Path(__file__).resolve().parents[1]


def test_policy_decisions() -> None:
    policy = LocalOpenTermsPolicy(BASE / "fixtures" / "openterms.json")
    assert policy.check("read_content").allowed is True
    assert policy.check("scrape_pricing").allowed is False
    assert policy.check("submit_contact_form").allowed is False


def test_demo_outputs_and_trace(tmp_path: Path) -> None:
    demo_dir = tmp_path / "demo"
    demo_dir.mkdir()
    (demo_dir / "fixtures").mkdir()
    (demo_dir / "fixtures" / "openterms.json").write_text((BASE / "fixtures" / "openterms.json").read_text(), encoding="utf-8")
    (demo_dir / "fixtures" / "vendor_page.html").write_text((BASE / "fixtures" / "vendor_page.html").read_text(), encoding="utf-8")

    def fake_browser(url: str, screenshot_path: str | Path, *, headless: bool = True) -> str:
        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
        Path(screenshot_path).write_bytes(b"fake-png")
        return "Northstar Robotics Vendor Portal"

    with patch("agent_runner.open_page_and_capture", side_effect=fake_browser) as mock_browser:
        traces = run_demo(demo_dir)

    assert mock_browser.call_count == 1
    assert len(traces) == 3
    assert (demo_dir / "output" / "final_report.html").exists()
    assert (demo_dir / "output" / "action_trace.json").exists()
    assert (demo_dir / "output" / "read_content.png").exists()

    trace = json.loads((demo_dir / "output" / "action_trace.json").read_text(encoding="utf-8"))
    assert [item["action"] for item in trace] == ["read_content", "scrape_pricing", "submit_contact_form"]
    assert trace[0]["allowed"] is True
    assert trace[0]["browser_executed"] is True
    assert trace[1]["allowed"] is False
    assert trace[1]["browser_executed"] is False
    assert trace[2]["allowed"] is False
    assert trace[2]["browser_executed"] is False
    required = {"step_number", "action", "decision", "allowed", "browser_executed", "reason", "timestamp"}
    for item in trace:
        assert required.issubset(item)


def test_report_contains_expected_sections(tmp_path: Path) -> None:
    traces = [
        ActionTrace.create(step_number=1, action="read_content", decision="allow", allowed=True, browser_executed=True, reason="ok", screenshot_path="read_content.png", page_title="Demo"),
        ActionTrace.create(step_number=2, action="scrape_pricing", decision="deny", allowed=False, browser_executed=False, reason="blocked"),
    ]
    path = tmp_path / "final_report.html"
    build_report(task="demo task", traces=traces, output_path=path)
    html = path.read_text(encoding="utf-8")
    assert "Agent Gateway Demo" in html
    assert "Execution Timeline" in html
    assert "Action Results" in html
    assert "OpenTerms Gateway" in html
    assert "BLOCKED BEFORE EXECUTION" in html
    assert "read_content.png" in html


def test_report_escapes_dynamic_values(tmp_path: Path) -> None:
    traces = [
        ActionTrace.create(
            step_number=1,
            action="<script>alert(1)</script>",
            decision="allow",
            allowed=True,
            browser_executed=True,
            reason="<b>bad</b>",
            screenshot_path="x.png",
            page_title="<title>",
        )
    ]
    path = tmp_path / "report.html"
    build_report(task="<task>", traces=traces, output_path=path)
    html = path.read_text(encoding="utf-8")
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "&lt;b&gt;bad&lt;/b&gt;" in html


def test_no_live_network_required_in_unit_tests() -> None:
    assert (BASE / "fixtures" / "vendor_page.html").exists()
    assert (BASE / "fixtures" / "openterms.json").exists()

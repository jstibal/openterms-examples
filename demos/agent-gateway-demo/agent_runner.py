from __future__ import annotations

from pathlib import Path

from browser_tools import open_page_and_capture
from policy_engine import LocalOpenTermsPolicy
from report_builder import build_report, write_action_trace
from timeline import ActionTrace

TASK = "Research the vendor page, extract pricing information, and submit a contact request."
PLAN = [
    (1, "read_content"),
    (2, "scrape_pricing"),
    (3, "submit_contact_form"),
]


def run_demo(base_dir: str | Path, *, headless: bool = True) -> list[ActionTrace]:
    base_dir = Path(base_dir)
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    policy = LocalOpenTermsPolicy(base_dir / "fixtures" / "openterms.json")
    vendor_page = (base_dir / "fixtures" / "vendor_page.html").resolve().as_uri()
    traces: list[ActionTrace] = []

    print("=" * 60)
    print("OpenTerms Agent Gateway Demo")
    print("=" * 60)
    print(f"TASK:\n{TASK}\n")

    for step_number, action in PLAN:
        print("-" * 60)
        print(f"STEP {step_number} — {action.upper()}")
        print("-" * 60)
        print(f"Agent requested browser action:\n{action}\n")

        decision = policy.check(action)
        decision_label = decision.decision.upper()
        print(f"OpenTerms decision:\n{decision_label}\n")

        if decision.allowed:
            screenshot = output_dir / "read_content.png"
            print("Browser execution:\nLAUNCHED\n")
            title = open_page_and_capture(vendor_page, screenshot, headless=headless)
            print(f"Screenshot captured:\n{screenshot}\n")
            traces.append(
                ActionTrace.create(
                    step_number=step_number,
                    action=action,
                    decision=decision.decision,
                    allowed=True,
                    browser_executed=True,
                    reason=decision.reason,
                    screenshot_path="read_content.png",
                    page_title=title,
                )
            )
        else:
            print("Browser execution:\nBLOCKED BEFORE LAUNCH\n")
            print(f"Reason:\n{decision.reason}\n")
            traces.append(
                ActionTrace.create(
                    step_number=step_number,
                    action=action,
                    decision=decision.decision,
                    allowed=False,
                    browser_executed=False,
                    reason=decision.reason,
                )
            )

    write_action_trace(traces, output_dir / "action_trace.json")
    build_report(task=TASK, traces=traces, output_path=output_dir / "final_report.html")

    allowed = sum(1 for trace in traces if trace.allowed)
    blocked = len(traces) - allowed
    executed = sum(1 for trace in traces if trace.browser_executed)

    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(f"Allowed actions: {allowed}")
    print(f"Blocked actions: {blocked}")
    print(f"Browser executions: {executed}")
    print(f"Blocked before execution: {blocked}")
    print("\nVisual report:")
    print(output_dir / "final_report.html")
    return traces

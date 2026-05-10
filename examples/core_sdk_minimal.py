"""Minimal local OpenTerms permission check. No network calls."""
import json
import os
from openterms import CheckResult

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "fixtures")

def load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES_DIR, f"{name}.json")) as f:
        return json.load(f)

def result_from_fixture(fixture_name: str, action: str) -> CheckResult:
    data = load_fixture(fixture_name)
    status = data.get("permissions", {}).get(action, {}).get("status", "not_specified")
    decision = "allow" if status == "allowed" else ("deny" if status == "denied" else "not_specified")
    return CheckResult(decision=decision, action=action, confidence=1.0)

def main() -> None:
    result = result_from_fixture("allow", "read_content")
    print(f"Decision: {result.decision}")
    print(f"Allowed: {bool(result)}")
    if not result:
        print("Agent halted: action not explicitly allowed.")
    else:
        print("Agent may proceed.")

if __name__ == "__main__":
    main()

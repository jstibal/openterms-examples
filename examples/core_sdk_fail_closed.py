"""Fail-closed OpenTerms example. Only explicit allow proceeds. No network calls."""
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
    action = "scrape_data"
    for fixture in ("allow", "deny", "not_specified", "conditional"):
        result = result_from_fixture(fixture, action)
        print(f"{fixture}: decision={result.decision}, allowed={bool(result)}")
        if not result:
            print("  Agent halted.")
        else:
            print("  Agent may proceed.")

if __name__ == "__main__":
    main()

"""Community-built CrewAI-style usage pattern. CrewAI, Inc. has not reviewed or approved this example. No network calls."""
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

def read_website_content(url: str, fixture_name: str = "allow") -> str:
    result = result_from_fixture(fixture_name, "read_content")
    if not result:
        return f"Action blocked: read_content not permitted ({result.decision})."
    return f"[mock] Content from {url}"

def post_content(url: str, content: str, fixture_name: str = "allow") -> str:
    result = result_from_fixture(fixture_name, "post_content")
    if not result:
        return f"Action blocked: post_content not permitted ({result.decision})."
    return f"[mock] Posted to {url}: {content[:40]}"

def main() -> None:
    for fixture in ("allow", "deny", "not_specified", "conditional"):
        print(f"{fixture}: {read_website_content('https://example.com', fixture)}")

if __name__ == "__main__":
    main()

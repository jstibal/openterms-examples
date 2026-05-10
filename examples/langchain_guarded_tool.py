"""Community-built LangChain guard pattern for OpenTerms. No network calls."""
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

class GuardedScrapeTool:
    name = "scrape_data"
    description = "Scrape data from a web page."

    def __init__(self, fixture_name: str = "allow"):
        self.fixture_name = fixture_name

    def run(self, url: str) -> str:
        result = result_from_fixture(self.fixture_name, "scrape_data")
        if not result:
            raise PermissionError(f"Blocked by OpenTerms: {result.decision}")
        return f"[mock] Scraped content from {url}"

def main() -> None:
    for fixture in ("allow", "deny", "not_specified", "conditional"):
        tool = GuardedScrapeTool(fixture)
        try:
            print(f"{fixture}: {tool.run('https://example.com')}")
        except PermissionError as exc:
            print(f"{fixture}: {exc}")

if __name__ == "__main__":
    main()

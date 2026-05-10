"""Permissive mode requires explicit opt-in. No network calls."""
import json
import os

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "fixtures")

def load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES_DIR, f"{name}.json")) as f:
        return json.load(f)

def check_with_mode(fixture_name: str, action: str, permissive: bool = False) -> bool:
    data = load_fixture(fixture_name)
    status = data.get("permissions", {}).get(action, {}).get("status", "not_specified")
    if status == "denied":
        return False
    if status == "allowed":
        return True
    return permissive

def main() -> None:
    for fixture in ("allow", "deny", "not_specified", "conditional"):
        print(f"{fixture}: strict={check_with_mode(fixture, 'read_content')}, permissive={check_with_mode(fixture, 'read_content', permissive=True)}")

if __name__ == "__main__":
    main()

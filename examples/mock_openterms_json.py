"""Build a mock openterms.json in memory. No network calls."""
from openterms import CheckResult

CANONICAL_KEYS = ["read_content", "scrape_data", "api_access", "create_account", "make_purchases", "post_content", "allow_training"]

def build_mock_openterms(service: str = "mock-service", default_status: str = "not_specified", overrides: dict | None = None) -> dict:
    overrides = overrides or {}
    return {
        "$schema": "https://openterms.com/schema/openterms.schema.json",
        "version": "1.0",
        "service": service,
        "last_updated": "2026-01-01",
        "permissions": {key: {"status": overrides.get(key, default_status)} for key in CANONICAL_KEYS},
    }

def parse_result(openterms_data: dict, action: str) -> CheckResult:
    status = openterms_data.get("permissions", {}).get(action, {}).get("status", "not_specified")
    decision = "allow" if status == "allowed" else ("deny" if status == "denied" else "not_specified")
    return CheckResult(decision=decision, action=action, confidence=1.0)

def main() -> None:
    mock = build_mock_openterms(default_status="denied", overrides={"read_content": "allowed"})
    for key in CANONICAL_KEYS:
        result = parse_result(mock, key)
        print(f"{key}: {result.decision}, allowed={bool(result)}")

if __name__ == "__main__":
    main()

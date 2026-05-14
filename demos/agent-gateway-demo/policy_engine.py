from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PolicyDecision:
    action: str
    decision: str
    allowed: bool
    reason: str


class LocalOpenTermsPolicy:
    def __init__(self, policy_path: str | Path) -> None:
        self.policy_path = Path(policy_path)
        self.policy = json.loads(self.policy_path.read_text(encoding="utf-8"))

    def check(self, action: str) -> PolicyDecision:
        permissions = self.policy.get("permissions", {})
        record = permissions.get(action)
        if record is None:
            return PolicyDecision(
                action=action,
                decision="not_specified",
                allowed=False,
                reason="Action is not listed in the local OpenTerms policy.",
            )
        decision = str(record.get("decision", "not_specified"))
        allowed = decision == "allow"
        return PolicyDecision(
            action=action,
            decision=decision,
            allowed=allowed,
            reason=str(record.get("reason", "No reason provided.")),
        )

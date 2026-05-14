from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class ActionTrace:
    step_number: int
    action: str
    decision: str
    allowed: bool
    browser_executed: bool
    reason: str
    timestamp: str
    screenshot_path: str | None = None
    page_title: str | None = None

    @classmethod
    def create(
        cls,
        *,
        step_number: int,
        action: str,
        decision: str,
        allowed: bool,
        browser_executed: bool,
        reason: str,
        screenshot_path: str | None = None,
        page_title: str | None = None,
    ) -> "ActionTrace":
        return cls(
            step_number=step_number,
            action=action,
            decision=decision,
            allowed=allowed,
            browser_executed=browser_executed,
            reason=reason,
            timestamp=datetime.now(timezone.utc).isoformat(),
            screenshot_path=screenshot_path,
            page_title=page_title,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

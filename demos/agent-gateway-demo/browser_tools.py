from __future__ import annotations

from pathlib import Path


def open_page_and_capture(url: str, screenshot_path: str | Path, *, headless: bool = True) -> str:
    """Open a local page with Playwright, capture screenshot, and return title."""
    from playwright.sync_api import sync_playwright

    screenshot_path = Path(screenshot_path)
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto(url)
        title = page.title()
        page.screenshot(path=str(screenshot_path), full_page=True)
        browser.close()
        return title

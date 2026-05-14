# OpenTerms Agent Gateway Demo

This is a deterministic local demo showing how OpenTerms can act as a runtime permission gate between an agent and browser tools.

The demo task is:

> Research the vendor page, extract pricing information, and submit a contact request.

The scripted agent attempts three actions:

1. `read_content`
2. `scrape_pricing`
3. `submit_contact_form`

The local OpenTerms policy allows `read_content` and blocks `scrape_pricing` and `submit_contact_form`. The browser executes only the allowed action.

## What this demonstrates

- OpenTerms checks occur before browser actions.
- Blocked actions do not execute browser automation.
- Screenshots are produced only for allowed actions.
- The final report shows the agent plan, permission decisions, browser execution state, and action trace.

## What this does not demonstrate

This demo uses local fixtures. It does not prove website-owner approval or any permission beyond the local fixture result.

## Run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
python demo.py
```

Open:

```bash
open output/final_report.html
open output/read_content.png
```

## Outputs

- `output/final_report.html`
- `output/action_trace.json`
- `output/read_content.png`

## Tests

```bash
pytest -q
```

No LLM API key is required. No live website is accessed. The demo uses `fixtures/vendor_page.html` and `fixtures/openterms.json` so results are reproducible.

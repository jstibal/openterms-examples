from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Iterable

from timeline import ActionTrace


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def write_action_trace(traces: Iterable[ActionTrace], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([trace.to_dict() for trace in traces], indent=2),
        encoding="utf-8",
    )


def build_report(
    *,
    task: str,
    traces: list[ActionTrace],
    output_path: str | Path,
) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = len(traces)
    allowed = sum(1 for t in traces if t.allowed)
    blocked = total - allowed
    executed = sum(1 for t in traces if t.browser_executed)

    cards = []
    timeline_items = []
    for trace in traces:
        state_class = "allowed" if trace.allowed else "blocked"
        state_label = "ALLOWED" if trace.allowed else "BLOCKED BEFORE EXECUTION"
        browser_state = "Browser launched" if trace.browser_executed else "Browser did not launch"
        screenshot = ""
        if trace.screenshot_path:
            screenshot = f'<img class="shot" src="{_esc(trace.screenshot_path)}" alt="Screenshot for {_esc(trace.action)}" />'
        cards.append(
            f"""
            <article class="action-card {state_class}">
              <div class="card-top"><span class="step">STEP {_esc(trace.step_number)}</span><span class="pill">{state_label}</span></div>
              <h3>{_esc(trace.action)}</h3>
              <p class="reason">{_esc(trace.reason)}</p>
              <dl>
                <div><dt>Decision</dt><dd>{_esc(trace.decision)}</dd></div>
                <div><dt>Browser</dt><dd>{_esc(browser_state)}</dd></div>
                <div><dt>Timestamp</dt><dd>{_esc(trace.timestamp)}</dd></div>
              </dl>
              {screenshot}
            </article>
            """
        )
        timeline_items.append(
            f"""
            <li class="timeline-row {state_class}">
              <span class="dot"></span>
              <div><strong>{_esc(trace.action)}</strong><br><span>{state_label} · {_esc(browser_state)}</span></div>
            </li>
            """
        )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenTerms Agent Gateway Demo</title>
  <style>
    :root {{ --bg:#080b14; --panel:#111827; --muted:#aab6cc; --line:rgba(255,255,255,.12); --green:#34d399; --red:#fb7185; --blue:#7dd3fc; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top left, rgba(59,130,246,.18), transparent 34%), var(--bg); color:#eef5ff; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 42px 24px 64px; }}
    header {{ display: grid; grid-template-columns: 72px 1fr; gap: 18px; align-items: center; padding: 24px; border:1px solid var(--line); border-radius: 28px; background: rgba(17,24,39,.72); box-shadow: 0 26px 90px rgba(0,0,0,.35); }}
    header img {{ width:72px; height:72px; }}
    h1 {{ margin:0; font-size: 44px; line-height:1; }}
    .subtitle {{ margin: 10px 0 0; color: var(--muted); font-size:18px; }}
    .summary {{ display:grid; grid-template-columns: 2fr repeat(4, 1fr); gap:14px; margin: 22px 0; }}
    .metric, .task {{ border:1px solid var(--line); background: rgba(255,255,255,.055); border-radius:22px; padding:18px; }}
    .metric b {{ display:block; font-size:32px; }}
    .metric span, .task span {{ color: var(--muted); font-size:13px; text-transform:uppercase; letter-spacing:.06em; }}
    .task p {{ margin:8px 0 0; color:#e7edf8; font-size:18px; }}
    .main {{ display:grid; grid-template-columns: .85fr 1.15fr; gap:22px; }}
    section {{ border:1px solid var(--line); background: rgba(17,24,39,.66); border-radius:28px; padding:24px; }}
    h2 {{ margin:0 0 18px; }}
    .timeline {{ list-style:none; padding:0; margin:0; position:relative; }}
    .timeline:before {{ content:""; position:absolute; left:13px; top:12px; bottom:12px; width:2px; background: rgba(255,255,255,.12); }}
    .timeline-row {{ display:grid; grid-template-columns:30px 1fr; gap:12px; margin:0 0 22px; position:relative; }}
    .dot {{ width:28px; height:28px; border-radius:999px; background:var(--panel); border:4px solid var(--blue); z-index:1; }}
    .timeline-row.allowed .dot {{ border-color: var(--green); }}
    .timeline-row.blocked .dot {{ border-color: var(--red); }}
    .timeline-row span {{ color: var(--muted); }}
    .cards {{ display:grid; gap:16px; }}
    .action-card {{ border:1px solid var(--line); border-left:6px solid var(--blue); background: rgba(255,255,255,.055); border-radius:24px; padding:18px; }}
    .action-card.allowed {{ border-left-color: var(--green); }}
    .action-card.blocked {{ border-left-color: var(--red); }}
    .card-top {{ display:flex; justify-content:space-between; align-items:center; gap:12px; }}
    .step {{ color: var(--muted); font-size:12px; letter-spacing:.08em; }}
    .pill {{ border-radius:999px; padding:7px 10px; font-size:12px; font-weight:800; background:rgba(125,211,252,.13); }}
    .allowed .pill {{ background:rgba(52,211,153,.16); color:#a7f3d0; }}
    .blocked .pill {{ background:rgba(251,113,133,.16); color:#fecdd3; }}
    h3 {{ margin: 10px 0 6px; font-size:24px; }}
    .reason {{ color: var(--muted); margin:0 0 14px; }}
    dl {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin:0 0 14px; }}
    dt {{ color:var(--muted); font-size:12px; }} dd {{ margin:4px 0 0; font-weight:700; }}
    .shot {{ width:100%; border-radius:16px; border:1px solid var(--line); margin-top:8px; }}
    .diagram {{ margin-top:22px; display:grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap:12px; align-items:center; }}
    .node {{ padding:16px; border-radius:20px; background:rgba(255,255,255,.065); border:1px solid var(--line); text-align:center; font-weight:800; }}
    .arrow {{ color:var(--blue); font-size:26px; }}
    footer {{ color: var(--muted); margin-top:22px; text-align:center; }}
    @media (max-width: 900px) {{ .summary,.main,.diagram {{ grid-template-columns:1fr; }} .arrow {{ transform: rotate(90deg); }} dl {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <img src="../assets/openterms-logo.svg" alt="OpenTerms" />
      <div>
        <h1>Agent Gateway Demo</h1>
        <p class="subtitle">OpenTerms checked each agent action before browser execution.</p>
      </div>
    </header>
    <div class="summary">
      <div class="task"><span>Agent task</span><p>{_esc(task)}</p></div>
      <div class="metric"><span>Attempted</span><b>{total}</b></div>
      <div class="metric"><span>Allowed</span><b>{allowed}</b></div>
      <div class="metric"><span>Blocked</span><b>{blocked}</b></div>
      <div class="metric"><span>Browser runs</span><b>{executed}</b></div>
    </div>
    <div class="main">
      <section>
        <h2>Execution Timeline</h2>
        <ol class="timeline">{''.join(timeline_items)}</ol>
        <div class="diagram">
          <div class="node">Agent</div><div class="arrow">↓</div><div class="node">OpenTerms Gateway</div><div class="arrow">↓</div><div class="node">Browser Tool or Block</div>
        </div>
      </section>
      <section>
        <h2>Action Results</h2>
        <div class="cards">{''.join(cards)}</div>
      </section>
    </div>
    <footer>Deterministic local demo. No LLM API key or live website required.</footer>
  </div>
</body>
</html>"""
    output_path.write_text(html_doc, encoding="utf-8")

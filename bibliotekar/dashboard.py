"""
entity_id=dashboard_module; type=module; state=ready

Static HTML dashboard for observing wiki state.  No web server dependency.
"""
from __future__ import annotations

import html
from pathlib import Path


def build_dashboard(base_dir: Path) -> Path:
    wiki_dir = base_dir / "wiki"
    out = base_dir / "dashboard.html"
    pages = sorted(p for p in wiki_dir.glob("**/*.md") if p.is_file())
    index_text = (wiki_dir / "index.md").read_text(encoding="utf-8", errors="ignore") if (wiki_dir / "index.md").exists() else ""
    log_text = (wiki_dir / "log.md").read_text(encoding="utf-8", errors="ignore") if (wiki_dir / "log.md").exists() else ""
    cards = []
    by_dir = {}
    for p in pages:
        rel = p.relative_to(wiki_dir)
        by_dir.setdefault(str(rel.parent), 0)
        by_dir[str(rel.parent)] += 1
    for key, value in sorted(by_dir.items()):
        cards.append(f"<div class='card'><b>{html.escape(key)}</b><br>{value} pages</div>")
    page_list = "\n".join(f"<li>{html.escape(str(p.relative_to(wiki_dir)))}</li>" for p in pages)
    content = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Bibliotekar Dashboard</title>
<style>
body{{font-family:Arial,sans-serif;margin:24px;line-height:1.4;background:#fafafa;color:#111}}
.card{{display:inline-block;padding:12px;margin:6px;border:1px solid #ddd;border-radius:10px;background:white}}
pre{{white-space:pre-wrap;background:white;border:1px solid #ddd;padding:12px;border-radius:8px;max-height:360px;overflow:auto}}
</style></head><body>
<h1>Bibliotekar Dashboard</h1>
<h2>Counts</h2>{''.join(cards)}
<h2>Pages</h2><ul>{page_list}</ul>
<h2>Index</h2><pre>{html.escape(index_text[-8000:])}</pre>
<h2>Log</h2><pre>{html.escape(log_text[-8000:])}</pre>
</body></html>"""
    out.write_text(content, encoding="utf-8")
    return out

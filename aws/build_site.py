#!/usr/bin/env python3
"""Assemble aws/site/ from the kit: landing page, rendered prep guide, graph, BI view, repo browser."""
import html
import pathlib
import shutil

KIT = pathlib.Path(__file__).resolve().parent.parent
SITE = pathlib.Path(__file__).resolve().parent / "site"
REPO = KIT / "legacy-payments-monolith"

CSS = """<style>
:root{--bg:#faf9f5;--fg:#141413;--muted:#6b6a64;--card:#fff;--line:#d9d7cf;--acc:#c2562f}
@media(prefers-color-scheme:dark){:root{--bg:#1f1e1d;--fg:#f0eee6;--muted:#a8a69c;--card:#2a2928;--line:#44423e;--acc:#e8845f}}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,sans-serif}
.w{max-width:900px;margin:0 auto;padding:24px 16px 48px}a{color:var(--acc)}
.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.c{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--fg)}
.c b{display:block;margin-bottom:4px}.c span{color:var(--muted);font-size:13px}
pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;overflow:auto;font-size:13px}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid var(--line);padding:6px 8px;text-align:left}
code{font-size:13px}
</style>"""


def page(title, body):
    return (f"<!doctype html><html lang=en><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>{CSS}</head>"
            f"<body><div class=w><p><a href='/'>&larr; Home</a></p>{body}</div></body></html>")


def render_md(text):
    try:
        import markdown
        return markdown.markdown(text, extensions=["tables", "fenced_code"])
    except ImportError:
        return f"<pre>{html.escape(text)}</pre>"


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "repo").mkdir(parents=True)
    shutil.copy(REPO / "outputs" / "graph.html", SITE / "graph.html")
    shutil.copy(REPO / "outputs" / "business-impact.html", SITE / "business-impact.html")
    (SITE / "prep-guide.html").write_text(page("Prep guide", render_md((KIT / "PREP-GUIDE.md").read_text())))

    # Repo browser: every text file rendered as an escaped page
    files = sorted(p for p in REPO.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts and p.suffix not in {".pyc"})
    rows = []
    for p in files:
        rel = p.relative_to(REPO).as_posix()
        out = SITE / "repo" / (rel + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(rel, f"<h2>{html.escape(rel)}</h2><pre>{html.escape(p.read_text())}</pre>"))
        rows.append(f"<tr><td><a href='/repo/{rel}.html'>{html.escape(rel)}</a></td></tr>")
    (SITE / "repo" / "index.html").write_text(
        page("Repo files", "<h2>Demo repo files</h2><table>" + "".join(rows) + "</table>"))

    cards = [
        ("prep-guide.html", "Prep guide", "Run of show, slide copy, demo runbook, Q&amp;A"),
        ("graph.html", "Dependency map", "Interactive: where the monolith needs cutting"),
        ("business-impact.html", "Business impact view", "Non-technical mobile speed and ROI model"),
        ("repo/index.html", "Demo repo", "Legacy code, skills, EKS manifests, analyzer"),
    ]
    body = ("<h1>Claude Code at FinTechCo: prep site</h1><p style='color:var(--muted)'>Synthetic demo data only.</p><div class=g>"
            + "".join(f"<a class=c href='/{h}'><b>{t}</b><span>{d}</span></a>" for h, t, d in cards) + "</div>")
    (SITE / "index.html").write_text(
        "<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>Prep site</title>{CSS}</head><body><div class=w>{body}</div></body></html>")
    print(f"built {SITE} ({sum(1 for _ in SITE.rglob('*.html'))} pages)")


if __name__ == "__main__":
    main()

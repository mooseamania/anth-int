#!/usr/bin/env python3
"""Inline outputs/graph.json into tools/graph_template.html -> outputs/graph.html"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
graph = (ROOT / "outputs" / "graph.json").read_text()
json.loads(graph)  # validate
html = (ROOT / "tools" / "graph_template.html").read_text().replace("__GRAPH__", graph)
(ROOT / "outputs" / "graph.html").write_text(html)
print("wrote outputs/graph.html")

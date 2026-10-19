#!/usr/bin/env python3
"""Static coupling analysis for fintechco_core.

Builds: import graph, data-coupling graph (shared db tables), cycles, fan-in/out,
and scores a proposed service split by how many edges cross each boundary.
Outputs outputs/graph.json and outputs/boundaries.md.  Stdlib + networkx.
"""
import ast
import json
import pathlib
import sys

import networkx as nx

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = ROOT / "fintechco_core"
OUT = ROOT / "outputs"

# Modules every other module leans on: candidates for a shared library, not a service.
PLATFORM = {"config", "db", "utils"}

# Proposed bounded contexts (the hypothesis we test against measured coupling).
PROPOSED = {
    "auth": "identity", "accounts": "identity",
    "ledger": "ledger-core",
    "payments": "payments-core", "fraud": "payments-core",
    "notifications": "notifications",
    "reporting": "reporting-bi", "batch_jobs": "reporting-bi",
    "mobile_api": "mobile-bff",
    "config": "platform-lib", "db": "platform-lib", "utils": "platform-lib",
}


def modules():
    return sorted(p.stem for p in PKG.glob("*.py") if p.stem != "__init__")


def parse(mod):
    src = (PKG / f"{mod}.py").read_text()
    tree = ast.parse(src)
    imports, tables = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "fintechco_core":
            imports.update(a.name for a in node.names)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "table" and node.args
                and isinstance(node.args[0], ast.Constant)):
            tables.add(node.args[0].value)
    return imports, tables, len(src.splitlines())


def main():
    mods = modules()
    G = nx.DiGraph()
    table_users, meta = {}, {}
    for m in mods:
        imports, tables, loc = parse(m)
        meta[m] = {"loc": loc, "tables": sorted(tables)}
        G.add_node(m)
        for i in imports:
            if i in mods:
                G.add_edge(m, i)
        for t in tables:
            table_users.setdefault(t, set()).add(m)

    cycles = [sorted(c) for c in nx.strongly_connected_components(G) if len(c) > 1]
    in_cycle = {m for c in cycles for m in c}

    nodes = []
    for m in mods:
        nodes.append({
            "id": m, "loc": meta[m]["loc"], "service": PROPOSED.get(m, "unassigned"),
            "fan_in": G.in_degree(m), "fan_out": G.out_degree(m),
            "tables": meta[m]["tables"], "in_cycle": m in in_cycle,
            "platform": m in PLATFORM,
        })

    edges = []
    for a, b in G.edges:
        cross = PROPOSED[a] != PROPOSED[b]
        edges.append({"source": a, "target": b, "cross_service": cross,
                      "to_platform": b in PLATFORM,
                      "in_cycle": a in in_cycle and b in in_cycle})

    # Boundary quality: edges that cross services (excluding platform lib) = APIs we must create.
    hard = [e for e in edges if e["cross_service"] and not e["to_platform"]]
    internal = [e for e in edges if not e["cross_service"]]

    # Shared-table coupling: tables touched by modules in >1 service = data ownership problems.
    shared_tables = {
        t: sorted(users) for t, users in table_users.items()
        if len({PROPOSED[u] for u in users if u not in PLATFORM}) > 1
    }

    # Data-driven check: undirected modularity communities vs proposal.
    U = G.to_undirected()
    U.remove_nodes_from(PLATFORM & set(U.nodes))
    comms = [sorted(c) for c in nx.algorithms.community.greedy_modularity_communities(U)]

    graph = {
        "nodes": nodes, "edges": edges, "cycles": cycles,
        "shared_tables": shared_tables, "detected_communities": comms,
        "summary": {
            "modules": len(mods), "total_loc": sum(n["loc"] for n in nodes),
            "import_edges": len(edges), "cross_service_edges": len(hard),
            "internal_edges": len(internal), "cycles": len(cycles),
            "shared_tables": len(shared_tables),
        },
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "graph.json").write_text(json.dumps(graph, indent=2))

    # Human report
    L = ["# Boundary analysis: fintechco_core", ""]
    s = graph["summary"]
    L += [f"- {s['modules']} modules, {s['total_loc']} LOC, {s['import_edges']} import edges",
          f"- Edges that would become network/API calls: **{s['cross_service_edges']}** "
          f"(internal to a service: {s['internal_edges']})",
          f"- Circular dependencies: **{s['cycles']}** -> {cycles}",
          f"- Tables touched by more than one service: **{s['shared_tables']}**", ""]
    L += ["## Hotspots (fan-in / fan-out)", "", "| module | fan-in | fan-out | proposed service |", "|---|---|---|---|"]
    for n in sorted(nodes, key=lambda n: -(n["fan_in"] + n["fan_out"])):
        L.append(f"| {n['id']} | {n['fan_in']} | {n['fan_out']} | {n['service']} |")
    L += ["", "## Cross-service calls to turn into APIs / events", ""]
    for e in hard:
        L.append(f"- {e['source']} ({PROPOSED[e['source']]}) -> {e['target']} ({PROPOSED[e['target']]})")
    L += ["", "## Shared tables (need a single owner)", ""]
    for t, u in shared_tables.items():
        L.append(f"- `{t}`: {', '.join(u)}")
    L += ["", "## Independent check: modularity communities (platform libs removed)", ""]
    for c in comms:
        L.append(f"- {', '.join(c)}")
    (OUT / "boundaries.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())

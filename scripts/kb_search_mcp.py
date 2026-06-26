#!/usr/bin/env python3
"""
Stdio MCP server — semantic search over chris-kb.
Tool: kb_search(query, top_k=5)
Add to Claude Code MCP config as a stdio server.
"""
import sys, json
import numpy as np
from pathlib import Path
from openai import OpenAI

INDEX_DIR  = Path(__file__).parent.parent / ".kb-search"
EMB_FILE   = INDEX_DIR / "embeddings.npy"
META_FILE  = INDEX_DIR / "metadata.json"
MODEL      = "text-embedding-3-small"

client     = OpenAI()
_emb       = None
_meta      = None


def load():
    global _emb, _meta
    if _emb is None:
        _emb  = np.load(EMB_FILE).astype(np.float32)
        _meta = json.loads(META_FILE.read_text())


def search(query: str, top_k: int = 5) -> list[dict]:
    load()
    vec  = np.array(client.embeddings.create(model=MODEL, input=[query]).data[0].embedding,
                    dtype=np.float32)
    norms = np.linalg.norm(_emb, axis=1)
    sims  = (_emb @ vec) / (norms * np.linalg.norm(vec) + 1e-9)
    top   = np.argsort(sims)[::-1][:top_k]
    return [{**_meta[i], "score": float(sims[i])} for i in top]


TOOLS = [{
    "name": "kb_search",
    "description": (
        "Semantic search over the chris-kb knowledge base. "
        "Returns the most relevant sections with file paths and excerpts."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "query":  {"type": "string",  "description": "Natural language search query"},
            "top_k":  {"type": "integer", "description": "Results to return (default 5)", "default": 5}
        },
        "required": ["query"]
    }
}]


def ok(id, result):
    return json.dumps({"jsonrpc": "2.0", "id": id, "result": result})

def err(id, code, msg):
    return json.dumps({"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": msg}})


def handle(req: dict) -> str | None:
    method = req.get("method", "")
    id     = req.get("id")

    if method == "initialize":
        return ok(id, {
            "protocolVersion": "2024-11-05",
            "capabilities":    {"tools": {}},
            "serverInfo":      {"name": "kb-search", "version": "1.0.0"}
        })
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return ok(id, {"tools": TOOLS})
    if method == "tools/call":
        name = req.get("params", {}).get("name")
        args = req.get("params", {}).get("arguments", {})
        if name == "kb_search":
            try:
                results = search(args.get("query", ""), args.get("top_k", 5))
                text = "\n\n".join(
                    f"**{r['path']}** — {r['header']} (score: {r['score']:.3f})\n{r['text']}"
                    for r in results
                )
                return ok(id, {"content": [{"type": "text", "text": text}]})
            except Exception as e:
                return err(id, -32000, str(e))
        return err(id, -32601, f"Unknown tool: {name}")
    return err(id, -32601, f"Unknown method: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        if resp:
            print(resp, flush=True)


if __name__ == "__main__":
    main()

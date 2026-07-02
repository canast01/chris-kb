#!/usr/bin/env python3
"""
FastAPI HTTP server wrapping the KB semantic search index.
Usage: python3 scripts/kb_search_api.py
Then open: http://localhost:8765
"""
import json
from pathlib import Path

import numpy as np
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
from pydantic import BaseModel

INDEX_DIR = Path(__file__).parent.parent / ".kb-search"
EMB_FILE  = INDEX_DIR / "embeddings.npy"
META_FILE = INDEX_DIR / "metadata.json"
HTML_FILE = Path(__file__).parent / "kb_search.html"
MODEL     = "text-embedding-3-small"
KB_BASE   = "https://chrisanastasiadis.com"

client = OpenAI()
_emb: np.ndarray | None = None
_meta: list[dict] | None = None


def _load():
    global _emb, _meta
    if _emb is None:
        _emb  = np.load(EMB_FILE).astype(np.float32)
        _meta = json.loads(META_FILE.read_text())


def _path_to_url(path: str) -> str:
    p = path.removeprefix("docs/")
    if p.endswith("/index.md"):
        return KB_BASE + "/" + p[: -len("/index.md")] + "/"
    if p.endswith(".md"):
        return KB_BASE + "/" + p[:-3] + "/"
    return KB_BASE + "/" + p


def _search(query: str, top_k: int) -> list[dict]:
    _load()
    vec   = np.array(
        client.embeddings.create(model=MODEL, input=[query]).data[0].embedding,
        dtype=np.float32,
    )
    norms = np.linalg.norm(_emb, axis=1)
    sims  = (_emb @ vec) / (norms * np.linalg.norm(vec) + 1e-9)
    top   = np.argsort(sims)[::-1][:top_k]
    results = []
    for i in top:
        m = _meta[i]
        text = m["text"]
        # Strip frontmatter and SVG lines for cleaner excerpts
        lines = [l for l in text.splitlines()
                 if not l.startswith("---") and "```" not in l
                 and not l.startswith("![") and l.strip()]
        excerpt = " ".join(lines)[:280].strip()
        results.append({
            "path":    m["path"],
            "header":  m["header"],
            "excerpt": excerpt,
            "score":   round(float(sims[i]), 4),
            "url":     _path_to_url(m["path"]),
        })
    return results


app = FastAPI(title="KB Search", docs_url=None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup():
    _load()


@app.get("/", response_class=FileResponse)
def index():
    return HTML_FILE


@app.get("/search")
def search(q: str = Query(..., min_length=2), top_k: int = Query(default=8, ge=1, le=20)):
    results = _search(q, top_k)
    return JSONResponse({"results": results})


class SearchRequest(BaseModel):
    query: str
    top_k: int = 8


@app.post("/search")
def search_post(req: SearchRequest):
    return JSONResponse({"results": _search(req.query, req.top_k)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")

#!/usr/bin/env python3
"""
Index chris-kb docs with OpenAI text-embedding-3-small.
Incremental: only re-embeds files whose content changed.
Run: python3 scripts/kb_embed.py
"""
import json, hashlib, sys, time, re
import numpy as np
from pathlib import Path
from openai import OpenAI, RateLimitError

DOCS_DIR   = Path(__file__).parent.parent / "docs"
INDEX_DIR  = Path(__file__).parent.parent / ".kb-search"
EMB_FILE   = INDEX_DIR / "embeddings.npy"
META_FILE  = INDEX_DIR / "metadata.json"
HASH_FILE  = INDEX_DIR / "hashes.json"
MODEL      = "text-embedding-3-small"
BATCH      = 20
BATCH_PACE = 5.5   # seconds between batches to stay under 40K TPM

client = OpenAI()


def chunk_file(path: Path, text: str) -> list[dict]:
    chunks, current, header = [], [], path.stem
    for line in text.splitlines():
        if line.startswith("## ") or line.startswith("### "):
            body = "\n".join(current).strip()
            if body:
                chunks.append({"header": header, "text": body})
            header = line.lstrip("#").strip()
            current = [line]
        else:
            current.append(line)
    body = "\n".join(current).strip()
    if body:
        chunks.append({"header": header, "text": body})
    return chunks or [{"header": path.stem, "text": text.strip()}]


def embed_batch(texts: list[str]) -> list[list[float]]:
    for attempt in range(8):
        try:
            resp = client.embeddings.create(model=MODEL, input=texts)
            return [r.embedding for r in resp.data]
        except RateLimitError as e:
            m = re.search(r'try again in (\d+\.?\d*)s', str(e))
            wait = float(m.group(1)) + 2 if m else 20 * (attempt + 1)
            print(f"  rate limit — waiting {wait:.0f}s...", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("Exceeded retry limit")


def fhash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main():
    INDEX_DIR.mkdir(exist_ok=True)

    saved_emb  = np.load(EMB_FILE)                   if EMB_FILE.exists()   else None
    metadata   = json.loads(META_FILE.read_text())   if META_FILE.exists()  else []
    hashes     = json.loads(HASH_FILE.read_text())   if HASH_FILE.exists()  else {}

    md_files   = sorted(DOCS_DIR.rglob("*.md"))
    all_paths  = {str(f.relative_to(DOCS_DIR.parent)) for f in md_files}
    print(f"Files: {len(md_files)}")

    changed, unchanged = [], set()
    for f in md_files:
        rel = str(f.relative_to(DOCS_DIR.parent))
        h   = fhash(f)
        if hashes.get(rel) == h:
            unchanged.add(rel)
        else:
            changed.append((f, rel, h))

    print(f"Unchanged: {len(unchanged)}  |  Changed/new: {len(changed)}")

    # Seed new index with unchanged rows
    new_meta = [m for m in metadata if m["path"] in unchanged]
    new_vecs = []
    if saved_emb is not None and new_meta:
        keep = [i for i, m in enumerate(metadata) if m["path"] in unchanged]
        new_vecs = list(saved_emb[keep])

    if changed:
        all_chunks = []
        for f, rel, h in changed:
            try:
                text   = f.read_text(encoding="utf-8", errors="ignore")
                chunks = chunk_file(f, text)
                for c in chunks:
                    all_chunks.append({"path": rel, "header": c["header"],
                                       "text": c["text"][:2000], "file_hash": h})
            except Exception as e:
                print(f"  skip {rel}: {e}", file=sys.stderr)

        print(f"Embedding {len(all_chunks)} chunks...")
        chunk_vecs = []
        for i in range(0, len(all_chunks), BATCH):
            batch = all_chunks[i:i+BATCH]
            texts = [f"{c['header']}\n\n{c['text']}" for c in batch]
            chunk_vecs.extend(embed_batch(texts))
            done = min(i + BATCH, len(all_chunks))
            print(f"  {done}/{len(all_chunks)}")
            if done < len(all_chunks):
                time.sleep(BATCH_PACE)

        for chunk, vec in zip(all_chunks, chunk_vecs):
            new_meta.append({"path": chunk["path"], "header": chunk["header"],
                             "text": chunk["text"][:500]})
            new_vecs.append(vec)

        for _, rel, h in changed:
            hashes[rel] = h
        hashes = {k: v for k, v in hashes.items() if k in all_paths}

    if new_vecs:
        np.save(EMB_FILE, np.array(new_vecs, dtype=np.float32))
    META_FILE.write_text(json.dumps(new_meta, indent=2))
    HASH_FILE.write_text(json.dumps(hashes, indent=2))
    print(f"Done. Index: {len(new_meta)} chunks from {len(all_paths)} files.")


if __name__ == "__main__":
    main()

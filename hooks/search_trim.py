"""Shrink search/search_index.json after the build by removing code blocks (<pre>...</pre>).

Pages themselves are unchanged; only the search index loses code-block text.
Titles, headings, body text and inline code stay searchable.
"""
import json
import os
import re

from mkdocs.plugins import event_priority

PRE_BLOCK = re.compile(r"<pre[^>]*>.*?</pre>", re.S)


@event_priority(-100)  # run after the search plugin has written the index
def on_post_build(config, **kwargs):
    path = os.path.join(config["site_dir"], "search", "search_index.json")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for doc in data.get("docs", []):
        if "text" in doc:
            doc["text"] = PRE_BLOCK.sub(" ", doc["text"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

"""Fail the build if two source files produce the same page URL.

Example: foo.md and foo/index.md both build to foo/. MkDocs silently keeps
one and drops the other, and the duplicate search entry breaks site search.
"""
from collections import defaultdict

from mkdocs.exceptions import PluginError


def on_files(files, config, **kwargs):
    seen = defaultdict(list)
    for f in files.documentation_pages():
        seen[f.dest_uri].append(f.src_uri)
    clashes = {k: v for k, v in seen.items() if len(v) > 1}
    if clashes:
        lines = [f"  {dest}: {', '.join(srcs)}" for dest, srcs in sorted(clashes.items())]
        raise PluginError("Pages that build to the same URL:\n" + "\n".join(lines))
    return files

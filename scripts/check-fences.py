#!/usr/bin/env python3
"""PostToolUse hook: validate code-fence parity in edited markdown files."""
import json, sys, re

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

file_path = data.get("tool_input", {}).get("file_path", "")

# Only process markdown files inside the docs/ tree
if not file_path.endswith(".md") or "/docs/" not in file_path:
    sys.exit(0)

try:
    text = open(file_path).read()
except OSError:
    sys.exit(0)

# Count opening vs closing fences (``` blocks)
opens = len(re.findall(r"^```\S*\s*$", text, re.MULTILINE))
closes = len(re.findall(r"^```\s*$", text, re.MULTILINE))
unclosed = opens - closes

if unclosed != 0:
    print(f"FENCE WARNING: {file_path} has {unclosed} unclosed code fence(s)", file=sys.stderr)
    sys.exit(1)

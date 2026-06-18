#!/usr/bin/env python3
import sys, json, re

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path") or \
       (data.get("tool_response") or {}).get("filePath") or ""

if not (path.endswith(".md") and "/docs/" in path):
    sys.exit(0)

try:
    lines = open(path).read().splitlines()
except Exception:
    sys.exit(0)

in_fence = False
tag = None
fence_line = 0
untagged = 0

for i, line in enumerate(lines):
    s = line.rstrip()
    if not in_fence:
        m = re.match(r"^```(\S*)$", s)
        if m:
            in_fence = True
            tag = m.group(1)
            fence_line = i + 1
            if not tag:
                untagged += 1
    else:
        if re.match(r"^```$", s):
            in_fence = False
            tag = None

issues = []
if untagged:
    issues.append(f"{untagged} untagged fence(s)")
if in_fence:
    issues.append(f"unclosed fence at L{fence_line}")

if issues:
    rel = path.split("/docs/")[-1]
    print(json.dumps({"systemMessage": f"Fence issue in {rel}: {', '.join(issues)}"}))

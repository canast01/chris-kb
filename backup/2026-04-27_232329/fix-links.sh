#!/usr/bin/env bash

set -e

echo
echo "Running backup first..."
echo

if [ -f "./backup.sh" ]; then
  ./backup.sh
else
  echo "ERROR: backup.sh not found."
  exit 1
fi

echo
echo "Fixing relative links across documentation..."
echo

find docs -type f -name "*.md" | while read file; do

  # Replace local directory links with index.md
  sed -i '' -E '
    s|\]\(([a-zA-Z0-9._/-]+)/\)|](\1/index.md)|g
  ' "$file"

done

echo
echo "All links fixed."
echo
echo "Next step:"
echo "mkdocs serve --clean"
echo

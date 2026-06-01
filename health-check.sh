#!/usr/bin/env bash
set -e

echo "== Health check =="

echo
echo "Current path:"
pwd

echo
echo "Markdown page count:"
find docs -name "*.md" | wc -l | tr -d ' '

echo
echo "Top section counts:"
for d in docs/*; do
  if [ -d "$d" ]; then
    count="$(find "$d" -name "*.md" | wc -l | tr -d ' ')"
    echo "$(basename "$d"): $count"
  fi
done

echo
echo "Checking required files..."
for f in mkdocs.yml docs/index.md docs/stylesheets/extra.css; do
  if [ -f "$f" ]; then
    echo "OK: $f"
  else
    echo "MISSING: $f"
    exit 1
  fi
done

echo
echo "Checking required scripts..."
for f in backup.sh validate-site.sh health-check.sh preview-site.sh safe-change.sh; do
  if [ -x "$f" ]; then
    echo "OK: $f"
  else
    echo "MISSING OR NOT EXECUTABLE: $f"
    exit 1
  fi
done

echo
echo "Checking for placeholder links..."
if grep -R 'href="#"' docs >/dev/null 2>&1; then
  echo "Found placeholder href links:"
  grep -R 'href="#"' docs
  exit 1
else
  echo "OK: no placeholder href links"
fi

echo
echo "Checking for empty markdown files..."
empty_files="$(find docs -name "*.md" -size 0)"
if [ -n "$empty_files" ]; then
  echo "$empty_files"
  exit 1
else
  echo "OK: no empty markdown files"
fi

echo
echo "Health check complete."

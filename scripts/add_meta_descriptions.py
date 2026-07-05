"""
Add a meta `description:` field to page frontmatter, derived from the
existing kb-summary block, for pages that don't already have one.

Why: mkdocs-material uses frontmatter `description:` for the page's
<meta name="description"> tag (SEO + social-link-preview text). As of
2026-07-04, only 3/2847 pages had one -- everything else falls back to a
generic/truncated snippet.

Usage:
  python3 scripts/add_meta_descriptions.py               # dry-run, report only
  python3 scripts/add_meta_descriptions.py --apply        # write frontmatter
  python3 scripts/add_meta_descriptions.py --apply path/to/one.md
"""
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
KB_SUMMARY_RE = re.compile(r'<div class="kb-summary">\s*\n(.*?)\n</div>', re.DOTALL)
APPLIES_TO_RE = re.compile(r'^\*Applies to:.*?\*\s*$', re.MULTILINE)
MD_STRIP_RE = re.compile(r'`([^`]*)`|\*\*([^*]*)\*\*|\*([^*]*)\*')
MAX_LEN = 155


def derive_description(text: str) -> str | None:
    m = KB_SUMMARY_RE.search(text)
    if not m:
        return None
    body = APPLIES_TO_RE.sub('', m.group(1)).strip()
    # collapse markdown emphasis/code markers to plain text
    body = MD_STRIP_RE.sub(lambda mo: next(g for g in mo.groups() if g is not None), body)
    body = re.sub(r'\s+', ' ', body).strip()
    if not body:
        return None
    if len(body) > MAX_LEN:
        cut = body[:MAX_LEN].rsplit(' ', 1)[0]
        body = cut.rstrip('.,;:') + '...'
    # YAML-safe: escape embedded double quotes
    return body.replace('"', "'")


def process_file(path: Path, dry_run: bool):
    text = path.read_text(encoding='utf-8')
    fm = FRONTMATTER_RE.match(text)
    if not fm:
        return None  # no frontmatter block at all -- skip, handled separately
    if re.search(r'^description:', fm.group(1), re.MULTILINE):
        return None  # already has one

    desc = derive_description(text)
    if not desc:
        return ('NO_KB_SUMMARY', None)

    new_fm = fm.group(1) + f'\ndescription: "{desc}"'
    new_text = text[:fm.start(1)] + new_fm + text[fm.end(1):]
    if not dry_run:
        path.write_text(new_text, encoding='utf-8')
    return ('OK', desc)


def main():
    dry_run = '--apply' not in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    files = [Path(a) for a in args] if args else sorted(Path('docs').rglob('*.md'))

    ok, no_summary, has_desc_already = 0, 0, 0
    for f in files:
        result = process_file(f, dry_run)
        if result is None:
            has_desc_already += 1
            continue
        status, desc = result
        if status == 'OK':
            ok += 1
            print(f'{f}: "{desc}"')
        else:
            no_summary += 1
            print(f'{f}: NO KB-SUMMARY -- needs manual description')

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f'\n{mode}: {ok} descriptions added, {no_summary} need manual review '
          f'(no kb-summary to derive from), {has_desc_already} already had one')


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Regenerate stats in docs/site-quality.md and docs/usage-metrics.md.

Run after bulk changes (new pages, diagram additions, tag updates):
    python3 scripts/update_admin_pages.py

Updates:
  - "Generated: YYYY-MM-DD" date lines
  - Stats tables (total pages, diagram counts, tag counts, audit score)
  - ASCII diagram box content totals
"""

import os, re, datetime, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
TODAY = datetime.date.today().isoformat()


def all_md():
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
        for f in sorted(files):
            if f.endswith('.md'):
                yield os.path.join(root, f)


def compute_stats():
    pages = list(all_md())
    total = len(pages)

    # Content sections (top-level dirs, excluding utility dirs)
    exclude = {'assets', 'images', 'icons', 'stylesheets', 'overrides',
               'offline', 'stats', 'javascripts'}
    sections = {
        d: sum(1 for r, _, fs in os.walk(os.path.join(DOCS, d))
               for f in fs if f.endswith('.md'))
        for d in os.listdir(DOCS)
        if os.path.isdir(os.path.join(DOCS, d)) and d not in exclude and not d.startswith('.')
    }
    top_sections = sorted(sections.items(), key=lambda x: -x[1])

    has_ascii = has_svg = has_mermaid = has_summary = has_tags = 0
    for p in pages:
        try:
            text = open(p, errors='replace').read()
        except Exception:
            continue
        if any(c in text for c in '┌│└'):
            has_ascii += 1
        if re.search(r'!\[.*?\]\(.*?\.svg\)', text):
            has_svg += 1
        if '```mermaid' in text:
            has_mermaid += 1
        if 'kb-summary' in text:
            has_summary += 1
        if re.search(r'^tags:', text, re.MULTILINE):
            has_tags += 1

    # Audit score (quick: count passing checks)
    try:
        result = subprocess.run(
            ['python3', 'scripts/site_audit.py'],
            capture_output=True, text=True, cwd=REPO
        )
        total_checks = len(re.findall(r'✅ Clean', result.stdout))
        fail_checks = len(re.findall(r'❌', result.stdout))
        audit_score = f'{total_checks} / {total_checks + fail_checks}'
    except Exception:
        audit_score = '?'

    return {
        'total': total,
        'section_count': len(top_sections),
        'has_ascii': has_ascii,
        'has_svg': has_svg,
        'has_mermaid': has_mermaid,
        'has_summary': has_summary,
        'has_tags': has_tags,
        'audit_score': audit_score,
        'top3': top_sections[:3],
        'sections': top_sections,
    }


def update_file(path, stats):
    content = open(path).read()

    # Update "Generated:" date
    content = re.sub(r'Generated: \d{4}-\d{2}-\d{2}', f'Generated: {TODAY}', content)

    # Update "Updated YYYY-MM-DD" inside the ASCII box
    content = re.sub(r'Updated \d{4}-\d{2}-\d{2}', f'Updated {TODAY}', content)

    # Update stat table rows — match "| Label | Number |" rows
    replacements = {
        r'(Total markdown pages\s*\|)\s*[\d,]+':
            rf'\g<1> {stats["total"]:,}',
        r'(Pages with full-width ASCII diagram[s]?\s*\|)\s*[\d,]+':
            rf'\g<1> {stats["has_ascii"]:,}',
        r'(Pages with SVG diagram[s]?\s*\|)\s*[\d,]+':
            rf'\g<1> {stats["has_svg"]:,}',
        r'(Pages with Mermaid diagram[s]?\s*\|)\s*[\d,]+':
            rf'\g<1> {stats["has_mermaid"]:,}',
        r'(Pages with kb-summary\s*\|)\s*[\d,]+':
            rf'\g<1> {stats["has_summary"]:,}',
        r'(Pages with tags\s*\|)\s*[\d,]+':
            rf'\g<1> {stats["has_tags"]:,}',
        r'(Audit score\s*\|)\s*[^\n]+\|':
            rf'\g<1> {stats["audit_score"]} |',
    }
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    # Update ASCII diagram box content totals line
    # "Total pages:       N,NNN" format
    content = re.sub(
        r'(Total pages:\s+)[\d,]+',
        lambda m: m.group(1) + f'{stats["total"]:,}',
        content
    )
    content = re.sub(
        r'(Sections:\s+)[\d,]+',
        lambda m: m.group(1) + f'{stats["section_count"]}',
        content
    )
    content = re.sub(
        r'(ASCII diagrams:\s+)[\d,]+',
        lambda m: m.group(1) + f'{stats["has_ascii"]:,}',
        content
    )
    content = re.sub(
        r'(SVG diagrams:\s+)[\d,]+',
        lambda m: m.group(1) + f'{stats["has_svg"]:,}',
        content
    )
    content = re.sub(
        r'(Mermaid diagrams:\s+)[\d,]+',
        lambda m: m.group(1) + f'{stats["has_mermaid"]:,}',
        content
    )
    content = re.sub(
        r'(kb-summary divs:\s+)[\d,]+',
        lambda m: m.group(1) + f'{stats["has_summary"]:,}',
        content
    )
    # Update "Audit score: N/N clean" in ASCII box
    content = re.sub(
        r'(Audit score: )[\d/]+ clean',
        lambda m: m.group(1) + f'{stats["audit_score"]} clean',
        content
    )

    with open(path, 'w') as f:
        f.write(content)
    return content


def main():
    print('Computing stats...')
    stats = compute_stats()
    print(f'  Total pages:     {stats["total"]:,}')
    print(f'  ASCII diagrams:  {stats["has_ascii"]:,}')
    print(f'  SVG diagrams:    {stats["has_svg"]:,}')
    print(f'  Mermaid:         {stats["has_mermaid"]:,}')
    print(f'  kb-summary:      {stats["has_summary"]:,}')
    print(f'  Tags:            {stats["has_tags"]:,}')
    print(f'  Audit score:     {stats["audit_score"]}')

    for fname in ('site-quality.md', 'usage-metrics.md'):
        path = os.path.join(DOCS, fname)
        if os.path.exists(path):
            update_file(path, stats)
            print(f'Updated {fname}')
        else:
            print(f'SKIP {fname} (not found)')

    print(f'\nDone. Generated: {TODAY}')


if __name__ == '__main__':
    main()

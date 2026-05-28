#!/usr/bin/env python3
"""
Fetch Cloudflare Web Analytics data and write docs/stats/index.md.
Run from repo root. Requires env vars:
  CF_API_TOKEN  — Cloudflare API token (Account Analytics: Read)
  CF_ACCOUNT_ID — Cloudflare account ID (visible in dash.cloudflare.com URL)
  CF_SITE_TAG   — Web Analytics site tag (from URL when viewing site in Cloudflare)
"""
import os, sys, json, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

TOKEN      = os.environ.get('CF_API_TOKEN', '')
ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID', '')
SITE_TAG   = os.environ.get('CF_SITE_TAG', '')
HOSTNAME   = 'chrisanastasiadis.com'
OUT        = 'docs/stats/index.md'

def cf_get(path):
    req = urllib.request.Request(
        f'https://api.cloudflare.com/client/v4{path}',
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def cf_graphql(query, variables):
    data = json.dumps({'query': query, 'variables': variables}).encode()
    req = urllib.request.Request(
        'https://api.cloudflare.com/client/v4/graphql',
        data=data,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

QUERY = """
query Stats($accountTag: string!, $siteTag: string!, $start7: Time!, $start30: Time!, $end: Time!) {
  viewer {
    accounts(filter: {accountTag: $accountTag}) {
      summary7: rumPageloadEventsAdaptiveGroups(
        filter: {AND: [{siteTag: $siteTag}, {datetime_geq: $start7}, {datetime_leq: $end}]}
        limit: 1
      ) { count sum { visits } }

      summary30: rumPageloadEventsAdaptiveGroups(
        filter: {AND: [{siteTag: $siteTag}, {datetime_geq: $start30}, {datetime_leq: $end}]}
        limit: 1
      ) { count sum { visits } }

      topPages: rumPageloadEventsAdaptiveGroups(
        filter: {AND: [{siteTag: $siteTag}, {datetime_geq: $start30}, {datetime_leq: $end}]}
        limit: 15
        orderBy: [count_DESC]
      ) { count dimensions { requestPath } }

      topCountries: rumPageloadEventsAdaptiveGroups(
        filter: {AND: [{siteTag: $siteTag}, {datetime_geq: $start30}, {datetime_leq: $end}]}
        limit: 10
        orderBy: [count_DESC]
      ) { count dimensions { country } }

      topReferrers: rumPageloadEventsAdaptiveGroups(
        filter: {AND: [{siteTag: $siteTag}, {datetime_geq: $start30}, {datetime_leq: $end}]}
        limit: 10
        orderBy: [count_DESC]
      ) { count dimensions { refererHost } }
    }
  }
}
"""

def fallback(reason):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    content = f"""---
title: Site Stats
description: Visitor statistics for chrisanastasiadis.com
---

# Site Stats

!!! warning "Stats unavailable"
    Could not fetch analytics data: {reason}

    Check the [Cloudflare Web Analytics dashboard](https://dash.cloudflare.com) directly.

*Last attempted: {now}*
"""
    os.makedirs('docs/stats', exist_ok=True)
    open(OUT, 'w').write(content)
    print(f'fetch_stats: wrote fallback page ({reason})')

def bar(count, max_count, width=20):
    if max_count == 0:
        return '░' * width
    filled = round(count / max_count * width)
    return '█' * filled + '░' * (width - filled)

def main():
    if not TOKEN or not ACCOUNT_ID or not SITE_TAG:
        fallback('CF_API_TOKEN, CF_ACCOUNT_ID, or CF_SITE_TAG not set')
        return

    site_tag = SITE_TAG

    # Build time windows
    now = datetime.now(timezone.utc)
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    variables = {
        'accountTag': ACCOUNT_ID,
        'siteTag':    site_tag,
        'start7':     (now - timedelta(days=7)).strftime(fmt),
        'start30':    (now - timedelta(days=30)).strftime(fmt),
        'end':        now.strftime(fmt),
    }

    try:
        result = cf_graphql(QUERY, variables)
    except Exception as e:
        fallback(f'GraphQL query failed: {e}')
        return

    errors = result.get('errors')
    if errors:
        fallback(f'GraphQL errors: {errors[0].get("message", errors)}')
        return

    acct = result['data']['viewer']['accounts'][0]

    views7   = sum(g['count'] for g in acct['summary7'])
    visits7  = sum(g['sum']['visits'] for g in acct['summary7'])
    views30  = sum(g['count'] for g in acct['summary30'])
    visits30 = sum(g['sum']['visits'] for g in acct['summary30'])

    top_pages = [(g['count'], g['dimensions']['requestPath']) for g in acct['topPages']]
    top_countries = [(g['count'], g['dimensions']['country'] or '—') for g in acct['topCountries']]
    top_referrers = [(g['count'], g['dimensions']['refererHost'] or 'Direct') for g in acct['topReferrers']]

    # Remove empty/duplicate paths
    seen = set()
    pages_deduped = []
    for count, path in top_pages:
        if path and path not in seen:
            seen.add(path)
            pages_deduped.append((count, path))

    max_pv = pages_deduped[0][0] if pages_deduped else 1
    max_cv = top_countries[0][0] if top_countries else 1
    max_rv = top_referrers[0][0] if top_referrers else 1

    updated = now.strftime('%Y-%m-%d %H:%M UTC')

    lines = [
        '---',
        'title: Site Stats',
        'description: Visitor statistics for chrisanastasiadis.com',
        '---',
        '',
        '# Site Stats',
        '',
        '## Summary',
        '',
        '|  | Last 7 days | Last 30 days |',
        '|---|---|---|',
        f'| **Page views** | {views7:,} | {views30:,} |',
        f'| **Unique visits** | {visits7:,} | {visits30:,} |',
        '',
        '## Top pages (30 days)',
        '',
        '| Views | Page |',
        '|---|---|',
    ]

    for count, path in pages_deduped[:10]:
        b = bar(count, max_pv)
        lines.append(f'| `{count:,}` {b} | `{path}` |')

    lines += [
        '',
        '## Top countries (30 days)',
        '',
        '| Views | Country |',
        '|---|---|',
    ]
    for count, country in top_countries:
        b = bar(count, max_cv)
        lines.append(f'| `{count:,}` {b} | {country} |')

    lines += [
        '',
        '## Top referrers (30 days)',
        '',
        '| Views | Source |',
        '|---|---|',
    ]
    for count, ref in top_referrers:
        b = bar(count, max_rv)
        lines.append(f'| `{count:,}` {b} | {ref} |')

    lines += ['', f'*Updated: {updated}*', '']

    os.makedirs('docs/stats', exist_ok=True)
    open(OUT, 'w').write('\n'.join(lines))
    print(f'fetch_stats: wrote {OUT} ({views30:,} views / {visits30:,} visits in 30 days)')

if __name__ == '__main__':
    main()

"""
Post-hoc verification for one day's cert-kb automation run. Checks the claims
in the run's JSON output against what actually happened -- found necessary
2026-07-09 after a trial run committed a "verified via direct fetch" claim
with zero actual web searches performed (confirmed via modelUsage.*.webSearchRequests).

Usage: python3 project-tracking/verify_daily_run.py path/to/run.json
Exit 0 = looks legitimate. Exit 1 = something doesn't add up, do not trust this run.
Prints a one-line summary either way (used by the daily prompt to decide whether
to send a push notification).
"""
import glob
import json
import os
import re
import subprocess
import sys


def check_web_search_happened(data):
    model_usage = data.get('modelUsage', {})
    total_searches = sum(m.get('webSearchRequests', 0) for m in model_usage.values())
    return total_searches, total_searches > 0


AUDIT_SUMMARY_RE = re.compile(r'SUMMARY:\s*(\d+)/(\d+) checks clean')


def find_transcript(session_id):
    if not session_id:
        return None
    hits = glob.glob(os.path.expanduser(f'~/.claude/projects/*/{session_id}.jsonl'))
    return hits[0] if hits else None


def _tool_result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return '\n'.join(c.get('text', '') for c in content if isinstance(c, dict))
    return ''


def check_audit_ran(data):
    """Evidence from the session transcript, not the run's own prose -- the
    old check passed if the final message merely contained the word "audit"
    (found 2026-11-25). Requires (a) a Bash call that ran site_audit.py and
    (b) a tool result showing "SUMMARY: N/N checks clean" with N == total.
    Returns (ok, reason)."""
    path = find_transcript(data.get('session_id'))
    if not path:
        return False, 'session transcript not found -- cannot prove site_audit.py ran'
    ran, summaries = False, []
    with open(path) as f:
        for line in f:
            try:
                msg = json.loads(line).get('message') or {}
            except ValueError:
                continue
            content = msg.get('content')
            if not isinstance(content, list):
                continue
            for c in content:
                if c.get('type') == 'tool_use' and c.get('name') == 'Bash':
                    if 'site_audit.py' in (c.get('input') or {}).get('command', ''):
                        ran = True
                elif c.get('type') == 'tool_result':
                    summaries += AUDIT_SUMMARY_RE.findall(_tool_result_text(c.get('content')))
    if not ran:
        return False, 'no Bash call ran site_audit.py in the session transcript'
    if not summaries:
        return False, 'site_audit.py was invoked but no "SUMMARY: N/N checks clean" output was seen'
    clean, total = summaries[-1]
    if clean != total:
        return False, f'last audit summary was {clean}/{total}, not fully clean'
    return True, f'audit {clean}/{total} clean'


def check_exactly_one_checkbox_moved(before_sha):
    """Diff from the SHA captured before this run started, not a hardcoded
    HEAD~1 -- if this run made zero commits, HEAD~1..HEAD would silently
    show yesterday's commit instead of correctly reporting zero changes."""
    diff = subprocess.run(
        ['git', 'diff', before_sha, 'HEAD', '--', 'project-tracking/cert_kb_queue.md'],
        capture_output=True, text=True
    ).stdout
    return diff.count('\n+- [x] ')


def check_commit_pushed():
    local = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    remote = subprocess.run(['git', 'rev-parse', '@{u}'], capture_output=True, text=True).stdout.strip()
    return local == remote


def main():
    if len(sys.argv) != 3:
        print('Usage: verify_daily_run.py path/to/run.json <git-sha-before-run-started>')
        return 1

    with open(sys.argv[1]) as f:
        data = json.load(f)
    before_sha = sys.argv[2]

    problems = []

    search_count, search_ok = check_web_search_happened(data)
    if not search_ok:
        problems.append(f'zero web searches performed (found {search_count}) despite research being required')

    audit_ok, audit_note = check_audit_ran(data)
    if not audit_ok:
        problems.append(audit_note)

    checked = check_exactly_one_checkbox_moved(before_sha)
    if checked != 1:
        problems.append(f'expected exactly 1 new [x] checkbox since this run started, found {checked}')

    if not check_commit_pushed():
        problems.append('local HEAD does not match remote -- push may have failed')

    if problems:
        print('VERIFICATION FAILED:')
        for p in problems:
            print(f'  - {p}')
        return 1

    print(f'VERIFICATION OK: {search_count} web search(es), {audit_note}, 1 item completed, pushed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

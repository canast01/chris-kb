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
import json
import subprocess
import sys


def check_web_search_happened(data):
    model_usage = data.get('modelUsage', {})
    total_searches = sum(m.get('webSearchRequests', 0) for m in model_usage.values())
    return total_searches, total_searches > 0


def check_audit_ran(data):
    result_text = data.get('result', '')
    return 'SUMMARY' in result_text or 'audit' in result_text.lower()


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

    if not check_audit_ran(data):
        problems.append('no mention of an audit/summary in the result -- site_audit.py may not have run')

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

    print(f'VERIFICATION OK: {search_count} web search(es), audit ran, 1 item completed, pushed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

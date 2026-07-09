# Certification-Grade KB — daily automation

Not part of the published site. Working files for the daily "one baby piece a day"
execution of `project_certification_grade_kb.md` (in Claude's memory system).

## Files

- `cert_kb_queue.md` — the task list. One unchecked `[ ]` item = one day's work.
- `daily_prompt.txt` — the exact prompt sent to Claude Code each day.
- `precheck.sh` — environment health check run before each day's work (clean git tree,
  network reachable, items remaining). Not committed to run if this fails.
- `run_daily.sh` — the actual entry point: precheck → run → verify → notify on failure.
- `verify_daily_run.py` — post-hoc check that a run's claims match what really happened
  (real web search occurred, audit ran, exactly one item completed, push landed).
- `daily_run.log` / `runs/*.json` — gitignored (would bloat the repo like `.cache/` did
  otherwise). Local-only, grows over time, safe to prune periodically.

## The scheduled job

Installed at `~/Library/LaunchAgents/com.chrisanastasiadis.chriskb.cert-daily.plist`,
runs daily at 9:13am local time via `run_daily.sh` — fully unattended, commits and
pushes automatically each day per your instruction (2026-07-09). If a day's run fails
precheck or fails post-hoc verification, it sends a real push notification instead of
silently trusting a bad result (added 2026-07-09 after finding a trial run had skipped
steps and fabricated a "verified" claim with zero actual web searches performed).

**Check status:**
```
launchctl list | grep chriskb
```

**Pause it** (stops future runs, keeps the job installed):
```
launchctl bootout gui/$(id -u)/com.chrisanastasiadis.chriskb.cert-daily
```

**Resume it:**
```
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.chrisanastasiadis.chriskb.cert-daily.plist
```

**Remove it entirely:**
```
launchctl bootout gui/$(id -u)/com.chrisanastasiadis.chriskb.cert-daily
rm ~/Library/LaunchAgents/com.chrisanastasiadis.chriskb.cert-daily.plist
```

**Check progress at a glance:**
```
grep -c '\[x\]' project-tracking/cert_kb_queue.md   # done so far
grep -c '\[ \]' project-tracking/cert_kb_queue.md   # remaining
```

## Why unattended, no daily approval needed

Each run is scoped to exactly one small, pre-defined queue item, self-audits before
committing, and stops itself after one item regardless of remaining budget — see
`daily_prompt.txt` step 9. If something's ambiguous it leaves a note and stops rather
than guessing. Designed to be safe to leave running for months without supervision, but
worth spot-checking `daily_run.log` occasionally.

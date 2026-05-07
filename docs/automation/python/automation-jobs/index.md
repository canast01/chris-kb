# Python Automation Jobs

## Scheduling with cron

The simplest scheduling mechanism on Linux is cron. Use absolute paths and redirect output.

```bash
# Edit the crontab for the current user
crontab -e

# List current crontab
crontab -l
```

```bash
# Crontab examples
# Run every day at 06:00
0 6 * * * /usr/bin/python3 /opt/scripts/daily_report.py >> /var/log/daily_report.log 2>&1

# Every 15 minutes
*/15 * * * * /opt/venv/bin/python /opt/scripts/health_check.py

# Monday to Friday at 08:30
30 8 * * 1-5 /opt/venv/bin/python /opt/scripts/sync_inventory.py >> /var/log/sync.log 2>&1

# First day of each month at midnight
0 0 1 * * /opt/venv/bin/python /opt/scripts/monthly_cleanup.py
```

## APScheduler for In-Process Scheduling

APScheduler lets you schedule jobs inside a running Python application.

```bash
pip install apscheduler
```

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

scheduler = BlockingScheduler()

@scheduler.scheduled_job(CronTrigger(hour=6, minute=0))
def daily_report():
    log.info("Running daily report")
    # ... report logic ...

@scheduler.scheduled_job('interval', minutes=15)
def health_check():
    log.info("Running health check")
    # ... check logic ...

if __name__ == '__main__':
    log.info("Scheduler starting")
    scheduler.start()
```

## Job Logging

Good logging is essential for scheduled jobs running unattended.

```python
import logging
import logging.handlers
from pathlib import Path

def configure_logging(job_name: str, log_dir: str = '/var/log/automation') -> logging.Logger:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = f"{log_dir}/{job_name}.log"

    logger = logging.getLogger(job_name)
    logger.setLevel(logging.INFO)

    # Rotate at midnight, keep 30 days
    handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when='midnight', backupCount=30
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())  # also print to stdout
    return logger
```

## Idempotency Patterns

Automation jobs should produce the same result whether run once or many times.

```python
import json
from pathlib import Path
from datetime import date

STATE_FILE = Path('/var/lib/automation/daily_report_state.json')

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, default=str))

def run_daily_report():
    state = load_state()
    today = str(date.today())

    if state.get('last_run_date') == today:
        print(f"Report already generated for {today}, skipping.")
        return

    # ... generate report ...
    print(f"Report generated for {today}")

    state['last_run_date'] = today
    save_state(state)
```

## Job Design Checklist

| Concern | Practice |
|---|---|
| Logging | Write timestamped logs to a file; rotate regularly |
| Error handling | Catch exceptions; log full tracebacks; exit with non-zero on failure |
| Idempotency | Check state before acting; safe to re-run without side effects |
| Timeouts | Set timeouts on all network and subprocess calls |
| Notifications | Alert on failure via email or monitoring system |
| Locking | Use a lockfile to prevent overlapping runs |

```python
import fcntl, sys

lock_file = open('/var/run/my_job.lock', 'w')
try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except OSError:
    print("Another instance is already running. Exiting.")
    sys.exit(0)
# ... job runs here ...
fcntl.flock(lock_file, fcntl.LOCK_UN)
```

# Scripts

> Part of the [CloudIQ](../) reference.

---

## Alert Poller

Polls the CloudIQ REST API for all active alerts across the storage estate and prints a formatted report grouped by severity. Exits non-zero if any CRITICAL alerts are found. Designed for cron or monitoring integration.

~~~python
#!/usr/bin/env python3
# cloudiq_alert_poller.py — Poll CloudIQ for active alerts across all systems
# Requirements: requests
# Usage: CLOUDIQ_CLIENT_ID=xxx CLOUDIQ_CLIENT_SECRET=yyy ./cloudiq_alert_poller.py

import os
import sys
import requests
import urllib3
from datetime import datetime
from collections import defaultdict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLIENT_ID     = os.environ.get("CLOUDIQ_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("CLOUDIQ_CLIENT_SECRET", "")
CLOUDIQ_BASE  = "https://cloudiq.dell.com"
AUTH_URL      = f"{CLOUDIQ_BASE}/auth/v1/token"
API_BASE      = f"{CLOUDIQ_BASE}/cloudiq/rest/v1"

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: CLOUDIQ_CLIENT_ID and CLOUDIQ_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path, params=None):
    resp = session.get(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0

    print("=" * 70)
    print("  CloudIQ Active Alert Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    token = get_token()

    data   = api_get(token, "/alerts", params={"state": "ACTIVE"})
    alerts = data.get("results", data if isinstance(data, list) else [])

    if not alerts:
        print("\nNo active alerts.")
        sys.exit(0)

    # Group by severity
    by_severity = defaultdict(list)
    for alert in alerts:
        sev = alert.get("severity", "UNKNOWN").upper()
        by_severity[sev].append(alert)

    for sev in ("CRITICAL", "ERROR", "WARNING", "INFO", "UNKNOWN"):
        group = by_severity.get(sev, [])
        if not group:
            continue
        print(f"\n--- {sev} ({len(group)}) ---")
        print(f"  {'SYSTEM':<30}  {'COMPONENT':<25}  DESCRIPTION")
        print("  " + "-" * 80)
        for a in group:
            system    = a.get("system_name", a.get("systemName", "unknown"))
            component = a.get("component_name", a.get("componentName", a.get("object_name", "unknown")))
            desc      = a.get("description", a.get("message", "no description"))
            print(f"  {system:<30}  {component:<25}  {desc}")
        if sev in ("CRITICAL", "ERROR"):
            exit_code = max(exit_code, 2)
        elif sev == "WARNING":
            exit_code = max(exit_code, 1)

    print(f"\n{'=' * 70}")
    print(f"  Total active alerts: {len(alerts)}")
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"  Overall: {labels.get(exit_code, 'UNKNOWN')}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Capacity Trend Reporter

Queries CloudIQ for all storage systems, fetches their capacity metrics, and prints a trend report showing current utilisation and projected days-to-full. Flags systems under 30 days to full.

~~~python
#!/usr/bin/env python3
# cloudiq_capacity_reporter.py — CloudIQ capacity trend and days-to-full reporter
# Requirements: requests
# Usage: CLOUDIQ_CLIENT_ID=xxx CLOUDIQ_CLIENT_SECRET=yyy WARN_DAYS=30 ./cloudiq_capacity_reporter.py

import os
import sys
import requests
from datetime import datetime

CLIENT_ID     = os.environ.get("CLOUDIQ_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("CLOUDIQ_CLIENT_SECRET", "")
WARN_DAYS     = int(os.environ.get("WARN_DAYS", "30"))
CLOUDIQ_BASE  = "https://cloudiq.dell.com"
API_BASE      = f"{CLOUDIQ_BASE}/cloudiq/rest/v1"

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: CLOUDIQ_CLIENT_ID and CLOUDIQ_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        f"{CLOUDIQ_BASE}/auth/v1/token",
        data={"grant_type": "client_credentials",
              "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path, params=None):
    resp = session.get(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0
    token = get_token()

    systems_data = api_get(token, "/storage-systems")
    systems = systems_data.get("results", [])

    print("=" * 80)
    print("  CloudIQ Capacity Trend Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"\n{'SYSTEM':<30}  {'TYPE':<15}  {'USED %':>7}  {'DAYS TO FULL':>13}  STATUS")
    print("-" * 80)

    for sys_obj in systems:
        sys_id   = sys_obj.get("id", "unknown")
        sys_name = sys_obj.get("system_name", sys_obj.get("name", sys_id))
        sys_type = sys_obj.get("system_type", sys_obj.get("type", "unknown"))

        try:
            cap = api_get(token, f"/storage-systems/{sys_id}/capacity")
        except Exception:
            cap = {}

        total  = float(cap.get("total_subscribed_tib", cap.get("total_tib", 0)))
        used   = float(cap.get("used_tib", 0))
        dtf    = cap.get("days_until_full", cap.get("daysUntilFull", None))
        pct    = (used / total * 100) if total > 0 else 0.0

        if dtf is not None:
            dtf_val = int(dtf)
            dtf_str = str(dtf_val)
        else:
            dtf_val = 9999
            dtf_str = "N/A"

        if dtf_val <= WARN_DAYS:
            status = f"WARNING — {dtf_str} days"
            exit_code = max(exit_code, 1)
        elif pct >= 85:
            status = "WARNING — over 85%"
            exit_code = max(exit_code, 1)
        else:
            status = "OK"

        print(f"{sys_name:<30}  {sys_type:<15}  {pct:>6.1f}%  {dtf_str:>13}  {status}")

    print("-" * 80)
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"\nOverall: {labels.get(exit_code, 'UNKNOWN')}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Ansible CloudIQ Daily Health Playbook

Playbook targeting localhost. Authenticates to CloudIQ, retrieves active alerts and capacity summaries, prints the output, and fails if critical alerts are present.

~~~yaml
---
# cloudiq_daily_health.yml — Ansible daily CloudIQ health check playbook
# Usage: ansible-playbook cloudiq_daily_health.yml

- name: Dell CloudIQ Daily Health Check
  hosts: localhost
  gather_facts: false
  vars:
    cloudiq_base: "https://cloudiq.dell.com"
    client_id: "{{ lookup('env', 'CLOUDIQ_CLIENT_ID') }}"
    client_secret: "{{ lookup('env', 'CLOUDIQ_CLIENT_SECRET') }}"
    warn_days_to_full: 30

  tasks:
    - name: Authenticate to CloudIQ API
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/auth/v1/token"
        method: POST
        body_format: form-urlencoded
        body:
          grant_type: client_credentials
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
        return_content: true
      register: auth_resp
      no_log: true

    - name: Set access token
      ansible.builtin.set_fact:
        cloudiq_token: "{{ auth_resp.json.access_token }}"
      no_log: true

    - name: Get active alerts
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/cloudiq/rest/v1/alerts?state=ACTIVE"
        method: GET
        headers:
          Authorization: "Bearer {{ cloudiq_token }}"
        return_content: true
      register: alerts_resp

    - name: Show active alerts
      ansible.builtin.debug:
        msg: "{{ alerts_resp.json.results | default([]) }}"

    - name: Get storage system capacity
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/cloudiq/rest/v1/storage-systems"
        method: GET
        headers:
          Authorization: "Bearer {{ cloudiq_token }}"
        return_content: true
      register: systems_resp

    - name: Show storage systems
      ansible.builtin.debug:
        msg: "{{ systems_resp.json.results | default([]) | map(attribute='system_name') | list }}"

    - name: Fail if CRITICAL alerts present
      ansible.builtin.fail:
        msg: "CRITICAL alerts active in CloudIQ. Review alerts_resp output above."
      when: >
        (alerts_resp.json.results | default([]) |
         selectattr('severity', 'equalto', 'CRITICAL') | list | length) > 0
~~~

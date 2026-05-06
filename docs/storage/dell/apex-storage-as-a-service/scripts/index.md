# Scripts

> Part of the [APEX Storage as a Service](../) reference.

---

## Subscription Capacity Monitor

Authenticates to the APEX REST API, retrieves all subscriptions, and checks committed vs. consumed capacity. Warns at 80% and goes critical at 90% of the committed tier.

~~~python
#!/usr/bin/env python3
# apex_capacity_monitor.py — APEX STaaS subscription capacity monitor
# Requirements: requests
# Usage:
#   APEX_CLIENT_ID=xxx APEX_CLIENT_SECRET=yyy ./apex_capacity_monitor.py

import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

APEX_CLIENT_ID     = os.environ.get("APEX_CLIENT_ID", "")
APEX_CLIENT_SECRET = os.environ.get("APEX_CLIENT_SECRET", "")
APEX_BASE          = os.environ.get("APEX_BASE", "https://console.cloudapex.dell.com/api/v1")
WARN_PCT           = float(os.environ.get("WARN_PCT", "80"))
CRIT_PCT           = float(os.environ.get("CRIT_PCT", "90"))

if not APEX_CLIENT_ID or not APEX_CLIENT_SECRET:
    print("ERROR: APEX_CLIENT_ID and APEX_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        f"{APEX_BASE}/auth/token",
        json={"client_id": APEX_CLIENT_ID, "client_secret": APEX_CLIENT_SECRET},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path):
    resp = session.get(
        f"{APEX_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0

    print("=" * 60)
    print("  APEX STaaS Subscription Capacity Monitor")
    print("=" * 60)

    try:
        token = get_token()
    except Exception as e:
        print(f"ERROR: Authentication failed: {e}")
        sys.exit(2)

    # List subscriptions
    try:
        subs_data = api_get(token, "/subscriptions")
        subscriptions = subs_data.get("subscriptions", subs_data if isinstance(subs_data, list) else [])
    except Exception as e:
        print(f"ERROR: Could not list subscriptions: {e}")
        sys.exit(2)

    if not subscriptions:
        print("No subscriptions found.")
        sys.exit(0)

    print(f"\n{'SUBSCRIPTION':<35}  {'COMMITTED':>12}  {'CONSUMED':>12}  {'PCT':>6}  STATUS")
    print("-" * 85)

    for sub in subscriptions:
        sub_id   = sub.get("id", "unknown")
        sub_name = sub.get("name", sub_id)

        # Fetch capacity for this subscription
        try:
            cap = api_get(token, f"/subscriptions/{sub_id}/capacity")
        except Exception as e:
            print(f"{sub_name:<35}  ERROR: {e}")
            continue

        committed_tib = float(cap.get("committed_tib", cap.get("committedTiB", 0)))
        consumed_tib  = float(cap.get("consumed_tib",  cap.get("consumedTiB",  0)))
        pct = (consumed_tib / committed_tib * 100) if committed_tib > 0 else 0.0

        if pct >= CRIT_PCT:
            status = "CRITICAL"
            exit_code = max(exit_code, 2)
        elif pct >= WARN_PCT:
            status = "WARNING"
            exit_code = max(exit_code, 1)
        else:
            status = "OK"

        print(f"{sub_name:<35}  {committed_tib:>10.2f}T  {consumed_tib:>10.2f}T  {pct:>5.1f}%  {status}")

    print("-" * 85)
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"\nOverall: {labels.get(exit_code, 'UNKNOWN')}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Active Alert Report

Polls the APEX REST API for all active alerts across subscriptions and prints a formatted report. Exits non-zero if any CRITICAL severity alerts are found.

~~~python
#!/usr/bin/env python3
# apex_alert_report.py — Retrieve and report active APEX STaaS alerts
# Requirements: requests
# Usage: APEX_CLIENT_ID=xxx APEX_CLIENT_SECRET=yyy ./apex_alert_report.py

import os
import sys
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

APEX_CLIENT_ID     = os.environ.get("APEX_CLIENT_ID", "")
APEX_CLIENT_SECRET = os.environ.get("APEX_CLIENT_SECRET", "")
APEX_BASE          = os.environ.get("APEX_BASE", "https://console.cloudapex.dell.com/api/v1")

if not APEX_CLIENT_ID or not APEX_CLIENT_SECRET:
    print("ERROR: APEX_CLIENT_ID and APEX_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        f"{APEX_BASE}/auth/token",
        json={"client_id": APEX_CLIENT_ID, "client_secret": APEX_CLIENT_SECRET},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path):
    resp = session.get(
        f"{APEX_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0
    token = get_token()

    print("=" * 65)
    print("  APEX STaaS Active Alert Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    try:
        data = api_get(token, "/alerts?status=active")
        alerts = data.get("alerts", data if isinstance(data, list) else [])
    except Exception as e:
        print(f"ERROR fetching alerts: {e}")
        sys.exit(2)

    if not alerts:
        print("\nNo active alerts.")
        sys.exit(0)

    print(f"\n{'SEVERITY':<12}  {'RESOURCE':<30}  {'DESCRIPTION'}")
    print("-" * 80)

    for alert in alerts:
        severity = alert.get("severity", "UNKNOWN").upper()
        resource = alert.get("resource_name", alert.get("resourceName", "unknown"))
        desc     = alert.get("description", alert.get("message", "no description"))

        print(f"{severity:<12}  {resource:<30}  {desc}")

        if severity in ("CRITICAL", "ERROR"):
            exit_code = max(exit_code, 2)
        elif severity == "WARNING":
            exit_code = max(exit_code, 1)

    print("-" * 80)
    print(f"\nTotal active alerts: {len(alerts)}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Ansible APEX Health Playbook

Playbook that calls the APEX REST API via the `uri` module to check subscription capacity and active alerts, printing a summary and failing the play if capacity is critical or critical alerts exist.

~~~yaml
---
# apex_health.yml — Ansible health check playbook for Dell APEX STaaS
# Required vars: apex_client_id, apex_client_secret
# Usage: ansible-playbook apex_health.yml

- name: Dell APEX STaaS Health Check
  hosts: localhost
  gather_facts: false
  vars:
    apex_base: "https://console.cloudapex.dell.com/api/v1"
    apex_client_id: "{{ lookup('env', 'APEX_CLIENT_ID') }}"
    apex_client_secret: "{{ lookup('env', 'APEX_CLIENT_SECRET') }}"
    warn_pct: 80
    crit_pct: 90

  tasks:
    - name: Authenticate to APEX API
      ansible.builtin.uri:
        url: "{{ apex_base }}/auth/token"
        method: POST
        body_format: json
        body:
          client_id: "{{ apex_client_id }}"
          client_secret: "{{ apex_client_secret }}"
        validate_certs: false
        return_content: true
      register: auth_resp
      no_log: true

    - name: Set bearer token
      ansible.builtin.set_fact:
        apex_token: "{{ auth_resp.json.access_token }}"
      no_log: true

    - name: List subscriptions
      ansible.builtin.uri:
        url: "{{ apex_base }}/subscriptions"
        method: GET
        headers:
          Authorization: "Bearer {{ apex_token }}"
        validate_certs: false
        return_content: true
      register: subs_resp

    - name: Show subscriptions
      ansible.builtin.debug:
        msg: "{{ subs_resp.json }}"

    - name: Get active alerts
      ansible.builtin.uri:
        url: "{{ apex_base }}/alerts?status=active"
        method: GET
        headers:
          Authorization: "Bearer {{ apex_token }}"
        validate_certs: false
        return_content: true
      register: alerts_resp

    - name: Show active alerts
      ansible.builtin.debug:
        msg: "{{ alerts_resp.json }}"

    - name: Fail if critical alerts present
      ansible.builtin.fail:
        msg: "Critical APEX alerts detected. Investigate via APEX Console."
      when: >
        alerts_resp.json is defined and
        (alerts_resp.json.alerts | default([]) |
         selectattr('severity', 'equalto', 'CRITICAL') | list | length) > 0
~~~

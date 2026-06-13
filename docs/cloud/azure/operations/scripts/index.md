---
tags:
  - azure
  - operations
---
# Azure — Scripts


<div class="kb-summary">
Part of the [Azure](../../index.md) reference.

*Applies to: Azure*
</div>
```text
┌─────────────────────────── Cloud Azure Operations — Scripts and Automation ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Azure scripts: automation for reporting, health monitoring, and provisioning         │   │
│   │         REST API available for all operations; PowerShell and Python modules supported        │   │
│   │          Scripts must run from dedicated service accounts with least-privilege roles          │   │
│   │        Store credentials in vault; rotate service account passwords on defined schedule       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Script → authenticate REST → execute operation → verify → log result                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Operations infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Operations platform overview and core concepts                    │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Script Categories

```mermaid
flowchart LR
    subgraph healthScripts["Health Check Scripts"]
        subHealth["Subscription Health Check\nVMs · LBs · SQL · Activity Log"]
        vmHealth["VM Health Report\npower state · provisioning"]
    end
    subgraph govScripts["Governance Scripts"]
        tagAudit["Tag Compliance Audit\nuntagged resources report"]
        rbacAudit["RBAC Audit\nstale assignments"]
    end
    subgraph costScripts["Cost Scripts"]
        costReport["Cost Report\nspend by RG · service"]
        unusedResources["Unused Resources\nunattached disks · idle VMs"]
    end
    output["Output\nConsole · CSV · Email"]

    healthScripts & govScripts & costScripts --> output
```

## Azure Subscription Health Check

Prints a formatted health report covering VMs, load balancers, SQL servers, and recent critical activity log events. Exits non-zero if any critical events are found.

```bash
#!/bin/bash
set -euo pipefail

SUBSCRIPTION_ID="${SUBSCRIPTION_ID:-$(az account show --query id -o tsv)}"
RESOURCE_GROUP="${RESOURCE_GROUP:-}"

BOLD="\033[1m"
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"

echo -e "${BOLD}=== Azure Subscription Health Check ===${RESET}"
echo "Subscription : ${SUBSCRIPTION_ID}"
[[ -n "${RESOURCE_GROUP}" ]] && echo "Resource Group: ${RESOURCE_GROUP}"
echo "Time         : $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

# --- Account ---
echo -e "${BOLD}--- Active Account ---${RESET}"
az account show --subscription "${SUBSCRIPTION_ID}" \
  --query '{name:name, id:id, tenantId:tenantId, state:state}' -o table
echo

# --- Virtual Machines ---
echo -e "${BOLD}--- Virtual Machines ---${RESET}"
if [[ -n "${RESOURCE_GROUP}" ]]; then
  az vm list \
    --subscription "${SUBSCRIPTION_ID}" \
    --resource-group "${RESOURCE_GROUP}" \
    --show-details \
    --query '[*].[name,resourceGroup,powerState,location,hardwareProfile.vmSize]' \
    -o table
else
  az vm list \
    --subscription "${SUBSCRIPTION_ID}" \
    --show-details \
    --query '[*].[name,resourceGroup,powerState,location,hardwareProfile.vmSize]' \
    -o table
fi
echo

# --- Load Balancers ---
echo -e "${BOLD}--- Load Balancers ---${RESET}"
az network lb list \
  --subscription "${SUBSCRIPTION_ID}" \
  --query '[*].[name,resourceGroup,location,sku.name,provisioningState]' \
  -o table
echo

# --- SQL Servers ---
echo -e "${BOLD}--- SQL Servers ---${RESET}"
az sql server list \
  --subscription "${SUBSCRIPTION_ID}" \
  --query '[*].[name,resourceGroup,location,fullyQualifiedDomainName,state]' \
  -o table
echo

# --- Critical Activity Log ---
echo -e "${BOLD}--- Recent Critical Activity Log Events (last 20) ---${RESET}"
CRITICAL_EVENTS=$(az monitor activity-log list \
  --subscription "${SUBSCRIPTION_ID}" \
  --max-events 20 \
  --filter "level eq 'Critical'" \
  --query '[*].[eventTimestamp,operationName.localizedValue,resourceGroup,status.localizedValue,caller]' \
  -o table)

echo "${CRITICAL_EVENTS}"
CRITICAL_COUNT=$(echo "${CRITICAL_EVENTS}" | grep -c -v "^-\|^Event\|^$" || true)

echo
if [[ "${CRITICAL_COUNT}" -gt 0 ]]; then
  echo -e "${RED}ALERT: ${CRITICAL_COUNT} critical event(s) found in activity log.${RESET}"
  exit 1
fi

echo -e "${GREEN}Health check PASSED — no critical events detected.${RESET}"
```

### How to run this script — step by step

**Before you start — what you need**
- Azure CLI installed (download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
- Logged in to Azure: run `az login` in your terminal first
- Git Bash installed (from https://gitforwindows.org) to run `.sh` scripts on Windows

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — prevents Notepad adding .txt)
5. Name it `azure-health-check.sh` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `RESOURCE_GROUP` | Optional — leave blank to check all resource groups | Azure Portal → Resource Groups |

**Step 3 — Open the right terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) → open Git Bash

**Step 4 — Run it**

```bash
cd ~/Desktop
bash azure-health-check.sh
```

**What you should see**

Tables showing your VMs with power state, load balancers, and SQL servers. Then a section showing any critical events from the Azure activity log. If critical events are found the script exits with an error and shows a red ALERT message.

---

## VM Health and Compliance Report

Authenticates via DefaultAzureCredential, lists all VMs across a subscription, checks tags, backup enrollment, and monitoring agent presence, then exports a CSV report.

```python
#!/usr/bin/env python3
"""Azure VM Health and Compliance Report — tags, backup, monitoring agent."""

import csv
import sys
import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
from azure.mgmt.resource import ResourceManagementClient

# --- Configuration ---
SUBSCRIPTION_ID   = "YOUR_SUBSCRIPTION_ID"
OUTPUT_FILE       = "azure_vm_compliance.csv"
REQUIRED_TAGS     = ["Owner", "Environment", "CostCenter"]
MONITORING_EXTS   = {"MicrosoftMonitoringAgent", "AzureMonitorWindowsAgent",
                     "AzureMonitorLinuxAgent", "OmsAgentForLinux"}
# ---------------------

FIELDS = [
    "Name", "ResourceGroup", "Location", "Size", "PowerState",
    "OSDisk", "Tags_Owner", "Tags_Environment", "Tags_CostCenter",
    "MonitoringAgent", "Flags",
]


def get_power_state(instance_view) -> str:
    if instance_view and instance_view.statuses:
        for s in instance_view.statuses:
            if s.code.startswith("PowerState/"):
                return s.code.split("/")[1]
    return "unknown"


def get_extensions(vm_name: str, rg: str, compute_client: ComputeManagementClient) -> list[str]:
    try:
        exts = list(compute_client.virtual_machine_extensions.list(rg, vm_name))
        return [e.virtual_machine_extension_type for e in exts if e.virtual_machine_extension_type]
    except Exception:
        return []


def main() -> None:
    cred           = DefaultAzureCredential()
    compute_client = ComputeManagementClient(cred, SUBSCRIPTION_ID)

    rows: list[dict] = []
    print(f"Enumerating VMs in subscription {SUBSCRIPTION_ID}...")

    for vm in compute_client.virtual_machines.list_all():
        rg_name = vm.id.split("/")[4]
        name    = vm.name

        try:
            iv = compute_client.virtual_machines.instance_view(rg_name, name)
            power_state = get_power_state(iv)
        except Exception:
            power_state = "unknown"

        tags       = vm.tags or {}
        extensions = get_extensions(name, rg_name, compute_client)
        has_monitor = bool(MONITORING_EXTS & set(extensions))

        os_disk = ""
        if vm.storage_profile and vm.storage_profile.os_disk:
            os_disk = vm.storage_profile.os_disk.name or ""

        flags = []
        for tag in REQUIRED_TAGS:
            if not tags.get(tag):
                flags.append(f"MISSING_TAG_{tag.upper()}")
        if not has_monitor:
            flags.append("NO_MONITORING_AGENT")

        rows.append({
            "Name":             name,
            "ResourceGroup":    rg_name,
            "Location":         vm.location,
            "Size":             vm.hardware_profile.vm_size if vm.hardware_profile else "",
            "PowerState":       power_state,
            "OSDisk":           os_disk,
            "Tags_Owner":       tags.get("Owner", ""),
            "Tags_Environment": tags.get("Environment", ""),
            "Tags_CostCenter":  tags.get("CostCenter", ""),
            "MonitoringAgent":  "yes" if has_monitor else "no",
            "Flags":            "|".join(flags),
        })
        print(f"  {name:40s}  {power_state:12s}  {('FLAGS: ' + '|'.join(flags)) if flags else 'OK'}")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    flagged = [r for r in rows if r["Flags"]]
    print(f"\nTotal VMs  : {len(rows)}")
    print(f"Flagged    : {len(flagged)}")
    print(f"Report     : {OUTPUT_FILE}")

    if flagged:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
```

### How to run this script — step by step

**Before you start — what you need**
- Python installed (download from https://python.org)
- Azure CLI installed and you are logged in (`az login`)
- The Azure Python SDK packages installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `azure_vm_compliance.py` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions → copy the Subscription ID |
| `REQUIRED_TAGS` | Tags you want to enforce on all VMs | Your company's tagging policy |
| `OUTPUT_FILE` | Where to save the CSV | Default: `azure_vm_compliance.csv` in the same folder |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt.

**Step 4 — Install packages and run**

```bash
cd C:\Users\YourName\Desktop
pip install azure-identity azure-mgmt-compute azure-mgmt-recoveryservicesbackup azure-mgmt-resource
python azure_vm_compliance.py
```

**What you should see**

One line per VM as it scans: VM name, power state, and either OK or a list of flags like `MISSING_TAG_OWNER` or `NO_MONITORING_AGENT`. A CSV file is created that you can open in Excel for a full report.

---

## Azure Cost Spike Alert

Compares daily average spend for the last 7 days versus the prior 7 days per service, flags any service with more than a configurable percentage increase, and sends an alert email via SMTP.

```python
#!/usr/bin/env python3
"""Azure Cost Spike Alert — detects per-service cost increases and emails alerts."""

import os
import smtplib
import datetime
from email.mime.text import MIMEText
from collections import defaultdict
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import (
    QueryDefinition, QueryTimePeriod, QueryDataset,
    QueryAggregation, QueryGrouping, TimeframeType,
)

# --- Configuration ---
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", "YOUR_SUBSCRIPTION_ID")
SMTP_SERVER     = os.environ.get("SMTP_SERVER",     "smtp.example.com")
SMTP_PORT       = int(os.environ.get("SMTP_PORT",   "587"))
SMTP_USER       = os.environ.get("SMTP_USER",       "")
SMTP_PASS       = os.environ.get("SMTP_PASS",       "")
ALERT_EMAIL     = os.environ.get("ALERT_EMAIL",     "ops@example.com")
FROM_EMAIL      = os.environ.get("FROM_EMAIL",      "azure-cost-bot@example.com")
THRESHOLD_PCT   = float(os.environ.get("THRESHOLD_PCT", "25"))
# ---------------------

TODAY   = datetime.date.today()
CURR_END   = TODAY
CURR_START = TODAY - datetime.timedelta(days=7)
PREV_END   = CURR_START
PREV_START = PREV_END - datetime.timedelta(days=7)


def fetch_cost(client: CostManagementClient, start: datetime.date, end: datetime.date) -> dict[str, float]:
    scope = f"/subscriptions/{SUBSCRIPTION_ID}"
    query = QueryDefinition(
        type="ActualCost",
        timeframe=TimeframeType.CUSTOM,
        time_period=QueryTimePeriod(
            from_property=datetime.datetime.combine(start, datetime.time.min),
            to=datetime.datetime.combine(end, datetime.time.min),
        ),
        dataset=QueryDataset(
            granularity="Daily",
            aggregation={"totalCost": QueryAggregation(name="Cost", function="Sum")},
            grouping=[QueryGrouping(type="Dimension", name="ServiceName")],
        ),
    )
    result = client.query.usage(scope=scope, parameters=query)
    service_cost: dict[str, float] = defaultdict(float)
    for row in result.rows:
        cost    = float(row[0])
        service = str(row[2])
        service_cost[service] += cost
    return dict(service_cost)


def send_alert(subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = FROM_EMAIL
    msg["To"]      = ALERT_EMAIL
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        if SMTP_USER:
            server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, ALERT_EMAIL, msg.as_string())


def main() -> None:
    cred   = DefaultAzureCredential()
    client = CostManagementClient(cred)

    print(f"Fetching costs {PREV_START} → {PREV_END} (prior 7d)...")
    prev = fetch_cost(client, PREV_START, PREV_END)
    print(f"Fetching costs {CURR_START} → {CURR_END} (current 7d)...")
    curr = fetch_cost(client, CURR_START, CURR_END)

    all_services = set(prev) | set(curr)

    prev_avg = {svc: prev.get(svc, 0) / 7 for svc in all_services}
    curr_avg = {svc: curr.get(svc, 0) / 7 for svc in all_services}

    spikes: list[tuple[str, float, float, float]] = []

    print(f"\n{'Service':<50} {'PrevAvg/d':>12} {'CurrAvg/d':>12} {'Change':>8}")
    print("-" * 88)

    for svc in sorted(all_services, key=lambda s: curr_avg.get(s, 0), reverse=True):
        p = prev_avg[svc]
        c = curr_avg[svc]
        pct = (c - p) / p * 100 if p > 0 else 0.0
        flag = "  *** SPIKE ***" if pct > THRESHOLD_PCT else ""
        print(f"{svc:<50} ${p:>11.4f} ${c:>11.4f} {pct:>+7.1f}%{flag}")
        if pct > THRESHOLD_PCT:
            spikes.append((svc, p, c, pct))

    print(f"\nSpikes detected (>{THRESHOLD_PCT}%): {len(spikes)}")

    if spikes:
        lines = [f"Azure Cost Spike Alert — {TODAY}\n",
                 f"Subscription: {SUBSCRIPTION_ID}\n",
                 f"Threshold: {THRESHOLD_PCT}%\n\n",
                 f"{'Service':<50} {'PrevAvg/d':>12} {'CurrAvg/d':>12} {'Change':>8}\n",
                 "-" * 88 + "\n"]
        for svc, p, c, pct in spikes:
            lines.append(f"{svc:<50} ${p:>11.4f} ${c:>11.4f} {pct:>+7.1f}%\n")
        body = "".join(lines)
        subject = f"[ALERT] Azure cost spike detected — {len(spikes)} service(s) >{THRESHOLD_PCT}%"
        try:
            send_alert(subject, body)
            print(f"Alert email sent to {ALERT_EMAIL}")
        except Exception as exc:
            print(f"Warning: could not send alert email: {exc}")


if __name__ == "__main__":
    main()
```

### How to run this script — step by step

**Before you start — what you need**
- Python installed
- Azure CLI installed and logged in (`az login`)
- An SMTP server to send alerts from (e.g. Gmail SMTP, Office 365, or your company's mail relay)
- The Azure Python SDK packages installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `azure_cost_spike.py` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `SMTP_SERVER` | Your mail server address | Your IT team or email provider settings |
| `SMTP_PORT` | Mail server port, usually `587` | Your email provider docs |
| `SMTP_USER` | Email account username | Your email account |
| `SMTP_PASS` | Email account password | Your email account |
| `ALERT_EMAIL` | Who to send alerts to | Your ops team email address |
| `THRESHOLD_PCT` | Percentage increase before alerting | Default is `25` |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt.

**Step 4 — Install packages and run**

```bash
cd C:\Users\YourName\Desktop
pip install azure-identity azure-mgmt-costmanagement
python azure_cost_spike.py
```

**What you should see**

A table showing each Azure service with its average daily spend for the previous 7 days and the current 7 days, plus a percentage change. Services that have spiked more than the threshold are marked with `*** SPIKE ***`. If spikes are found and SMTP is configured, an alert email is sent.

---

## Network Security Group Audit

Lists all NSGs across a subscription, identifies inbound rules that allow Internet traffic, and flags any rule permitting SSH, RDP, or unrestricted TCP from any source.

```python
#!/usr/bin/env python3
"""Azure NSG Audit — flags overly permissive inbound rules."""

import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

# --- Configuration ---
SUBSCRIPTION_ID = "YOUR_SUBSCRIPTION_ID"
DANGEROUS_PORTS = {22, 3389}
# ---------------------

INTERNET_SOURCES = {"Internet", "Any", "*", "0.0.0.0/0"}

HEADER = (
    f"{'NSG':<35} {'ResourceGroup':<25} {'RuleName':<30} "
    f"{'Port':<10} {'Protocol':<10} {'Action':<8} {'Finding'}"
)
SEP = "-" * len(HEADER)

findings: list[dict] = []


def port_matches_dangerous(port_range: str) -> bool:
    if port_range in ("*", "Any"):
        return True
    if "-" in port_range:
        lo, hi = port_range.split("-", 1)
        try:
            rng = range(int(lo), int(hi) + 1)
            return any(p in rng for p in DANGEROUS_PORTS)
        except ValueError:
            return False
    try:
        return int(port_range) in DANGEROUS_PORTS
    except ValueError:
        return False


def is_internet_source(prefix: str) -> bool:
    return prefix in INTERNET_SOURCES


def main() -> None:
    cred   = DefaultAzureCredential()
    client = NetworkManagementClient(cred, SUBSCRIPTION_ID)

    nsgs  = list(client.network_security_groups.list_all())
    print(f"Auditing {len(nsgs)} NSG(s)...\n")
    print(HEADER)
    print(SEP)

    total_issues = 0

    for nsg in nsgs:
        nsg_name = nsg.name
        rg_name  = nsg.id.split("/")[4]
        rules    = nsg.security_rules or []

        nsg_issues = 0
        for rule in rules:
            if rule.direction != "Inbound":
                continue
            if rule.access != "Allow":
                continue

            src_prefix = rule.source_address_prefix or ""
            src_prefixes = rule.source_address_prefixes or []
            all_sources  = [src_prefix] + list(src_prefixes)

            if not any(is_internet_source(s) for s in all_sources):
                continue

            # Source is Internet / Any — check ports
            dest_port_range  = rule.destination_port_range or ""
            dest_port_ranges = rule.destination_port_ranges or []
            all_ports        = [dest_port_range] + list(dest_port_ranges)

            for port in all_ports:
                finding = None
                if port in ("*", "Any"):
                    finding = "ALLOWS_ALL_PORTS_FROM_INTERNET"
                elif port_matches_dangerous(port):
                    port_num = port if port not in ("*", "Any") else "ALL"
                    if "22" in str(port) or port_num == "22":
                        finding = "SSH_OPEN_TO_INTERNET"
                    elif "3389" in str(port) or port_num == "3389":
                        finding = "RDP_OPEN_TO_INTERNET"
                    else:
                        finding = f"DANGEROUS_PORT_{port}_FROM_INTERNET"

                if finding:
                    findings.append({
                        "NSG":          nsg_name,
                        "ResourceGroup": rg_name,
                        "RuleName":     rule.name,
                        "Port":         port,
                        "Protocol":     rule.protocol,
                        "Action":       rule.access,
                        "Finding":      finding,
                    })
                    print(
                        f"{nsg_name:<35} {rg_name:<25} {rule.name:<30} "
                        f"{port:<10} {rule.protocol:<10} {rule.access:<8} {finding}"
                    )
                    nsg_issues += 1
                    total_issues += 1

        if nsg_issues == 0:
            print(f"{nsg_name:<35} {rg_name:<25} {'(no public inbound issues)'}")

    print(SEP)
    print(f"\nNSGs audited      : {len(nsgs)}")
    print(f"Issues found      : {total_issues}")

    if total_issues > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
```

### How to run this script — step by step

**Before you start — what you need**
- Python installed
- Azure CLI installed and logged in (`az login`)
- Your Azure account must have Network Contributor or Reader access to the subscription
- The Azure Python SDK packages installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `azure_nsg_audit.py` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `DANGEROUS_PORTS` | Ports to flag as dangerous when open to the internet | Default: `{22, 3389}` (SSH and RDP) |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt.

**Step 4 — Install packages and run**

```bash
cd C:\Users\YourName\Desktop
pip install azure-identity azure-mgmt-network
python azure_nsg_audit.py
```

**What you should see**

A table with one row per problematic NSG rule. Each row shows the NSG name, resource group, rule name, port, protocol, and a finding code like `SSH_OPEN_TO_INTERNET` or `RDP_OPEN_TO_INTERNET`. NSGs with no issues show `(no public inbound issues)`. The script exits with an error if any issues are found.

---

## VM DR Failover with Azure Site Recovery (Ansible)

Checks ASR replication health, triggers failover for specified VMs, waits for completion, verifies the VMs are running in the target region, and prints a summary.

```yaml
---
# azure_dr_failover.yml
# Requires: azure.azcollection
# ansible-galaxy collection install azure.azcollection

- name: Azure VM DR Failover via Site Recovery
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    subscription_id:      "YOUR_SUBSCRIPTION_ID"
    source_rg:            "rg-production"
    target_rg:            "rg-dr"
    recovery_vault_name:  "rsv-prod-dr"
    recovery_vault_rg:    "rg-dr"
    vm_names:             []          # e.g. ["vm-app01", "vm-db01"]
    failover_direction:   "PrimaryToRecovery"
    wait_timeout_minutes: 30

  tasks:

    - name: Authenticate and set Azure subscription context
      azure.azcollection.azure_rm_subscription_info:
        id: "{{ subscription_id }}"
      register: sub_info

    - name: Check ASR replication health for each VM
      azure.azcollection.azure_rm_siterecoveryfabric_info:
        resource_group:    "{{ recovery_vault_rg }}"
        recovery_vault_name: "{{ recovery_vault_name }}"
      register: asr_fabric_info

    - name: Display replication fabric info
      ansible.builtin.debug:
        var: asr_fabric_info

    - name: Trigger planned failover for each VM
      azure.azcollection.azure_rm_siterecoveryreplications:
        resource_group:      "{{ recovery_vault_rg }}"
        recovery_vault_name: "{{ recovery_vault_name }}"
        fabric_name:         "{{ item }}"
        replication_policy:  "{{ failover_direction }}"
        state:               present
      loop: "{{ vm_names }}"
      register: failover_results

    - name: Wait for failover completion (poll VM power state)
      azure.azcollection.azure_rm_virtualmachine_info:
        resource_group: "{{ target_rg }}"
        name:           "{{ item }}"
      loop: "{{ vm_names }}"
      register: vm_status
      until: >
        vm_status.vms | default([]) | length > 0 and
        vm_status.vms[0].power_state == 'running'
      retries: "{{ wait_timeout_minutes * 3 }}"
      delay: 20

    - name: Verify VMs are running in target resource group
      ansible.builtin.assert:
        that: >
          item.vms | default([]) | length > 0 and
          item.vms[0].power_state == 'running'
        fail_msg:    "VM {{ item.item }} failed to reach running state in {{ target_rg }}"
        success_msg: "VM {{ item.item }} is running in {{ target_rg }}"
      loop: "{{ vm_status.results }}"

    - name: Print DR failover summary
      ansible.builtin.debug:
        msg:
          - "===== Azure DR Failover Summary ====="
          - "Source RG       : {{ source_rg }}"
          - "Target RG       : {{ target_rg }}"
          - "Recovery Vault  : {{ recovery_vault_name }}"
          - "VMs failed over : {{ vm_names | join(', ') }}"
          - "Status          : COMPLETED"
      loop: "{{ vm_status.results }}"

    - name: Print new VM IP addresses
      ansible.builtin.debug:
        msg: >-
          {{ item.item }}: private IP
          {{ item.vms[0].network_interface_names | default(['(check portal)']) | first }}
      loop: "{{ vm_status.results }}"
      when: item.vms is defined and item.vms | length > 0
```

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on Linux or WSL (Ansible does not run natively on Windows)
- Azure Ansible collection installed: `ansible-galaxy collection install azure.azcollection`
- Azure Site Recovery set up in your subscription with replication already configured for the VMs
- Azure credentials available via `az login` or service principal environment variables

**Step 1 — Save the file**

1. Open your WSL terminal (Windows key → type `wsl`)
2. Create the file: `nano azure_dr_failover.yml`
3. Paste the code, then press `Ctrl+X`, `Y`, `Enter` to save

**Step 2 — Fill in your details**

Open the file and update the `vars:` section:

| Variable | What to enter | Where to find it |
|---|---|---|
| `subscription_id` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `source_rg` | Resource group where your production VMs live | Azure Portal → Resource Groups |
| `target_rg` | Resource group in your DR region | Azure Portal → Resource Groups |
| `recovery_vault_name` | Name of your Recovery Services Vault | Azure Portal → Recovery Services Vaults |
| `recovery_vault_rg` | Resource group containing the Recovery Vault | Same page as above |
| `vm_names` | List of VM names to fail over, e.g. `["vm-app01"]` | Azure Portal → Virtual Machines |

**Step 3 — Open the right terminal**

- **For .yml (Ansible):** Needs Linux or WSL. Open your WSL terminal.

**Step 4 — Run it**

```bash
cd ~
ansible-playbook azure_dr_failover.yml
```

**What you should see**

Ansible checks ASR replication health, triggers the failover for each VM in your list, then polls until the VMs come up running in the DR resource group. At the end it prints a summary confirming each VM's name and the result. The whole process can take 10–30 minutes depending on VM size.

---

## Managed Disk Snapshot Audit

Lists all managed disk snapshots, identifies those older than 30 days, calculates total wasted storage cost, and optionally deletes them with a confirmation prompt.

```bash
#!/bin/bash
set -euo pipefail

SUBSCRIPTION_ID="${SUBSCRIPTION_ID:-$(az account show --query id -o tsv)}"
AGE_DAYS="${AGE_DAYS:-30}"
DELETE_OLD="${1:-}"

BOLD="\033[1m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
GREEN="\033[0;32m"
RESET="\033[0m"

echo -e "${BOLD}=== Azure Managed Disk Snapshot Audit ===${RESET}"
echo "Subscription : ${SUBSCRIPTION_ID}"
echo "Age threshold: ${AGE_DAYS} days"
echo "Time         : $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

SNAPSHOTS_JSON=$(az snapshot list \
  --subscription "${SUBSCRIPTION_ID}" \
  -o json)

python3 - <<PYEOF
import json, os, sys, datetime

snapshots  = json.loads("""${SNAPSHOTS_JSON}""".replace('${SNAPSHOTS_JSON}', ''))
age_thresh = int("${AGE_DAYS}")
now        = datetime.datetime.utcnow()

old_snaps      = []
total_size_gb  = 0
old_size_gb    = 0

print(f"{'Snapshot':<50} {'Disk':<40} {'RG':<25} {'Created':<12} {'Age(d)':>6} {'Size(GB)':>9}")
print("-" * 150)

for snap in sorted(snapshots, key=lambda s: s.get("timeCreated", ""), reverse=True):
    name       = snap.get("name", "")[:49]
    disk       = (snap.get("creationData") or {}).get("sourceResourceId", "")
    disk       = disk.split("/")[-1] if disk else "(detached)"
    rg         = snap.get("resourceGroup", "")[:24]
    created_str= snap.get("timeCreated", "")[:10]
    size_gb    = snap.get("diskSizeGb", 0) or 0
    total_size_gb += size_gb

    try:
        created = datetime.datetime.strptime(created_str, "%Y-%m-%d")
        age     = (now - created).days
    except ValueError:
        age = -1

    flag = "  <-- OLD" if age >= age_thresh else ""
    print(f"{name:<50} {disk:<40} {rg:<25} {created_str:<12} {age:>6} {size_gb:>9}{flag}")

    if age >= age_thresh:
        old_snaps.append(snap)
        old_size_gb += size_gb

print("-" * 150)
print(f"\nTotal snapshots      : {len(snapshots)}")
print(f"Snapshots >= {age_thresh}d      : {len(old_snaps)}")
print(f"Total size           : {total_size_gb} GB")
print(f"Old snapshot size    : {old_size_gb} GB (estimated wasted cost)")

PYEOF

export SNAPSHOTS_JSON
python3 - <<'PYEOF'
import json, os, sys, datetime

snapshots  = json.loads(os.environ["SNAPSHOTS_JSON"])
age_thresh = int(os.environ.get("AGE_DAYS", "30"))
now        = datetime.datetime.utcnow()

old_snaps = []
for snap in snapshots:
    created_str = snap.get("timeCreated", "")[:10]
    try:
        created = datetime.datetime.strptime(created_str, "%Y-%m-%d")
        age     = (now - created).days
    except ValueError:
        continue
    if age >= age_thresh:
        old_snaps.append(snap)

if old_snaps:
    os.environ["OLD_SNAP_IDS"] = json.dumps([s["id"] for s in old_snaps])
    os.environ["OLD_SNAP_NAMES"] = json.dumps([s["name"] for s in old_snaps])

PYEOF

# Optional deletion
if [[ "${DELETE_OLD:-}" == "--delete" ]]; then
  echo -e "\n${RED}WARNING: About to delete old snapshots.${RESET}"
  read -r -p "Type DELETE to confirm: " CONFIRM
  if [[ "${CONFIRM}" == "DELETE" ]]; then
    OLD_NAMES=$(python3 -c "import json,os; print(' '.join(json.loads(os.environ.get('OLD_SNAP_NAMES','[]'))))")
    for snap_name in ${OLD_NAMES}; do
      echo "Deleting snapshot: ${snap_name}"
      az snapshot delete \
        --subscription "${SUBSCRIPTION_ID}" \
        --name "${snap_name}" \
        --resource-group "$(az snapshot show --subscription "${SUBSCRIPTION_ID}" --name "${snap_name}" --query resourceGroup -o tsv)" \
        --yes
    done
    echo -e "${GREEN}Deletion complete.${RESET}"
  else
    echo "Aborted."
  fi
fi
```

### How to run this script — step by step

**Before you start — what you need**
- Azure CLI installed and you are logged in (`az login`)
- Git Bash installed (from https://gitforwindows.org) to run `.sh` scripts on Windows
- Your Azure account needs Contributor access to manage snapshots

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `azure-snapshot-audit.sh` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `AGE_DAYS` | Flag snapshots older than this many days | Default: `30` |

**Step 3 — Open the right terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) → open Git Bash

**Step 4 — Run it**

```bash
cd ~/Desktop
bash azure-snapshot-audit.sh
```

To also delete old snapshots (use with caution — this is permanent):

```text
bash azure-snapshot-audit.sh --delete
```

**What you should see**

A table listing every managed disk snapshot with its age in days and size in GB. Snapshots older than your threshold are marked `<-- OLD`. At the bottom you see totals: how many old snapshots exist and how many GB they are taking up. If you run with `--delete` you will be asked to type `DELETE` to confirm before anything is removed.

---

## Key Vault Certificate Expiry Check

Lists all Key Vaults in a subscription, checks every certificate's expiration date, and flags certificates expiring within 30 days (WARNING) or 14 days (CRITICAL). Exits non-zero if any CRITICAL certificates are found.

```python
#!/usr/bin/env python3
"""Azure Key Vault Certificate Expiry Check — WARNING <30d, CRITICAL <14d."""

import sys
import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault.certificates import CertificateClient

# --- Configuration ---
SUBSCRIPTION_ID    = "YOUR_SUBSCRIPTION_ID"
WARNING_DAYS       = 30
CRITICAL_DAYS      = 14
# ---------------------

NOW = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

HEADER = f"{'Vault':<30} {'Certificate':<40} {'Expiry':<22} {'DaysLeft':>9} {'Status'}"
SEP    = "-" * len(HEADER)


def check_vault(vault_name: str, vault_url: str, cred) -> list[dict]:
    client = CertificateClient(vault_url=vault_url, credential=cred)
    results = []
    try:
        for cert_prop in client.list_properties_of_certificates():
            try:
                cert = client.get_certificate(cert_prop.name)
                expiry = cert.properties.expires_on
                if expiry is None:
                    continue
                days_left = (expiry - NOW).days

                if days_left <= CRITICAL_DAYS:
                    status = "CRITICAL"
                elif days_left <= WARNING_DAYS:
                    status = "WARNING"
                else:
                    status = "OK"

                results.append({
                    "Vault":       vault_name,
                    "Certificate": cert_prop.name,
                    "Expiry":      expiry.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "DaysLeft":    days_left,
                    "Status":      status,
                })
            except Exception as exc:
                results.append({
                    "Vault":       vault_name,
                    "Certificate": cert_prop.name,
                    "Expiry":      "ERROR",
                    "DaysLeft":    -1,
                    "Status":      f"ERROR: {exc}",
                })
    except Exception as exc:
        print(f"  Warning: could not access vault {vault_name}: {exc}")
    return results


def main() -> None:
    cred   = DefaultAzureCredential()
    kv_mgmt = KeyVaultManagementClient(cred, SUBSCRIPTION_ID)

    vaults = list(kv_mgmt.vaults.list())
    print(f"Checking {len(vaults)} Key Vault(s)...\n")
    print(HEADER)
    print(SEP)

    all_results: list[dict] = []
    for vault in vaults:
        vault_url = vault.properties.vault_uri
        results   = check_vault(vault.name, vault_url, cred)
        all_results.extend(results)

    # Sort: CRITICAL first, then WARNING, then by days left
    status_order = {"CRITICAL": 0, "WARNING": 1, "OK": 2}
    all_results.sort(key=lambda r: (status_order.get(r["Status"], 3), r["DaysLeft"]))

    for r in all_results:
        print(
            f"{r['Vault']:<30} {r['Certificate']:<40} {r['Expiry']:<22} "
            f"{r['DaysLeft']:>9}  {r['Status']}"
        )

    print(SEP)

    critical = [r for r in all_results if r["Status"] == "CRITICAL"]
    warnings = [r for r in all_results if r["Status"] == "WARNING"]

    print(f"\nTotal certificates : {len(all_results)}")
    print(f"Critical (<{CRITICAL_DAYS}d)      : {len(critical)}")
    print(f"Warning (<{WARNING_DAYS}d)       : {len(warnings)}")

    if critical:
        print("\nCRITICAL certificates:")
        for r in critical:
            print(f"  {r['Vault']}/{r['Certificate']}  — {r['DaysLeft']} days remaining")
        raise SystemExit(1)

    print("\nAll certificates OK.")


if __name__ == "__main__":
    main()
```

### How to run this script — step by step

**Before you start — what you need**
- Python installed
- Azure CLI installed and logged in (`az login`)
- Your Azure account needs Key Vault Reader access plus `certificates/get` and `certificates/list` permissions on the Key Vaults
- The Azure Python SDK packages installed

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `azure_cert_expiry.py` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `WARNING_DAYS` | Days before expiry to warn | Default: `30` |
| `CRITICAL_DAYS` | Days before expiry to mark as critical | Default: `14` |

**Step 3 — Open the right terminal**

- **For .py (Python):** Open Command Prompt.

**Step 4 — Install packages and run**

```bash
cd C:\Users\YourName\Desktop
pip install azure-identity azure-mgmt-keyvault azure-keyvault-certificates
python azure_cert_expiry.py
```

**What you should see**

A table sorted with CRITICAL certificates first, then WARNING, then OK. Each row shows the vault name, certificate name, expiry date, days remaining, and status. The script exits with an error if any CRITICAL certificates are found.

---

## Ansible Azure Infrastructure Health Playbook

Checks VM power states, load balancer health, storage account tiers, Key Vault certificate expiry, and NSG rule permissiveness across production resource groups, then prints a consolidated summary.

```yaml
---
# azure_infra_health.yml
# Requires: azure.azcollection
# ansible-galaxy collection install azure.azcollection

- name: Azure Infrastructure Health Check
  hosts: localhost
  connection: local
  gather_facts: true

  vars:
    subscription_id: "YOUR_SUBSCRIPTION_ID"
    resource_groups:
      - "rg-production-01"
      - "rg-production-02"
    keyvault_names:
      - "kv-prod-01"
      - "kv-prod-02"
    cert_warning_days: 30

  tasks:

    # ---------------------------------------------------------------
    # Virtual Machines
    # ---------------------------------------------------------------
    - name: Get VM facts for each production resource group
      azure.azcollection.azure_rm_virtualmachine_info:
        resource_group: "{{ item }}"
        subscription_id: "{{ subscription_id }}"
      loop: "{{ resource_groups }}"
      register: vm_facts_all

    - name: Assert all VMs are in running state
      ansible.builtin.assert:
        that: >
          item.vms | default([]) | selectattr('power_state', '!=', 'running') | list | length == 0
        fail_msg: >-
          Non-running VMs in {{ item.item }}:
          {{ item.vms | selectattr('power_state', '!=', 'running') | map(attribute='name') | list }}
        success_msg: "All VMs running in {{ item.item }}"
      loop: "{{ vm_facts_all.results }}"

    # ---------------------------------------------------------------
    # Load Balancers
    # ---------------------------------------------------------------
    - name: Get load balancer info per resource group
      azure.azcollection.azure_rm_loadbalancer_info:
        resource_group:  "{{ item }}"
        subscription_id: "{{ subscription_id }}"
      loop: "{{ resource_groups }}"
      register: lb_facts_all

    - name: Report load balancer provisioning states
      ansible.builtin.debug:
        msg: >-
          LB {{ item.1.name }} ({{ item.0.item }}) —
          state: {{ item.1.provisioning_state | default('unknown') }}
      loop: "{{ lb_facts_all.results | subelements('loadbalancers', skip_missing=true) }}"

    # ---------------------------------------------------------------
    # Storage Accounts
    # ---------------------------------------------------------------
    - name: Get storage account info per resource group
      azure.azcollection.azure_rm_storageaccount_info:
        resource_group:  "{{ item }}"
        subscription_id: "{{ subscription_id }}"
      loop: "{{ resource_groups }}"
      register: storage_facts_all

    - name: Report storage account access tiers
      ansible.builtin.debug:
        msg: >-
          Storage {{ item.1.name }} ({{ item.0.item }}) —
          tier: {{ item.1.access_tier | default('Standard') }},
          kind: {{ item.1.kind | default('unknown') }}
      loop: "{{ storage_facts_all.results | subelements('storageaccounts', skip_missing=true) }}"

    # ---------------------------------------------------------------
    # Key Vault — Certificate Expiry
    # ---------------------------------------------------------------
    - name: Get Key Vault key/certificate info
      azure.azcollection.azure_rm_keyvaultkey_info:
        vault_uri:       "https://{{ item }}.vault.azure.net/"
        subscription_id: "{{ subscription_id }}"
      loop: "{{ keyvault_names }}"
      register: kv_facts
      ignore_errors: true

    - name: Flag Key Vault certificates expiring within warning window
      ansible.builtin.debug:
        msg: >-
          WARNING: {{ item.0.item }}/{{ item.1.kid | default(item.1.name) }}
          expires {{ item.1.attributes.expires | default('unknown') }}
      loop: "{{ kv_facts.results | subelements('keys', skip_missing=true) }}"
      when: >
        item.1.attributes is defined and
        item.1.attributes.expires is defined

    # ---------------------------------------------------------------
    # NSG — Overly Permissive Rules
    # ---------------------------------------------------------------
    - name: Get NSG info per resource group
      azure.azcollection.azure_rm_securitygroup_info:
        resource_group:  "{{ item }}"
        subscription_id: "{{ subscription_id }}"
      loop: "{{ resource_groups }}"
      register: nsg_facts_all

    - name: Flag overly permissive NSG inbound rules
      ansible.builtin.debug:
        msg: >-
          OVERLY PERMISSIVE: NSG {{ item.1.name }} in {{ item.0.item }}
          has inbound Allow from Any — review immediately.
      loop: "{{ nsg_facts_all.results | subelements('securitygroups', skip_missing=true) }}"
      when: >
        item.1.security_rules is defined and
        item.1.security_rules | selectattr('direction', 'equalto', 'Inbound')
                               | selectattr('access', 'equalto', 'Allow')
                               | selectattr('source_address_prefix', 'in', ['*', 'Any', 'Internet'])
                               | list | length > 0

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    - name: Print infrastructure health summary
      ansible.builtin.debug:
        msg:
          - "===== Azure Infrastructure Health Summary ====="
          - "Subscription    : {{ subscription_id }}"
          - "Resource Groups : {{ resource_groups | join(', ') }}"
          - "Key Vaults      : {{ keyvault_names | join(', ') }}"
          - "Run date        : {{ ansible_date_time.iso8601 }}"
          - "Result          : PASSED (assertions above would have failed otherwise)"
```

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on Linux or WSL (Ansible does not run natively on Windows)
- Azure Ansible collection: `ansible-galaxy collection install azure.azcollection`
- Azure credentials via `az login` or a service principal

**Step 1 — Save the file**

1. Open your WSL terminal (Windows key → type `wsl`)
2. Create the file: `nano azure_infra_health.yml`
3. Paste the code, then press `Ctrl+X`, `Y`, `Enter` to save

**Step 2 — Fill in your details**

Open the file and update the `vars:` section:

| Variable | What to enter | Where to find it |
|---|---|---|
| `subscription_id` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `resource_groups` | List of resource group names to check | Azure Portal → Resource Groups |
| `keyvault_names` | List of Key Vault names to check | Azure Portal → Key Vaults |
| `cert_warning_days` | Days before expiry to flag | Default: `30` |

**Step 3 — Open the right terminal**

- **For .yml (Ansible):** Needs Linux or WSL. Open your WSL terminal.

**Step 4 — Run it**

```bash
cd ~
ansible-playbook azure_infra_health.yml
```

**What you should see**

Ansible works through each check in sequence. VM asserts show green `ok` if all VMs are running or red `failed` with the list of problem VMs. Load balancer, storage, Key Vault, and NSG info is printed as debug messages. At the end a summary block shows what was checked.

---

## Windows: Azure VM Health Check via Azure CLI (CMD Batch)

Check your Azure VMs, monitor alerts, and get Advisor recommendations directly from Windows using the Azure CLI.

```batch
@echo off
REM azure-health-check.bat
REM Requires: Azure CLI for Windows
REM Download: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows
REM Run "az login" in Command Prompt first to authenticate.

set SUBSCRIPTION_ID=YOUR_SUBSCRIPTION_ID
set RESOURCE_GROUP=YOUR_RESOURCE_GROUP

echo === Azure VM Health Check ===
echo Subscription : %SUBSCRIPTION_ID%
echo Resource Group: %RESOURCE_GROUP%
echo.

echo --- Setting subscription context ---
az account set --subscription %SUBSCRIPTION_ID%
echo.

echo --- VM List with Power State ---
az vm list --show-details --query "[*].{Name:name,Status:powerState,RG:resourceGroup}" --output table
echo.

echo --- Activity Log Alerts ---
az monitor activity-log alert list --output table
echo.

echo --- High Availability Advisor Recommendations ---
az advisor recommendation list --category HighAvailability --output table
echo.

echo Health check complete.
pause
```

### How to run this script — step by step

**Before you start — what you need**
- Azure CLI for Windows installed (download the MSI from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
- Logged in to Azure: open Command Prompt and run `az login` — this opens your browser for authentication
- Your Azure account must have at least Reader access on the subscription

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — prevents Notepad adding .txt)
5. Name it `azure-health-check.bat` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `SUBSCRIPTION_ID` | Your Azure subscription ID | Azure Portal → Subscriptions → copy the Subscription ID |
| `RESOURCE_GROUP` | Your resource group name | Azure Portal → Resource Groups |

**Step 3 — Open the right terminal**

- **For .bat / .cmd:** Open Command Prompt or just double-click the file

**Step 4 — Run it**

```bash
cd C:\Users\YourName\Desktop
azure-health-check.bat
```

Or just double-click the file from your Desktop.

**What you should see**

A table of all your Azure VMs with their current power state (running, stopped, deallocated). Then any activity log alerts that are configured, followed by any High Availability recommendations from Azure Advisor. The window stays open so you can read the output.

---

## Windows: Azure Resource Health Report (PowerShell with Az Module)

Get a full health and recommendations report for your Azure subscription using the official Az PowerShell module.

```powershell
# azure-resource-health.ps1
# Requires: Az PowerShell module
# Install with: Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force

param(
    [string]$SubscriptionId = "YOUR_SUBSCRIPTION_ID",
    [string]$ResourceGroup  = "YOUR_RESOURCE_GROUP"
)

# Install Az module if not present
if (-not (Get-Module -ListAvailable -Name Az.Accounts)) {
    Write-Host "Installing Az module (this may take a few minutes)..." -ForegroundColor Yellow
    Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
}

Import-Module Az.Accounts
Import-Module Az.Compute
Import-Module Az.Advisor -ErrorAction SilentlyContinue

Write-Host "`n=== Azure Resource Health Report ===" -ForegroundColor Cyan

# Connect (opens browser for MFA login)
Connect-AzAccount -SubscriptionId $SubscriptionId

Write-Host "`n--- VM Power States ---" -ForegroundColor White

$vms = if ($ResourceGroup) {
    Get-AzVM -ResourceGroupName $ResourceGroup -Status
} else {
    Get-AzVM -Status
}

$vmReport = $vms | ForEach-Object {
    $powerState = ($_.Statuses | Where-Object { $_.Code -like "PowerState/*" }).DisplayStatus
    [PSCustomObject]@{
        Name          = $_.Name
        ResourceGroup = $_.ResourceGroupName
        Location      = $_.Location
        Size          = $_.HardwareProfile.VmSize
        PowerState    = $powerState
        Status        = if ($powerState -eq "VM running") { "OK" } else { "ATTENTION" }
    }
}

$vmReport | Format-Table -AutoSize

$notRunning = $vmReport | Where-Object { $_.Status -ne "OK" }
if ($notRunning.Count -gt 0) {
    Write-Host "VMs not running:" -ForegroundColor Yellow
    $notRunning | ForEach-Object {
        Write-Host "  $($_.Name) ($($_.ResourceGroup)) — $($_.PowerState)" -ForegroundColor Yellow
    }
}

Write-Host "`n--- Advisor Recommendations ---" -ForegroundColor White
try {
    $recommendations = Get-AzAdvisorRecommendation
    if ($recommendations) {
        $recommendations | Select-Object -Property Category, Impact, ShortDescription, ResourceId |
            Format-Table -AutoSize
        Write-Host "Total recommendations: $($recommendations.Count)"
    } else {
        Write-Host "No Advisor recommendations found." -ForegroundColor Green
    }
} catch {
    Write-Host "Could not retrieve Advisor recommendations: $_" -ForegroundColor Yellow
}

Write-Host "`n--- Summary ---" -ForegroundColor Cyan
Write-Host "Subscription  : $SubscriptionId"
Write-Host "Resource Group: $(if ($ResourceGroup) { $ResourceGroup } else { 'All' })"
Write-Host "Total VMs     : $($vmReport.Count)"
Write-Host "VMs running   : $(($vmReport | Where-Object { $_.Status -eq 'OK' }).Count)"
Write-Host "VMs not running: $($notRunning.Count)"
```

### How to run this script — step by step

**Before you start — what you need**
- Windows PowerShell 5.1 or PowerShell 7
- Internet access so PowerShell can download the Az module
- An Azure account — the script will open your browser for MFA login

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search for Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — prevents Notepad adding .txt)
5. Name it `azure-resource-health.ps1` and save to your Desktop

**Step 2 — Fill in your details**

Open the saved file and update these values at the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `$SubscriptionId` | Your Azure subscription ID | Azure Portal → Subscriptions |
| `$ResourceGroup` | Your resource group name, or leave as empty `""` for all | Azure Portal → Resource Groups |

**Step 3 — Open the right terminal**

- **For .ps1 (PowerShell):** Windows key → `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```bash
cd C:\Users\YourName\Desktop
.\azure-resource-health.ps1
```

**What you should see**

The first time it runs, it installs the Az PowerShell module automatically (can take 5–10 minutes). Then your browser opens for Azure login. After login, it prints a table of VMs with their power state and flags any that are not running. Then it shows any Azure Advisor recommendations for improving your environment.

---

## Daily Check Script

Azure environment daily health check covering authentication, VM power states, Advisor HIGH severity HA issues, NSG rule count, and resource group population.

```bash
#!/bin/bash
# azure_daily_check.sh — Azure environment daily health check
SUBSCRIPTION_ID="${SUBSCRIPTION_ID:-}"
RESOURCE_GROUP="${RESOURCE_GROUP:-}"
FAIL=0

check() { local l="$1"; shift; "$@" &>/dev/null && echo "[OK]   $l" || { echo "[FAIL] $l"; FAIL=$((FAIL+1)); }; }

echo "=== Azure Daily Check: $RESOURCE_GROUP — $(date) ==="
check "Azure CLI auth" az account show
check "All VMs running" bash -c "[ \$(az vm list --resource-group $RESOURCE_GROUP --query \"[?powerState!='VM running'].name\" --show-details -o tsv | wc -l) -eq 0 ]"
check "No Azure Advisor HIGH severity" bash -c "[ \$(az advisor recommendation list --category HighAvailability --query \"[?impact=='High'].id\" -o tsv | wc -l) -eq 0 ]"
check "NSG rules within expected count" az network nsg list --resource-group $RESOURCE_GROUP --query '[*].name' -o tsv | wc -l | grep -qv "^0$"
check "Resource health OK" bash -c "az resource list --resource-group $RESOURCE_GROUP -o tsv | wc -l | grep -qv '^0$'"

echo ""
echo "Daily check: $FAIL failure(s)"
[[ $FAIL -gt 0 ]] && exit 2 || exit 0
```

---

## Incident Triage Script

Capture VM states, NSG rules, storage account status, Key Vault access logs, recent Activity Log events, and Advisor recommendations to a timestamped file.

```bash
#!/bin/bash
# azure_triage.sh
# Usage: SUBSCRIPTION_ID=<id> RESOURCE_GROUP=<rg> ./azure_triage.sh

SUBSCRIPTION_ID="${SUBSCRIPTION_ID:?SUBSCRIPTION_ID is required}"
RESOURCE_GROUP="${RESOURCE_GROUP:?RESOURCE_GROUP is required}"
OUTFILE="/tmp/azure_triage_${RESOURCE_GROUP}_$(date +%Y%m%d_%H%M%S).txt"

{
  echo "=== Azure Incident Triage: $RESOURCE_GROUP — $(date) ==="
  echo ""
  echo "--- VM states ---"
  az vm list --resource-group "$RESOURCE_GROUP" --show-details \
    --query '[*].[name,powerState,location]' -o table
  echo ""
  echo "--- NSG rules ---"
  az network nsg list --resource-group "$RESOURCE_GROUP" -o table
  echo ""
  echo "--- Storage account status ---"
  az storage account list --resource-group "$RESOURCE_GROUP" \
    --query '[*].[name,statusOfPrimary,provisioningState]' -o table
  echo ""
  echo "--- Recent Activity Log events (last 2h) ---"
  START=$(date -u -v-2H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '2 hours ago' +%Y-%m-%dT%H:%M:%SZ)
  az monitor activity-log list --resource-group "$RESOURCE_GROUP" \
    --start-time "$START" --max-events 50 \
    --query '[*].[eventTimestamp,operationName.localizedValue,status.localizedValue,caller]' -o table
  echo ""
  echo "--- Advisor recommendations ---"
  az advisor recommendation list --resource-group "$RESOURCE_GROUP" \
    --query '[*].[category,impact,shortDescription.problem]' -o table
} > "$OUTFILE" 2>&1

echo "Triage data saved to: $OUTFILE"
```

---

## Change Pre-Check Script

Validate Azure environment before a deployment. Exits 2 if any critical condition is found.

```bash
#!/bin/bash
# azure_precheck.sh
# Usage: SUBSCRIPTION_ID=<id> RESOURCE_GROUP=<rg> ./azure_precheck.sh

SUBSCRIPTION_ID="${SUBSCRIPTION_ID:?SUBSCRIPTION_ID is required}"
RESOURCE_GROUP="${RESOURCE_GROUP:?RESOURCE_GROUP is required}"
FAIL=0

echo "=== Azure Pre-Change Check: $RESOURCE_GROUP — $(date) ==="

# All VMs running
NOT_RUNNING=$(az vm list --resource-group "$RESOURCE_GROUP" --show-details \
  --query "[?powerState!='VM running'].name" -o tsv | wc -l | tr -d ' ')
if [ "$NOT_RUNNING" -gt 0 ]; then
  echo "[FAIL] $NOT_RUNNING VM(s) not in running state"; FAIL=$((FAIL+1))
else
  echo "[OK]   All VMs running"
fi

# No active Resource Health incidents (proxy: no recent critical activity log events)
CRITICAL=$(az monitor activity-log list --resource-group "$RESOURCE_GROUP" \
  --max-events 20 --filter "level eq 'Critical'" \
  --query 'length([*])' -o tsv 2>/dev/null || echo 0)
if [ "${CRITICAL:-0}" -gt 0 ]; then
  echo "[FAIL] $CRITICAL critical event(s) in activity log"; FAIL=$((FAIL+1))
else
  echo "[OK]   No critical events in activity log"
fi

# Advisor has no HIGH severity HA issues
HIGH_ADVISOR=$(az advisor recommendation list --category HighAvailability \
  --query "[?impact=='High'].id" -o tsv | wc -l | tr -d ' ')
if [ "$HIGH_ADVISOR" -gt 0 ]; then
  echo "[FAIL] $HIGH_ADVISOR HIGH severity Advisor recommendation(s)"; FAIL=$((FAIL+1))
else
  echo "[OK]   No HIGH severity Advisor HA issues"
fi

echo ""
echo "Pre-check: $FAIL failure(s)"
[ "$FAIL" -gt 0 ] && exit 2 || exit 0
```

---

## Post-Change Validation Script

After a deployment: confirm new resources exist and are healthy, no new Activity Log errors, VMs still accessible, and tags applied correctly.

```bash
#!/bin/bash
# azure_postcheck.sh
# Usage: SUBSCRIPTION_ID=<id> RESOURCE_GROUP=<rg> [NEW_RESOURCE_NAME=<name>] ./azure_postcheck.sh

SUBSCRIPTION_ID="${SUBSCRIPTION_ID:?SUBSCRIPTION_ID is required}"
RESOURCE_GROUP="${RESOURCE_GROUP:?RESOURCE_GROUP is required}"
NEW_RESOURCE_NAME="${NEW_RESOURCE_NAME:-}"
FAIL=0

echo "=== Azure Post-Change Validation: $RESOURCE_GROUP — $(date) ==="

# New resource exists (if name provided)
if [ -n "$NEW_RESOURCE_NAME" ]; then
  EXISTS=$(az resource list --resource-group "$RESOURCE_GROUP" \
    --query "[?name=='$NEW_RESOURCE_NAME'].id" -o tsv | wc -l | tr -d ' ')
  if [ "$EXISTS" -gt 0 ]; then
    echo "[OK]   Resource $NEW_RESOURCE_NAME exists"
  else
    echo "[FAIL] Resource $NEW_RESOURCE_NAME not found"; FAIL=$((FAIL+1))
  fi
fi

# All VMs still running
NOT_RUNNING=$(az vm list --resource-group "$RESOURCE_GROUP" --show-details \
  --query "[?powerState!='VM running'].name" -o tsv | wc -l | tr -d ' ')
if [ "$NOT_RUNNING" -gt 0 ]; then
  echo "[FAIL] $NOT_RUNNING VM(s) not running after change"; FAIL=$((FAIL+1))
else
  echo "[OK]   All VMs running"
fi

# No new Activity Log errors
START=$(date -u -v-30M +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%SZ)
ERRORS=$(az monitor activity-log list --resource-group "$RESOURCE_GROUP" \
  --start-time "$START" --filter "level eq 'Error'" \
  --query 'length([*])' -o tsv 2>/dev/null || echo 0)
if [ "${ERRORS:-0}" -gt 0 ]; then
  echo "[WARN] $ERRORS error event(s) in activity log since change — review"
else
  echo "[OK]   No error events in recent activity log"
fi

echo ""
echo "Post-change validation: $FAIL failure(s)"
[ "$FAIL" -gt 0 ] && exit 2 || exit 0
```

---

## Health Check Script

Cron-safe summary: VM counts (running/stopped), storage account count, Advisor HIGH/MEDIUM recommendations, and recent Activity Log error count. Exits 0 (OK), 1 (WARNING), or 2 (CRITICAL).

```bash
#!/bin/bash
# azure_health_check.sh
# Cron: */5 * * * * SUBSCRIPTION_ID=<id> RESOURCE_GROUP=<rg> /opt/scripts/azure_health_check.sh

SUBSCRIPTION_ID="${SUBSCRIPTION_ID:?SUBSCRIPTION_ID is required}"
RESOURCE_GROUP="${RESOURCE_GROUP:?RESOURCE_GROUP is required}"

RUNNING=$(az vm list --resource-group "$RESOURCE_GROUP" --show-details \
  --query "length([?powerState=='VM running'])" -o tsv 2>/dev/null || echo 0)
STOPPED=$(az vm list --resource-group "$RESOURCE_GROUP" --show-details \
  --query "length([?powerState!='VM running'])" -o tsv 2>/dev/null || echo 0)
STORAGE=$(az storage account list --resource-group "$RESOURCE_GROUP" \
  --query "length([*])" -o tsv 2>/dev/null || echo 0)
HIGH_ADV=$(az advisor recommendation list --category HighAvailability \
  --query "length([?impact=='High'])" -o tsv 2>/dev/null || echo 0)
MED_ADV=$(az advisor recommendation list --category HighAvailability \
  --query "length([?impact=='Medium'])" -o tsv 2>/dev/null || echo 0)
START=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
ACT_ERRORS=$(az monitor activity-log list --resource-group "$RESOURCE_GROUP" \
  --start-time "$START" --filter "level eq 'Error'" \
  --query 'length([*])' -o tsv 2>/dev/null || echo 0)

echo "rg=$RESOURCE_GROUP vms_running=$RUNNING vms_stopped=$STOPPED storage_accounts=$STORAGE advisor_high=$HIGH_ADV advisor_medium=$MED_ADV activity_errors_24h=$ACT_ERRORS"

if [ "${STOPPED:-0}" -gt 2 ] || [ "${HIGH_ADV:-0}" -gt 2 ]; then
  exit 2
elif [ "${STOPPED:-0}" -gt 0 ] || [ "${HIGH_ADV:-0}" -gt 0 ] || [ "${ACT_ERRORS:-0}" -gt 5 ]; then
  exit 1
fi
exit 0
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Azure — Procedures](../procedures/)
- [Azure — CLI Reference](../cli-reference/)
- [Azure — Health Checks](../health-checks/)

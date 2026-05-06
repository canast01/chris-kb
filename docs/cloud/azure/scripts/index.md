# Scripts

> Part of the [Azure](../) reference.

---

## Azure Subscription Health Check

Prints a formatted health report covering VMs, load balancers, SQL servers, and recent critical activity log events. Exits non-zero if any critical events are found.

~~~bash
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
~~~

---

## VM Health and Compliance Report

Authenticates via DefaultAzureCredential, lists all VMs across a subscription, checks tags, backup enrollment, and monitoring agent presence, then exports a CSV report.

~~~python
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
~~~

---

## Azure Cost Spike Alert

Compares daily average spend for the last 7 days versus the prior 7 days per service, flags any service with more than a configurable percentage increase, and sends an alert email via SMTP.

~~~python
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
~~~

---

## Network Security Group Audit

Lists all NSGs across a subscription, identifies inbound rules that allow Internet traffic, and flags any rule permitting SSH, RDP, or unrestricted TCP from any source.

~~~python
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
~~~

---

## VM DR Failover with Azure Site Recovery (Ansible)

Checks ASR replication health, triggers failover for specified VMs, waits for completion, verifies the VMs are running in the target region, and prints a summary.

~~~yaml
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
~~~

---

## Managed Disk Snapshot Audit

Lists all managed disk snapshots, identifies those older than 30 days, calculates total wasted storage cost, and optionally deletes them with a confirmation prompt.

~~~bash
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
~~~

---

## Key Vault Certificate Expiry Check

Lists all Key Vaults in a subscription, checks every certificate's expiration date, and flags certificates expiring within 30 days (WARNING) or 14 days (CRITICAL). Exits non-zero if any CRITICAL certificates are found.

~~~python
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
~~~

---

## Ansible Azure Infrastructure Health Playbook

Checks VM power states, load balancer health, storage account tiers, Key Vault certificate expiry, and NSG rule permissiveness across production resource groups, then prints a consolidated summary.

~~~yaml
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
~~~

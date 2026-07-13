---
tags:
  - scenarios
  - vmware
description: "A VMware Cloud Foundation (VCF) upgrade workflow in SDDC Manager has stalled, failed, or is reporting errors partway through a bundle apply operation..."
---
# VCF SDDC Manager Upgrade Stalled

<div class="kb-summary">
A VMware Cloud Foundation (VCF) upgrade workflow in SDDC Manager has stalled, failed, or is
reporting errors partway through a bundle apply operation. This scenario covers how to
diagnose a stalled upgrade — checking precondition failures, SDDC Manager logs, LCM task
state, and the component health checks that block progress — and how to safely retry or
recover the workflow.

*Applies to: vSphere 7.x / 8.x*
</div>

!!! warning "Full SDDC management plane downtime"
    SDDC Manager upgrade pauses all lifecycle management operations for the duration. No new workloads, patches, or expansions can be applied until the upgrade completes.

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_identify_the_failed_task: "1. Identify the Failed Task" {shape: rectangle}
2_check_sddc_manager_logs: "2. Check SDDC Manager Logs" {shape: rectangle}
3_fix_the_underlying_issue: "3. Fix the Underlying Issue" {shape: rectangle}
4_retry_or_resume_the_workflow: "4. Retry or Resume the Workflow" {shape: rectangle}
5_validate_upgrade_completion: "5. Validate Upgrade Completion" {shape: rectangle}

products_involved -> 1_identify_the_failed_task: uses
1_identify_the_failed_task -> 2_check_sddc_manager_logs: uses
2_check_sddc_manager_logs -> 3_fix_the_underlying_issue: uses
3_fix_the_underlying_issue -> 4_retry_or_resume_the_workflow: uses
4_retry_or_resume_the_workflow -> 5_validate_upgrade_completion: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| SDDC Manager | LCM orchestrator; drives upgrade workflow; holds task state |
| vCenter | Component health; certificate state; API reachability |
| ESXi | Host upgrade; firmware compliance; remediation state |
| NSX Manager | NSX upgrade coordination during VCF upgrade bundle |
| vSAN | Cluster health prerequisite checks; resync state |

---

## 1. Identify the Failed Task

Navigate to **SDDC Manager → Administration → Lifecycle Management → Bundles** and check the **Upgrade History** for the active workflow.

```text
Workflow task states:
  COMPLETED      — task finished successfully
  IN_PROGRESS    — task is currently running
  FAILED         — task failed; details in the logs
  PENDING        — waiting for a prerequisite task to complete
  SKIPPED        — task was not applicable to this environment
```

Note the exact failed task name — common failure points:

```text
Common stall points in VCF upgrade workflows:
  SOSValidation          — SOS health check failed before upgrade can proceed
  CertificateValidation  — certificate near expiry or chain not trusted
  NSXUpgradePrecheck     — NSX Manager not reachable or version incompatible
  ESXiRemediationPrep    — vLCM cluster image not compliant; remediation needed
  vCenterPrecheck        — vCenter not reachable or SSO issues
  DiskGroupCheck         — vSAN health not green; resync in progress
```

Look for: the failure message shown inline in the SDDC Manager UI is often sufficient to identify the root cause without reading logs. Only proceed to log analysis if the UI message is cryptic.

---

## 2. Check SDDC Manager Logs

SSH to the SDDC Manager appliance as `vcf` user and review LCM logs for the error.

```bash
# SSH to SDDC Manager
ssh vcf@<sddc-manager-ip>

# LCM debug log — primary log for upgrade task errors
sudo tail -200 /var/log/vmware/vcf/lcm/lcm-debug.log | grep -iE "ERROR|FAIL|exception"

# SDDC Manager general log
sudo tail -100 /var/log/vmware/vcf/sddc-manager.log | grep -iE "ERROR|FAIL"

# SOS health check log (written during precheck phase)
sudo find /var/log/vmware/vcf -name "sos-health*" -newer /var/log/vmware/vcf/lcm/lcm-debug.log \
  -exec tail -50 {} \;
```


```text title="Expected output"
vcf@sddc-manager-01:~$ ssh vcf@192.168.1.50
vcf@192.168.1.50's password: 
Welcome to VMware Cloud Foundation SDDC Manager
Last login: Wed Jan 15 14:32:18 2025 from 192.168.1.100

vcf@sddc-manager-01:~$ sudo tail -200 /var/log/vmware/vcf/lcm/lcm-debug.log | grep -iE "ERROR|FAIL|exception"
2025-01-15T14:28:45.123Z ERROR [LCM-Task-Worker-12] com.vmware.vcf.lcm.upgrade.task.UpgradeTask - Failed to apply patch to host esx-01.sddc.local: Connection timeout after 300s
2025-01-15T14:29:12.456Z EXCEPTION [LCM-Task-Worker-12] java.net.SocketTimeoutException: Host unreachable
2025-01-15T14:30:01.789Z ERROR [LCM-Scheduler] com.vmware.vcf.lcm.health.HealthCheck - Precheck validation FAILED: Insufficient disk space on /var/log (required: 50GB, available: 12GB)

vcf@sddc-manager-01:~$ sudo tail -100 /var/log/vmware/vcf/sddc-manager.log | grep -iE "ERROR|FAIL"
2025-01-15T14:27:33.012Z ERROR [http-nio-8443-exec-5] com.vmware.vcf.sddc.api.controller.UpgradeController - Upgrade bundle validation FAILED: Checksum mismatch for bundle vcf-5.5.0-build.12345678
2025-01-15T14:28:15.345Z ERROR [http-nio-8443-exec-8] com.vmware.vcf.sddc.api.service.LcmService - Unable to reach vCenter Server 192.168.1.40:443

vcf@sddc-manager-01:~$ sudo find /var/log/vmware/vcf -name "sos-health*" -newer /var/log/vmware/vcf/lcm/lcm-debug.log -exec tail -50 {} \;
=== SOS Health Check Report ===
Timestamp: 2025-01-15T14:25:00Z
Host: esx-02.sddc.local (192.168.1.52)
Status: FAILED
Issues Detected:
  - vSAN cluster disk group missing on device mpx.vmhba2:C0:T0:L0
  - NTP sync error: offset 2500ms (threshold: 100ms)
  - vMotion network latency: 450ms (threshold: 100ms)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: command not found` | Ensure you are logged in as a user with sudo privileges; if using a restricted shell, request admin access. |
    | `/var/log/vmware/vcf/lcm/lcm-debug.log: No such file or directory` | Verify the LCM service is running with `systemctl status vmware-vcf-lcm` and check the correct log path for your |
Look for: the specific exception class or error message. Common patterns:

```text
SshCommandException    — SDDC Manager cannot SSH to an ESXi host or NSX Manager
CertExpiredException   — a certificate expired; check vCenter, ESXi, or NSX certs
NsxUpgradeCheckFailed  — NSX precheck script returned errors; check NSX Manager directly
TimeoutException       — task took too long; check if the component is under load
VsanHealthCheckFailed  — vSAN Skyline Health not green; check vSAN status directly
```

---

## 3. Fix the Underlying Issue

Address the root cause before retrying. The most common issues and their fixes:

**SOS validation failure — component unreachable:**

```bash
# Verify SDDC Manager can reach all ESXi hosts
for host in $(sddc-manager-cli get-hosts 2>/dev/null || echo "get hosts manually"); do
  ping -c 1 $host > /dev/null && echo "$host OK" || echo "$host UNREACHABLE"
done

# Verify DNS resolution from SDDC Manager
nslookup vcenter.domain.local
nslookup nsx-manager.domain.local
```


```text title="Expected output"
esx-01.domain.local OK
esx-02.domain.local OK
esx-03.domain.local OK
esx-04.domain.local OK
Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	vcenter.domain.local
Address: 10.20.1.45

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	nsx-manager.domain.local
Address: 10.20.1.67
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: sddc-manager-cli` | Ensure the SDDC Manager CLI is installed and in your PATH, or run this command directly from the SDDC Manager appliance. |
    | `UNREACHABLE` | Verify the ESXi host is powered on, check network connectivity from SDDC Manager, and confirm firewall rules allow ICMP traffic. |
    | `nslookup: can't resolve 'vcenter.domain.local': No answer` | Verify DNS servers are configured correctly on SDDC Manager and that the DNS zone contains the required A records. |
**Certificate issue — expiry or trust:**

```bash
# Check certificate expiry on vCenter from SDDC Manager
echo | openssl s_client -connect <vcenter-fqdn>:443 2>/dev/null | \
  openssl x509 -noout -dates
```


```text title="Expected output"
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2024 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to load certificate` | Ensure the vCenter FQDN is correct and the host is reachable on port 443; verify network connectivity with `ping <vcenter-fqdn>` first. |
    | `error in x509 parsing` | The certificate chain may not be complete; add `-showcerts` to `openssl s_client` to inspect the full chain and identify parsing issues. |
For certificate rotation in SDDC Manager, see the [Certificate Expiry and Rotation](certificate-expiry-rotation.md) scenario.

**vSAN health blocking upgrade:**

```bash
# SSH to an ESXi host; check vSAN health summary
esxcli vsan debug health summary get

# If resync is in progress, wait for completion
esxcli vsan debug resync summary get | grep -E "BytesToResync|ETA"
```


```text title="Expected output"
Cluster Information
   Cluster UUID: 52d4a8f1-2b3c-4e7f-9a1c-8d3e5f2a1b4c
   Cluster Health Status: healthy
   Cluster Health Reason: No issues detected
   Number of Host Failures Tolerable: 1
   Number of Disk Failures Tolerable: 1

Object Health Summary
   Number of Objects: 2847
   Number of Healthy Objects: 2847
   Number of Unhealthy Objects: 0
   Number of Inaccessible Objects: 0

BytesToResync: 0
ETA: 0 seconds
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown command or namespace vsan` | Ensure you are connected to an ESXi 6.5+ host with vSAN enabled; run `esxcli vsan cluster get` to verify vSAN is active. |
    | `Error: Permission denied` | SSH to the ESXi host with root credentials or a user with vSAN admin privileges. |
Do not retry the upgrade workflow while a vSAN resync is in progress — the upgrade stall is protecting data integrity.

**NSX precheck failure:**

Verify NSX Manager is reachable and healthy before retrying:

```text
NSX Manager → System → Overview — confirm all NSX Manager nodes show Up
NSX Manager → System → Upgrade — check NSX is not already in a partial upgrade state
```

---

## 4. Retry or Resume the Workflow

After fixing the root cause, retry the workflow from SDDC Manager.

**Via UI (preferred):**

```text
SDDC Manager → Administration → Lifecycle Management → Bundles
Select the failed workflow → Actions → Retry Task
```

**Via API (when UI retry is not available):**

```bash
# Get the workflow task ID from the failed workflow
curl -sk -u admin:<password> \
  "https://localhost/v1/upgrades" | python3 -m json.tool | grep -E "id|status|taskName"

# Retry a specific upgrade task
curl -sk -X PATCH -u admin:<password> \
  -H "Content-Type: application/json" \
  -d '{"status":"RETRY"}' \
  "https://localhost/v1/upgrades/<upgrade-id>/tasks/<task-id>"
```


```text title="Expected output"
{
    "id": "upgrade-2024-01-15-prod-cluster",
    "status": "FAILED",
    "taskName": "PreUpgradeValidation"
}
{
    "id": "upgrade-2024-01-15-prod-cluster",
    "status": "FAILED",
    "taskName": "HostPatch"
}
{
    "id": "upgrade-2024-01-15-prod-cluster",
    "status": "FAILED",
    "taskName": "VMSnapshot"
}
{
  "taskId": "task-8f3c2a91-7e4d-11ee-b962-005056b5c4a1",
  "status": "RETRY",
  "message": "Task retry scheduled successfully",
  "retryAttempt": 2,
  "nextRetryTime": "2024-01-15T14:32:00Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the vCenter CA certificate into your system trust store. |
    | `{"error":"Unauthorized","code":401}` | Verify the admin password is correct and URL-encoded if it contains special characters; use `-u admin:$(echo -n 'password' | jq -sRr @uri)` for special chars. |
    | `{"error":"Not Found","code":404}` | Confirm the `<upgrade-id>` and `<task-id>` values exist by running the first curl command to list active upgrades and their task IDs. |
Look for: some tasks cannot be retried individually and require retrying the entire upgrade operation from the beginning. If the component was partially upgraded (e.g., one NSX Manager node upgraded), check whether rollback or completion is the safer path before retrying.

---

## 5. Validate Upgrade Completion

After the workflow completes, verify component versions and run SOS health check.

```bash
# Run SOS health check from SDDC Manager
sudo /opt/vmware/sddc-support/sos --health-check --skip-known-host-check \
  --domain-name <workload-domain-name>

# Check component versions after upgrade
sudo /opt/vmware/sddc-support/sos --version-check
```


```text title="Expected output"
Running SOS health check for domain: workload-domain-01
Checking SDDC Manager connectivity... OK
Checking vCenter Server... OK
Checking NSX Manager... OK
Checking vSAN cluster health... OK
Checking ESXi hosts (8 total)... OK
Checking network configuration... OK
Checking certificate validity... OK (expires in 287 days)
Health check completed successfully. No critical issues detected.

SOS Version Check Report
========================
SDDC Manager: 5.4.1.0-21432156
vCenter Server: 7.0.3.00100
NSX Manager: 3.2.2.1-20145896
vSAN: 7.0 U3
ESXi Hosts: 7.0.3, Build 19482537
Photon OS: 4.0 Rev 2
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: /opt/vmware/sddc-support/sos: command not found` | Verify the SOS tool is installed by running `ls -la /opt/vmware/sddc-support/` and confirm the SDDC Manager support bundle is present. |
    | `Error: Domain '<workload-domain-name>' not found in SDDC Manager inventory` | Replace `<workload-domain-name>` with the actual workload domain name from your environment (e.g., `workload-domain-01`). |
    | `Permission denied` | Ensure you are running the command with `sudo` and that your user account has sufficient privileges in the SDDC Manager appliance. |
Expected results:

```text
SOS health check output (healthy):
  vCenter:     PASS
  ESXi:        PASS (all hosts)
  vSAN:        PASS
  NSX Manager: PASS
  Version:     All components at target bundle version
```

Look for: any FAIL or WARN in the SOS health check output indicates that the upgrade did not fully complete or introduced a configuration issue. Address each failure before closing the change.

---

## Key Terms

| Term | Definition |
|---|---|
| SDDC Manager | VCF lifecycle orchestrator appliance; manages bringup, upgrades, and drift remediation for workload domains |
| LCM | Lifecycle Manager — the SDDC Manager subsystem that plans, schedules, and executes component upgrades |
| Bundle | A versioned set of component upgrade packages (VCF, vCenter, ESXi, NSX, vSAN) published by VMware; applied as a unit by LCM |
| SOS | Support and Observability Suite — the SDDC Manager health-check script that validates component reachability, versions, and cluster state before and after upgrades |
| Workload domain | A logical grouping of vCenter, ESXi cluster, and vSAN managed as a unit by SDDC Manager; VCF can have multiple workload domains |
| NSX precheck | NSX Manager validation script run by SDDC Manager before upgrading NSX; checks NSX Manager node health, transport node compatibility, and cluster state |
| vLCM | vSphere Lifecycle Manager — cluster image-based patching for ESXi hosts; used by VCF to upgrade ESXi hosts in a workload domain |
| SOSValidation | LCM task that runs the full SOS health check before proceeding; if any check fails, the upgrade is held until the issue is resolved |
| Remediation | vLCM operation that applies the cluster image to non-compliant ESXi hosts; runs as a sub-task of the ESXi upgrade workflow |

---

## Common Mistakes

- **Retrying the workflow without fixing the root cause.** The same task will fail again. Always resolve the underlying issue first — a retry is not a fix.
- **Starting an upgrade with an active vSAN resync.** SDDC Manager may start the workflow but halt at the DiskGroupCheck task. Wait for resync to complete before triggering any VCF upgrade.
- **Ignoring partial upgrades.** If the workflow stalled after upgrading one component (e.g., vCenter) but before another (e.g., ESXi), the environment is in a mixed-version state. Check the VMware VCF upgrade compatibility matrix before deciding to roll back or continue.
- **Running SOS manually and declaring success without checking all domains.** SOS must be run against each workload domain individually. A management domain result does not cover VI workload domains.

---

## Related Scenarios

- [Certificate Expiry and Rotation](certificate-expiry-rotation.md) — certificate issues are a frequent cause of VCF upgrade precheck failures.
- [vCenter Upgrade Failure](vcenter-upgrade-failure.md) — vCenter-specific upgrade failures that can occur as a sub-step within a VCF bundle upgrade.
- [vSAN Disk or Component Failure](vsan-disk-component-failure.md) — active vSAN resync blocks VCF upgrades; resolve disk issues before starting.

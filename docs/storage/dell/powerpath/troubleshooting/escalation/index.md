# PowerPath — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.
</div>

## Support Portal

Dell EMC Support: [https://www.dell.com/support](https://www.dell.com/support)

- Log in with your MyDell account linked to your support contract
- Navigate to **Cases** to open or track cases
- The E-Lab Interoperability Navigator ([https://elabnavigator.dell.com](https://elabnavigator.dell.com)) is the authoritative source for PowerPath compatibility with OS versions and array firmware

## Opening a Case

1. Confirm the affected host and the PowerPath version are covered by an active support contract
2. Collect the information listed in the next section before opening the case
3. Go to [https://www.dell.com/support](https://www.dell.com/support) → **Contact Support** → **Create Service Request**
4. Select product: **Dell EMC PowerPath** (specify the platform variant: PowerPath for Linux, Windows, AIX, or PowerPath/VE for ESXi)
5. Set severity:
   - **Severity 1** — host has lost all paths to storage; production I/O failing
   - **Severity 2** — degraded path count (some paths dead); risk of failover impact
   - **Severity 3** — non-critical issue (policy question, licensing enquiry, unexpected path count)
   - **Severity 4** — general enquiry or configuration question

## Information to Collect

```bash
# PowerPath version
powermt version

# License registration status
powermt check_registration

# All device and path state (save full output)
powermt display dev=all

# All HBA port states
powermt display ports class=all

# Load balancing policy and options
powermt display options

# OS and kernel version (Linux)
uname -r
cat /etc/os-release

# OS version (Windows — run in PowerShell)
# Get-ComputerInfo | Select-Object OsName, OsVersion, OsBuildNumber

# HBA driver version (Linux Fibre Channel)
systool -c fc_host -v 2>/dev/null | grep -E "driver_version|firmware_version|port_name"

# Recent PowerPath-related kernel messages (Linux)
dmesg | grep -i "emcp\|PowerPath" | tail -50
journalctl -k --since "1 hour ago" | grep -i "emcp\|powerpath"

# System logs for I/O errors around the time of the issue (Linux)
grep -i "emcp\|scsi\|hba" /var/log/messages | tail -100
```

Also provide:
- Description of the issue and approximate time it started
- Array model and firmware version that the host is connected to
- Zoning or LUN masking changes made recently
- Output of `powermt display dev=<affected device>` for the specific device(s) affected
- Any relevant OS or HBA driver upgrade activity

## SLA Tiers

| Severity | Description | Initial Response Target | Update Frequency |
|---|---|---|---|
| Severity 1 | Complete path loss / production I/O failure | 30 minutes | Every 2 hours until resolved |
| Severity 2 | Degraded path count / elevated risk | 2 hours | Every 4 hours |
| Severity 3 | Non-critical issue | Next business day | As updated |
| Severity 4 | General question | 2 business days | As updated |

Response times are subject to your support contract tier (ProSupport, ProSupport Plus, or Mission Critical).

## Escalation Path

1. **Case comment**: Request escalation directly within the support case if response time or progress is insufficient
2. **Technical Account Manager (TAM)**: Contact your TAM to drive priority Sev1/Sev2 cases
3. **Mission Critical support line**: Available 24x7 for Mission Critical contract holders; bypasses standard queue
4. **E-Lab Navigator**: For compatibility questions (OS upgrade, kernel update), the E-Lab Navigator is self-service and does not require a support case

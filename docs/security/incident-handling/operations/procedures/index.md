---
tags:
  - operations
  - security
---
# Incident Handling — Standard Procedures

<div class="kb-summary">
Standard procedures covering the full incident lifecycle: declaration through post-incident review and runbook update. Follow these steps in sequence for any security, infrastructure, or availability incident.
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Declare an Incident

An incident is formally declared when an event meets severity criteria. Early declaration ensures timely escalation and resource mobilisation.

**Severity criteria:**

| Priority | Definition | Examples |
|----------|------------|---------|
| P1 | Critical — production down, data breach, active intrusion | Ransomware, complete service outage, confirmed data exfiltration |
| P2 | High — significant degradation, potential breach, key system impaired | Failed authentication flood, partial outage, suspected compromise |
| P3 | Medium — limited impact, no immediate data risk, workaround available | Single system anomaly, suspicious process on non-critical host |

**Steps:**

1. Confirm the event meets P1/P2/P3 criteria above. If uncertain, treat as the higher severity.

2. Create an incident ticket in the ticketing system with:
   - Incident priority (P1/P2/P3)
   - One-line description of the observed symptom
   - Affected systems or services
   - Time first observed

3. Send initial notification using the communication template:
```text
   INCIDENT DECLARED — <Priority>
   Time: <HH:MM UTC>
   Summary: <one sentence>
   Affected: <system/service>
   IC: <name>
   Bridge: <call link or channel>
   Next update in: 30 minutes
   ```

4. Open the incident bridge (Slack channel, conference call, or Teams channel) and pin the ticket link.

5. Log the declaration time in the incident timeline.

---

## Assemble the Incident Response Team

Assign roles immediately after declaration to ensure clear ownership throughout the incident.

**Core roles:**

| Role | Responsibility |
|------|----------------|
| Incident Commander (IC) | Owns the incident end-to-end; drives decisions; communicates status |
| Technical Lead | Leads investigation and remediation; coordinates technical responders |
| Communications Lead | Manages stakeholder updates, executive notifications, and external comms |
| Executive Sponsor | Available for P1 escalations; authorises emergency change or spend |

**Steps:**

1. IC pages the on-call Technical Lead via the alerting system (PagerDuty or equivalent).

2. For P1: simultaneously notify the Communications Lead and Executive Sponsor via phone or high-priority page.

3. Announce role assignments in the incident bridge at the start of the call:
```text
   IC: <name> | Tech Lead: <name> | Comms: <name> | Exec: <name>
   ```

4. Technical Lead recruits additional SMEs (network, storage, security, application) as the scope becomes clear.

5. Document the team roster and join time in the incident ticket.

6. Maintain a contact list in the format:
```text
   <Role> | <Name> | <Phone> | <Pager/Slack handle> | <Time paged>
   ```

---

## Isolate Affected Systems

Immediately isolate compromised or suspected systems to prevent lateral movement before full investigation begins.

1. **vCenter network isolation** — disconnect the VM's NIC without powering it off (preserves memory for forensics):
   - vCenter → select VM → Edit Settings → Network Adapter → uncheck **Connected** → OK.

2. **NSX Distributed Firewall (DFW) block** — add an emergency deny rule for the affected VM:
   - NSX Manager → Security → Distributed Firewall → add a rule at the top:
     - Source: affected VM's security group
     - Destination: Any
     - Action: Drop
     - Apply immediately.

3. **VLAN reassignment** — move the port to a quarantine VLAN if DFW is not available:
   - vCenter → Host → Networking → locate the VM's port group → reassign to `VLAN-QUARANTINE`.
   - Or on the physical switch: `switchport access vlan <quarantine-vlan>` on the relevant port.

4. **Firewall perimeter block** — if the affected IP may have initiated outbound connections, add a deny rule at the perimeter firewall for the affected IP.

5. Confirm isolation by verifying no traffic is flowing from the isolated IP (check firewall logs or NetFlow).

6. Log the isolation action in the incident ticket: system name, IP, method used, and time isolated.

---

## Preserve Evidence

Collect volatile and persistent evidence before any remediation step that could alter or destroy it.

1. **VM memory dump** — take a memory snapshot before any reboot or shutdown:
   - In vCenter: right-click VM → **Snapshot** → **Take Snapshot** → check **Quiesce guest file system** off, check **Include virtual machine's memory** on.
   - On Linux using `avml`:
     ```bash
     avml /evidence/<hostname>-memory-$(date +%Y%m%d%H%M).lime
     ```

2. **Disk image** — clone the VM disk before remediation:
   - In vCenter: right-click VM → **Clone** → **Clone to Virtual Machine** → name it `<hostname>-evidence-<date>`.

3. **Log collection** — export relevant logs before log rotation:
   ```powershell
   # Windows: export Security and System event logs
   wevtutil epl Security C:\evidence\Security-<hostname>-<date>.evtx
   wevtutil epl System C:\evidence\System-<hostname>-<date>.evtx
   ```
   ```bash
   # Linux: copy auth, syslog, and application logs
   cp /var/log/auth.log /evidence/
   cp /var/log/syslog /evidence/
   journalctl > /evidence/journal-<hostname>-$(date +%Y%m%d).log
   ```

4. **Network capture** — if the threat is active, start a packet capture on the affected segment.

5. Hash all collected evidence files (SHA-256) and record the hashes in the incident ticket:
   ```powershell
   Get-FileHash <evidence-file> -Algorithm SHA256
   ```

6. Write-protect or place evidence in a read-only network share accessible only to the IR team.

7. Document chain of custody: who collected each item, when, and where it is stored.

---

## Contain the Threat

Stop the threat from spreading while preserving the ability to investigate. Containment actions depend on the threat type.

1. **Lock compromised accounts** — disable any accounts known or suspected to be compromised:
   ```powershell
   Disable-ADAccount -Identity <username>
   ```

2. **Revoke active sessions** — force log-off active sessions on affected systems:
   ```powershell
   # On Windows, force log off a user session
   query session /server:<server>
   logoff <SessionID> /server:<server>
   ```

3. **Revoke tokens** — if OAuth/OIDC tokens are compromised, invalidate them via the identity provider (Entra ID, Okta, etc.).

4. **Disable compromised service accounts** in Active Directory:
   ```powershell
   Disable-ADAccount -Identity <service-account-name>
   ```

5. **Rotate compromised secrets** — change passwords for any credentials that may have been exposed; update in CyberArk immediately.

6. **Block malicious IPs or domains** — add block entries to the perimeter firewall and DNS sinkhole.

7. **Disable affected services** temporarily if they are the attack vector:
   ```powershell
   Stop-Service <ServiceName>
   Set-Service <ServiceName> -StartupType Disabled
   ```

8. Document each containment action with the exact command, operator, and timestamp.

---

## Eradicate the Root Cause

Remove the threat from the environment after containment. Do not proceed to recovery until eradication is confirmed.

1. **Malware scan** — run a full AV/EDR scan on the affected system and all systems with which it communicated:
   ```powershell
   # Windows Defender full scan example
   Start-MpScan -ScanType FullScan
   ```

2. **Identify backdoors** — review scheduled tasks, startup items, registry run keys, and local user accounts added during the incident window:
   ```powershell
   Get-ScheduledTask | Where-Object { $_.Date -gt "<incident-start>" }
   Get-LocalUser | Where-Object { $_.CreateDate -gt "<incident-start>" }
   ```

3. **Remove malicious artefacts** — delete identified malware files, unauthorised user accounts, and malicious scheduled tasks.

4. **Apply the security patch or configuration fix** that closes the exploited vulnerability. Test in a non-production environment first if time permits.

5. **Verify clean state** — re-run AV/EDR scan after remediation and confirm no detections.

6. **Check lateral movement scope** — review authentication logs and EDR telemetry to confirm no other systems were compromised; eradicate from those as well.

7. Document every artefact removed with its file path, hash, and deletion time.

---

## Restore Systems

Bring systems back to service from a known-good state only after eradication is confirmed.

1. **Select restore method** based on the level of compromise:
   - Full rebuild from golden image (preferred for confirmed compromise).
   - Restore from a backup taken before the incident window (confirm the backup pre-dates the intrusion).

2. **Restore from backup:**
   ```cmd
   # Windows Server Backup restore example
   wbadmin start recovery -version:<backup-version> -itemType:Volume -items:<drive-letter>: -recoveryTarget:<target>
   ```
   Or restore the VM from a pre-incident snapshot in vCenter.

3. **Verify file integrity** after restore:
   ```powershell
   sfc /scannow
   ```

4. **Apply current patches** before reconnecting to the network — patch the system to current levels.

5. **Reconnect in a controlled sequence:**
   - Re-enable the VM NIC in vCenter.
   - Remove the emergency NSX DFW block rule.
   - Monitor traffic from the restored system for 30 minutes before declaring it clean.

6. **Validate application functionality** — run smoke tests or ask the application owner to confirm normal operation.

7. **Re-enable accounts and services** that were disabled during containment once the system is confirmed clean.

8. Log the restore completion time and validation result in the incident ticket.

---

## Conduct Post-Incident Review

Hold a post-incident review (PIR) within 5 business days of incident closure to understand what happened and prevent recurrence.

1. Circulate the incident ticket and timeline to all participants before the meeting.

2. **Reconstruct the timeline** in chronological order:
   - Initial indicator of compromise (IOC) or alert.
   - Each action taken by the attacker (if applicable).
   - Each action taken by the IR team.
   - Resolution and restoration.

3. **Apply the 5-Whys methodology** to reach the root cause:
   - Why did the incident occur?
   - Why was that condition allowed to exist?
   - Repeat until the systemic cause is identified (typically 5 levels deep).

4. **Identify contributing factors:**
   - Detection gap (would better monitoring have caught this earlier?)
   - Response gap (did the team have the right tools and access?)
   - Prevention gap (could a control have prevented the incident?)

5. **Document lessons learned** — at minimum record:
   - What went well.
   - What could have been done faster or better.
   - Specific action items with owners and due dates.

6. Assign each action item to an owner with a 30/60/90-day target and track in the ticketing system.

---

## Write the Incident Report

Produce a written incident report within 5 business days of closure. The report is the permanent record of the incident.

**Required sections:**

1. **Executive Summary** — 1 paragraph, non-technical: what happened, impact, and outcome. Written for C-level readers.

2. **Timeline** — chronological table of all key events:
   | Time (UTC) | Event | Actor |
   |------------|-------|-------|
   | 08:14      | Alert fired in SIEM | Automated |
   | 08:22      | IC declared P2 incident | J. Smith |

3. **Impact Assessment** — systems affected, data involved, users impacted, duration of outage or degradation.

4. **Root Cause** — the technical root cause identified during the PIR, written in plain language.

5. **Actions Taken** — bullet list of every containment, eradication, and recovery action with timestamps.

6. **Recommendations** — specific, actionable items to prevent recurrence. Each recommendation should reference the gap it closes.

7. **Appendices** — evidence hashes, raw log excerpts, network diagrams, or screenshots relevant to the incident.

Store the report in the incident ticket and in the designated IR documentation repository. Distribute to stakeholders as appropriate for the severity level.

---

## Update the Runbook

Feed findings from each incident back into runbooks and contact lists so the next response is faster.

1. Identify which runbook(s) would have guided responders during the incident.

2. Review each relevant runbook section against what actually happened:
   - Were the commands accurate?
   - Were the contact details current?
   - Were any steps missing that the team had to improvise?

3. Open a change ticket for each runbook that needs updating.

4. Update the runbook content:
   - Add any new commands or procedures discovered during the incident.
   - Correct inaccurate steps.
   - Add a new sub-section if a scenario was not previously covered.

5. Update the contact list with any personnel changes discovered during on-call paging.

6. Review escalation paths and vendor support contacts — update phone numbers and portal URLs if stale.

7. Commit the runbook changes and request a peer review from another team member before merging.

8. Record the runbook update in the incident ticket as a closed action item.

9. Schedule a tabletop exercise within 90 days if the incident revealed a significant gap that requires team practice.

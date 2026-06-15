---
tags:
  - operations
  - security
---
# Security Monitoring — Procedures

<div class="kb-summary">
Step-by-step procedures for reviewing SIEM alerts, investigating security events, tuning detection rules, and generating monitoring reports.
</div>

```text
┌────────────────────────────────── Security Monitoring — Operations ───────────────────────────────────┐
│                                                                                                       │
│   SIEM platforms: Splunk, Microsoft Sentinel (KQL), Elastic SIEM, IBM QRadar                          │
│   Daily triage: sort Critical first; classify TP / FP / Needs Tuning; escalate TPs to IR              │
│   Detection source: MITRE ATT&CK technique mapping; alert-only mode before enabling auto-response     │
│   Reporting metrics: MTTD, MTTR, true positive rate, top 5 rules by volume                            │
│                                                                                                       │
│   Alert investigation workflow                                                                        │
│   Triage   Filter last 24h; sort by severity; open Critical/High events for context                   │
│   Investigate  Pull auth history (AD / Entra ID); check endpoint telemetry (Defender / CrowdStrike)   │
│   Contain   Revoke sessions (Revoke-MgUserSignInSession); reset AD password; network isolation        │
│   ATT&CK    Map observed indicators to technique IDs (e.g., T1078 Valid Accounts, T1110 Brute Force)  │
│                                                                                                       │
│   Detection engineering                                                                               │
│   Tune noisy rule  Identify FP pattern (30d data); add exclusion (NOT src_ip / AccountName !in)       │
│   New rule         Write KQL/SPL query on historical data; tune FPs; set severity + MITRE tags        │
│   Deploy           Alert-only mode 7d; verify on historical data before enabling automated response   │
│                                                                                                       │
│   Suspicious login response                                                                           │
│   Check source IP, geo, device, time; verify with user via phone if unusual location                  │
│   If unverified or denied: revoke sessions + reset password + enable risk-based CA                    │
│   Review all actions taken in the session window: mail forwarding, file access, lateral movement      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   MTTD          = Mean Time to Detect; time from attack start to first SIEM alert                     │
│   MTTR          = Mean Time to Respond; time from alert to containment action                         │
│   KQL           = Kusto Query Language; used by Microsoft Sentinel for log queries                    │
│   SPL           = Splunk Processing Language; search and reporting language for Splunk                │
│   MITRE ATT&CK  = framework of adversary tactics, techniques, and procedures (TTPs)                   │
│   T1078         = Valid Accounts; adversary uses legitimate credentials to gain access                │
│   blast radius  = all systems the compromised account or host communicated with in the incident window│
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Daily SIEM Alert Review

Perform the morning triage of overnight SIEM alerts to identify threats requiring analyst investigation.

1. Log in to the SIEM platform (Splunk, Microsoft Sentinel, Elastic SIEM, or IBM QRadar) and open the alert queue.
2. Filter alerts to the last 24 hours and sort by severity (Critical first).
3. For each Critical or High alert, open the event and review: source IP, destination, username, process name, and alert rule triggered.
4. In Splunk, run a quick context search on the source IP:
   ```splunk
   index=firewall OR index=proxy src_ip=<alerting_ip> earliest=-24h | stats count by action, dest_ip, url | sort -count
   ```
5. Classify each alert as: **True Positive** (escalate to investigation), **False Positive** (close with note), or **Needs Tuning** (flag for rule adjustment).
6. Escalate all True Positives to the incident response workflow and assign to an analyst.
7. Log the daily triage summary in the monitoring shift log, including: alerts received, true positives, false positives, and open investigations.

---

## Investigate a Security Alert

Conduct a structured investigation of a promoted alert to determine scope, impact, and required response.

1. Open the incident ticket created from the alert and review the initial SIEM alert details.
2. Gather additional context from supporting data sources:
   ```splunk
   # Splunk — all events for the involved user in the last 7 days
   index=* user=<username> earliest=-7d | stats count by index, sourcetype, action | sort -count
   ```
3. Pull the full authentication history for the involved account from AD or Entra ID sign-in logs.
4. Check endpoint telemetry (Microsoft Defender, CrowdStrike, or Carbon Black) for the affected host: look for unusual processes, network connections, and file writes.
5. Determine the attack technique by mapping observed indicators to the MITRE ATT&CK framework.
6. Assess the blast radius: identify all systems the account or compromised host communicated with during the incident window.
7. Document findings in the incident ticket: timeline, affected assets, attacker techniques, and recommended containment actions.
8. Escalate to Tier 3 or the IR team if the investigation reveals lateral movement, data exfiltration, or ransomware indicators.

---

## Tune an Overactive Alert Rule

Reduce false positive rate for a noisy detection rule without reducing its ability to detect genuine threats.

1. Identify the noisy rule from the false positive classification log or alert volume metrics in the SIEM dashboard.
2. Pull 30 days of alert data for the rule and categorise triggers by source:
   ```splunk
   index=siem_alerts rule_name="<NoisyRule>" earliest=-30d |
     stats count by src_ip, user, action | sort -count
   ```
3. Identify the dominant false positive pattern (e.g., a specific backup service, monitoring IP, or scheduled task).
4. Add an exclusion to the rule logic to suppress known-good sources without removing the core detection logic:
   - In Sentinel: update the KQL query with `| where AccountName !in ("svc-backup", "svc-monitoring")`.
   - In Splunk: add `NOT src_ip IN (10.0.1.10, 10.0.1.11)` to the search filter.
5. Run the updated rule against historical data to confirm the false positive rate drops and genuine test cases still trigger.
6. Document the tuning change (reason, pattern suppressed, date) in the SIEM rule change log.
7. Monitor the rule for 2 weeks post-change to confirm the improvement holds.

---

## Add a New Threat Detection Rule

Create and deploy a new detection rule based on a threat intelligence feed, incident findings, or a new MITRE technique.

1. Identify the threat or technique to detect; reference the MITRE ATT&CK technique ID (e.g., T1078 — Valid Accounts).
2. Determine which data source contains the relevant events (e.g., Windows Security event log, firewall logs, EDR telemetry).
3. Write the detection query against historical data to test its coverage:
   ```kql
   // Sentinel KQL — detect logins from unusual countries
   SigninLogs
   | where TimeGenerated > ago(7d)
   | where Location !in ("GB", "US", "IE")
   | where ResultType == 0
   | project TimeGenerated, UserPrincipalName, Location, IPAddress, AppDisplayName
   ```
4. Tune the query to eliminate known false positives (exclude known travel IPs, service accounts, etc.).
5. Set the alert severity, MITRE technique tags, and response playbook link in the rule metadata.
6. Deploy the rule in **alert-only** (not blocking) mode and monitor for 7 days before enabling automated response actions.
7. Document the new rule in the detection engineering register: rule ID, technique, data source, tuning history, and owner.

---

## Respond to a Suspicious Login Alert

Investigate and contain an alert triggered by a login event with anomalous characteristics.

1. Open the alert and note the key details: account name, source IP, geolocation, device, and time.
2. Check the user's recent login history for context:
   ```kql
   // Sentinel — last 30 logins for the user
   SigninLogs
   | where UserPrincipalName == "<user@corp.local>"
   | where TimeGenerated > ago(30d)
   | project TimeGenerated, Location, IPAddress, DeviceDetail, ResultDescription
   | order by TimeGenerated desc
   ```
3. If the login is from an unusual country or IP and occurred outside business hours, attempt to contact the user via phone to verify whether they initiated the login.
4. If unable to reach the user or if they deny the login, immediately revoke all active sessions and reset the account password:
   ```powershell
   # Revoke Entra ID sessions
   Revoke-MgUserSignInSession -UserId <ObjectId>
   # Reset AD password
   Set-ADAccountPassword -Identity <SamAccountName> -Reset -NewPassword (ConvertTo-SecureString "TempP@ss1!" -AsPlainText -Force)
   ```
5. Enable risk-based Conditional Access for the account (if not already active) to force MFA re-enrolment.
6. Review all actions taken by the account during the suspicious session period; check for mail forwarding rules, file access, and lateral movement.
7. Document the investigation and outcome in the incident ticket; escalate to a full IR if compromise is confirmed.

---

## Review Failed Authentication Trends

Analyse failed authentication patterns across the environment to detect brute-force, password spray, or credential stuffing activity.

1. In the SIEM, query the Security event log for Event ID 4625 (failed logon) over the last 7 days:
   ```splunk
   index=wineventlog EventCode=4625 earliest=-7d |
     stats count by Account_Name, src_ip, Logon_Type |
     where count > 50 | sort -count
   ```
2. In Entra ID sign-in logs, filter for `ResultType != 0` over the last 7 days, group by IP and user:
   ```kql
   SigninLogs
   | where TimeGenerated > ago(7d) and ResultType != 0
   | summarize FailCount=count() by IPAddress, UserPrincipalName
   | where FailCount > 20
   | order by FailCount desc
   ```
3. Identify IPs with high failure counts across many different usernames — this is characteristic of password spray; block at the perimeter firewall: `Set-NetFirewallRule -DisplayName "Block-Spray-IP" -RemoteAddress <IP> -Action Block`.
4. Identify accounts with high failure counts from a single IP — this may be a targeted brute force; lock the account and alert the user.
5. Check whether failures are targeting valid accounts only (suggests enumerated credential list) versus random usernames (suggests generic spray).
6. Report the trend analysis to the Security team with recommendations (e.g., geo-blocking, rate limiting, account lockout policy tightening).

---

## Export Alert Data for Reporting

Extract SIEM alert data for inclusion in the monthly security operations report.

1. In Splunk, run the monthly alert summary query and export to CSV:
   ```splunk
   index=siem_alerts earliest=-30d
   | stats count by rule_name, severity, disposition
   | sort severity, -count
   | outputcsv /tmp/monthly-alerts-$(date +%Y%m).csv
   ```
2. In Microsoft Sentinel, export the incidents table:
   ```kql
   SecurityIncident
   | where CreatedTime > ago(30d)
   | project IncidentName, Severity, Status, Owner, CreatedTime, ClosedTime
   | order by Severity asc, CreatedTime desc
   ```
   Copy the query output to Excel for the report.
3. Calculate key metrics:
   - Total alerts by severity
   - True positive rate: `True Positives / Total Alerts * 100`
   - Mean time to detect (MTTD) and mean time to respond (MTTR)
   - Top 5 triggered rules by volume
4. Produce a trend comparison against the previous month to show whether alert volume and true positive rates are improving.
5. Insert the metrics and charts into the monthly Security Operations report template and distribute to the Security Manager and CISO.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Security — Overview](../)

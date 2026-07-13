---
tags:
  - security
  - troubleshooting
search:
  boost: 1.5
description: "Common Issues reference covering Certificate Issue Triage Flow, Common checks, Incident notes, Change notes, Known issues and 2 more sections."
---
# Certificates — Common Issues

<div class="kb-summary">
Common Issues reference covering Certificate Issue Triage Flow, Common checks, Incident notes, Change notes, Known issues and 2 more sections.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
certificate_issue_triage_flow: "Certificate Issue Triage Flow" {shape: rectangle}
common_checks: "Common checks" {shape: rectangle}
incident_notes: "Incident notes" {shape: rectangle}
change_notes: "Change notes" {shape: rectangle}
known_issues: "Known issues" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> certificate_issue_triage_flow: investigate
symptom -> common_checks: investigate
symptom -> incident_notes: investigate
symptom -> change_notes: investigate
symptom -> known_issues: investigate
diagnostic_flow -> resolution
certificate_issue_triage_flow -> resolution
common_checks -> resolution
incident_notes -> resolution
change_notes -> resolution
known_issues -> resolution
```

## Diagnostic Flow

```d2
direction: right

A1: "A1" {shape: rectangle}
A2: "P1 incident: 1-hour SLA\nEmergency renewal via CA" {shape: rectangle}
A3: "certutil -verify\nRenew via ADCS or ACME" {shape: rectangle}
A4: "Expired Certificate Response" {shape: rectangle}
B: "B" {shape: rectangle}
B1: "openssl s_client check chain\nAdd intermediate cert to TLS config\nDistribute root CA via GPO" {shape: rectangle}
B2: "Certificate Issue Triage Flow" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "Check DNS/HTTP challenge\nVerify ACME client logs\nConfirm port 80/443 reachable" {shape: rectangle}
C3: "certutil -pulse\nCheck CA service and CRL\nVerify template permissions" {shape: rectangle}
C4: "Common ADCS Issues" {shape: rectangle}
D: "D" {shape: rectangle}
D1: "openssl x509 -text -in cert.pem\nCompare SAN list to hostname\nRequest new cert with correct SANs" {shape: rectangle}
D2: "Certificate Issue Triage Flow" {shape: rectangle}
E: "E" {shape: rectangle}
E1: "openssl verify cert against key\nIf mismatch: re-issue cert\nor restore correct private key" {shape: rectangle}
E2: "Expired Certificate Response" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
A: "A" {shape: rectangle}
C: "C" {shape: rectangle}

A1 -> A2
A1 -> A3
A3 -> A4
B -> B1
B1 -> B2
C1 -> C2
C1 -> C3
C3 -> C4
D -> D1
D1 -> D2
E -> E1
E1 -> E2
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Certificate Issue Triage Flow

```d2
direction: right

issue: "Certificate error reported\n(TLS failure / untrusted / expired" {shape: rectangle}
checkExpiry: "Is the certificate\nexpired?" {shape: rectangle}
expiredPath: "Emergency renewal\n(P1 if external — 1 hour SLA" {shape: rectangle}
checkChain: "Chain validation\nfails?" {shape: rectangle}
chainFix: "Intermediate not sent by server\nAdd intermediate to TLS config\nopenssl verify to confirm" {shape: rectangle}
checkTrust: "Root CA trusted\nby client?" {shape: rectangle}
addRoot: "Distribute root CA cert\nvia GPO / system trust store" {shape: rectangle}
checkRevoke: "Certificate\nrevoked?" {shape: rectangle}
replaceRevoked: "Replace with new cert\nIssue on clean host" {shape: rectangle}
checkSAN: "CN / SAN matches\nhostname?" {shape: rectangle}
newCert: "Request new cert with\ncorrect CN and SANs" {shape: rectangle}
deepDiag: "Further diagnostics:\nopenssl s_client full output\ncertutil -verify -urlfetch" {shape: rectangle}

issue -> checkExpiry
checkExpiry -> expiredPath
checkExpiry -> checkChain
checkChain -> chainFix
checkChain -> checkTrust
checkTrust -> addRoot
checkTrust -> checkRevoke
checkRevoke -> replaceRevoked
checkRevoke -> checkSAN
checkSAN -> newCert
checkSAN -> deepDiag
```

## Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Known issues

Add known issues here as they come up.

## Common ADCS Issues

| Symptom | First Check | Command |
|---|---|---|
| Auto-enrollment not working | GPO applied, CA reachable, template permissions | `certutil -pulse; gpresult /r` |
| CRL download failing | HTTP/LDAP CDP accessibility | `certutil -URL <cdp_url>` |
| CA service fails to start | CA cert or CRL expired | Check `certsvc` event log, `certutil -verify` |
| Certificate request pending | Template requires CA Manager approval | `certsrv.msc` → Pending Requests |

## Expired Certificate Response

```powershell
# Find all expired certificates in the machine store
Get-ChildItem Cert:\LocalMachine\My |
  Where-Object { $_.NotAfter -lt (Get-Date) } |
  Select-Object Subject, NotAfter, Thumbprint

# Check which service is using an expired certificate
netsh http show sslcert | Select-String -Pattern "Thumbprint|IP:port"
```

Target resolution time: expired internal certificate — 2 hours. Expired external/public certificate — 1 hour (P1 incident).

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Certificates — Diagnostics](../diagnostics/)
- [Certificates — Escalation](../escalation/)
- [Certificates — Procedures](../../operations/procedures/)

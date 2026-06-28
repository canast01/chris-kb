---
tags:
  - security
  - troubleshooting
search:
  boost: 1.5
---
# Venafi — Common Issues


<div class="kb-summary">
Known issues and resolution steps for frequent Venafi problems.

*Applies to: Venafi TLS Protect*
</div>
![Venafi — Common Issues](../../../../assets/security-venafi-troubleshooting-common-issues-index.svg)




| Symptom | First Check |
|---|---|
| Certificate renewal stuck in pending | Check CA connector health; verify CA is reachable; check approval workflow |
| TPP web UI unreachable | Verify IIS app pool running; check SQL connectivity; review VdcLogFile |
| Discovery scan finds no certificates | Check scan range, port list, and Edge Proxy registration |
| LDAP/AD auth failing in Venafi | Test LDAP bind from TPP server; verify service account password not expired |
| Syslog events not appearing in SIEM | Check Log Server service; verify syslog target IP/port; check firewall |

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
known_issues: "Known Issues" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> known_issues: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
known_issues -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A{Certificate discovery\nnot finding endpoints?}
    S --> B{Policy violation\nblocking issuance?}
    S --> C{CA connection\nerror?}
    S --> D{Workflow approval\nstuck?}
    S --> E{TPP service\ncrash?}
    A -->|Yes| A1[Check Edge Proxy registration\nVerify scan range and port list\nCheck firewall from Edge to targets]
    A1 --> A2[Known Issues]
    B -->|Yes| B1[Review policy folder in TPP\nIdentify violated rule: CN · SAN · key size\nAdjust CSR or update policy]
    B1 --> B2[Known Issues]
    C -->|Yes| C1{CA type: ADCS\nor external?}
    C1 -->|ADCS| C2[Verify DCOM/RPC to CA\nCheck CA template permissions\nReview VdcLogFile for error]
    C1 -->|External| C3[Check CA API endpoint reachable\nVerify credential / API key\nCheck TPP CA connector config]
    C3 --> C4[Known Issues]
    D -->|Yes| D1[Check workflow approver mailbox\nVerify workflow policy config\nManually advance or escalate]
    D1 --> D2[Known Issues]
    E -->|Yes| E1[Verify IIS app pool running\nCheck SQL connectivity\nReview VdcLogFile for exception]
    E1 --> E2[Known Issues]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A2,B2,C4,D2,E2 section
    class A,B,C,C1,D,E decision
    class S start
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Known Issues

Add known issues here as they come up.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Venafi — Diagnostics](../diagnostics/)
- [Venafi — Escalation](../escalation/)
- [Venafi — Procedures](../../operations/procedures/)

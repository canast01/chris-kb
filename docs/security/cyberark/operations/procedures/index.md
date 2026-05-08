# CyberArk — Procedures

Operational procedures for account management, password rotation, session management, and audit tasks.

## Password Rotation Workflow

```mermaid
flowchart TD
    trigger["Rotation trigger\n(scheduled / on-demand / post-checkout)"]
    trigger --> cpmRetrieve["CPM retrieves current credential\nfrom Vault"]
    cpmRetrieve --> connectTarget["CPM connects to target system\nusing current credential"]
    connectTarget --> generatePwd["Generate new password\n(platform plugin policy)"]
    generatePwd --> setPwd["Set new password on target\n(RDP / SSH / API)"]
    setPwd --> verify["Verify new password works\n(CPM test logon)"]
    verify -->|"Success"| storeVault["Store new credential in Vault"]
    verify -->|"Failure"| rollback["Log failure + alert\nRetry on next cycle"]
    storeVault --> auditLog["Write audit event to SIEM"]
```

---

## Account Management

Use this section for practical account management procedures, checks, and field references.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

---

## Password Rotation

Use this section for password rotation procedures.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

---

## Session Management

Use this section for PSM session management procedures and field references.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

---

## Audit

Use this section for audit procedures and reporting.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

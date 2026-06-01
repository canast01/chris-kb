# Venafi — Procedures


<div class="kb-summary">
Operational procedures for certificate renewal, automation, and reporting.
</div>

## Renewal and Reporting Workflow

```mermaid
flowchart TD
    expiryAlert["Expiry alert triggered\n(30 / 14 / 7 days)"]
    expiryAlert --> checkAuto{"Automated renewal\nconfigured?"}
    checkAuto -->|"yes — Venafi driver"| autoRenew["Venafi auto-renews\nand deploys to target"]
    checkAuto -->|"no — manual"| manualRenew["Certificate owner notified\nManual renewal required"]
    manualRenew --> genCSR["Generate new CSR\non target host"]
    genCSR --> submitVenafi["Submit via vcert / UI / API\nto Venafi policy folder"]
    submitVenafi --> policyCheck["Policy validation"]
    policyCheck --> caIssue["CA issues new cert"]
    caIssue --> install["Install on target service\n+ validate TLS"]
    install --> closeAlert["Close alert — update\ncert inventory"]
    autoRenew --> closeAlert
```

---

## Renewal

Use this section for certificate renewal procedures and field references.

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

## Automation

Use this section for Venafi automation procedures and field references.

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

## Reporting

Use this section for Venafi reporting procedures and field references.

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

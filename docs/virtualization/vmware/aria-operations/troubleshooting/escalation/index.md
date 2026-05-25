# Aria Operations — Escalation

```
┌─────────────────────────────────────────────────────────────┐
│            Aria Operations Escalation Path                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L1 / Internal Ops                                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Run triage checklist → generate support bundle      │   │
│  │  Collect: version, cluster nodes, affected adapter   │   │
│  └────────────────────────┬─────────────────────────────┘   │
│           not resolved    │                                 │
│                           ▼                                 │
│  Broadcom TAC                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  support.broadcom.com                                │   │
│  │  Product: VMware Cloud Foundation → Aria Operations  │   │
│  │  P1: 30 min  P2: 4h  P3/P4: next business day        │   │
│  │  Attach: support bundle, logs, screenshots           │   │
│  └────────────────────────┬─────────────────────────────┘   │
│           no progress     │                                 │
│                           ▼                                 │
│  Portal escalation → duty manager → TAM (if available)      │
└─────────────────────────────────────────────────────────────┘
```

## Support Portal

**Broadcom Support Portal:** [https://support.broadcom.com](https://support.broadcom.com)

Log in with your Broadcom Customer Connect account. Aria Operations (formerly vRealize Operations) cases are filed under the **VMware Cloud Foundation** or **Aria** product category.

---

## Support Bundle Collection

Always attach a support bundle when opening a case.

### Via UI

```
Administration > Support > Generate Support Bundle
```

Download the bundle from the UI once generated.

### Via CLI

```bash
ssh admin@<aria-ops-primary-fqdn>

# Generate support bundle
vracli support bundle generate

# List available bundles
ls -lh /storage/log/support-bundle/

# SCP bundle to local machine
scp admin@<aria-ops-primary-fqdn>:/storage/log/support-bundle/<bundle-file>.zip /tmp/
```

---

## Information to Collect Before Opening a Case

| Item | Where to Find |
|------|--------------|
| Product version | Administration > About |
| Cluster topology (nodes, roles) | Administration > Cluster Management |
| Affected adapter / resource | Administration > Solutions |
| Symptom description and timeline | Incident notes |
| Active alerts / error messages | Screenshots or alert export |
| Support bundle | Generated above |
| vSphere / NSX version interop | Check interop matrix |

---

## SLA Tiers

| Priority | Description | Initial Response |
|----------|-------------|-----------------|
| P1 — Critical | Production down, full outage | 30 minutes |
| P2 — High | Significant degradation, workaround available | 4 hours |
| P3 — Medium | Partial impact, non-urgent | Next business day |
| P4 — Low | General question, enhancement request | Next business day |

---

## Escalation Path

1. Open case via Broadcom Support Portal with all information collected above.
2. If no response within SLA: use portal escalation button or call support line.
3. For P1: request **duty manager escalation** via phone.
4. Engage internal VMware/Broadcom TAM (Technical Account Manager) if available.

---

## Useful Links

| Resource | URL |
|----------|-----|
| Broadcom Support Portal | https://support.broadcom.com |
| Aria Operations Documentation | https://docs.vmware.com/en/VMware-Aria-Operations/ |
| VMware Interoperability Matrix | https://interopmatrix.vmware.com/ |
| Broadcom Lifecycle Policy | https://support.broadcom.com/lifecycle-management |
| Broadcom Knowledge Base | https://kb.vmware.com |

---

## Related Sections

- [Operations](../../operations/index.md) — support bundle generation
- [Diagnostics](../diagnostics/index.md) — pre-case diagnostics
- [Install & Upgrade](../../operations/install-upgrade/index.md) — version and EOL information

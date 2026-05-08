# Aria Automation — Escalation
## Support Portal

**Broadcom Support Portal:** https://support.broadcom.com

Log in with your Broadcom Support account (formerly VMware Customer Connect). Aria Automation support cases are raised under the **VMware Cloud Foundation > Aria Automation** product.

---

## Generating a Support Bundle

The Aria Automation support bundle is collected from the appliance CLI:

```bash
# SSH to the Aria Automation appliance
ssh root@<aria-automation-fqdn>

# Generate the support bundle
vracli support-bundle
```

The bundle is saved to `/tmp/` and includes service logs, configuration, and diagnostic output.

Alternatively, collect logs from `/services-logs/` on the appliance for targeted troubleshooting.

---

## Information to Collect Before Opening a Case

| Item | Where to Find |
|---|---|
| Aria Automation version | `vracli version` or admin UI |
| vSphere / vCenter version | vCenter About page |
| NSX version | NSX Manager About page |
| LCM version | LCM admin UI |
| Support bundle | Generated via `vracli support-bundle` |
| Deployment event logs | UI: Deployments > \<deployment\> > Events |
| Kubernetes pod logs | `kubectl logs <pod> -n prelude` |
| Description of the issue with exact timestamps | — |
| Steps to reproduce | — |
| Impact — how many users / deployments affected | — |

---

## SLA Tiers

| Priority | Definition | Initial Response |
|---|---|---|
| **P1 — Critical** | Production system down, no workaround | 30 minutes |
| **P2 — Major** | Significant functionality impacted, workaround available | 2 business hours |
| **P3 — Minor** | Limited impact, workaround available | Next business day |
| **P4 — General** | How-to questions, enhancement requests | 2 business days |

---

## Useful Links

- Broadcom Support Portal: https://support.broadcom.com
- Aria Automation Documentation: https://docs.vmware.com/en/VMware-Aria-Automation/
- VMware Product Lifecycle Matrix: https://lifecycle.vmware.com
- VMware Interoperability Matrix: https://interopmatrix.vmware.com
- Broadcom Security Advisories: https://support.broadcom.com/security-advisory

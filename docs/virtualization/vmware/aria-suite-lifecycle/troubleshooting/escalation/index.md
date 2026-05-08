# Aria Suite Lifecycle — Escalation

## When to Escalate to Broadcom Support

Escalate when the following conditions are met and internal troubleshooting has not resolved the issue:

- Upgrade workflow is stuck and **Retry** does not clear it
- LCM application cannot be started after a failed upgrade
- Locker data is inaccessible (lost Master Password requires SR-guided recovery)
- Product appliance VMs are in an unknown state following an LCM rollback that failed partway through
- LCM API returns 500 errors persistently with no clear cause in logs
- Certificate replacement via LCM causes a product outage and re-apply does not recover it

Do not power cycle product VMs without SR guidance if they are in a partially upgraded state — this can cause split-brain or unrecoverable database corruption.

---

## Opening a Broadcom Support Request

Broadcom support for LCM is accessed via the [Broadcom Support Portal](https://support.broadcom.com).

**Product to select:** VMware Aria Suite Lifecycle (under the VMware Cloud Foundation portfolio)

**Severity definitions:**

| Severity | Description | Target Initial Response |
|---|---|---|
| S1 | Production environment down, no workaround | 30 minutes (24x7) |
| S2 | Major feature unavailable, significant business impact | 4 hours (24x7) |
| S3 | Partial degradation, workaround available | Next business day |
| S4 | General question, documentation request, or enhancement | Next business day |

---

## Data to Collect Before Opening an SR

Collect all of the following before opening the SR — providing this upfront avoids the first support response being a data collection request.

**LCM system details:**

```bash
# LCM version — note output
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.corp.local/lcm/lcmservice/api/v2/system/details" | jq '.'

# Or via UI: LCM → Settings → System Details → Version
```

**Log bundle (required for all SRs):**

```bash
# Generate support bundle from LCM appliance SSH
ssh admin@lcm-prod-01.corp.local
vracli support-bundle generate

# Bundle location — typically /data/support-bundles/<timestamp>.tar.gz
ls -lh /data/support-bundles/
```

The bundle includes: LCM application logs, service logs, deployment history, Locker metadata (no passwords), system diagnostics, and recent request audit trail.

**Additional data for specific issues:**

| Issue Type | Additional Data |
|---|---|
| Upgrade failure | Request ID from LCM UI; upgrade-specific log from `/var/log/vmware/vrlcm/upgrade/` |
| VIDM/authentication failure | VIDM appliance log bundle; browser HAR file of the failed login flow |
| Certificate failure | `openssl x509 -text` output for the failing certificate; trust chain verification output |
| UI issue | Browser console errors (F12 → Console); browser HAR file of the failing page load |
| Network/connectivity issue | `traceroute`, `curl -v` output between LCM and affected endpoint |

---

## SR Handoff Checklist

Before handing an SR to the next shift or to a specialist:

- [ ] SR number documented in the incident ticket
- [ ] Support bundle uploaded to the SR (confirm upload complete in the portal)
- [ ] Exact LCM version and affected product versions noted
- [ ] Timeline of events: last known good state → first observed failure → actions taken
- [ ] Any commands run on the LCM appliance or product VMs documented
- [ ] Current state of the product VMs (powered on/off, snapshot present/absent)
- [ ] Broadcom support contact name and case manager noted

---

## VMware by Broadcom Knowledge Base

Before opening an SR, search the Broadcom knowledge base for known issues:

- Search: `site:kb.vmware.com aria suite lifecycle <error message>`
- LCM release notes list known issues for each version — review before upgrades
- The VMware by Broadcom communities forum often has workarounds for common LCM errors

**Useful KB categories for LCM:**
- Upgrade failures: search `vRealize Suite Lifecycle upgrade fails`
- Certificate errors: search `LCM locker certificate import`
- VIDM integration: search `LCM identity manager`

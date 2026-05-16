# Aria Operations for Networks — Escalation

---

## Before Opening a Support Case

Collect the following before contacting VMware Support:

| Item | How to Collect |
|---|---|
| Support bundle | Settings → Support → Download Support Bundle (Platform + all Collectors) |
| vRNI version | Settings → About → Version |
| Data source list | Settings → Data Sources → export or screenshot |
| Symptom timeline | When issue started, what changed before it started |
| Affected component | Collector, data source, UI, API, specific feature |
| Error messages | Screenshots or copy of exact error text |
| Network topology | Which sites, how many VMs, how many switches |

---

## Severity Definitions

| Severity | Condition | Response Target |
|---|---|---|
| Sev 1 | Complete loss of vRNI platform — no data, no UI | 30 minutes (with active collab) |
| Sev 2 | Major feature unavailable — e.g., all flows missing, NSX integration down | 4 business hours |
| Sev 3 | Specific data source failing, UI slow, one collector disconnected | Next business day |
| Sev 4 | General how-to, feature request, minor cosmetic issue | Standard queue |

---

## Generate Support Bundle via CLI

If the UI is unavailable:

```bash
ssh ubuntu@vrni.corp.local

# Generate support bundle from CLI
sudo /etc/init.d/support-bundle.sh

# Bundle is placed in:
ls /data/support-bundles/
# Transfer via SCP:
scp ubuntu@vrni.corp.local:/data/support-bundles/<bundle>.tar.gz /local/path/
```

---

## Log Files to Include

If the support bundle generation fails, manually collect:

```bash
# Platform logs
tar czf vrni-platform-logs-$(date +%Y%m%d).tar.gz /var/log/vmware/

# Collector logs (run on each Collector VM)
tar czf vrni-collector-logs-$(date +%Y%m%d).tar.gz /var/log/vmware/
```

---

## Engage VMware Support

1. Go to **customerconnect.vmware.com** (or Broadcom Support Portal)
2. Select product: **VMware Aria Operations for Networks** (or **vRealize Network Insight**)
3. Attach: support bundle, version info, symptom description
4. If Sev 1: call support hotline directly after creating the case to request phone bridge

---

## Escalation Path

| Escalation Level | Trigger |
|---|---|
| Standard support | Initial case creation |
| Technical Account Manager | Recurring issue, contract SLA breach |
| Engineering escalation | Support cannot reproduce; feature defect suspected |
| Executive escalation | Business-critical outage, multi-day unresolved Sev 1 |

---

## Knowledge Base and Community

- VMware Aria Operations for Networks Documentation: docs.vmware.com/aria-networks
- VMware KB: kb.vmware.com (search "vRealize Network Insight" or "Aria Operations for Networks")
- VMware Community Forums: communities.vmware.com/community/vmtn/vrealize-network-insight
- Release Notes: check before upgrade for known issues and resolved bugs

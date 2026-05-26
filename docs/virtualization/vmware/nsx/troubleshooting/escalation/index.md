# NSX — Escalation

## Support Portal

All VMware/NSX support is handled through the Broadcom Support Portal:

**https://support.broadcom.com**

Log in with your Broadcom Support account. NSX support entitlement is tied to your licence contract. Navigate to **My Dashboard → Support → Create Case**.

---

## When to Escalate

Escalate to Broadcom Support when:

- NSX Manager cluster is UNSTABLE and cannot be recovered with documented procedures
- All BGP sessions down on a T0 gateway after confirming physical underlay is healthy
- DFW rules not syncing to transport nodes (hosts show old policy after NSX Manager shows updated policy)
- Transport node preparation failing repeatedly after VIB reinstall attempts
- Corfu DB (control plane) corruption: `get corfu-cluster status` shows repeated errors
- Certificate operations failing and blocking API/UI access
- Post-upgrade regression: known-good functionality broken after NSX version upgrade

---

## Information to Collect Before Opening a Case

Collecting the right data upfront reduces time-to-resolution significantly.

### Environment Information

| Field | How to Retrieve |
|---|---|
| NSX version and build | `get version` on NSX Manager CLI |
| ESXi version and build | `vmware -v` on any ESXi host |
| vCenter version | vSphere Client → Help → About |
| Edge node version | `get version` on Edge CLI |
| VCF version (if applicable) | SDDC Manager UI |
| Topology | Number of Manager nodes, Edge clusters, ESXi hosts, T0/T1 gateways |

### Symptom Data

| Item | Collection Method |
|---|---|
| Error message (exact text) | Screenshot or copy from UI/CLI |
| Time of first occurrence | NSX Manager audit log + vCenter events timestamp |
| Reproducibility | Consistent or intermittent; steps to reproduce |
| Impact scope | Which segments, VMs, or tenants are affected |
| Recent changes | List of changes within 72 hours before symptom started |

### NSX Support Bundle

Generate and download the NSX support bundle — this includes all Manager logs, DB state, and system configuration.

From NSX Manager UI: **System → Support Bundle → Download**

Or via API:

```bash
# Trigger support bundle generation
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"log_age": 48}' \
  "https://<nsx-manager>/api/v1/node/support-bundles"

# Poll for completion
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/node/support-bundles/status"

# Download the bundle (URL returned in the status response)
curl -sk -u 'admin:password' \
  -O "https://<nsx-manager>/api/v1/node/support-bundles/download/<bundle-id>"
```

### Edge Node Logs

For routing or Edge-specific issues, collect Edge node logs separately:

```bash
# SSH to Edge node
get log edge follow        # Real-time log
get logs                   # Recent logs snapshot

# Log files on Edge node
ls /var/log/vmware/nsx-edge/
tail -500 /var/log/vmware/nsx-edge/edge.log
```

### ESXi Host DFW Logs

For DFW-related issues, collect from the affected ESXi host:

```bash
# SSH to ESXi host
vm-support -n -w /tmp/
# Copy bundle to accessible location
cp /tmp/esx-*.tgz /vmfs/volumes/<datastore>/support/
```

Key files within the ESXi support bundle for NSX:
- `/var/log/vmkernel.log` — NSX VIB and Geneve events
- Filter-specific logs from `vsipioctl` output
- `/etc/vmware/nsx/` — NSX configuration on host

---

## Severity Levels

| Severity | Criteria | Examples |
|---|---|---|
| P1 — Critical | Production down; data loss risk; no workaround | NSX Manager cluster UNSTABLE; all VMs on an overlay segment unreachable |
| P2 — Major | Production degraded; workaround exists | One Edge node down (second Edge still active); specific DFW rules not pushing |
| P3 — Minor | Non-production affected; low business impact | Lab NSX Manager unreachable; minor DFW logging issues |
| P4 — Informational | How-to questions; feature requests | Best practice questions; upgrade planning |

Set the correct severity at case creation — P1 cases receive immediate 24x7 engineer response.

---

## Support Tier Response Times

| Support Tier | P1 Initial Response | P2 Initial Response | Coverage |
|---|---|---|---|
| Production Support | 30 minutes | 4 hours | 24x7 |
| Business Critical Support | 15 minutes | 2 hours | 24x7 + dedicated TAM |

Business Critical Support includes a Technical Account Manager (TAM) for proactive guidance and expedited escalation.

---

## Escalation Path

1. **Initial case** — Broadcom Support Portal. Provide all required data upfront.
2. **Status stall** — If no meaningful progress within the expected response SLA, request case escalation through the support portal.
3. **TAM escalation** — If Business Critical tier, contact your TAM directly by phone or email.
4. **Executive escalation** — For P1 incidents not progressing, request Broadcom Escalation Management via the TAM or directly through the support portal escalation workflow.

---

## Diagnostic Commands to Run Before Calling Support

Run these commands and have the output ready before opening a case:

```bash
# NSX Manager CLI (SSH to any Manager node)
nsxcli
get cluster status
get managers
get services
get corfu-cluster status
get transport-node-status
get tunnel status
get version

# Edge node CLI (SSH to each Edge)
get version
get services
get interfaces
get bgp neighbor summary
get edge-cluster status

# From NSX Manager API
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/cluster/status"
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/transport-nodes/status"
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL"
```

Save all output with timestamps. Support engineers will ask for these as a first step — having them ready accelerates triage.

---

## Known VMware Security Advisories (VMSA) — NSX

Subscribe to VMware Security Advisories for NSX CVE notifications:

- RSS/email: **https://support.broadcom.com/web/ecx/security-advisory**
- Filter by: Product = NSX-T Data Center

Patch response SLAs (align with your security policy):

| CVSS Score | Classification | Response |
|---|---|---|
| 9.0+ (Critical) | Critical | Patch within 72 hours; emergency change if active exploitation |
| 7.0–8.9 (High) | High | Patch within 30 days |
| 4.0–6.9 (Medium) | Medium | Include in next quarterly cycle |
| < 4.0 (Low) | Low | Risk-assess; patch in next scheduled window |

Note: NSX CVEs that affect the DFW bypass or allow unauthenticated API access should be treated as Critical regardless of CVSS score due to the security control impact.

# VMware ESXi Vendor Support

## Support Portal

Broadcom acquired VMware in 2023. All VMware product support is now handled through the Broadcom Support Portal:

**https://support.broadcom.com**

Log in with your Broadcom Support account (formerly VMware Customer Connect). Support contracts are attached to your Broadcom account. If your organisation has a VCPP (VMware Cloud Provider Programme) partner agreement, support may be routed through your VCPP partner.

## Opening a Case

When opening a support case for an ESXi issue, collect and provide the following information upfront to avoid back-and-forth and reduce time to first response:

| Field | How to Retrieve |
|---|---|
| ESXi version and build | `vmware -v` on the host shell |
| Host hardware model and serial | `esxcli hardware platform get` |
| vCenter version and build | vSphere Client > Help > About |
| Symptom description | Specific error message, affected operations, time of first occurrence |
| Affected VMs | VM names, guest OS, workload type |
| Recent changes | Patches, configuration changes, hardware replacements |
| Reproducibility | Intermittent vs. consistent; steps to reproduce |

Set the correct severity when opening the case:

| Severity | Criteria |
|---|---|
| P1 — Critical | Production system down, data loss risk, no workaround |
| P2 — Major | Production degraded, workaround exists |
| P3 — Minor | Non-production affected or low-impact issue |
| P4 — Informational | Questions, how-to, documentation requests |

## Information to Collect

Generate an ESXi support bundle before contacting support. The bundle includes vmkernel logs, hostd logs, network config, storage config, and system state.

**From ESXi shell:**

```bash
vm-support -w /tmp/
# Bundle is created at /tmp/esx-<hostname>-<timestamp>.tgz
# Copy to a datastore for retrieval:
cp /tmp/esx-*.tgz /vmfs/volumes/<datastore>/
```

**From vSphere Client:**

vSphere Client > Host > Monitor > System > Support > Generate Support Bundle

The bundle is downloaded via the browser.

**Log files included in the bundle:**

| Log | Content |
|---|---|
| `vmkernel.log` | VMkernel events, storage, network, hardware errors |
| `hostd.log` | Host daemon API, VM operations, configuration changes |
| `vpxa.log` | vCenter agent communication |
| `fdm.log` | vSphere HA fault domain manager |
| `vobd.log` | VMkernel observations and hardware events |
| `auth.log` | Authentication events |
| `shell.log` | Shell commands |

For performance issues, also collect:

```bash
# esxtop snapshot (batch mode, 60 seconds, 2-second intervals)
esxtop -b -d 2 -n 30 > /tmp/esxtop.csv
```

## SLA Tiers

| Support Tier | P1 Response | P2 Response | Coverage |
|---|---|---|---|
| Production Support | 30 minutes | 4 hours | 24x7 |
| Business Critical Support | 15 minutes | 2 hours | 24x7 |

Business Critical Support also includes a designated Technical Account Manager (TAM) and proactive guidance. Response times are for initial contact; resolution timelines depend on issue complexity.

## Escalation

**TAM (Technical Account Manager):** Available with Business Critical Support. Engage the TAM for high-impact incidents, planned major upgrades, or architectural reviews. The TAM can escalate internally to engineering when standard support is not progressing.

**Executive Escalation:** For P1 incidents not progressing, request escalation to Broadcom's Escalation Management team through the support portal or via your TAM.

**VCPP Partner Support:** If licenced through a VCPP partner, the partner provides first-level support and escalates to Broadcom on your behalf. Ensure your partner has the correct support tier for your SLA requirements.

**VMware HCL (Hardware Compatibility List):** Before raising a case for hardware-related issues, verify the host is on the HCL at https://compatibilityguide.broadcom.com. Support may request HCL verification as an early step.

# vCenter — Escalation

```
Escalation Path — Broadcom / VMware Support
════════════════════════════════════════════════════════

  Internal Triage (you)
  ┌─────────────────────────────────────────────────┐
  │  Collect evidence before opening case:          │
  │  ├── df -h output                               │
  │  ├── service-control --status --all             │
  │  ├── vpxd.log tail (last 500 lines)             │
  │  ├── SSO log tail                               │
  │  ├── vCenter build number (Help → About)        │
  │  ├── ESXi build numbers for affected hosts      │
  │  └── Recent change log from CMDB                │
  └───────────────────┬─────────────────────────────┘
                      │
                      ▼
  ┌─────────────────────────────────────────────────┐
  │  Generate vm-support bundle                     │
  │  VAMI :5480 → Support → Create Support Bundle  │
  │  OR: /usr/bin/vm-support -n <vcenter>           │
  └───────────────────┬─────────────────────────────┘
                      │
                      ▼
  ┌─────────────────────────────────────────────────┐
  │  Open case: support.broadcom.com                │
  │  ├── S1 (production down)  → 30 min SLA         │
  │  ├── S2 (significant impact) → 4 hr SLA         │
  │  └── S3/S4 (minor / question) → 8-12 hr SLA    │
  └───────────────────┬─────────────────────────────┘
                      │
                      ▼ if no progress within SLA
  ┌─────────────────────────────────────────────────┐
  │  Escalate within Broadcom case                  │
  │  ├── Request Senior PSE assignment              │
  │  ├── Loop in TAM (if you have one) for S1/S2   │
  │  └── Executive escalation via account team     │
  │       for prolonged P1 outages                 │
  └─────────────────────────────────────────────────┘
```

## Support Portal

All VMware/vSphere support is now handled through **Broadcom Support** following the 2023 VMware acquisition:

- Portal: [https://support.broadcom.com](https://support.broadcom.com)
- My Cases: Log in → Support → My Cases
- Download Center: Log in → VMware Cloud Foundation → vSphere

Ensure your Broadcom account is linked to your company's entitlement. Contact your account team if entitlement is missing after the migration.

## Opening a Support Case

### Information to Collect Before Opening

| Item | How to Get It |
|---|---|
| vCenter version + build number | `https://<vcenter>/ui` → Help → About |
| ESXi version + build numbers | `esxcli system version get` or vCenter host summary |
| Issue symptom and timeline | Document exact error, first occurrence, and change history |
| Number of hosts/VMs affected | Cluster inventory from vCenter |
| HA/DRS status at time of issue | vCenter Events tab |
| Recent changes (patches, upgrades, config) | Change log / CMDB |

### Log Bundle Collection

**From vCenter VAMI (recommended):**
```
https://<vcenter>:5480 → Support → Create Support Bundle
```

**From vCenter UI:**
```
vSphere Client → Administration → Deployment → System Configuration → Export System Logs
```

**From VCSA shell (`vm-support` bundle):**
```bash
/usr/bin/vm-support -n <vcenter-name>
# Output: /var/core/esx-<timestamp>.tgz
```

**ESXi Tech Support Mode logs** (from ESXi shell or DCUI → Troubleshooting Options):
```bash
vm-support
# Bundle created in /var/core/
```

**NSX Manager support bundle** (if NSX issue involved):
```
NSX Manager UI → System → Support Bundle → Generate
```

### Severity Levels

| Severity | Definition | VMware Response Target |
|---|---|---|
| S1 (Critical) | Production down, no workaround | 30 min (Production), 15 min (Business Critical) |
| S2 (High) | Significant impact, partial workaround | 4 hours |
| S3 (Medium) | Minor impact, workaround available | 8 business hours |
| S4 (Low) | General question or enhancement | 12 business hours |

Request severity upgrade if business impact increases.

## SLA Tiers

| Support Tier | Description |
|---|---|
| Basic | Business hours only; S1 response: next business day |
| Production | 24×7 for S1/S2; standard response SLAs |
| Business Critical | 24×7 with faster SLAs; assigned Senior PSE |
| Enterprise / TAM | Dedicated Technical Account Manager; proactive support |

Verify your support tier in the Broadcom portal under **My Entitlements**.

## Escalation Path

1. **Open case** — provide full symptom description, logs, and build numbers
2. **Request escalation** — if no progress within SLA, ask for Senior PSE or escalation manager
3. **TAM engagement** — if you have a TAM, loop them into the case immediately for S1/S2
4. **Executive escalation** — through your Broadcom account team for prolonged P1 outages

## Useful Broadcom Resources

| Resource | URL |
|---|---|
| Security Advisories (VMSA) | https://support.broadcom.com/web/ecx/security-advisory |
| Product Lifecycle Matrix | https://support.broadcom.com/group/ecx/productlifecycle |
| Interoperability Matrix | https://interopmatrix.broadcom.com |
| VMware HCL | https://compatibilityguide.broadcom.com |
| Knowledge Base | https://knowledge.broadcom.com |
| vSphere Release Notes | Search by version in Knowledge Base |

## Information Broadcom Will Ask For

- **vCenter build number** (not just version — the 7-digit build number uniquely identifies the patch level)
- **ESXi build numbers** for affected hosts
- **`vm-support`** bundle from vCenter appliance
- **ESXi TSM log bundle** from affected host
- **Steps to reproduce** the issue
- **Frequency and scope** (one host, one cluster, all clusters)
- **Recent changes** (patches, firmware, network changes, vCenter upgrades)

Upload logs directly to the case via the Broadcom portal file upload — do not send via email due to size limits.

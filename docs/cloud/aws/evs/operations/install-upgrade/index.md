# Amazon EVS — Lifecycle & Upgrades

<div class="kb-summary">
VCF upgrades via SDDC Manager, ESXi patching lifecycle, NSX-T upgrade sequence, and EVS host AMI updates managed through AWS.
</div>

```text
┌────────────────────────────────── Amazon EVS — Lifecycle & Upgrades ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VCF upgrades: SDDC Manager → Lifecycle Management → Bundle download → Sequential upgrade   │    │
│   │   Upgrade order: SDDC Manager → vCenter → NSX-T → ESXi (one host at time)                   │     │
│   │   ESXi patches: AWS manages OS-level host AMI; VCF LCM manages ESXi version within VCF       │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## VCF Upgrade Sequence

```text
Correct upgrade order for VCF (must not be skipped):

1. SDDC Manager update (upgrade SDDC Manager itself first)
2. vCenter Server upgrade
3. NSX-T Manager upgrade
4. NSX-T Edge upgrade
5. ESXi host upgrade (via VCF LCM, one host at a time with vSAN evacuation)
6. HCX upgrade (if deployed; optional last step)

Each step must complete successfully before the next begins.
Upgrade bundles are downloaded and staged in SDDC Manager before initiating.
```

## SDDC Manager Lifecycle

```bash
# Access SDDC Manager
# URL: https://sddc-manager.vcf.internal
# Credentials: from AWS Secrets Manager /evs/<env-name>/sddc-manager-credentials

# Check for available bundles
# SDDC Manager UI → Lifecycle Management → Bundle Management → Download Available Bundles

# Trigger upgrade workflow
# SDDC Manager UI → Lifecycle Management → Upgrade
#   Select target VCF version → precheck → schedule → execute

# Monitor upgrade progress
# SDDC Manager → Lifecycle Management → Upgrade → running workflow task
# Takes: 4-8 hours for full stack (all components)
```

## ESXi Patching (VCF LCM)

```bash
# VCF LCM (Lifecycle Manager) handles ESXi patching as part of VCF upgrades.
# Do NOT patch ESXi hosts manually via esxcli or vSphere Update Manager independently
# — this puts the host out of VCF compliance.

# To check patch compliance:
# SDDC Manager → Inventory → Hosts → select host → View Compliance

# ESXi patch process (triggered by VCF LCM):
# 1. LCM evacuates VMs from host via vMotion
# 2. Puts host in maintenance mode with vSAN evacuation
# 3. Applies patch/upgrade bundle
# 4. Reboots host
# 5. Exits maintenance mode
# 6. Moves to next host

# Patch timeline per host: ~30-60 min
# Cluster patch timeline: hosts × 30-60 min (sequential, not parallel)
```

## HCX Upgrade

```bash
# Check current HCX version
# On-prem HCX Manager UI: Summary → HCX Version

# Upgrade HCX Manager (on-premises)
# HCX Manager UI → Updates → Check for Updates → Upgrade
# Takes ~30 minutes; HCX service mesh pauses during upgrade

# After HCX Manager upgrade: upgrade service mesh appliances
# HCX Manager → Interconnect → Service Mesh → Update (for each mesh)
# Takes ~15-20 minutes per service mesh

# Verify after upgrade
curl -sk -u "admin:$HCX_PASSWORD" \
  "https://$HCX_MANAGER_IP/hybridity/api/about" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Version: {d.get('version')}\")"
```

## Version Compatibility Matrix

| VCF Version | ESXi Version | NSX-T Version | vCenter Version |
|---|---|---|---|
| VCF 5.1 | ESXi 8.0 U2 | NSX 4.1 | vCenter 8.0 U2 |
| VCF 5.0 | ESXi 8.0 U1 | NSX 4.0 | vCenter 8.0 U1 |
| VCF 4.5 | ESXi 7.0 U3 | NSX 3.2 | vCenter 7.0 U3 |

Always verify the VMware Product Interoperability Matrix before upgrading EVS components.

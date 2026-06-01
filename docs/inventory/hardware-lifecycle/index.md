# Hardware Lifecycle Management


<div class="kb-summary">
Track physical infrastructure from procurement through secure disposal to optimise refresh cycles and maintain vendor support coverage.
</div>

## Lifecycle Stages

| Stage | Activities | Key Decisions |
|---|---|---|
| **Procurement** | Define specs; raise PO; receive and PAT test | Lead time; vendor selection; warranty tier |
| **Deployment** | Rack, cable, configure; add to CMDB; tag | Network segment; power zone; naming |
| **Operation** | Monitor health; apply firmware; manage capacity | Upgrade vs replace; performance tuning |
| **Maintenance** | Replace failed components; extend warranty | Cost of repair vs refresh cost |
| **Refresh planning** | Evaluate performance vs EoL; plan replacement | Refresh cycle timing; budget |
| **Decommission** | Migrate workloads; remove from service | Data wiping standard; resale or scrap |
| **Disposal** | Certify data destruction; return or dispose | WEEE compliance; data protection |

## Typical Refresh Cycles

| Equipment Type | Typical Lifespan | EoL Trigger |
|---|---|---|
| x86 Server | 5–7 years | EoS support from vendor; performance bottleneck |
| Storage array | 5–7 years | Vendor EoS; no more drive/module options |
| Core network switch | 7–10 years | Vendor EoS; capacity limits |
| Access switch | 7–10 years | PoE budget insufficient; no firmware updates |
| Firewall / security appliance | 5–7 years | Vendor EoL; throughput limits |
| UPS | 10 years (batteries every 3–5) | Battery replacement cost exceeds replacement value |

## Firmware / BIOS Management

```bash
# Dell — check and update firmware via iDRAC
racadm getversion                        # current firmware versions
racadm fwupdate -g -u -a <tftp-server>  # update all components

# HPE iLO — firmware inventory
hponcfg -f get_fw_version.xml

# Check vendor EoS dates
# Dell: https://www.dell.com/support/lifecycle/
# HPE: https://support.hpe.com/hpesc/public/home

# Linux — check BIOS version
dmidecode -t bios | grep -E "Version|Release Date"

# Check if fwupd supports the device
fwupdmgr get-devices
fwupdmgr refresh && fwupdmgr update  # update via LVFS
```
┌─────────────────────────────────── Inventory — Hardware Lifecycle ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Track hardware from purchase through active use to end-of-life and decommission        │   │
│   │       EOL: no more patches; EOSL: no more support calls — both require replacement plan       │   │
│   │        Refresh: budget cycle (18-24 months lead); decommission: secure wipe + disposal        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Lifecycle Phases               │  │             EOL/Refresh Actions             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │             Plan: spec + budget              │  │            Query vendor EOL dates           │   │
│   │            Procure: PO + delivery            │  │            Flag 18-month warning            │   │
│   │            Deploy: rack + config             │  │            Raise refresh project            │   │
│   │          Operate: maintain + patch           │  │           Migrate workloads first           │   │
│   │         Decommission: wipe + retire          │  │           Secure wipe certificate           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    EOL      = End of Life; vendor stops selling and developing the product                            │
│    EOSL     = End of Service Life; vendor stops providing support and security patches                │
│    Refresh  = Replace ageing hardware with current generation before EOSL                             │
│    Secure wipe= Cryptographic erasure or DoD overwrite before disposal to prevent data recovery       │
│    ITAD     = IT Asset Disposition; certified disposal with chain-of-custody and destruction cert     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```powershell

## Decommission Procedure

1. **Workload migration** — migrate or decommission all VMs/services on the host
2. **Remove from monitoring** — delete host from Prometheus, Zabbix, SCOM
3. **Remove from management** — remove from Ansible inventory, SSM, vCenter
4. **Remove from network** — remove switch port config; revoke firewall rules; remove DNS entries
5. **Update CMDB** — mark CI as "Decommissioned"; record date and reason
6. **Data destruction** — wipe all drives per policy (see below)
7. **Physical removal** — unrack and label for disposal/return
8. **Disposal documentation** — obtain WEEE certificate or vendor return confirmation

## Data Destruction Standards

| Standard | Method | When to Use |
|---|---|---|
| DoD 5220.22-M | Multi-pass overwrite | HDD; non-encrypted |
| Cryptographic erase | Destroy encryption key | SED / FIPS 140 drives |
| Secure erase (ATA) | `hdparm --security-erase` | SSD internal wipe |
| Physical destruction | Degauss + shred | Classified / Restricted data |

```bash
# Secure erase a drive (ATA)
hdparm -I /dev/sda | grep -i "security"  # check if security-erase supported
hdparm --security-set-pass Erase /dev/sda
hdparm --security-erase Erase /dev/sda

# shred overwrite (for drives without ATA secure erase)
shred -vzn 3 /dev/sda  # 3-pass overwrite + verify
```

## Hardware Lifecycle Checklist

- [ ] Hardware older than 5 years reviewed for refresh planning
- [ ] All in-service hardware has active vendor support coverage
- [ ] Firmware/BIOS current within 2 releases of latest stable
- [ ] SMART health checks run on all HDDs/SSDs monthly
- [ ] Decommissioned hardware removed from all monitoring and management systems
- [ ] Data destruction certificate obtained for retired drives
- [ ] CMDB updated to reflect current hardware state

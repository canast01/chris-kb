# VCF — Integrations


<div class="kb-summary">
Integrations reference covering NSX Federation (Multi-Site VCF), Backup Integration, SIEM and Syslog Integration.
</div>

VCF Integration Topology
```text
┌─────────────────────────────────────────────────────┐
│  SDDC Manager (integration hub)                      │
└──┬──────┬──────┬──────┬──────┬──────────────────────┘
```
   │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼
```text
┌──────┐ ┌────┐ ┌────┐ ┌────┐ ┌──────────────────────┐
│ Aria │ │Aria│ │ AD │ │SIEM│ │  Backup                │
│ Ops  │ │Auto│ │LDAP│ │Sys-│ │  (Veeam/NetBackup)     │
│      │ │    │ │    │ │log │ │                        │
│VCF MP│ │Cloud│ │SSO│ │TLS │ │  per-domain vCenter    │
│ adds │ │Acct│ │IDp │ │6514│ │  as managed server     │
│ SDDC │ │+NSX│ │    │ │    │ │                        │
│ data │ │creds│ │    │ │    │ │  SFTP for SDDC Mgr    │
└──────┘ └────┘ └────┘ └────┘ └──────────────────────┘
```

NSX Federation (multi-site)
```text
```
┌──────────────────────────────────────────────────────┐
│  Global NSX Manager (outside VCF LCM)                │
│                        │ global policy               │
│              ┌─────────┴──────────┐                  │
│              ▼                    ▼                  │
│   ┌──────────────────┐  ┌──────────────────┐         │
│   │ VCF Site A       │  │ VCF Site B       │         │
│   │ Local NSX Mgr    │  │ Local NSX Mgr    │         │
│   │ (data plane)     │  │ (data plane)     │         │
│   └──────────────────┘  └──────────────────┘         │
└──────────────────────────────────────────────────────┘
```text
┌─────────────────────────────── VMware Cloud Foundation — Integrations ────────────────────────────────┐
│                                                                                                       │
│  VCF integrates with external identity (AD/LDAP), backup tools, external KMS,                         │
│  monitoring (Aria Operations), and cloud connectivity (VMware Cloud Gateway).                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Identity Integrations             │  │             Backup Integrations             │   │
│   │         AD/LDAP: per vCenter domain          │  │            VADP: Veeam/Commvault            │   │
│   │           SSO: per workload domain           │  │             vSAN: CBT snapshots             │   │
│   │            vIDM: unified identity            │  │           SDDC Mgr: config backup           │   │
│   │         SAML federation: Aria suite          │  │              NSX: config export             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Identity integrates per domain; vIDM provides unified SSO across all VCF components.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Monitoring & Security             │  │              Cloud Integrations             │   │
│   │         Aria Operations: all domains         │  │             VMware Cloud Gateway            │   │
│   │         Aria Logs: syslog ingestion          │  │              HCX: VM migration              │   │
│   │           KMS: per vSAN encryption           │  │            VMC on AWS integration           │   │
│   │             SIEM: forward syslog             │  │           Tanzu: Kubernetes on VCF          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Integration traffic crosses management network; KMS must be reachable from all hosts;                │
│  HCX uses dedicated uplink network for VM migrations.                                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM       = VMware Identity Manager; unified SSO across VCF products                                │
│  SAML       = Security Assertion Markup Language; federation token format                             │
│  HCX        = Hybrid Cloud Extension; WAN-optimised VM migration                                      │
│  VMC        = VMware Cloud on AWS; extend VCF to public cloud                                         │
│  Cloud GW   = on-prem appliance connecting VCF to VMware cloud services                               │
│  Tanzu      = Kubernetes runtime integrated into VCF workload domains                                 │
│  Aria Ops   = operations management; multi-domain visibility                                          │
│  Aria Logs  = centralised log management for all VCF components                                       │
│  KMS        = external key server for vSAN at-rest encryption                                         │
│  VADP       = vStorage APIs for Data Protection; backup integration                                   │
│  SDDC Mgr backup= exports SDDC Manager config; restore to rebuild                                     │
│  SIEM       = Security Information and Event Management; log receiver                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Test AD connectivity from SDDC Manager appliance:**

```bash
ldapsearch -H ldaps://<dc-ip>:636 -x -D "<bind-account-dn>" -W \
  -b "dc=domain,dc=com" "(sAMAccountName=<test-user>)"
```

---

## NSX Federation (Multi-Site VCF)

NSX Federation allows a single NSX policy plane to span multiple VCF instances across sites via a Global Manager (GM).

**Key design points:**

- The Global Manager is deployed outside VCF LCM — it is not upgraded via SDDC Manager.
- Local NSX Managers in each VCF instance handle data-plane operations.
- Stretched segments, global gateway policies, and security policies are defined at the GM level.
- GM upgrade is planned separately from each VCF site's NSX upgrade cycle.

---

## Backup Integration

VCF does not provide a native VM backup solution. VM backup is handled at the vCenter layer per workload domain.

**Veeam B&R:**

1. Add each workload domain vCenter as a Managed Server in Veeam.
2. VMs appear in Veeam inventory as standard vSphere VMs.
3. Ensure backup proxies have access to vSAN datastores in each domain.

**SDDC Manager configuration backup** (separate from VM data backup):

```text
SDDC Manager → Administration → Backup → Configure
→ Set SFTP target → schedule daily → retain 7+ restore points
```

---

## SIEM and Syslog Integration

```text
SDDC Manager → Administration → Syslog → Add Syslog Server
→ Protocol: TLS (recommended) or UDP/TCP → Port: 6514 or 514
```

**Verify forwarding is working:**

1. Perform a test action in SDDC Manager (e.g., browse a domain, rotate a password).
2. Confirm the event appears in the SIEM within a few minutes.
3. Check that the SIEM source IP matches the SDDC Manager appliance IP.

**vCenter syslog per workload domain (PowerCLI):**

```powershell
# Configure syslog forwarding on all ESXi hosts in a cluster
Get-Cluster "ClusterName" | Get-VMHost | ForEach-Object {
  Set-VMHostSysLogServer -VMHost $_ -SysLogServer "udp://<siem-ip>:514"
  Restart-VMHostService -VMHost $_ -Key "syslog" -Confirm:$false
}
```

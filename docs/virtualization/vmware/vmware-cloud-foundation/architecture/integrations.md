---
tags:
  - architecture
  - vcf
  - vmware
---
# VMware Cloud Foundation — Integrations

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
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Global NSX Manager (outside VCF LCM)                                                                 │
│                        │ global policy                                                                │
│              ┌─────────┴──────────┐                                                                   │
│              ▼                    ▼                                                                   │
│   ┌──────────────────┐  ┌──────────────────┐                                                          │
│   │ VCF Site A       │  │ VCF Site B       │                                                          │
│   │ Local NSX Mgr    │  │ Local NSX Mgr    │                                                          │
│   │ (data plane)     │  │ (data plane)     │                                                          │
│   └──────────────────┘  └──────────────────┘                                                          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
ldapsearch -H ldaps://<dc-ip>:636 -x -D "<bind-account-dn>" -W \
  -b "dc=domain,dc=com" "(sAMAccountName=<test-user>)"
```
```text
SDDC Manager → Administration → Backup → Configure
→ Set SFTP target → schedule daily → retain 7+ restore points
```
```text
SDDC Manager → Administration → Syslog → Add Syslog Server
→ Protocol: TLS (recommended) or UDP/TCP → Port: 6514 or 514
```
```powershell
## Configure syslog forwarding on all ESXi hosts in a cluster
Get-Cluster "ClusterName" | Get-VMHost | ForEach-Object {
  Set-VMHostSysLogServer -VMHost $_ -SysLogServer "udp://<siem-ip>:514"
  Restart-VMHostService -VMHost $_ -Key "syslog" -Confirm:$false
}
```

## See also

- [VMware Cloud Foundation — How It Works](how-it-works/)
- [VMware Cloud Foundation — Deploy](../deploy/)

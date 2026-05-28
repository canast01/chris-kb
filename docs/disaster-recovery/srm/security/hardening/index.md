# SRM Security — Hardening

```
┌─────────────────────────────────────────── SRM — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   SRM — Hardening Checklist                                   │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │          [ ] Restrict management port (443 (SRM HTTPS)) to jump host / management VLAN        │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │        [ ] Firewall: allow only 443 (SRM HTTPS) · 9086 (SRM-SRM pairing) · 443 (vCenter)      │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Test Failover Network Isolation

Recovery plan tests must never reach production networks. Enforce this:

1. Create an isolated port group on the recovery site ESXi cluster: `vPG-SRM-Test-Bubble` (no uplinks)
2. Configure network mapping in SRM: source production network → `vPG-SRM-Test-Bubble`
3. Verify no routing exists from the test bubble to production VLANs
4. If using NSX: create a dedicated overlay segment with no uplink for test failover

```powershell
# Verify test network mapping
Get-SrmRecoveryPlan | Get-SrmNetworkMapping | Select Name, RecoveryNetwork
```

## Audit Logging

SRM logs all recovery plan events. Ensure logs are forwarded to SIEM:

- SRM logs location: `C:\ProgramData\VMware\VMware vCenter Site Recovery Manager\Logs\`
- Forward using a log collector agent (Filebeat, Splunk UF) on the SRM server
- SIEM alert rules:
  - Recovery plan started outside business hours or without change ticket
  - Recovery plan started on production (non-test) mode
  - Failed recovery plan steps (suggests misconfiguration before actual DR event)

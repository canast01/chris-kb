# SRM Security — Hardening

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

---
tags:
  - operations
  - windows
---
# Active Directory — Health Checks


<div class="kb-summary">
Daily operations centre on replication health and authentication event monitoring across all Domain Controllers.

*Applies to: Windows Server 2019 / 2022*
</div>
```text
┌──────────────────────── Security Active Directory Operations — Health Checks ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Active Directory health checks: routine verification of operational status and performance  │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Active Directory Operations infrastructure · management network · monitoring    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Active Directory   = Security Active Directory Operations platform overview and core concepts      │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these commands each morning to verify Active Directory health before issues impact authentication or Group Policy delivery.

1. **DC replication status** — check for replication failures across all domain controllers:
   ```powershell
   repadmin /showrepl
   ```

2. **DC replication summary** — review fail count for all DCs:
   ```powershell
   repadmin /replsummary
   ```

3. **FSMO roles** — verify each FSMO role is on the expected DC:
   ```powershell
   netdom query fsmo
   ```

4. **DC services** — confirm critical services are running (repeat per DC):
   ```powershell
   Get-Service adws,dns,kdc,netlogon,w32tm | Select Name,Status
   ```

5. **AD replication queue** — should be empty or near-zero:
   ```powershell
   repadmin /queue
   ```

6. **SYSVOL replication (DFSR)** — check for no backlog:
   ```powershell
   dfsrdiag replicationstate
   ```

7. **DNS health** — all tests should return PASS:
   ```powershell
   dcdiag /test:dns /s:<dc-name>
   ```

8. **Time sync** — check Source and Stratum; offset should be less than 5 seconds:
   ```powershell
   w32tm /query /status
   ```

9. **DC connectivity** — verify network-level DC reachability:
   ```powershell
   dcdiag /test:connectivity /s:<dc-name>
   ```

10. **Event log errors (last 24h)** — surface recent Directory Service errors:
    ```powershell
    Get-EventLog -LogName "Directory Service" -EntryType Error -Newest 20 -ComputerName <dc>
    ```

---

 Run `repadmin /replsummary` and `dcdiag /test:replications` each morning to surface any replication failures before they impact authentication or Group Policy delivery. Review Windows Event Log on all DCs for Event ID 4625 (logon failures) and Event ID 4740 (account lockouts), and confirm SYSVOL share accessibility and DNS zone health before declaring a DC healthy.

**Daily checks:**

- `repadmin /replsummary` — replication health across all DCs
- `dcdiag /test:replications` — per-DC replication diagnostics
- Review Event IDs 4625, 4740, 4776 on all DCs
- Verify `\\domain\SYSVOL` and `\\domain\NETLOGON` are accessible
- Check DNS forward and reverse lookup zones for SOA and NS record integrity
- Confirm time synchronisation (PDC Emulator → reliable NTP source, all DCs within 5 minutes)

**Weekly checks:**

- `repadmin /showrepl` — full replication partner detail
- Review FSMO role holders with `netdom query fsmo`
- Confirm DC OS patch levels are current

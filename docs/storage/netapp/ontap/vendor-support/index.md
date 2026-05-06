# ONTAP Vendor Support

## Support Portal

[https://mysupport.netapp.com](https://mysupport.netapp.com)

- Case management, knowledge base, downloads, and compatibility tools
- Login with NetApp SSO credentials tied to your support contract serial numbers
- Active IQ / BlueXP dashboard: [https://bluexp.netapp.com](https://bluexp.netapp.com)

## AutoSupport

AutoSupport is the primary mechanism for NetApp support engineers to diagnose your system remotely. Ensure it is configured and delivering before opening a case.

```bash
# Verify AutoSupport configuration
system node autosupport show

# Test AutoSupport delivery
system node autosupport invoke -node * -type test

# Generate a support AutoSupport tied to an open case
system node autosupport invoke -node * -type all -message "case <number> - <brief description>"

# Show AutoSupport delivery history
system node autosupport history show -node * -most-recent 10
```

## Information to Collect

Before opening a case or during initial triage, collect:

| Item | Command / Source |
|---|---|
| ONTAP version and platform | `system node show -fields model,ontap-version,serial-number` |
| Cluster health summary | `cluster show`; `storage failover show` |
| Active health alerts | `system health alert show` |
| EMS event log (last 24h) | `event log show -severity error -time-range 24h` |
| AutoSupport bundle | `system node autosupport invoke -node * -type all -message "case <number>"` |
| Aggregate and volume status | `storage aggregate show`; `volume show -fields used-percent` |
| SnapMirror relationship health | `snapmirror show -fields lag-time,healthy,relationship-status` |
| Network interface status | `network interface show`; `network port show -fields health-status` |
| Storage disk broken list | `storage disk show -broken` |
| Node sysconfig | `system node run -node <node> sysconfig -a` |

For performance issues, also collect:
```bash
# QoS statistics
qos statistics performance show

# Network interface statistics
network interface statistics show

# Disk latency histogram (node shell)
system node run -node <node> sysstat -c 5 -x 2
```

## SLA Tiers — NetApp SupportEdge

| Priority | Response Time | Criteria |
|---|---|---|
| P1 — Critical | 1 hour | Production system down; no workaround; data at risk |
| P2 — High | 2 hours | Significant degradation; workaround exists but impractical |
| P3 — Medium | 4 hours | Partial degradation; workaround available; non-urgent issues |
| P4 — Low | Next business day | General questions, planning, non-impacting issues |

SLA clock starts from case creation and first engineer acknowledgment. For P1, call the NetApp support line directly after opening the case online to ensure immediate pickup — do not rely on the web portal alone for critical cases.

**NetApp support phone (US/Global)**: +1-888-463-8277 (SupportEdge 24×7 required for P1/P2 after-hours)

## Escalation Path

1. **Initial case**: Open via [mysupport.netapp.com](https://mysupport.netapp.com) or phone; assigned to a Technical Support Engineer (TSE)
2. **Escalation to specialist**: TSE escalates to a product specialist or escalation engineer if the issue requires deeper expertise — typically within the same business day for P1/P2
3. **Duty Manager escalation**: If response is inadequate, request escalation to the Support Duty Manager via the support portal or phone; state the case number and the escalation reason
4. **Account team escalation**: Engage your NetApp Account Manager and Systems Engineer for persistent P1 issues, commercial disputes, or SLA breach claims
5. **Executive escalation**: NetApp has a formal executive escalation process for critical accounts — initiated by your Account Manager

When escalating, always reference:
- Case number
- System serial number(s)
- Business impact (applications affected, data at risk, revenue impact)
- Timeline of events and actions already taken

---
tags:
  - troubleshooting
  - iscsi
  - networking
  - known-issues
---
# iSCSI — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known iSCSI issues covering initiator discovery, session stability, multipath, and CHAP authentication.

*Applies to: Linux open-iscsi, Windows iSCSI initiator, VMware iSCSI*
</div>

```text
┌──────────────────────────────────────────────── iSCSI ────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Block storage over TCP/IP — discovery, sessions, CHAP, multipath               │   │
│   │                                  Protocols: iSCSI (TCP 3260)                                  │   │
│   │              Management: iscsiadm (Linux) / iSCSI Initiator (Windows) / array UI              │   │
│   │              Discovery -> Login (CHAP) -> Session established -> LUN -> Multipath             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Initiator          │  │      SW/HW iSCSI client     │  │         IQN identity        │   │
│   │            Target           │  │      Array iSCSI portal     │  │        1+ portal IPs        │   │
│   │             Auth            │  │             CHAP            │  │    Optional, recommended    │   │
│   │           Session           │  │        iSCSI session        │  │     1+ TCP conn per path    │   │
│   │          Multipath          │  │      DM-multipath/MPIO      │  │    Required for HA paths    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    Initiator     │Host iSCSI client │      TCP 3260     │   CHAP (opt.)    │    iqn naming    │   │
│   │  Target portal   │  Array endpoint  │      TCP 3260     │   CHAP (opt.)    │ Multi-IP for HA  │   │
│   │    Discovery     │   Find targets   │      TCP 3260     │       N/A        │iscsiadm discovery│   │
│   │    Multipath     │ Path aggregation │        N/A        │       N/A        │multipathd service│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: host NICs/iSCSI HBAs - IP network - array iSCSI portal ports                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IQN            = iSCSI Qualified Name; unique initiator/target ID                                    │
│  Portal         = an IP:port pair where a target listens                                              │
│  CHAP           = Challenge Handshake Auth Protocol for iSCSI sessions                                │
│  Session        = logical connection, 1+ TCP conns, between init/target                               │
│  Multipath      = aggregating paths to a LUN for redundancy/perf                                      │
│  node.startup   = iscsiadm setting controlling auto-login at boot                                     │
│  Jumbo frames   = MTU 9000; reduces overhead for iSCSI throughput                                     │
│  Discovery session = temp session used to enumerate available targets                                 │
│  Keepalive timeout = how long before a stalled session is dead                                        │
│  multipathd     = Linux daemon managing device-mapper multipath                                       │
│  Failback       = returning I/O to the preferred path after recovery                                  │
│  iface binding  = associating a specific NIC with an iSCSI session                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Linux iSCSI: `iscsiadm -m session` for active sessions; `/var/log/syslog` or `dmesg` for errors.
- Windows: iSCSI Initiator Properties → Sessions tab.
- Multipath must be configured before multiple paths are visible — a single-path iSCSI setup is not redundant.

## Discovery and Login

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| `iscsiadm -m discovery` returns nothing | Target portal unreachable; TCP 3260 blocked | Verify TCP 3260 from initiator to target IP; check iSCSI portal on array |
| `Login failed: authentication failure` | CHAP credentials mismatch | Verify CHAP username/password on initiator matches array CHAP configuration |
| Session logs out intermittently | Network instability or iSCSI keepalive timeout | Increase `node.session.timeo.replacement_timeout`; check network for packet loss |

## Multipath

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Only one path visible despite two target IPs | Initiator only discovering one portal | Configure discovery for both target IPs; verify `node.startup = automatic` for both |
| Device mapper multipath showing `failed faulty running` | Path failure; multipath detected I/O error | Check physical connectivity; run `multipath -ll` to verify path state; `multipath -r` to reload |
| iSCSI device shown twice with no multipath | Multipath daemon not running or not configured | Start multipath: `systemctl start multipathd`; configure `multipath.conf` |

## Performance

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| High latency on iSCSI LUN | Network congestion; Jumbo Frames not configured | Enable Jumbo Frames (MTU 9000) end-to-end; verify with `ping -s 8972 -M do <target>` |

## See also


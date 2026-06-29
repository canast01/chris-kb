---
tags:
  - networking
---
# iSCSI — Sessions

```text
Each session can carry multiple connections (TCP streams) for performance.

## Session Lifecycle

```

```d2
direction: right

A: "Discovery" {shape: rectangle}
B: "Login" {shape: rectangle}
C: "Session Active" {shape: rectangle}
D: "D" {shape: rectangle}
E: "Session Closed" {shape: rectangle}
F: "Session Recovery" {shape: rectangle}

A -> B
B -> C
D -> C
D -> E
C -> F
F -> C
```

## Session Establishment and Multipath Data Flow

The sequence below covers the full path from initial iSCSI discovery through SendTargets negotiation, session login, and MPIO/DM-Multipath path selection for active I/O.

```mermaid
sequenceDiagram
    autonumber
    participant INI as Initiator<br/>(Linux / Windows / ESXi)
    participant ISW as IP Network<br/>(Storage VLAN)
    participant TGT as iSCSI Target<br/>(Portal :3260)
    participant MPIO as MPIO Layer<br/>(dm-multipath / NMP)

    Note over INI,TGT: Phase 1 — Discovery (SendTargets)
    INI->>ISW: TCP SYN → Target IP:3260 (discovery session)
    ISW-->>INI: TCP SYN-ACK
    INI->>TGT: iSCSI Login Request (discovery session type)
    TGT-->>INI: Login Response (Auth negotiation if CHAP configured)
    INI->>TGT: SendTargets (text request)
    TGT-->>INI: SendTargets response (IQN list + portal group addresses)
    INI->>TGT: Logout (discovery session closed)
    Note over INI: Initiator now knows target IQNs and all portal IPs

    Note over INI,TGT: Phase 2 — Normal Session Login (per path)
    INI->>ISW: TCP SYN → Portal A IP:3260  (path 1 — NIC0)
    ISW-->>INI: TCP SYN-ACK
    INI->>TGT: Login Request (operational session, ISID, CmdSN=0)
    TGT-->>INI: Login Response — negotiate MaxRecvDataSegmentLength, ImmediateData, HeaderDigest
    INI->>TGT: Login Request (final — transition to Full Feature Phase)
    TGT-->>INI: Login Response (StatSN, TSIH assigned — session handle)
    Note over INI,TGT: Session 1 active on path 1 (NIC0 → Portal A)

    INI->>ISW: TCP SYN → Portal B IP:3260  (path 2 — NIC1)
    ISW-->>INI: TCP SYN-ACK
    INI->>TGT: Login Request (same ISID, new connection CID)
    TGT-->>INI: Login Response (TSIH matches — MCS connection added to session)
    Note over INI,TGT: Session 1 now has 2 TCP connections (MCS)<br/>OR Session 2 established independently for MPIO

    Note over INI,MPIO: Phase 3 — MPIO Path Registration
    INI->>MPIO: Register block device sdb (path 1 — Portal A)
    INI->>MPIO: Register block device sdc (path 2 — Portal B)
    MPIO->>MPIO: ALUA query (Report Target Port Groups) → identify Active-Optimized vs Active-Non-Optimized
    MPIO-->>INI: Expose single multipath device /dev/mapper/mpatha

    Note over INI,MPIO: Phase 4 — I/O Path Selection
    INI->>MPIO: Write 512KB to /dev/mapper/mpatha
    MPIO->>MPIO: Path selector (Round Robin / Service-Time / Least-Queue)
    MPIO->>TGT: iSCSI SCSI Command PDU via active path (e.g. sdb — Portal A)
    TGT-->>MPIO: iSCSI SCSI Response PDU (status 0x00 — success)
    Note over MPIO: On path failure: MPIO marks path down,<br/>retries on remaining active path within error recovery window
```

| Phase | Protocol | Key Negotiation | Outcome |
|---|---|---|---|
| Discovery | iSCSI text (SendTargets) | None (or CHAP) | IQN list + portal group IPs returned |
| Session login | iSCSI Login PDU sequence | MaxRecvDataSegmentLength, ImmediateData, digest | TSIH (session handle) assigned |
| MCS / MPIO | TCP + iSCSI | Additional CID on same TSIH (MCS) or separate sessions | Multiple TCP paths to same target |
| ALUA | SCSI RTPG (Report Target Port Groups) | Active-Optimized vs Standby port group | MPIO prefers optimized path |
| Path failover | dm-multipath / NMP | Failover timeout, path checker (tur / readsector0) | I/O retried on next available path |
```bash
## List all active sessions (brief)
iscsiadm -m session

## Detailed session info (connections, state, target IQN)
iscsiadm -m session -P 3

## Show session parameters (timeouts, queue depth)
iscsiadm -m session -P 3 | grep -E "Target|State|Recovery|Queue"

## Session stats (bytes tx/rx, retries)
iscsiadm -m session -s
```
```bash
## Login to all discovered targets (persistent)
iscsiadm -m node --login

## Login to a specific target
iscsiadm -m node -T <IQN> -p <ip>:3260 --login

## Make login persistent across reboots
iscsiadm -m node -T <IQN> -p <ip>:3260 -o update -n node.startup -v automatic

## Logout from a target
iscsiadm -m node -T <IQN> -p <ip>:3260 --logout

## Logout all sessions
iscsiadm -m node --logoutall=all
```
```bash
## /etc/iscsi/iscsid.conf
node.session.nr_sessions = 2

## Or per-node override
iscsiadm -m node -T <IQN> -p <ip> -o update -n node.session.nr_sessions -v 2
```
```bash
## Check session state during recovery
iscsiadm -m session -P 3 | grep -i state

## Force session re-establishment
iscsiadm -m node -T <IQN> -p <ip>:3260 --logout
iscsiadm -m node -T <IQN> -p <ip>:3260 --login
```

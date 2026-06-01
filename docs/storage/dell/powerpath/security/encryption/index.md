# PowerPath — Encryption


<div class="kb-summary">
Encryption reference covering Overview, Encryption Responsibility Matrix.
</div>

```
┌──────────────────────────────── Dell PowerPath Security — Encryption ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    PowerPath is transparent to data encryption; DARE operates at array drive layer below it   │   │
│   │   FC transport: no native data encryption; rely on FC-SP or fabric-level encryption SAN ISL   │   │
│   │     iSCSI transport: CHAP for authentication; IPSec for data-in-flight encryption per hop     │   │
│   │     PowerPath does not inspect or modify data; encryption/decryption at host HBA or array     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host I/O → PowerPath load-balances path → FC/iSCSI transport → array decrypts at DARE layer        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         FC Transport        │  │       iSCSI Transport       │  │       Array Encryption      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       FC-SP (optional)      │  │          CHAP auth          │  │        DARE at drives       │   │
│   │        ISL encryption       │  │         IPSec tunnel        │  │       KMIP key server       │   │
│   │        VSAN isolation       │  │           TLS iSNS          │  │       Transparent pass      │   │
│   │       Zoning boundary       │  │         Mutual CHAP         │  │         Key rotation        │   │
│   │        No PP inspect        │  │        No PP inspect        │  │         Crypto erase        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Enable iSCSI CHAP or IPSec at transport layer; DARE configured at array; PowerPath unaffected      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │      Layer       │    Transport     │     Mechanism     │ Config location  │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Data at rest   │    FC / iSCSI    │    DARE (array)   │    Array GUI     │ Below PowerPath  │   │
│   │       Auth       │      iSCSI       │    CHAP secret    │ iSCSI initiator  │   Mutual CHAP    │   │
│   │    In-flight     │      iSCSI       │     IPSec ESP     │   OS / network   │  Per-hop config  │   │
│   │     FC link      │        FC        │  FC-SP / ISL enc  │    SAN switch    │     Optional     │   │
│                                                                                                       │
│    Physical: FC-SP on HBA and switch; IPSec on iSCSI NIC/NIC driver; DARE on array drive bays         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DARE           = Data At Rest Encryption; array-side SED encryption; transparent to PowerPath      │
│    FC-SP          = Fibre Channel Security Protocol; DH-CHAP authentication on FC links               │
│    ISL encryption = In-flight encryption between fabric switches; configured at SAN switch level      │
│    CHAP           = Challenge Handshake Authentication Protocol; iSCSI initiator/target auth          │
│    Mutual CHAP    = Both initiator and target authenticate each other; stronger than one-way          │
│    IPSec ESP      = Encapsulating Security Payload; encrypts iSCSI packets in-flight                  │
│    iSNS TLS       = iSCSI Name Service secured with TLS; optional discovery plane protection          │
│    Transparent pass= PowerPath passes I/O bytes unchanged; does not encrypt or decrypt data           │
│    KMIP key server= External key manager for DARE; unreachable KMIP can lock array volumes            │
│    Crypto erase   = Destroy DARE encryption key on decommission; all data permanently unreadable      │
│    VSAN isolation = FC VSAN separates storage traffic; limits blast radius of any breach              │
│    Zoning boundary= FC zone restricts which HWWNs can communicate; primary FC security control        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

PowerPath operates at the block I/O layer and does not encrypt data in transit between the host and array. Encryption at this layer is handled by:

- **Array-side encryption**: PowerMax, Unity, and PowerStore provide AES-256 encryption at rest on the array; PowerPath is transparent to this
- **Host-side encryption**: Use OS-level encryption (dm-crypt/LUKS on Linux, BitLocker on Windows) on top of the PowerPath pseudo device if host-side encryption is required
- **FC fabric encryption**: Some FC switch vendors (Brocade, Cisco MDS) offer in-flight FC frame encryption; PowerPath is transparent to this

## Encryption Responsibility Matrix

| Encryption Scope | Technology | PowerPath Role |
|---|---|---|
| Data at rest on array | AES-256 (PowerMax/Unity/PowerStore) | Transparent — PowerPath passes I/O through |
| Data in transit (FC fabric) | FC frame encryption (Brocade/Cisco MDS) | Transparent — PowerPath operates above this layer |
| Host-side data at rest | dm-crypt/LUKS (Linux), BitLocker (Windows) | Applied on top of PowerPath pseudo device |
| Management plane | Host OS authentication (SSH, RDP) | Out of scope for PowerPath |

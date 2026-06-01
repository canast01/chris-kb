# MDS — Troubleshooting


<div class="kb-summary">
MDS — Troubleshooting reference.
</div>

```text
┌────────────────────────────────── Cisco MDS 9000 — Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           MDS troubleshooting: port offline, VSAN isolated, login failures, ISL flap          │   │
│   │         Port offline: check SFP Rx/Tx power, cable continuity, HBA driver, VSAN assign        │   │
│   │          VSAN isolated: domain ID conflict or ISL allowed-VSAN mismatch; check trunk          │   │
│   │          Login failure: device not in FLOGI DB; verify zone membership and VSAN port          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → show command → physical check → config verify → resolve → document                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Port Issues         │  │         VSAN / Zone         │  │          ISL Issues         │   │
│   │         Port offline        │  │        VSAN isolated        │  │           ISL down          │   │
│   │         SFP degraded        │  │       Domain conflict       │  │        Trunk mismatch       │   │
│   │          FLOGI fail         │  │         Zone lockout        │  │         Allowed VSAN        │   │
│   │         HBA mismatch        │  │        Alias missing        │  │         Port channel        │   │
│   │        Speed mismatch       │  │       Wrong active ZS       │  │         ISL overload        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always run show tech-support fc before TAC escalation; save output off-switch                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │  First command   │     Key output    │    Resolution    │    Escalation    │   │
│   │   Port offline   │ show int fc X/Y  │   State, reasons  │  SFP/cable fix   │  TAC if persist  │   │
│   │  VSAN isolated   │   show vsan X    │   State=isolated  │  Fix domain ID   │  TAC merge help  │   │
│   │    FLOGI miss    │  show flogi db   │    WWN present?   │  Fix zone/VSAN   │   TAC + sniff    │   │
│   │     ISL down     │ show int fc X/Y  │    Trunk state    │  Fix trunk mode  │   TAC if link    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SFP Tx/Rx dBm · LC cable · patch panel continuity · HBA driver and firmware              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    show int fc X/Y  = Interface state, SFP power, error counters; first command for port issues       │
│    show flogi db    = FC fabric login table; confirms which devices have joined the fabric            │
│    show vsan X      = VSAN membership and state (active/isolated); isolated = domain conflict         │
│    show zoneset act = Active zone set contents per VSAN; verify initiator/target pairs                │
│    VSAN isolated    = MDS quarantines VSAN when domain ID conflict detected on ISL                    │
│    Domain ID        = Unique numeric ID per switch per VSAN; conflict causes isolation                │
│    Trunk mismatch   = ISL port trunk mode or allowed-VSAN list differs between both ends              │
│    FLOGI            = Fabric Login; device registers WWN with Name Server when joining VSAN           │
│    SFP degraded     = Optical Rx below −14 dBm or Tx out-of-spec; replace transceiver                 │
│    HBA mismatch     = HBA driver/firmware version incompatible with FC speed or features              │
│    show tech-support fc = Full diagnostic bundle for FC; attach to TAC case before escalate           │
│    Zone lockout     = Device can FLOGI but not see storage; zone missing or wrong VSAN                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

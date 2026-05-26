# Dell Capacity on Demand

<div class="kb-summary">
Dell Capacity on Demand — software-defined capacity licensing for PowerMax and VMAX. Pre-installed drives are activated via license key with no truck roll required. Covers architecture, operations, and troubleshooting for COD lifecycle management.
</div>

```
┌──────────────────────────────────── Dell Capacity on Demand (CoD) ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CoD: pre-installed dark capacity on Dell arrays activated via license key when needed     │   │
│   │  Hardware ships fully populated; drives/nodes locked; capacity unlocked by purchasing CoD key │   │
│   │      Supported on PowerMax, VMAX, Unity XT, PowerStore, PowerScale, Data Domain platforms     │   │
│   │       Managed via Dell Licensing Portal; keys applied through array management UI or CLI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Array ships with dark capacity → purchase CoD key → apply key → capacity unlocked instantly        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          CoD Model          │  │        Array Support        │  │          Management         │   │
│   │       Pre-installed hw      │  │       PowerMax / VMAX       │  │       Licensing portal      │   │
│   │        Dark capacity        │  │           Unity XT          │  │        Array UI / CLI       │   │
│   │      License key unlock     │  │          PowerStore         │  │       CloudIQ monitor       │   │
│   │        Pay when used        │  │          PowerScale         │  │        Support portal       │   │
│   │      Instant expansion      │  │         Data Domain         │  │      Dell account team      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    No truck roll needed for expansion; drives or nodes already installed; zero downtime unlock        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │       Owner       │       Tool       │      Notes       │   │
│   │     Array hw     │  Pre-installed   │        Dell       │     Factory      │   Dark at ship   │   │
│   │     CoD key      │ Unlocks capacity │   Customer buys   │  License portal  │  Per pool/frame  │   │
│   │    Array mgr     │   Applies key    │    Storage eng.   │    GUI or CLI    │  Instant effect  │   │
│   │     CloudIQ      │  Monitors usage  │    Storage team   │   SaaS portal    │ Triggers alerts  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: drives/nodes pre-installed in array chassis; locked by firmware until key applied        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CoD            = Capacity on Demand; Dell licensing model for pre-installed dark capacity          │
│    Dark capacity  = Physically installed but software-locked storage; visible in management as locked │
│    CoD key        = License file purchased from Dell; applied to array to unlock specific capacity    │
│    Licensing portal = Dell portal at licensing.dell.com for purchasing and downloading CoD keys       │
│    Instant expansion = Capacity available within seconds of key application; no reboot required       │
│    Pay-as-you-grow = Only pay for capacity license when business need justifies expansion             │
│    Frame license  = CoD key scoped to a specific array serial number; not transferable                │
│    Pool unlock    = Specific storage pool capacity unlocked by key; other pools remain locked         │
│    CloudIQ alert  = CloudIQ notifies when used capacity approaches CoD threshold requiring next key   │
│    No truck roll  = Pre-installed hw means no engineer site visit needed for expansion                │
│    VMAX CoD       = VMAX All Flash uses CoD for engine and bay additions; applied via Unisphere       │
│    PowerMax CoD   = PowerMax uses Hypermax OS feature licensing model alongside CoD drives            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
</div>

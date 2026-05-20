# Aria Suite Lifecycle — Troubleshooting

```
┌───────────────────────────────────── Aria LCM — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Environment install failures; upgrade stall mid-way through product deployment sequence    │   │
│   │    Certificate mismatch between LCM and managed products; vIDM connectivity issues for SSO    │   │
│   │         Disk space on LCM appliance blocking upgrades; API errors for day-2 operations        │   │
│   │     Diagnostics: LCM UI request logs, /var/log/vlcm, vIDM diagnostics, REST API debug mode    │   │
│   │     Escalation: LCM support bundle export from UI; pre-check report; TAM escalation for P1    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate LCM or product layer · escalation engage│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │       Env install fail      │  │       LCM UI req logs       │  │       LCM support bndl      │   │
│   │        Upgrade stall        │  │        /var/log/vlcm        │  │        GSS case open        │   │
│   │        Cert mismatch        │  │       vIDM diagnostics      │  │        Pre-chk report       │   │
│   │         vIDM offline        │  │        REST API debug       │  │        TAM escalation       │   │
│   │          Disk space         │  │        Pre-chk output       │  │        Version matrix       │   │
│   │          API errors         │  │         Product logs        │  │          Log export         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use LCM logs and pre-check output · escalation bundles for│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   Install fail   │   LCM UI logs    │   /var/log/vlcm   │    LCM bundle    │  Retry install   │   │
│   │  Upgrade stall   │  REST API debug  │    /var/log/vra   │   GSS P1 case    │    Resume upg    │   │
│   │  Cert mismatch   │  Pre-chk output  │    /var/log/vro   │   TAM escalate   │  Re-issue cert   │   │
│   │   vIDM offline   │    vIDM diag     │   /var/log/vidm   │  Version matrix  │   Restart vIDM   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter · vIDM/Workspace ONE                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Environment installation = LCM workflow deploying Aria products into a new or existing named Environm│
│  Upgrade orchestration = LCM upgrade wizard that sequences product upgrades to maintain compatibility │
│  Certificate mismatch  = TLS cert on LCM or product does not match expected CA or SAN; causes auth fai│
│  vIDM connectivity     = LCM requires vIDM to be reachable for SSO; vIDM failure breaks all product lo│
│  Disk space threshold  = LCM appliance disk usage limit; upgrade aborts if insufficient space detected│
│  Pre-check validation  = Automated checks before install/upgrade; catches misconfig before deployment │
│  LCM support bundle    = Diagnostic archive from LCM UI; contains vlcm logs and request history for GS│
│  Day-2 operation       = Post-install LCM task such as cert rotation, password rotation, or content de│
│  API debug             = Verbose REST API logging mode in LCM; shows detailed request and response dat│
│  BOM version mismatch  = Aria products in an Environment on incompatible versions; blocks LCM upgrade │
│  TAM escalation        = Escalation to Technical Account Manager for critical LCM P1 upgrade or instal│
│  Product log collection = Gathering logs from individual Aria products (vRA/vROps/vRLI) to diagnose fa│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>

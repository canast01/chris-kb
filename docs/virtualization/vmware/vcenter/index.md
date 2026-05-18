# vCenter

<div class="kb-summary">
Technical and operational reference for VMware vCenter Server (VCSA). Covers architecture, cluster management, lifecycle, security, and troubleshooting for the vSphere management plane.
</div>

```
vCenter in the VMware Stack
════════════════════════════════════════════════════════

  Consumers
  ┌─────────────┐   ┌──────────────┐   ┌────────────────┐
  │ vSphere     │   │  PowerCLI /  │   │  Aria Ops /    │
  │ Client (UI) │   │  REST API    │   │  3rd-party     │
  └──────┬──────┘   └──────┬───────┘   └───────┬────────┘
         │                 │                   │
         └─────────────────┼───────────────────┘
                           │ HTTPS :443
                    ┌──────▼───────┐
                    │  vCenter     │  ← management plane
                    │  Server      │    (VCSA / Photon OS)
                    │  (VCSA)      │
                    └──────┬───────┘
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼───────┐
   │  ESXi-01    │  │  ESXi-02    │  │  ESXi-03    │
   │  (compute)  │  │  (compute)  │  │  (compute)  │
   └──────┬──────┘  └──────┬──────┘  └─────┬───────┘
          └────────────────┼────────────────┘
                    ┌──────▼───────┐
                    │  Shared      │
                    │  Storage /   │
                    │  vSAN / NFS  │
                    └──────────────┘

  Integrations (registered to vCenter)
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │   NSX    │  │  vSAN    │  │  Aria    │  │  Backup  │
  │ Manager  │  │ (built-  │  │  Suite   │  │  (VADP)  │
  │          │  │  in)     │  │          │  │          │
  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>

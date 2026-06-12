# PowerCLI — Architecture

<div class="kb-summary">
PowerCLI module architecture, vSphere API connectivity model, credential management, and integration with vCenter, ESXi, NSX, and vSAN.
</div>

![PowerCLI Architecture Overview](../../../../assets/powercli-architecture-overview.svg)

```text
┌─────────────────────────────────── PowerCLI — Module Architecture ────────────────────────────────────┐
│                                                                                                       │
│   PowerCLI is a set of PowerShell modules that wrap the vSphere REST and SOAP APIs                    │
│   Each VMware product has its own sub-module; VMware.PowerCLI is the meta-package                     │
│   Sessions are per-connection; multiple vCenter connections are supported simultaneously              │
│                                                                                                       │
│   Module structure                                                                                    │
│   VMware.PowerCLI = meta-package that installs all sub-modules in one command                         │
│   VMware.VimAutomation.Core = vCenter/ESXi cmdlets (VMs, hosts, clusters, storage, networking)        │
│   VMware.VimAutomation.Vds = Distributed Switch cmdlets                                               │
│   VMware.VimAutomation.Storage = vSAN, SPBM, and storage policy cmdlets                               │
│   VMware.VimAutomation.Nsxt = NSX-T Manager cmdlets (separate Connect-NsxtServer required)            │
│   VMware.VimAutomation.Sdk = base SDK shared by all modules; not used directly                        │
│                                                                                                       │
│   Connection model                                                                                    │
│   Connect-VIServer: authenticates to vCenter or directly to ESXi; returns a VIServer object           │
│   Multiple connections: use -Server parameter to target specific vCenter on each cmdlet               │
│   $global:DefaultVIServers: array of active connections; used when -Server is omitted                 │
│   Credential store: Store-VICredentialStoreItem saves encrypted credentials for scripts               │
│                                                                                                       │
│   Key terms:                                                                                          │
│   VIM     = vSphere Infrastructure Management; the SOAP API layer that PowerCLI wraps                 │
│   VI object = any vSphere managed entity returned by Get- cmdlets (VM, VMHost, Datastore)             │
│   $_ (pipeline) = current object in the pipeline; used with ForEach-Object or Where-Object            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Module structure, connection model, session handling, and vSphere API binding.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Multi-product support: NSX, vSAN, vCD, HCX, Site Recovery Manager, and vROps.</span>
</a>

</div>

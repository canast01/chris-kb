# Azure

<div class="kb-summary">
Microsoft Azure knowledge base covering compute, storage, networking, identity, monitoring, backup, security, governance, and cost management. Includes architecture references, operational procedures, CLI commands, and troubleshooting guides.
</div>

```
┌─────────────────────────────────────────────────────────┐
│                Azure Service Hierarchy                  │
│                                                         │
│  Tenant (Entra ID)                                      │
│  └── Management Groups (policy + RBAC inheritance)      │
│       └── Subscription (billing + quota boundary)       │
│            └── Resource Group (lifecycle boundary)      │
│                 └── Resources                           │
│                      ├── VMs · VMSS · AKS               │
│                      ├── VNet · Subnets · NSG            │
│                      ├── Storage Accounts · Disks        │
│                      └── Key Vault · Entra ID roles      │
└─────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Overview, components, integrations, and standards.</span>
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

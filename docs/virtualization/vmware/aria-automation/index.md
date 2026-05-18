# Aria Automation

<div class="kb-summary">
Technical and operational reference for VMware Aria Automation. Covers infrastructure automation, service catalogue, blueprint design, deployment management, and IaC pipeline integration across the vSphere and cloud platforms.
</div>

```
┌─────────────────────────────────────────────────────────────┐
│              Aria Automation — Platform Flow                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User / CI-CD Pipeline                                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Service Catalog / Portal  (VIDM SSO)                │   │
│  │  Request item → approval policy → approved           │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Blueprint / Cloud Template                          │   │
│  │  YAML → resources: VM + network + storage            │   │
│  │  Constraints: project scope, cloud zone tags         │   │
│  └───────────────┬──────────────────┬───────────────────┘   │
│                  │                  │                       │
│                  ▼                  ▼                       │
│  ┌───────────────────┐  ┌────────────────────────────────┐  │
│  │  vCenter / vSphere│  │  NSX: segment / security group │  │
│  │  VM provisioned   │  │  provisioned alongside VM      │  │
│  └───────────────────┘  └────────────────────────────────┘  │
│                                                             │
│  ABX actions / vRO workflows fire on provisioning events    │
└─────────────────────────────────────────────────────────────┘
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

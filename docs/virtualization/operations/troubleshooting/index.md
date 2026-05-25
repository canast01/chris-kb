# Virtualization Troubleshooting

```text
┌─────────────────────────────────────────────────────────────────┐
│          VIRTUALIZATION TROUBLESHOOTING DECISION TREE           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Symptom?   │
                    └──────┬──────┘
          ┌────────────────┼─────────────────────┐
          ▼                ▼                     ▼
   ┌─────────────┐  ┌─────────────┐     ┌─────────────┐
   │  VM Slow /  │  │ Host Down / │     │ Storage /   │
   │  No Power   │  │ Disconnected│     │ Datastore   │
   └──────┬──────┘  └──────┬──────┘     └──────┬──────┘
          ▼                ▼                   ▼ 
   ┌─────────────┐  ┌─────────────┐     ┌─────────────┐
   │ CPU/Mem/Disk│  │ Ping ► SSH  │     │ Path state  │
   │ Perf triage │  │ vpxa/hostd  │     │ APD/PDL/full│
   └──────┬──────┘  └──────┬──────┘     └──────┬──────┘
          │                │                    │
          └────────────────┴──────────┬─────────┘
                    ┌─────────────────▼──────────────────┐
                    │  Network │ Certificate │ Login/Auth │
                    │  NIC/PG  │  Expiry     │  SSO/AD    │
                    └─────────────────┬──────────────────┘
                                      ▼
                          ┌───────────────────────┐
                          │  Unresolved ► Escalate │
                          │  Dell / VMware Support │
                          └───────────────────────┘
```

Common virtualization troubleshooting workflows.

## Troubleshooting Flow

Start by defining the scope, then work down through the stack.

1. **Define scope** — one VM, one host, one cluster, or full vCenter outage?
2. **Check vCenter health** — can you log in? Are services running? Any critical alarms?
3. **Check host health** — are all hosts connected? Any in warning or not responding?
4. **Check storage and vSAN** — are datastores accessible? Is vSAN Skyline Health green?
5. **Check network** — are VM and management networks reachable? Any vMotion failures?
6. **Review recent tasks and events** — what changed in the last 24 hours?
7. **Check logs** — hostd, vpxa, vmkernel, vCenter events, Aria for Logs
8. **Escalate** — open a Dell or VMware support case if the root cause is unclear

<div class="kb-grid kb-grid-7">

<a class="kb-card" href="vm-performance-issue/">
  <strong>VM Performance Issue</strong>
  <span>First-pass workflow for CPU, memory, storage, and network symptoms.</span>
</a>

<a class="kb-card" href="host-disconnected/">
  <strong>Host Disconnected</strong>
  <span>Workflow for disconnected or not responding ESXi hosts.</span>
</a>

<a class="kb-card" href="datastore-inaccessible/">
  <strong>Datastore Inaccessible</strong>
  <span>Troubleshooting VMFS, NFS, vSAN, and storage visibility issues.</span>
</a>

<a class="kb-card" href="network-connectivity-issue/">
  <strong>Network Connectivity Issue</strong>
  <span>VM, host, VLAN, distributed switch, and NSX connectivity checks.</span>
</a>

<a class="kb-card" href="certificate-issue/">
  <strong>Certificate Issue</strong>
  <span>vCenter, NSX, VxRail, and Aria certificate symptoms and workflow.</span>
</a>

<a class="kb-card" href="login-access-issue/">
  <strong>Login or Access Issue</strong>
  <span>SSO, LDAP, AD, permissions, MFA, and local account checks.</span>
</a>


<a class="kb-card" href="known-issues/">
  <strong>Known Issues</strong>
  <span>Known issues and workarounds.</span>
</a>
</div>

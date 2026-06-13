---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# Virtualization Troubleshooting


<div class="kb-summary">
Common virtualization troubleshooting workflows.
</div>
```text
┌───────────────────── Virtualization Operations Troubleshooting — Troubleshooting ─────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Operations troubleshooting: structured diagnostic process for common issues          │   │
│   │         Start with health dashboard, then check recent changes, then review event logs        │   │
│   │        Collect support bundle before contacting vendor support to accelerate resolution       │   │
│   │         Escalation matrix: L1 → L2 → vendor support based on severity and SLA targets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check health → review changes → examine logs → diagnose → resolve                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Operations Troubleshooting infrastructure · management network · monitor  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Operations         = Virtualization Operations Troubleshooting platform overview and core concept  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

## Symptom Index

| Symptom | Component | First steps |
|---|---|---|
| Host disconnected in vCenter | ESXi | Check host DCUI; ping host IP; `vim-cmd hostsvc/hostsummary` |
| VMs powered off unexpectedly | ESXi / HA | Check HA event log; check host hardware faults |
| vSAN health red | vSAN | vCenter → vSAN → Skyline Health; `esxcli vsan health cluster` |
| vSAN disk offline | vSAN | Check disk group health; check disk hardware errors |
| Horizon connection failure | Horizon | Check Connection Server health; check Composer; test blast/pcoip ports |
| Tanzu cluster not ready | Tanzu | `kubectl get nodes`; check Supervisor cluster VMs |
| VxRail upgrade stuck | VxRail | VxRail Manager → Upgrade History; check bundle download |
| SRM recovery plan failed | SRM | Check SRM event log; verify VRMS connectivity |

## ESXi Host Diagnostics

```bash
# From ESXi SSH:
esxcli system stats uptime        # uptime in seconds
esxcli hardware ipmi sel list     # IPMI hardware events
vim-cmd vmsvc/getallvms           # list all VMs and states
esxcli storage core path list | grep -v Active   # check for dead paths
esxcli network ip connection list | grep ESTABLISHED  # active connections
```

## vSAN Health Check

```bash
# Via ESXi SSH:
esxcli vsan health cluster list
esxcli vsan debug disk list
esxcli vsan cluster get    # cluster UUID and node count

# Via DCLI / RVC (legacy):
rvc user@vcenter -c "vsan.health.health_summary /<dc>/computers/<cluster>"
```

## Horizon Connection Diagnosis

```text
1. Check Connection Server health: https://cs01.corp.local/broker/xml
2. Check event log in Horizon Admin console
3. Verify pool composition (desktops powered on)
4. Test blast: nc -zv <connection-server> 8443
5. Test PCoIP: nc -zv <connection-server> 4172/udp
6. Check Horizon Composer service (if instant clone pool)
```

## Tanzu / Kubernetes Troubleshooting

```bash
kubectl get nodes -o wide                          # node health
kubectl get pods -A | grep -v Running | grep -v Completed   # problem pods
kubectl describe pod <pod> -n <ns>                 # pod events
kubectl logs <pod> -n <ns> --previous             # previous container logs
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -20
```

## VxRail Troubleshooting

```bash
# Collect support bundle
/usr/lib/vmware-marvin/marvind.py collect_support_bundle

# VxRail Manager service status
systemctl status vmware-marvin

# Check VxRail log
tail -100 /var/log/vmware/vmware-vxrail-manager.log
```

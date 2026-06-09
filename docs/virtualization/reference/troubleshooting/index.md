# Virtualization — Troubleshooting

<div class="kb-summary">
Virtualization troubleshooting — vSphere host failures, vSAN issues, Horizon connection failures, Tanzu cluster problems, VxRail update errors, and SRM replication issues.
</div>

<div class="kb-grid kb-grid-1">
<a class="kb-card" href="vm-performance/"><strong>VM Performance</strong><span>CPU ready, memory balloon, storage latency, and network drop diagnosis for VMs.</span></a>
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

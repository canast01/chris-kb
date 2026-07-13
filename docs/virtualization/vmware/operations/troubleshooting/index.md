---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
description: "Virtualization troubleshooting: VM power-on failures, network port-group misconfiguration, storage access loss, HA admission control issues, and..."
---
# Virtualization Troubleshooting

<div class="kb-summary">
Virtualization troubleshooting: VM power-on failures, network port-group misconfiguration, storage access loss, HA admission control issues, and escalation workflows.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
troubleshooting_flow: "Troubleshooting Flow" {shape: rectangle}
symptom_index: "Symptom Index" {shape: rectangle}
esxi_host_diagnostics: "ESXi Host Diagnostics" {shape: rectangle}
vsan_health_check: "vSAN Health Check" {shape: rectangle}
horizon_connection_diagnosis: "Horizon Connection Diagnosis" {shape: rectangle}
tanzu_kubernetes_troubleshooting: "Tanzu / Kubernetes Troubleshooting" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> troubleshooting_flow: investigate
symptom -> symptom_index: investigate
symptom -> esxi_host_diagnostics: investigate
symptom -> vsan_health_check: investigate
symptom -> horizon_connection_diagnosis: investigate
symptom -> tanzu_kubernetes_troubleshooting: investigate
troubleshooting_flow -> resolution
symptom_index -> resolution
esxi_host_diagnostics -> resolution
vsan_health_check -> resolution
horizon_connection_diagnosis -> resolution
tanzu_kubernetes_troubleshooting -> resolution
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


```text title="Expected output"
Uptime: 86400 seconds

EventID | Timestamp           | Severity | Message
--------|---------------------|----------|------------------------------------------
1       | 2024-01-15 14:23:45 | Warning  | Temperature threshold exceeded
2       | 2024-01-15 13:12:10 | Info     | Power supply redundancy lost
3       | 2024-01-15 12:05:33 | Critical | Fan speed below threshold

Vmid Name                                   File
---- ---------------------------------------- -----
1    prod-web-01                            [datastore1] prod-web-01/prod-web-01.vmx
2    prod-db-02                             [datastore2] prod-db-02/prod-db-02.vmx
3    dev-test-vm                            [datastore1] dev-test-vm/dev-test-vm.vmx

Path: vmhba2:C0:T5:L0
State: Dead
Adapter: vmhba2
Target: 5
LUN: 0

Proto Recv-Q Send-Q Local-Address           Foreign-Address         State
----- ------ ------ ----------------------- ----------------------- -----------
tcp   0      0      192.168.1.45:22         10.50.100.12:54321      ESTABLISHED
tcp   0      0      192.168.1.45:443        10.50.100.15:49876      ESTABLISHED
tcp   0      0      192.168.1.45:902        10.50.100.20:38765      ESTABLISHED
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vim-cmd: command not found` | Verify the ESXi host is in maintenance mode or use the vSphere Client API instead; vim-cmd requires the host's management services to be fully operational. |
    | `Permission denied` | Run commands with root privileges or ensure your SSH user account has administrative rights on the ESXi host. |
    | `IPMI sel list: Unknown command` | Confirm IPMI is enabled in the host's BIOS and the management controller is accessible via `esxcli hardware ipmi sel info` first. |
**Expected output:** `storage core path list | grep -v Active` returns no output (all paths active). `hardware ipmi sel list` returns no critical hardware events. IPMI critical events require hardware replacement ticket.

## vSAN Health Check

```bash
# Via ESXi SSH:
esxcli vsan health cluster list
esxcli vsan debug disk list
esxcli vsan cluster get    # cluster UUID and node count

# Via DCLI / RVC (legacy):
rvc user@vcenter -c "vsan.health.health_summary /<dc>/computers/<cluster>"
```


```text title="Expected output"
Cluster UUID: 522e4dce-1234-5678-abcd-ef1234567890
Cluster Health: Healthy
Node Count: 4
Disk Groups: 3

Name                          Health Status
----                          ------
vsan-cluster-01               Healthy
vsan-cluster-02               Healthy
vsan-cluster-03               Healthy
vsan-cluster-04               Healthy

Disk Name       Capacity      Used          Health
---------       --------      ----          ------
naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m  1.6TB  892GB  Healthy
naa.6001405a9z8y7x6w5v4u3t2s1r0q9p8o7  1.6TB  756GB  Healthy
naa.6001405a1a2b3c4d5e6f7g8h9i0j1k2l3  1.6TB  1.2TB  Healthy
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vsan health cluster list: Unknown command or namespace` | Verify VSAN is licensed and enabled on the cluster; run `esxcli vsan cluster get` first to confirm VSAN is initialized. |
    | `Error: Unable to connect to host <hostname>: Connection refused` | Ensure SSH is enabled on the ESXi host and you have network connectivity; check firewall rules with `esxcli network firewall get`. |
    | `RVC Error: Connection refused or timeout connecting to vCenter` | Verify vCenter hostname/IP is correct, credentials are valid, and vCenter service is running with `systemctl status vpxd` on the vCenter appliance. |
**Expected output:** `vsan health cluster list` shows all checks as `green`. `vsan cluster get` confirms node count matches expected cluster size. Any `yellow` or `red` check requires investigation before any scheduled maintenance.

## Horizon Connection Diagnosis

```text title="Diagnosis steps"
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


```text title="Expected output"
NAME                    STATUS   ROLES           AGE    VERSION            INTERNAL-IP      EXTERNAL-IP   OS-IMAGE
esx-k8s-master-01       Ready    control-plane   45d    v1.28.2            10.42.10.15      <none>        VMware Photon OS/Linux
esx-k8s-worker-01       Ready    worker          45d    v1.28.2            10.42.10.16      <none>        VMware Photon OS/Linux
esx-k8s-worker-02       Ready    worker          44d    v1.28.2            10.42.10.17      <none>        VMware Photon OS/Linux
esx-k8s-worker-03       NotReady worker          2d     v1.28.2            10.42.10.18      <none>        VMware Photon OS/Linux

NAMESPACE     NAME                              READY   STATUS             RESTARTS   AGE
kube-system   coredns-5d78c0854d-7x9kl          0/1     CrashLoopBackOff   12         3h22m
monitoring    prometheus-operator-6f4d8c2b9     0/1     ImagePullBackOff   0          1h45m
default       nginx-deployment-7d4f8b6c2-q2r8t  0/2     Pending            0          2h10m
kube-system   etcd-backup-job-27481             0/1     Error              5          45m

Name:         nginx-deployment-7d4f8b6c2-q2r8t
Namespace:    default
Events:
  Type     Reason            Age   Message
  ----     ------            ---   -------
  Warning  FailedScheduling  2h    0/3 nodes available: 1 NotReady, 2 insufficient resources
  Warning  FailedScheduling  1h    0/3 nodes available: 1 NotReady, 2 insufficient resources

(no output — command completes silently)

LAST SEEN              TYPE      REASON                    OBJECT                                MESSAGE
2024-01-15T14:32:10Z   Warning   FailedScheduling         pod/nginx-deployment-7d4f8b6c2-q2r8t  0/3 nodes available
2024-01-15T14:28:45Z   Warning   BackOff                  pod/coredns-5d78c0854d-7x9kl          Back-off restarting failed container
2024-01-15T14:15:22Z   Warning   ImagePullBackOff         pod/prometheus-operator-6f4d8c2b9     Failed to pull image "prometheus:v2.41.0"
2024-01-15T13:50:18Z   Normal    NodeNotReady             node/esx-k8s-worker-03                Node esx-k8s-worker-03 status is now: NotReady
2024-01-15T13:48:02Z   Normal    NodeStatusUpdate         node/esx-k8s-worker-03                Kubelet stopped posting node status.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "pods"` | Verify the cluster context with |
## VxRail Troubleshooting

```bash
# Collect support bundle
/usr/lib/vmware-marvin/marvind.py collect_support_bundle

# VxRail Manager service status
systemctl status vmware-marvin

# Check VxRail log
tail -100 /var/log/vmware/vmware-vxrail-manager.log
```


```text title="Expected output"
Collecting support bundle...
Support bundle collection started with ID: sb-20240115-a7f3k9m2
Estimated time: 2-3 minutes
Bundle will be saved to: /var/log/vmware/support-bundles/

● vmware-marvin.service - VMware VxRail Manager
     Loaded: loaded (/etc/systemd/system/vmware-marvin.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
   Main PID: 4521 (marvind.py)
      Tasks: 12 (limit: 4915)
     Memory: 487.3M
     CGroup: /system.slice/vmware-marvin.service
             └─4521 /usr/bin/python3 /usr/lib/vmware-marvin/marvind.py

2024-01-15 14:45:22.891 [INFO] VxRail Manager initialized successfully
2024-01-15 14:45:23.104 [INFO] Connected to vCenter: vc-prod-01.corp.local
2024-01-15 14:45:24.567 [INFO] Cluster health check: HEALTHY
2024-01-15 14:45:25.234 [INFO] Storage capacity: 89.2% utilized
2024-01-15 14:45:26.891 [WARN] Node esx-node-04 CPU temp: 78°C (normal range)
2024-01-15 14:45:27.445 [INFO] Replication lag: 0.3ms
2024-01-15 14:45:28.112 [INFO] Last backup: 2024-01-15 02:15:00 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: Permission denied: /usr/lib/vmware-marvin/marvind.py` | Run the command with `sudo` or as root user. |
    | `ERROR: vmware-marvin.service not found` | Verify VMware VxRail Manager is installed with `rpm -qa | grep vmware-marvin` and reinstall if missing. |
    | `tail: cannot open '/var/log/vmware/vmware-vxrail-manager.log' for reading: No such file or directory` | Check the correct log path with `find /var/log -name '*vxrail*' -o -name '*marvin*'` and adjust the path accordingly. |
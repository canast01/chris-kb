# Cisco Nexus Dashboard — Troubleshooting Common Issues

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Overall cluster health
acs health

# Detailed node status
acs nodes list

# Check Kubernetes node status
kubectl get nodes
# If a node shows NotReady: investigate the node-specific issue below
```

```text
┌──────────────────────── Cisco Nexus Dashboard — Troubleshooting Common Issues ────────────────────────┐
│                                                                                                       │
│  Most frequent ND issues: cluster quorum, app failures, site disconnects, auth errors.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Cluster Problems               │  │           Authentication Failures           │   │
│   │         Node unreachable: NIC/cable          │  │         Login fail: AAA unreachable         │   │
│   │          Quorum lost: 2+ nodes down          │  │          SAML error: cert mismatch          │   │
│   │         Disk full: Elasticsearch log         │  │          Token expired: re-auth API         │   │
│   │         NTP drift: TLS cert failure          │  │             LDAP: bind DN wrong             │   │
│   │          etcd crash: restore backup          │  │           401 REST: creds rotated           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Check acs health first; auth issues need AAA server reachability confirmed                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Site and App Issues              │  │               Resolution Steps              │   │
│   │          Site offline: REST timeout          │  │           acs health: check nodes           │   │
│   │           NDFC: pod crash-looping            │  │          acs logs <app>: pod errors         │   │
│   │            NDI: no telemetry data            │  │            Renew cert or fix NTP            │   │
│   │          NDO: deploy stuck/timeout           │  │           Restart app: acs restart          │   │
│   │         SSL cert expired: 503 error          │  │          TAC: quorum unrecoverable          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · management switch · NTP · AAA server · APIC · firewall                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  acs health     = ND CLI command; shows cluster node and service health at a glance                   │
│  Quorum         = Requires 2 of 3 nodes; loss makes cluster read-only                                 │
│  etcd crash     = State-store failure; requires cluster restore from backup                           │
│  Disk full      = Elasticsearch retains telemetry; purge old data or expand volume                    │
│  NTP drift      = Clock skew breaks TLS validation and JWT expiry calculations                        │
│  Crash-loop     = Pod restarting repeatedly; acs logs shows root cause                                │
│  503 error      = HTTP Service Unavailable; typically expired TLS cert on ND                          │
│  401 error      = HTTP Unauthorized; API credentials rotated but not updated in ND                    │
│  Bind DN        = LDAP distinguished name ND uses to connect; fails if password changed               │
│  SAML cert mismatch= IdP signing cert changed but not updated in ND SP config                         │
│  acs restart    = ND CLI command to restart a specific app service gracefully                         │
│  TAC            = Cisco TAC; escalate cluster quorum loss or etcd corruption                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Check NDI pods
kubectl get pods -n ndi
# All should be Running

# Check flow collector logs
kubectl logs -n ndi deployment/ndi-flow-collector --tail=100 | grep -i "error\|drop\|overflow"

# Check disk usage for NDI data
kubectl exec -n ndi deployment/ndi-elasticsearch -- df -h /usr/share/elasticsearch/data
# If > 85% full: NDI stops writing new data (Elasticsearch circuit breaker)
```
```bash
# Test remote backup connectivity
ssh ndadmin@nd-dc1-1.corp.example.com
acs backup remote test
# Review output for the specific error

# If SSH key authentication: check if key is still authorized on backup server
# Update the backup configuration if credentials changed:
acs backup remote update \
  --server backup-server.corp.example.com \
  --user nd-bkp \
  --key-file /home/ndadmin/.ssh/nd-backup-key
```
```bash
# Check ND authentication service logs for SAML errors
kubectl logs -n nd-platform deployment/nd-keycloak --tail=100 | grep -i "saml\|assertion\|redirect"
```
```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check app status
acs apps status

# Check for pods stuck in Init or Error states
kubectl get pods --all-namespaces | grep -Ev "Running|Completed"

# Describe a stuck pod
kubectl describe pod -n ndfc <pod-name>
# Check Events section for resource constraints, image pull errors, etc.

# Check node resource availability
acs system resources
# If nodes are at memory/CPU limit: scale down other apps or add resources

# If the install image is corrupt:
acs apps remove-image <app> <version>
# Re-upload the image from a fresh download
```
```bash
# Check NTP on all nodes
acs system ntp show

# If NTP is not synchronised, re-add NTP servers:
acs system ntp add --server 10.10.0.10 --prefer
acs system ntp add --server 10.10.0.11

# Wait 2-3 minutes and check again
acs system ntp show
# Expected offset: < 100ms

# If offset is large and nodes cannot sync (isolated network):
# Use chronyc on the node OS to force a step correction:
sudo chronyc makestep
```

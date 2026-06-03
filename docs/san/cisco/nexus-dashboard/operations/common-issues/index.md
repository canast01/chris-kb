```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check cluster health
acs health

# Show node detail
acs nodes list

# Check if Kubernetes agrees with ND's view
kubectl get nodes
# Expected: all nodes Ready

# Check failing pods on the affected node
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-hostname> | grep -v Running
```

```text
┌────────────────────────── Cisco Nexus Dashboard — Operations Common Issues ───────────────────────────┐
│                                                                                                       │
│  Frequent ND operational issues: cluster quorum loss, app failures, site disconnects.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Cluster Issues                │  │                 App Failures                │   │
│   │          Quorum lost: 2 nodes down           │  │            NDFC pod crash-looping           │   │
│   │       etcd split-brain: net partition        │  │         NDI no telemetry: gRPC down         │   │
│   │        Node offline: NIC/cable fault         │  │         NDO deploy stuck: APIC busy         │   │
│   │        Disk full: log or data volume         │  │           OOM: pod evicted by K8s           │   │
│   │       NTP drift: cert validation fail        │  │          App upgrade failed: retry          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cluster health checked first; then app-level pod logs for targeted troubleshooting                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Site Connectivity Issues           │  │               Resolution Steps              │   │
│   │        Site unreachable: REST timeout        │  │          acs health: cluster state          │   │
│   │         Cred expired: 401 from APIC          │  │         acs logs: pod error messages        │   │
│   │         SSL cert expired: handshake          │  │         kubectl describe pod detail         │   │
│   │          Firewall: port 443 blocked          │  │          Renew cert or rotate creds         │   │
│   │        Version mismatch: app incompat        │  │         TAC: if quorum unrecoverable        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · management switches · APIC cluster · NTP server · firewall                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Quorum         = Minimum node count for cluster consensus; loss stops all writes                     │
│  etcd           = K8s state store; split-brain means two halves disagree on state                     │
│  Split-brain    = Network partition causing cluster halves to diverge independently                   │
│  Crash-loop     = Pod repeatedly starting and failing; check logs for root cause                      │
│  OOM            = Out Of Memory; Kubernetes evicts pod when node memory exhausted                     │
│  gRPC           = Streaming protocol; NDI telemetry stops if gRPC session drops                       │
│  NDO deploy     = Pushing policy templates to remote APIC; can time out if APIC busy                  │
│  NTP drift      = Time skew between nodes breaks TLS cert validation                                  │
│  401 error      = HTTP Unauthorized; credentials rejected by APIC REST API                            │
│  Version mismatch= ND app version incompatible with connected fabric controller                       │
│  kubectl describe= Kubernetes command showing pod events and failure reason                           │
│  TAC            = Cisco Technical Assistance Center; escalate unrecoverable faults                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Test remote backup connectivity
acs backup remote test

# Check backup status and last error
acs backup status

# Check backup logs
acs system logs --component backup --tail 50
```

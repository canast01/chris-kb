# Aria Automation — Health Checks

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Automation Health Check Stack                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Services layer                                      │   │
│  │  vracli status  ·  kubectl get pods --all-namespaces │   │
│  │  Expected: all pods Running or Completed             │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Cloud Accounts                                      │   │
│  │  Infrastructure → Connections → Cloud Accounts       │   │
│  │  All green  ·  API: GET /iaas/api/cloud-accounts     │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Database + Queue                                    │   │
│  │  kubectl logs -l app=postgres -n prelude             │   │
│  │  kubectl logs -l app=rabbitmq -n prelude             │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Deployments                                         │   │
│  │  Deployments → All → filter by FAILED status        │    │
│  │  No stuck CREATE_INPROGRESS > 30 min                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Daily Checks

### Cloud Account Status

All vCenter and NSX cloud accounts must show a green status indicator:

```
Infrastructure → Connections → Cloud Accounts
```

Any account showing a warning or error status means Aria Automation cannot provision into that target. Common causes: expired service account password, vCenter certificate change, NSX Manager unreachable.

```bash
# Check cloud account status via API
TOKEN=$(curl -sk -X POST "https://vra-prod-01.corp.local/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' | jq -r '.token')

curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.corp.local/iaas/api/cloud-accounts" | \
  jq '.content[] | {name: .name, type: .cloudAccountType, status: .cloudAccountStatus}'
```

---

### Kubernetes Pod Health

```bash
ssh root@vra-prod-01.corp.local

# Check all pods are Running or Completed
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"
# Any output here indicates a failing pod

# Quick summary of pod states
kubectl get pods --all-namespaces | \
  awk 'NR>1 {print $4}' | sort | uniq -c | sort -rn

# Describe a CrashLoopBackOff or Pending pod for diagnostics
kubectl describe pod -n prelude <pod-name>
```

---

### Review Deployment Event Log

```
Deployments → All Deployments → filter by "Failed" status
```

Failed deployments should be investigated, even if they are not actively blocking users. Persistent failures in a specific cloud zone may indicate a resource, network, or credential issue.

```bash
# API — list recent failed deployments
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.corp.local/deployment/api/deployments?status=FAILED&size=20" | \
  jq '.content[] | {name: .name, status: .status, reason: .reason}'
```

---

## Weekly Checks

### Pending Approval Requests

Review and action approval requests older than 5 business days:

```
Catalog → Deployments → Pending Approvals
```

Escalate stale requests (user not responding) or reject if the requester has left the organisation.

---

### Quota Utilisation

Check whether any projects are approaching their VM or CPU/memory quota limits:

```
Infrastructure → Administration → Projects → select project → Quota
```

Projects at >80% quota will start failing new deployments without a clear error to end users. Review and extend quotas proactively.

---

### Deployment Lease Expiry

```
Deployments → All Deployments → filter by lease expiry in next 7 days
```

Contact deployment owners for renewals or confirm expiry is intended. Expired deployments are automatically deleted according to the lease policy — ensure owners have been warned.

---

### Service Certificate Expiry

```bash
# Check Aria Automation UI certificate expiry
echo | openssl s_client -connect vra-prod-01.corp.local:443 2>/dev/null | \
  openssl x509 -noout -dates

# Check VAMI certificate expiry
echo | openssl s_client -connect vra-prod-01.corp.local:5480 2>/dev/null | \
  openssl x509 -noout -dates
```

---

## Pre-Maintenance Checks

Run before any planned change (upgrade, certificate rotation, cloud account re-credential):

- [ ] No deployments in progress: **Deployments → All Deployments** — no CREATING or UPDATING state
- [ ] All cloud accounts green
- [ ] All Kubernetes pods Running: `kubectl get pods --all-namespaces | grep -v Running | grep -v Completed`
- [ ] Backup completed successfully within the last 24 hours (VAMI → Lifecycle Management → Backup)
- [ ] VM snapshots taken for all Aria Automation appliance nodes
- [ ] Inform users of maintenance window

---

## Platform Service Health Commands

```bash
ssh root@vra-prod-01.corp.local

# Overall appliance and service health
vracli status

# Show cluster member status (for 3-node deployments)
vracli cluster health

# Show current Aria Automation version
vracli version

# Restart a specific Kubernetes deployment (use as last resort — pods self-heal)
kubectl rollout restart deployment/<deployment-name> -n prelude

# View recent events in the prelude namespace (useful for deployment failures)
kubectl get events -n prelude --sort-by='.metadata.creationTimestamp' | tail -30
```

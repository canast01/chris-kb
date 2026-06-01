# Tanzu — Scripts


<div class="kb-summary">
Scripts reference covering Get All TKG Clusters and Status, Get All PVCs Across All Namespaces (Identify Unbound), Check All Node Resource Usage, Export All Deployments and Services from Namespace, Verify Harbor Vulnerability Scanning and 2 more sections.
</div>

---

## Get All TKG Clusters and Status

```bash
#!/bin/bash
# List all clusters across all Supervisor namespaces

SUPERVISOR="https://supervisor.example.local"
kubectl vsphere login --server $SUPERVISOR \
  --username administrator@vsphere.local --insecure-skip-tls-verify 2>/dev/null

kubectl get tanzukubernetescluster -A \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,PHASE:.status.phase,READY:.status.conditions[?(@.type=="Ready")].status'
```

---

## Get All PVCs Across All Namespaces (Identify Unbound)

```bash
#!/bin/bash
echo "=== Unbound PVCs ==="
kubectl get pvc -A --field-selector=status.phase!=Bound \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,STORAGECLASS:.spec.storageClassName,SIZE:.spec.resources.requests.storage'

echo ""
echo "=== All PVC Summary ==="
kubectl get pvc -A | awk 'NR>1 {print $5}' | sort | uniq -c | sort -rn
# Shows count by status: Bound, Pending, Lost
```

---

## Check All Node Resource Usage

```bash
#!/bin/bash
# Requires metrics-server installed in cluster
echo "=== Node Resource Usage ==="
kubectl top nodes

echo ""
echo "=== Top 20 CPU-consuming Pods ==="
kubectl top pods -A --sort-by=cpu | head -21

echo ""
echo "=== Top 20 Memory-consuming Pods ==="
kubectl top pods -A --sort-by=memory | head -21
```

---

## Export All Deployments and Services from Namespace

```bash
#!/bin/bash
NAMESPACE="production"
EXPORT_DIR="./k8s-export-$(date +%Y%m%d)"
mkdir -p "$EXPORT_DIR"

for resource in deployments services configmaps secrets persistentvolumeclaims; do
  kubectl get $resource -n $NAMESPACE -o yaml > "$EXPORT_DIR/${resource}.yaml" 2>/dev/null
  count=$(kubectl get $resource -n $NAMESPACE --no-headers 2>/dev/null | wc -l)
  echo "Exported $resource: $count items"
done

echo "Export complete: $EXPORT_DIR"
```

---

## Verify Harbor Vulnerability Scanning

```python
#!/usr/bin/env python3
"""Check all Harbor repositories have vulnerability scanning enabled."""
import requests, sys

HARBOR_URL = "https://harbor.example.local"
USER = "admin"
PASS = "Harbor12345"

resp = requests.get(f"{HARBOR_URL}/api/v2.0/projects", auth=(USER, PASS), verify=False)
projects = resp.json()

issues = []
for proj in projects:
    name = proj["name"]
    meta_resp = requests.get(
        f"{HARBOR_URL}/api/v2.0/projects/{name}",
        auth=(USER, PASS), verify=False
    )
    meta = meta_resp.json().get("metadata", {})
    if meta.get("auto_scan") != "true":
        issues.append(f"Project '{name}': auto_scan not enabled")

if issues:
    print("ISSUES FOUND:")
    for i in issues:
        print(f"  {i}")
    sys.exit(1)
else:
    print(f"OK: all {len(projects)} projects have auto_scan enabled")
    sys.exit(0)
```

---

## Check Certificate Expiry on TKG Cluster API Endpoints

```bash
#!/bin/bash
# Check cert expiry for all clusters in kubeconfig
for context in $(kubectl config get-contexts -o name); do
  server=$(kubectl config view -o jsonpath="{.clusters[?(@.name=='$context')].cluster.server}" 2>/dev/null)
  if [ -n "$server" ]; then
    host=$(echo "$server" | sed 's|https://||' | cut -d: -f1)
    port=$(echo "$server" | sed 's|https://||' | cut -d: -f2)
    port=${port:-443}
    expiry=$(echo | timeout 3 openssl s_client -connect "$host:$port" 2>/dev/null \
      | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -n "$expiry" ]; then
      echo "$context: $expiry"
    fi
  fi
done
```

---

## List Harbor Images with Critical CVEs

```python
#!/usr/bin/env python3
import requests

HARBOR_URL = "https://harbor.example.local"
USER = "admin"
PASS = "Harbor12345"

def get_projects():
    r = requests.get(f"{HARBOR_URL}/api/v2.0/projects", auth=(USER, PASS), verify=False)
    return [p["name"] for p in r.json()]

def get_repositories(project):
    r = requests.get(
        f"{HARBOR_URL}/api/v2.0/projects/{project}/repositories",
        auth=(USER, PASS), verify=False
    )
    return [repo["name"] for repo in r.json()]

def check_artifacts(project, repo):
    repo_encoded = repo.split("/", 1)[-1].replace("/", "%2F")
    r = requests.get(
        f"{HARBOR_URL}/api/v2.0/projects/{project}/repositories/{repo_encoded}/artifacts",
        params={"with_scan_overview": "true"},
        auth=(USER, PASS), verify=False
    )
    for artifact in r.json():
        scan = artifact.get("scan_overview", {})
        for scanner, result in scan.items():
            critical = result.get("severity", "")
            vuln_counts = result.get("summary", {}).get("summary", {})
            critical_count = vuln_counts.get("Critical", 0)
            if critical_count > 0:
                digest = artifact["digest"][:12]
                print(f"  CRITICAL({critical_count}): {repo}@{digest}")

for proj in get_projects():
    for repo in get_repositories(proj):
        check_artifacts(proj, repo)
```

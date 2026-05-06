# Nexus Dashboard CLI Reference

Nexus Dashboard management is primarily via the web UI and REST API. SSH access to ND nodes is available for platform diagnostics. The NDFC REST API and ACI APIC REST API provide programmatic access to fabric management and health data.

**ND Node SSH Commands**

```bash
# Check overall ND platform health
acs health

# Check Kubernetes pod status for ND services
kubectl get pods -n nd-platform

# Show ND node software version
show version

# Check cluster node status
acs status
```

**NDFC REST API — Key Endpoints**

| Endpoint | Method | Purpose |
|---|---|---|
| `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics` | GET | List all fabrics |
| `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric}/health` | GET | Fabric health score |
| `/appcenter/cisco/ndfc/api/v1/elastic-service/fabrics/{fabric}/deployment-status` | GET | Policy deployment status |

**ACI APIC REST API**

```bash
# Query fabric faults via APIC REST API
GET https://<apic>/api/node/class/faultInst.json?query-target-filter=and(gt(faultInst.severity,"minor"))
```

---
tags:
  - nsx
  - networking
description: "Top-10 NSX commands for transport nodes, segments, T0/T1 gateways, and DFW via the NSX Manager CLI and REST API."
---
# NSX Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 NSX commands for transport nodes, segments, T0/T1 gateways, and DFW via the NSX Manager CLI and REST API.
</div>
![NSX Cheat Sheet](../../assets/reference-cheat-sheets-nsx.svg)

## NSX Manager CLI (SSH to NSX Manager)

```bash
get version                                    # NSX version and build
get cluster status                             # cluster node health
get transport-nodes                            # all transport nodes and state
get logical-switch                             # list all logical switches (MP API)
get bgp neighbor                               # BGP peer state on Edge nodes
get interface                                  # interfaces on Edge/Manager
get certificate cluster                        # cluster certificate thumbprint
```


```text title="Expected output"
NSX version: 3.2.1.0 (Build 19480675)
Cluster Status: STABLE
  Node nsx-manager-01.lab.local: UP (Leader)
  Node nsx-manager-02.lab.local: UP
  Node nsx-manager-03.lab.local: UP

Transport Nodes:
  nsx-edge-01 (192.168.1.45): REALIZED
  nsx-edge-02 (192.168.1.46): REALIZED
  nsx-tn-host-01 (192.168.1.50): REALIZED
  nsx-tn-host-02 (192.168.1.51): REALIZED

Logical Switches:
  ls-prod-web (UUID: 12a4f8c9-3e2b-4d7f-91c2-8f5a6b2c1d9e): 4 ports
  ls-prod-db (UUID: 5c8d2f1a-9b4e-4a6c-b3f2-7e1d9c4a5b8f): 2 ports
  ls-mgmt (UUID: 8f2c1b9a-4d5e-6f7a-c8e1-2d3f4a5b6c7d): 3 ports

BGP Neighbors:
  nsx-edge-01: 192.168.0.1 (AS 65001) - ESTABLISHED
  nsx-edge-02: 192.168.0.1 (AS 65001) - ESTABLISHED

Interfaces:
  nsx-edge-01 eth0: 192.168.1.45/24 (UP)
  nsx-edge-01 eth1: 10.0.0.1/24 (UP)
  nsx-manager-01 eth0: 192.168.1.10/24 (UP)

Cluster Certificate Thumbprint: A1:B2:C3:D4:E5:F6:7G:8H:9I:0J:K1:L2:M3:N4:O5:P6:Q7:R8:S9:T0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused (Connection refused)` | Verify NSX Manager is running and accessible on the configured IP/hostname and port (default 443). |
    | `Error: Invalid credentials (Unauthorized)` | Ensure your NSX API user account has appropriate role permissions and credentials are correctly configured in your CLI session. |
    | `Error: Certificate verification failed` | Add the NSX Manager certificate to your trusted store or disable certificate verification if in a lab environment (use `--insecure` flag if available). |
## REST API (curl examples)

```bash
BASE="https://nsx-mgr"
AUTH="-u admin:VMware1!"

# Transport nodes
curl -sk $AUTH $BASE/api/v1/transport-nodes | python3 -m json.tool

# Segments (Policy API)
curl -sk $AUTH $BASE/policy/api/v1/infra/segments | python3 -m json.tool

# T0 gateways
curl -sk $AUTH $BASE/policy/api/v1/infra/tier-0s | python3 -m json.tool

# Firewall rules (DFW)
curl -sk $AUTH $BASE/policy/api/v1/infra/domains/default/security-policies | python3 -m json.tool

# BGP route table on Edge
curl -sk $AUTH "$BASE/api/v1/logical-routers/<lr-id>/routing/bgp/neighbors" | python3 -m json.tool
```


```text title="Expected output"
{
  "results": [
    {
      "id": "tn-001",
      "display_name": "EdgeNode-01",
      "node_deployment_info": {
        "deployment_type": "VIRTUAL_MACHINE",
        "os_type": "ESXI"
      },
      "transport_zone_endpoints": [
        {
          "transport_zone_id": "tz-vlan-001"
        }
      ]
    },
    {
      "id": "tn-002",
      "display_name": "EdgeNode-02",
      "node_deployment_info": {
        "deployment_type": "VIRTUAL_MACHINE",
        "os_type": "ESXI"
      }
    }
  ],
  "result_count": 2
}
{
  "results": [
    {
      "id": "segment-prod-web",
      "display_name": "prod-web-vlan100",
      "subnets": [
        {
          "gateway_address": "10.1.100.1/24"
        }
      ]
    },
    {
      "id": "segment-prod-db",
      "display_name": "prod-db-vlan101",
      "subnets": [
        {
          "gateway_address": "10.1.101.1/24"
        }
      ]
    }
  ],
  "result_count": 2
}
{
  "results": [
    {
      "id": "t0-primary",
      "display_name": "T0-Primary-GW",
      "ha_mode": "ACTIVE_ACTIVE",
      "default_rule_logging": false
    }
  ],
  "result_count": 1
}
{
  "results": [
    {
      "id": "default-policy",
      "display_name": "Default Security Policy",
      "rules": [
        {
          "id": "rule-001",
          "display_name": "Allow-HTTPS",
          "action": "ALLOW",
          "services": ["HTTPS"]
        }
      ]
    }
  ],
  "result_count": 1
}
curl: (7) Failed to connect to nsx-mgr port 443: Name or service not known
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to nsx-mgr port 443: Name or service not known` | Replace `nsx-mgr` with the actual NSX Manager FQDN or IP address (e.g., `https://10.0.0.10`). |
    | `HTTP/1.1 401 Unauthorized` | Verify the admin credentials in the AUTH variable match your NSX Manager user account (reset password in NSX UI if needed). |
    | `curl: (60) SSL certificate problem: self signed certificate` | The `-k` flag already ignores SSL warnings; if curl still fails, ensure NSX Manager is reachable and not blocked by firewall rules. |
## See also

- [NSX Operations](../../../virtualization/vmware/products/nsx/operations/procedures/)
- [NSX Troubleshooting](../../../virtualization/vmware/products/nsx/troubleshooting/common-issues/)
- [NSX Health Checks](../../../virtualization/vmware/products/nsx/operations/health-checks/)

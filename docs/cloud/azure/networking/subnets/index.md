# Subnets


<div class="kb-summary">
Subnets segment a Virtual Network address space into smaller ranges.
</div>
```
┌─────────────────────────────────────── Cloud Azure Networking ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Azure: Cloud Azure Networking platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Cloud Azure Networking management console                     │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│    Physical: Cloud Azure Networking infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Networking platform overview and core concepts                    │
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


## Service Endpoints

Service endpoints extend VNet identity to Azure PaaS services, ensuring traffic flows over the Azure backbone rather than the public internet.

```bash
# Enable service endpoints for Storage and Key Vault on a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --service-endpoints Microsoft.Storage Microsoft.KeyVault

# List service endpoints on a subnet
az network vnet subnet show \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --query serviceEndpoints \
  --output json
```

## Subnet Delegation

Delegation allows certain Azure services (e.g., Azure Container Instances, Azure NetApp Files, Azure Databricks) to inject resources directly into a subnet.

```bash
# Delegate a subnet to Azure Container Instances
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name aci-subnet \
  --delegations Microsoft.ContainerInstance/containerGroups

# Delegate to Azure Databricks
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name databricks-private \
  --delegations Microsoft.Databricks/workspaces

# Remove a delegation
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name aci-subnet \
  --remove delegations
```

## NSG and Route Table Association

```bash
# Associate an NSG with a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --network-security-group myNSG

# Associate a route table with a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --route-table myRouteTable

# Disassociate NSG from a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --network-security-group ""
```

## Private Endpoint Network Policies

```bash
# Disable private endpoint network policies (required before creating a private endpoint)
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --disable-private-endpoint-network-policies true

# Show all subnet properties
az network vnet subnet show \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --output json
```

# Load Balancer

Azure Load Balancer — layer 4 TCP/UDP load balancing for Azure VMs and VM scale sets.

## Types

| Type | Scope | Use Case |
|---|---|---|
| Public Load Balancer | Internet-facing | External traffic to VMs; replaces NAT |
| Internal Load Balancer | VNet-internal | Private traffic between tiers (app → DB) |
| Standard SKU | Zone-redundant, SLA | Production — recommended |
| Basic SKU | Limited, no SLA | Dev/test only |

> For HTTP/HTTPS with path routing, use **Application Gateway** instead of Load Balancer.

## Common Azure CLI Commands

```bash
# List load balancers
az network lb list -g <rg> \
  --query '[*].{Name:name,SKU:sku.name,Type:properties.frontendIPConfigurations[0].properties.publicIPAddress.id}' -o table

# List backend pools
az network lb address-pool list -g <rg> --lb-name <lb-name> -o table

# List health probes
az network lb probe list -g <rg> --lb-name <lb-name> \
  --query '[*].{Name:name,Protocol:protocol,Port:port,Path:requestPath,Interval:intervalInSeconds}' -o table

# List load balancing rules
az network lb rule list -g <rg> --lb-name <lb-name> \
  --query '[*].{Name:name,Protocol:protocol,FrontendPort:frontendPort,BackendPort:backendPort,Probe:probe.id}' -o table

# Add a backend VM to the backend pool
az network nic ip-config update \
  -g <rg> --nic-name <nic-name> --name ipconfig1 \
  --lb-name <lb-name> --lb-address-pools <pool-name>
```

## Create Health Probe

```bash
az network lb probe create -g <rg> --lb-name <lb-name> \
  --name http-health \
  --protocol Http \
  --port 80 \
  --path /health \
  --interval 15 \
  --threshold 2
```

## Create Load Balancing Rule

```bash
az network lb rule create -g <rg> --lb-name <lb-name> \
  --name app-rule \
  --frontend-ip-name LoadBalancerFrontEnd \
  --frontend-port 443 \
  --backend-pool-name <pool-name> \
  --backend-port 443 \
  --protocol Tcp \
  --probe-name http-health \
  --idle-timeout 4
```

## Inbound NAT Rules (for direct VM access)

```bash
# Create NAT rule — map external port 50001 to VM port 22
az network lb inbound-nat-rule create -g <rg> --lb-name <lb-name> \
  --name ssh-vm01 \
  --protocol Tcp \
  --frontend-ip-name LoadBalancerFrontEnd \
  --frontend-port 50001 \
  --backend-port 22
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| All backends unhealthy | Health probe | Verify probe port/path returns correct response from the subnet |
| Intermittent connection drops | Idle timeout | Increase idle timeout on rule (default 4 min); app should send keepalives |
| VMs not receiving traffic | Backend pool membership | Check NIC is in the pool; verify NSG allows LB inbound (`AzureLoadBalancer` tag) |
| No SLA | Basic SKU | Upgrade to Standard SKU for production |

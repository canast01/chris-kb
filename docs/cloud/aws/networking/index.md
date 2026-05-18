# AWS Networking

<div class="kb-summary">
AWS networking is built around VPCs with public and private subnets across availability zones, with Transit Gateway providing hub-and-spoke connectivity between accounts and on-premises. Coverage includes Security Groups, NACLs, route tables, VPC endpoints, load balancers, Route 53, and VPC Flow Logs.
</div>

```
┌─────────────────────────────────────────────────────────┐
│              VPC Networking Overview                    │
│                                                         │
│  Internet ──► IGW ──► Public Subnet (ALB · NAT GW)      │
│                            │                            │
│                     NAT GW (outbound only)              │
│                            │                            │
│                       Private Subnet (EC2 · ECS)        │
│                            │                            │
│                       Isolated Subnet (RDS)             │
│                                                         │
│  On-Premises ──VPN/DX──► VGW ──► Private Subnet         │
│                                                         │
│  Security: Security Group (instance) · NACL (subnet)    │
└─────────────────────────────────────────────────────────┘
```

![AWS Networking Architecture](../../../assets/aws-networking-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="vpc/">
  <strong>VPC</strong>
  <span>VPC layout, routing, address planning, endpoints, and controls.</span>
</a>

<a class="kb-card" href="subnets/">
  <strong>Subnets</strong>
  <span>Subnet design, route scope, availability zones, and segmentation.</span>
</a>

<a class="kb-card" href="route-tables/">
  <strong>Route Tables</strong>
  <span>Routing paths, default routes, private routes, and validation.</span>
</a>

<a class="kb-card" href="internet-gateway/">
  <strong>Internet Gateway</strong>
  <span>Public internet routing and edge connectivity.</span>
</a>

<a class="kb-card" href="nat-gateway/">
  <strong>NAT Gateway</strong>
  <span>Private subnet outbound internet access and troubleshooting.</span>
</a>

<a class="kb-card" href="vpc-endpoints/">
  <strong>VPC Endpoints</strong>
  <span>Private service access, gateway endpoints, and interface endpoints.</span>
</a>

<a class="kb-card" href="security-groups/">
  <strong>Security Groups</strong>
  <span>Instance-level firewall rules and access validation.</span>
</a>

<a class="kb-card" href="network-acls/">
  <strong>Network ACLs</strong>
  <span>Subnet-level stateless filtering and traffic control.</span>
</a>

<a class="kb-card" href="elastic-load-balancer/">
  <strong>Elastic Load Balancer</strong>
  <span>ALB, NLB, target groups, listeners, and health checks.</span>
</a>

<a class="kb-card" href="route-53/">
  <strong>Route 53</strong>
  <span>Hosted zones, DNS records, routing policies, and resolver notes.</span>
</a>

<a class="kb-card" href="vpc-flow-logs/">
  <strong>VPC Flow Logs</strong>
  <span>Network traffic logging, query patterns, and troubleshooting.</span>
</a>

</div>

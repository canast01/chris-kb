# AWS VPC

<div class="kb-summary">
An AWS Virtual Private Cloud (VPC) is your own isolated private network inside AWS. You control the IP ranges, subnets, routing, and security. Everything you run in AWS lives inside a VPC.
</div>

## VPC Anatomy

```text
┌───────────────────────────────────── VPC — Virtual Private Cloud ─────────────────────────────────────┐
│                                                                                                       │
│  VPC is an isolated virtual network within AWS; you control CIDR, subnets, and routing.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VPC Core Components              │  │             Connectivity Options            │   │
│   │      CIDR block: /16 to /28 IPv4 range       │  │       Internet Gateway: public access       │   │
│   │       Subnets: per-AZ CIDR sub-blocks        │  │        NAT Gateway: private outbound        │   │
│   │       Route tables: traffic direction        │  │         VPC Peering: direct VPC link        │   │
│   │      Security groups: stateful firewall      │  │          Transit Gateway: hub-spoke         │   │
│   │       NACLs: stateless subnet firewall       │  │          DirectConnect/VPN: on-prem         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Multi-AZ design with public + private + data tiers; TGW for cross-account connectivity.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VPC Design Decisions             │  │                 Default VPC                 │   │
│   │       RFC1918 CIDR: avoid prod overlap       │  │         Auto-created in every region        │   │
│   │     Secondary CIDR: expand if exhausted      │  │       /16 CIDR; public subnets per AZ       │   │
│   │      Enable DNS hostnames + resolution       │  │       IGW attached; auto-assign IP on       │   │
│   │        Flow logs: capture all traffic        │  │        Do not use for prod workloads        │   │
│   │      Shared VPC: RAM for multi-account       │  │       Recreate if accidentally deleted      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional network fabric · Multiple physical AZ data centres · Global backbone                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VPC             = Logically isolated section of AWS cloud with its own network configuration         │
│  CIDR block      = IP range for the VPC; primary + optional secondary blocks                          │
│  Tenancy         = Default (shared hardware) or dedicated (single-tenant physical host)               │
│  DNS resolution  = VPC attribute enabling DNS queries to route through Route 53 resolver              │
│  DNS hostnames   = VPC attribute giving instances public DNS names for their public IPs               │
│  Secondary CIDR  = Additional CIDR block added to expand VPC IP address space                         │
│  Shared VPC      = VPC owned by one account; subnets shared to others via RAM                         │
│  VPC Peering     = Private routing between two VPCs; no TGW required; no transitive                   │
│  Transit Gateway = Regional hub connecting many VPCs and on-prem; supports transitive                 │
│  Default VPC     = AWS-created VPC in every region; do not use for production                         │
│  Flow Logs       = VPC-level capture of accept/reject traffic for network analysis                    │
│  RFC1918         = Private address ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── VPC — Virtual Private Cloud ─────────────────────────────────────┐
│                                                                                                       │
│  VPC is an isolated virtual network within AWS; you control CIDR, subnets, and routing.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VPC Core Components              │  │             Connectivity Options            │   │
│   │      CIDR block: /16 to /28 IPv4 range       │  │       Internet Gateway: public access       │   │
│   │       Subnets: per-AZ CIDR sub-blocks        │  │        NAT Gateway: private outbound        │   │
│   │       Route tables: traffic direction        │  │         VPC Peering: direct VPC link        │   │
│   │      Security groups: stateful firewall      │  │          Transit Gateway: hub-spoke         │   │
│   │       NACLs: stateless subnet firewall       │  │          DirectConnect/VPN: on-prem         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Multi-AZ design with public + private + data tiers; TGW for cross-account connectivity.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VPC Design Decisions             │  │                 Default VPC                 │   │
│   │       RFC1918 CIDR: avoid prod overlap       │  │         Auto-created in every region        │   │
│   │     Secondary CIDR: expand if exhausted      │  │       /16 CIDR; public subnets per AZ       │   │
│   │      Enable DNS hostnames + resolution       │  │       IGW attached; auto-assign IP on       │   │
│   │        Flow logs: capture all traffic        │  │        Do not use for prod workloads        │   │
│   │      Shared VPC: RAM for multi-account       │  │       Recreate if accidentally deleted      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional network fabric · Multiple physical AZ data centres · Global backbone                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VPC             = Logically isolated section of AWS cloud with its own network configuration         │
│  CIDR block      = IP range for the VPC; primary + optional secondary blocks                          │
│  Tenancy         = Default (shared hardware) or dedicated (single-tenant physical host)               │
│  DNS resolution  = VPC attribute enabling DNS queries to route through Route 53 resolver              │
│  DNS hostnames   = VPC attribute giving instances public DNS names for their public IPs               │
│  Secondary CIDR  = Additional CIDR block added to expand VPC IP address space                         │
│  Shared VPC      = VPC owned by one account; subnets shared to others via RAM                         │
│  VPC Peering     = Private routing between two VPCs; no TGW required; no transitive                   │
│  Transit Gateway = Regional hub connecting many VPCs and on-prem; supports transitive                 │
│  Default VPC     = AWS-created VPC in every region; do not use for production                         │
│  Flow Logs       = VPC-level capture of accept/reject traffic for network analysis                    │
│  RFC1918         = Private address ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Daily Checks

```bash
# List VPCs in current region
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' --output table

# List subnets
aws ec2 describe-subnets --query 'Subnets[*].[SubnetId,VpcId,CidrBlock,AvailabilityZone,MapPublicIpOnLaunch]' --output table

# Check route tables
aws ec2 describe-route-tables --query 'RouteTables[*].[RouteTableId,VpcId,Routes[*].[DestinationCidrBlock,GatewayId]]' --output text

# Check internet gateways
aws ec2 describe-internet-gateways --query 'InternetGateways[*].[InternetGatewayId,Attachments[*].VpcId]' --output table

# Check NAT gateways and their state
aws ec2 describe-nat-gateways --query 'NatGateways[*].[NatGatewayId,VpcId,State,SubnetId]' --output table

# Check VPN connections
aws ec2 describe-vpn-connections --query 'VpnConnections[*].[VpnConnectionId,State,VgwTelemetry[*].[OutsideIpAddress,Status]]' --output text
```

---

## Common Issues

| Symptom | Likely Cause | Check |
|---|---|---|
| EC2 can't reach internet | Missing IGW route or no public IP | Route table — does 0.0.0.0/0 point to IGW? |
| Private subnet EC2 can't reach internet | Missing NAT Gateway or route | Route table — does 0.0.0.0/0 point to NAT GW? |
| Can't SSH/RDP to EC2 | Security group blocking port 22/3389 | Security group inbound rules |
| Two subnets can't talk to each other | Missing route or NACL blocking | Route table + NACL rules |
| On-prem can't reach VPC | VPN tunnel down or BGP issue | VPN connection status + BGP session |
| EC2 can't reach on-prem | Missing route to on-prem CIDR via VGW | Route table — is on-prem CIDR routed to VGW? |

---

## VPC Subnet Architecture

```text
┌────────────────────── VPC Subnet Architecture — Public, Private, and Data Tiers ──────────────────────┐
│                                                                                                       │
│    Multi-tier VPC: public (internet-facing), private (app), data (DB) subnets per AZ.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Public Subnet (internet-facing)       │  │        Private Subnet (app/compute tier)    │   │
│   │  ALB: routes inbound internet traffic        │  │  EC2, ECS, EKS workloads live here          │   │
│   │  NAT Gateway: private outbound traffic       │  │  No direct inbound internet path            │   │
│   │  Bastion host (if needed)                    │  │  Route table: 0.0.0.0/0 via NAT GW          │   │
│   │  Route table: 0.0.0.0/0 via IGW              │  │  Security groups: allow from ALB SG         │   │
│   │  IGW: internet gateway attached to VPC       │  │  Connects to data tier via SG rules         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    IGW enables internet; NAT GW enables private outbound without public IPs.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      Security Groups (instance-level)        │  │      NACLs (subnet-level)                   │   │
│   │  Stateful: return traffic auto-allowed       │  │  Stateless: must allow both directions      │   │
│   │  Attached to ENI (per-instance)              │  │  Applied to subnet boundary                 │   │
│   │  Allow rules only; no explicit deny          │  │  Allow and deny rules both available        │   │
│   │  Rules evaluated together (OR logic)         │  │  Rules evaluated in number order            │   │
│   │  Default SG: allows all from same SG         │  │  Default NACL: allows all traffic           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    AWS regional network fabric · AZ data centres · physical NICs backing ENIs                         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    IGW         = Internet Gateway; allows public subnets to reach the internet                        │
│    NAT Gateway = Managed NAT; private subnet instances can reach internet outbound only               │
│    Security Group = Stateful firewall at the instance (ENI) level; allow rules only                   │
│    NACL        = Network ACL; stateless firewall at subnet boundary; allow + deny                     │
│    Stateful    = Return traffic automatically allowed; no explicit rule needed                        │
│    Stateless   = Every direction needs an explicit rule; no tracking                                  │
│    Route table = Per-subnet list of destinations and their targets (IGW, NAT, etc.)                   │
│    ENI         = Elastic Network Interface; virtual NIC; SG is attached to ENI                        │
│    Bastion host= EC2 in public subnet used as SSH jump host to private EC2 instances                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```



---

## AWS Network Connectivity Options

```text
┌────────────────────────────────── AWS Network Connectivity Options ───────────────────────────────────┐
│                                                                                                       │
│    Multiple options connect on-prem to AWS or VPCs to each other; choose by need.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      Internet Gateway / NAT Gateway          │  │      Site-to-Site VPN                       │   │
│   │  IGW: public subnet internet access          │  │  IPSec tunnel over the public internet      │   │
│   │  NAT GW: private outbound only (no in)       │  │  Virtual Private Gateway on VPC side        │   │
│   │  Managed by AWS; HA within AZ                │  │  Customer Gateway on on-prem side           │   │
│   │  NAT GW: charged per GB + hourly             │  │  Bandwidth: up to ~1.25 Gbps per VPN        │   │
│   │  Scales automatically; no maintenance        │  │  Low cost; quick to set up; encrypted       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    VPN is encrypted but uses shared internet; Direct Connect is dedicated private link.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      AWS Direct Connect (DX)                 │  │     PrivateLink / Transit Gateway           │   │
│   │  Dedicated physical link to AWS              │  │  PrivateLink: expose service to VPC         │   │
│   │  1 Gbps or 10 Gbps ports available           │  │  No internet; no peering; private IP        │   │
│   │  Lower latency + consistent bandwidth        │  │  Endpoint in consumer VPC; NLB backed       │   │
│   │  DX Gateway: one DX to many Regions          │  │  Transit Gateway: hub-spoke for VPCs        │   │
│   │  Not encrypted by default; use IPSec         │  │  TGW: transitive routing; centrally         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    AWS backbone fibre · DX colocation partner facilities · physical DX ports                          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Site-to-Site VPN = IPSec encrypted tunnel from on-prem to VPC via internet                         │
│    Direct Connect   = Dedicated private physical connection; bypasses internet                        │
│    VGW              = Virtual Private Gateway; VPN/DX attachment point on VPC                         │
│    CGW              = Customer Gateway; on-prem router configuration in AWS                           │
│    DX Gateway       = Connect one Direct Connect to VPCs in multiple Regions                          │
│    Transit Gateway  = Regional hub; connects many VPCs and on-prem via single hub                     │
│    PrivateLink      = Expose a service privately; no internet traversal; NLB-backed                   │
│    VPC Peering      = Direct 1:1 routing between two VPCs; not transitive                             │
│    Transitive routing= Traffic A→B→C; TGW supports it; VPC Peering does not                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Route 53 Routing Policies

```text
┌─────────────────────────────── Route 53 Routing Policies — Comparison ────────────────────────────────┐
│                                                                                                       │
│    Route 53 supports 7 routing policies; choose based on traffic distribution goal.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Policy                                │  │      Use Case / Behaviour                   │   │
│   │  Simple                                      │  │  Single record; basic DNS; no health        │   │
│   │  Weighted                                    │  │  Split traffic by % (A/B testing)           │   │
│   │  Latency                                     │  │  Route to lowest-latency AWS Region         │   │
│   │  Failover                                    │  │  Primary + secondary with health chk        │   │
│   │  Geolocation                                 │  │  Route by user country or continent         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Policy (continued)                    │  │      Use Case / Behaviour                   │   │
│   │  Geoproximity                                │  │  Route by geographic proximity; bias        │   │
│   │  Multivalue Answer                           │  │  Return up to 8 healthy records             │   │
│   │  Health checks                               │  │  Monitor endpoints; failover if down        │   │
│   │  Alias records                               │  │  Point to AWS resources (ALB, CF, S3)       │   │
│   │  Private hosted zone                         │  │  DNS inside VPC; internal resolution        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    Route 53 anycast infrastructure · 100+ edge PoPs globally · DNSSEC support                         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Simple routing     = Single resource; multiple values returned randomly (no health)                │
│    Weighted routing   = Assign weights (0-255) to split traffic; A/B testing                          │
│    Latency routing    = Measure latency to AWS Regions; send user to lowest latency                   │
│    Failover routing   = Active/passive; primary serves traffic; secondary if unhealthy                │
│    Geolocation        = Route based on user geographic location (country, continent)                  │
│    Geoproximity       = Route by proximity to resource; bias shifts boundary                          │
│    Multivalue         = Up to 8 healthy records returned; basic load distribution                     │
│    Health check       = HTTP/HTTPS/TCP probe; marks record unhealthy if failing                       │
│    Alias record       = Native Route 53 record type pointing to AWS service endpoints                 │
│    Private hosted zone= DNS zone only resolvable inside VPC or associated VPCs                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

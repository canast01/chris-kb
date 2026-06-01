# AWS VPC

<div class="kb-summary">
An AWS Virtual Private Cloud (VPC) is your own isolated private network inside AWS. You control the IP ranges, subnets, routing, and security. Everything you run in AWS lives inside a VPC.
</div>

## VPC Anatomy

```text
AWS VPC — Virtual Private Cloud
                                          │
│  ← your own private section of AWS
│  ← isolated from other AWS customers
│  ← you control the IP ranges, subnets,
│     routing, and security
                                          │
```
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

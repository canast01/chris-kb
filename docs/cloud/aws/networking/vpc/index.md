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
┌─────────────────────────────────────────┐
│           AWS VPC                       │
│           (Virtual Private Cloud)       │
│           IP range: 172.16.0.0/16       │
│                                         │
│  ┌──────────────┐  ┌──────────────┐     │
│  │ Public       │  │ Private      │     │
│  │ Subnet       │  │ Subnet       │     │
│  │              │  │              │     │
│  │ ├── Load     │  │ ├── EC2      │     │
│  │ │   Balancer │  │ │   Instance │     │
│  │ └── Bastion  │  │ │   (VM)     │     │
│  │     Host     │  │ │            │     │
│  │              │  │ ├── EBS      │     │
│  │  faces       │  │ │   Volume   │     │
│  │  internet    │  │ │   (disk)   │     │
│  │              │  │ │            │     │
│  │              │  │ └── RDS      │     │
│  │              │  │     Database │     │
│  └──────────────┘  └──────────────┘     │
│           │                │            │
│     Internet           VPN Gateway      │
│     Gateway            (connects back   │
│     (public            to on-prem)      │
│      traffic)                           │
└─────────────────────────────────────────┘
```

## Key Terms

| Term | What It Is | On-Premises Equivalent |
|---|---|---|
| VPC | Your own isolated network inside AWS | Your data centre LAN |
| Subnet | A smaller IP range inside the VPC (public or private) | VLAN |
| EC2 | A VM running in AWS | ESXi virtual machine |
| EBS | A disk attached to an EC2 instance | Pure Storage LUN |
| RDS | Managed relational database (AWS runs the OS/DB) | On-prem SQL Server |
| IGW | Internet Gateway — how public subnets reach the internet | Firewall/router egress |
| VGW | Virtual Private Gateway — how the VPC connects to on-prem over VPN | VPN endpoint |
| NAT Gateway | Lets private subnet instances reach the internet (outbound only) | NAT firewall rule |
| Security Group | Stateful firewall rules per EC2 instance | Host-based firewall |
| NACL | Network ACL — stateless rules per subnet | VLAN ACL |

---

## Subnet Types

```text
PUBLIC SUBNET                    PRIVATE SUBNET
─────────────────                ─────────────────
Has a route to IGW               No direct internet route
Instances can have public IPs    Instances use NAT Gateway
Used for: load balancers,        Used for: app servers,
          bastion hosts,                   databases,
          NAT Gateways                     internal services

Traffic in:  internet → IGW → subnet    Traffic in:  VPN → VGW → subnet
Traffic out: subnet → IGW → internet    Traffic out: subnet → NAT GW → IGW → internet
```

---

## VPC to On-Premises — Connection Options

```text
YOUR DATA CENTRE                 AWS
─────────────────                ─────────────────────────
Core Network                     VPC
     │                                │
     │                                │
  VPN GW ═══ IPSec tunnel ══════► VGW (Virtual Private Gateway)
     │        (encrypted,             │
     │         over internet)         └── your private subnets
     │
     │
  Router ──── dedicated line ──► Direct Connect location
              (private, no           │
               public internet)      └── VGW or Transit Gateway

VPN:            cheaper, uses internet, easy to set up
Direct Connect: faster, private, more expensive, needs carrier
Both can run:   Direct Connect primary + VPN as failover
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

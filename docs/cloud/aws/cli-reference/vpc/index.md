---
tags:
  - aws
---
# VPC & Networking


<div class="kb-summary">
VPC & networking CLI: `aws ec2 describe-vpcs`, `create-subnet`, `describe-route-tables`, `authorize-security-group-ingress`, and peering/NAT gateway management.

*Applies to: AWS*
</div>

```text
┌──────────────────────────────────────────── AWS CLI — VPC ────────────────────────────────────────────┐
│                                                                                                       │
│  VPC CLI commands for network creation, subnets, routing, security groups, and peering.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                VPC and Subnet                │  │                   Routing                   │   │
│   │             create-vpc: new VPC              │  │              create-route-table             │   │
│   │             describe-vpcs: list              │  │           create-route: add route           │   │
│   │            create-subnet: segment            │  │            associate-route-table            │   │
│   │            describe-subnets: list            │  │           create-internet-gateway           │   │
│   │       modify-subnet-attribute: auto-ip       │  │           attach-internet-gateway           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VPC and subnets created first; route tables and IGW attached to enable connectivity                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Security Groups                │  │            Peering and Endpoints            │   │
│   │            create-security-group             │  │        create-vpc-peering-connection        │   │
│   │       authorize-security-group-ingress       │  │        accept-vpc-peering-connection        │   │
│   │       authorize-security-group-egress        │  │             create-vpc-endpoint             │   │
│   │        revoke-security-group-ingress         │  │            describe-vpc-endpoints           │   │
│   │           describe-security-groups           │  │       describe-vpc-peering-connections      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS VPC hardware (Nitro cards) · internet edge (IGW) · NAT GW · Transit Gateway                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  create-vpc      = Provisions new VPC with specified CIDR; no subnets yet                             │
│  modify-subnet-attribute= Enables auto-assign public IP on instance launch                            │
│  Security group  = Stateful virtual firewall on ENI; inbound + outbound rules                         │
│  authorize-ingress= Adds inbound allow rule to security group                                         │
│  VPC endpoint    = Gateway or interface endpoint for private AWS service access                       │
│  Gateway endpoint= S3 and DynamoDB only; free; route-table based                                      │
│  Interface endpoint= PrivateLink ENI for other services; costs per hour                               │
│  VPC peering     = Direct routing between two VPCs; no transitive routing                             │
│  Transit Gateway = Hub router for transitive VPC connectivity                                         │
│  Internet Gateway= Allows internet access for public subnet resources                                 │
│  NAT Gateway     = Outbound-only internet for private subnet resources                                │
│  Nitro card      = AWS-built network card handling VPC packet forwarding                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## See also

- [AWS CLI Reference](../index.md)
- [AWS Networking](../../networking/index.md)
- [AWS Security](../../security/index.md)

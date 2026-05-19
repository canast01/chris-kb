# Cloud

<div class="kb-summary">
Cloud infrastructure knowledge base covering AWS and Azure. Includes architecture, IAM, networking, compute, storage, monitoring, backup, security, governance, and cost management — with CLI references and operational procedures for both platforms.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="aws/">
  <strong>AWS</strong>
  <span>Amazon Web Services operations, services, and troubleshooting.</span>
</a>

<a class="kb-card" href="azure/">
  <strong>Azure</strong>
  <span>Microsoft Azure operations, services, and troubleshooting.</span>
</a>
</div>

```
┌──────────────────────────────────────── Cloud Infrastructure ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Cloud Management                                       │   │
│   │     AWS: Console · CloudWatch · CloudTrail · Organizations · Control Tower · Cost Explorer    │   │
│   │    Azure: Portal · Monitor · Log Analytics · Entra ID · Management Groups · Cost Management   │   │
│   │            AWS Config + Service Control Policies enforce governance across accounts           │   │
│   │               Azure Policy + Blueprints enforce governance across subscriptions               │   │
│   │           Both platforms expose REST APIs and CLIs (aws-cli / az-cli) for automation          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Governance, monitoring, and automation span all resources across both platforms                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   AWS IAM                    │  │             Azure Entra ID (AAD)            │   │
│   │      Users · groups · roles · policies       │  │     Users · groups · service principals     │   │
│   │     Policy: allow/deny on AWS resources      │  │     RBAC: role assignments on resources     │   │
│   │   STS: temporary credentials + AssumeRole    │  │     PIM: just-in-time privileged access     │   │
│   │      Federation: SAML 2.0 · OIDC · SSO       │  │      Conditional Access: MFA + location     │   │
│   │    Managed policies · SCPs · permissions     │  │   Service principals · managed identities   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identity controls who can access what — least-privilege IAM is the security foundation             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 AWS Compute                  │  │                Azure Compute                │   │
│   │      EC2: VMs — on-demand/reserved/spot      │  │     VMs: sizes — pay-as-you-go/reserved     │   │
│   │    Auto Scaling + ALB/NLB load balancers     │  │     VMSS + Azure Load Balancer / App GW     │   │
│   │      ECS/EKS: container and Kubernetes       │  │       AKS: managed Kubernetes clusters      │   │
│   │    Lambda: serverless function execution     │  │    Azure Functions: serverless execution    │   │
│   │    AMI: VM image; instance store/EBS root    │  │     Compute Gallery: VM image versioning    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Compute resources run inside VPCs (AWS) or VNets (Azure) for network isolation                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           AWS Storage & Networking           │  │          Azure Storage & Networking         │   │
│   │  S3: object storage, lifecycle, versioning   │  │     Blob Storage: hot/cool/archive tiers    │   │
│   │      EBS: block volumes attached to EC2      │  │     Managed Disks: block volumes for VMs    │   │
│   │    EFS/FSx: managed NFS and SMB services     │  │     Azure Files + NetApp Files (NFS/SMB)    │   │
│   │     VPC: subnets · SGs · NACLs · routes      │  │    VNet: subnets · NSGs · UDRs · peering    │   │
│   │     Route53 · CloudFront · WAF · Shield      │  │     Azure DNS · Front Door · WAF · DDoS     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hybrid connectivity links on-premises data centres to cloud resources                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Hybrid Connectivity                                      │   │
│   │    AWS Direct Connect · Azure ExpressRoute: dedicated private circuits to cloud (1/10 Gbps)   │   │
│   │        AWS Site-to-Site VPN · Azure VPN Gateway: IPsec tunnels over the public internet       │   │
│   │           VPC Peering · VNet Peering: private routing between cloud network segments          │   │
│   │          AWS Transit Gateway · Azure Virtual WAN: hub-and-spoke WAN topology at scale         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Cloud regions and availability zones; data centres owned and operated by AWS and Microsoft           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Region       = geographic area containing multiple isolated data centre clusters (AZs)               │
│  AZ           = Availability Zone; isolated data centre within a region for fault tolerance           │
│  IAM          = Identity and Access Management; controls who can call which AWS API actions           │
│  Entra ID     = Azure Active Directory; cloud identity for users and service principals               │
│  RBAC         = Role-Based Access Control; Azure permission model built on role assignments           │
│  STS          = AWS Security Token Service; issues temporary credentials for AssumeRole calls         │
│  EC2          = Elastic Compute Cloud; AWS virtual machines with many instance type families          │
│  VMSS         = Azure Virtual Machine Scale Set; auto-scaling pool of identical VMs                   │
│  VPC          = Virtual Private Cloud; isolated AWS network with subnets and route tables             │
│  VNet         = Azure Virtual Network; isolated Azure network with subnets and NSG rules              │
│  S3           = Simple Storage Service; AWS object store with 11 nines durability guarantee           │
│  NSG          = Network Security Group; Azure stateful firewall applied to subnets or NICs            │
│  SG           = Security Group; AWS stateful firewall applied to EC2 instances and ENIs               │
│  EKS          = Elastic Kubernetes Service; AWS managed Kubernetes control plane                      │
│  AKS          = Azure Kubernetes Service; Azure managed Kubernetes control plane                      │
│  Direct Connect= Dedicated private circuit from on-prem to AWS — bypasses public internet             │
│  ExpressRoute = Dedicated private circuit from on-prem to Azure — bypasses public internet            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

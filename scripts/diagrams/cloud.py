"""
Cloud (AWS, Azure) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

@kb_diagram(
    'cloud',
    'docs/cloud/index.md',
    'Cloud Infrastructure — AWS and Azure: IAM, compute, storage, networking, connectivity',
)
def cloud_infrastructure_overview():
    """Cloud Infrastructure Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99   # full-width, inner=95

    # Two-cloud layout
    AWS_L, AWS_R = 3, 50    # inner=46, MID=26
    AZ_L,  AZ_R  = 53, 99  # inner=45, MID=76

    AWS_MID = (AWS_L + AWS_R) // 2   # 26
    AZ_MID  = (AZ_L  + AZ_R)  // 2   # 76

    CONN_L, CONN_R = 3, 99

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'Cloud Infrastructure'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Cloud Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS: Console · CloudWatch · CloudTrail · Organizations · Control Tower · Cost Explorer')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Azure: Portal · Monitor · Log Analytics · Entra ID · Management Groups · Cost Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS Config + Service Control Policies enforce governance across accounts')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Azure Policy + Blueprints enforce governance across subscriptions')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Both platforms expose REST APIs and CLIs (aws-cli / az-cli) for automation')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Governance, monitoring, and automation span all resources across both platforms'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Identity & Access tier ────────────────────────────────────────────────
    lines.append(R(merge(bTop(AWS_L, AWS_R), bTop(AZ_L, AZ_R))))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AWS IAM'),
        bMid(AZ_L,  AZ_R,  'Azure Entra ID (AAD)'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Users · groups · roles · policies'),
        bMid(AZ_L,  AZ_R,  'Users · groups · service principals'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Policy: allow/deny on AWS resources'),
        bMid(AZ_L,  AZ_R,  'RBAC: role assignments on resources'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'STS: temporary credentials + AssumeRole'),
        bMid(AZ_L,  AZ_R,  'PIM: just-in-time privileged access'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Federation: SAML 2.0 · OIDC · SSO'),
        bMid(AZ_L,  AZ_R,  'Conditional Access: MFA + location'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Managed policies · SCPs · permissions'),
        bMid(AZ_L,  AZ_R,  'Service principals · managed identities'),
    )))
    lines.append(R(merge(bBot(AWS_L, AWS_R), bBot(AZ_L, AZ_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Identity controls who can access what — least-privilege IAM is the security foundation'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Compute tier ──────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(AWS_L, AWS_R), bTop(AZ_L, AZ_R))))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AWS Compute'),
        bMid(AZ_L,  AZ_R,  'Azure Compute'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'EC2: VMs — on-demand/reserved/spot'),
        bMid(AZ_L,  AZ_R,  'VMs: sizes — pay-as-you-go/reserved'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Auto Scaling + ALB/NLB load balancers'),
        bMid(AZ_L,  AZ_R,  'VMSS + Azure Load Balancer / App GW'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'ECS/EKS: container and Kubernetes'),
        bMid(AZ_L,  AZ_R,  'AKS: managed Kubernetes clusters'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Lambda: serverless function execution'),
        bMid(AZ_L,  AZ_R,  'Azure Functions: serverless execution'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AMI: VM image; instance store/EBS root'),
        bMid(AZ_L,  AZ_R,  'Compute Gallery: VM image versioning'),
    )))
    lines.append(R(merge(bBot(AWS_L, AWS_R), bBot(AZ_L, AZ_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute resources run inside VPCs (AWS) or VNets (Azure) for network isolation'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Storage & Networking tier ─────────────────────────────────────────────
    lines.append(R(merge(bTop(AWS_L, AWS_R), bTop(AZ_L, AZ_R))))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AWS Storage & Networking'),
        bMid(AZ_L,  AZ_R,  'Azure Storage & Networking'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'S3: object storage, lifecycle, versioning'),
        bMid(AZ_L,  AZ_R,  'Blob Storage: hot/cool/archive tiers'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'EBS: block volumes attached to EC2'),
        bMid(AZ_L,  AZ_R,  'Managed Disks: block volumes for VMs'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'EFS/FSx: managed NFS and SMB services'),
        bMid(AZ_L,  AZ_R,  'Azure Files + NetApp Files (NFS/SMB)'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'VPC: subnets · SGs · NACLs · routes'),
        bMid(AZ_L,  AZ_R,  'VNet: subnets · NSGs · UDRs · peering'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Route53 · CloudFront · WAF · Shield'),
        bMid(AZ_L,  AZ_R,  'Azure DNS · Front Door · WAF · DDoS'),
    )))
    lines.append(R(merge(bBot(AWS_L, AWS_R), bBot(AZ_L, AZ_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Hybrid connectivity links on-premises data centres to cloud resources'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Connectivity tier ─────────────────────────────────────────────────────
    lines.append(R(bTop(CONN_L, CONN_R)))
    lines.append(R(bMid(CONN_L, CONN_R, 'Hybrid Connectivity')))
    lines.append(R(bMid(CONN_L, CONN_R, 'AWS Direct Connect · Azure ExpressRoute: dedicated private circuits to cloud (1/10 Gbps)')))
    lines.append(R(bMid(CONN_L, CONN_R, 'AWS Site-to-Site VPN · Azure VPN Gateway: IPsec tunnels over the public internet')))
    lines.append(R(bMid(CONN_L, CONN_R, 'VPC Peering · VNet Peering: private routing between cloud network segments')))
    lines.append(R(bMid(CONN_L, CONN_R, 'AWS Transit Gateway · Azure Virtual WAN: hub-and-spoke WAN topology at scale')))
    lines.append(R(bBot(CONN_L, CONN_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Cloud regions and availability zones; data centres owned and operated by AWS and Microsoft'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Region       = geographic area containing multiple isolated data centre clusters (AZs)'))
    lines.append(txt_row('AZ           = Availability Zone; isolated data centre within a region for fault tolerance'))
    lines.append(txt_row('IAM          = Identity and Access Management; controls who can call which AWS API actions'))
    lines.append(txt_row('Entra ID     = Azure Active Directory; cloud identity for users and service principals'))
    lines.append(txt_row('RBAC         = Role-Based Access Control; Azure permission model built on role assignments'))
    lines.append(txt_row('STS          = AWS Security Token Service; issues temporary credentials for AssumeRole calls'))
    lines.append(txt_row('EC2          = Elastic Compute Cloud; AWS virtual machines with many instance type families'))
    lines.append(txt_row('VMSS         = Azure Virtual Machine Scale Set; auto-scaling pool of identical VMs'))
    lines.append(txt_row('VPC          = Virtual Private Cloud; isolated AWS network with subnets and route tables'))
    lines.append(txt_row('VNet         = Azure Virtual Network; isolated Azure network with subnets and NSG rules'))
    lines.append(txt_row('S3           = Simple Storage Service; AWS object store with 11 nines durability guarantee'))
    lines.append(txt_row('NSG          = Network Security Group; Azure stateful firewall applied to subnets or NICs'))
    lines.append(txt_row('SG           = Security Group; AWS stateful firewall applied to EC2 instances and ENIs'))
    lines.append(txt_row('EKS          = Elastic Kubernetes Service; AWS managed Kubernetes control plane'))
    lines.append(txt_row('AKS          = Azure Kubernetes Service; Azure managed Kubernetes control plane'))
    lines.append(txt_row('Direct Connect= Dedicated private circuit from on-prem to AWS — bypasses public internet'))
    lines.append(txt_row('ExpressRoute = Dedicated private circuit from on-prem to Azure — bypasses public internet'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws',
    'docs/cloud/aws/index.md',
    'AWS Platform Stack — IAM, Compute, Networking, Storage, DB, Security, Connectivity',
)
def aws_platform_stack():
    """AWS Platform Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    IA_L, IA_R =  3, 33;  IA_MID = (IA_L + IA_R) // 2
    CP_L, CP_R = 36, 66;  CP_MID = (CP_L + CP_R) // 2
    NW_L, NW_R = 69, 99;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R =  3, 33
    DB_L, DB_R = 36, 66
    SC_L, SC_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'AWS Platform Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Console · CloudWatch · CloudTrail · Organizations · Control Tower · Cost Explorer')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS Config: resource compliance rules · SCPs: account-level permission guardrails')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Trusted Advisor: cost, security, and performance best-practice checks')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS CLI · SDK (boto3) · CloudFormation · CDK: infrastructure as code')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Governance and automation span all AWS services and accounts'))
    lines.append(txt_row())
    lines.append(R(arrow([IA_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(IA_L, IA_R), bTop(CP_L, CP_R), bTop(NW_L, NW_R))))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'AWS IAM'),
        bMid(CP_L, CP_R, 'Compute'),
        bMid(NW_L, NW_R, 'Networking'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'Users · groups · roles'),
        bMid(CP_L, CP_R, 'EC2: on-demand/reserved'),
        bMid(NW_L, NW_R, 'VPC: subnets · routing'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'Policies: allow/deny'),
        bMid(CP_L, CP_R, 'Auto Scaling · ALB/NLB'),
        bMid(NW_L, NW_R, 'SG · NACL: stateful FW'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'STS: temp credentials'),
        bMid(CP_L, CP_R, 'ECS · EKS: containers'),
        bMid(NW_L, NW_R, 'Route53: DNS service'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'AssumeRole: delegation'),
        bMid(CP_L, CP_R, 'Lambda: serverless FaaS'),
        bMid(NW_L, NW_R, 'CloudFront: global CDN'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'SAML 2.0 · OIDC · SSO'),
        bMid(CP_L, CP_R, 'Spot: spare capacity'),
        bMid(NW_L, NW_R, 'WAF · Shield: DDoS'),
    )))
    lines.append(R(merge(bBot(IA_L, IA_R), bBot(CP_L, CP_R), bBot(NW_L, NW_R))))

    lines.append(txt_row())
    lines.append(txt_row('  IAM controls access · EC2 runs inside VPCs · networking isolates workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([IA_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ST_L, ST_R), bTop(DB_L, DB_R), bTop(SC_L, SC_R))))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Storage'),
        bMid(DB_L, DB_R, 'Database'),
        bMid(SC_L, SC_R, 'Security & Monitoring'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'S3: object + versioning'),
        bMid(DB_L, DB_R, 'RDS: managed relational'),
        bMid(SC_L, SC_R, 'GuardDuty: threat detect'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'EBS: block volumes (EC2)'),
        bMid(DB_L, DB_R, 'Aurora: MySQL/PostgreSQL'),
        bMid(SC_L, SC_R, 'Security Hub: findings'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'EFS: managed NFS share'),
        bMid(DB_L, DB_R, 'DynamoDB: serverless KV'),
        bMid(SC_L, SC_R, 'CloudTrail: API audit log'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'FSx: Windows/Lustre/ONTAP'),
        bMid(DB_L, DB_R, 'ElastiCache: Redis/Memcd'),
        bMid(SC_L, SC_R, 'Config: compliance rules'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Glacier: archive storage'),
        bMid(DB_L, DB_R, 'Redshift: data warehouse'),
        bMid(SC_L, SC_R, 'KMS: key management'),
    )))
    lines.append(R(merge(bBot(ST_L, ST_R), bBot(DB_L, DB_R), bBot(SC_L, SC_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Storage, databases, and security services consumed as fully managed APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([IA_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Hybrid & Multi-Account Connectivity')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Direct Connect: dedicated private circuit from on-premises to AWS (1/10 Gbps)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Site-to-Site VPN: IPsec tunnel over the public internet to a VPC endpoint')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Transit Gateway: hub-and-spoke router connecting VPCs and on-prem networks')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VPC Peering: private routing between two VPCs within or across regions')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global regions and availability zones; data centres owned and operated by Amazon'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IAM           = Identity and Access Management; controls which API actions a principal can call'))
    lines.append(txt_row('STS           = Security Token Service; issues temporary credentials via AssumeRole'))
    lines.append(txt_row('EC2           = Elastic Compute Cloud; virtual machines with hundreds of instance type families'))
    lines.append(txt_row('ECS           = Elastic Container Service; managed container orchestration on EC2 or Fargate'))
    lines.append(txt_row('EKS           = Elastic Kubernetes Service; AWS managed Kubernetes control plane'))
    lines.append(txt_row('Lambda        = Serverless function execution; event-driven, no server provisioning required'))
    lines.append(txt_row('VPC           = Virtual Private Cloud; isolated network with subnets, route tables, and gateways'))
    lines.append(txt_row('SG            = Security Group; stateful firewall applied to EC2 instances and ENIs'))
    lines.append(txt_row('S3            = Simple Storage Service; object store with 11 nines durability guarantee'))
    lines.append(txt_row('EBS           = Elastic Block Store; persistent block volumes for EC2; gp3 and io2 Block Express'))
    lines.append(txt_row('RDS           = Relational Database Service; managed MySQL, PostgreSQL, SQL Server, Oracle'))
    lines.append(txt_row('Route53       = AWS managed DNS; latency routing, geo-routing, and health-check failover'))
    lines.append(txt_row('CloudFront    = AWS CDN; caches content at 400+ global edge locations; integrates with WAF'))
    lines.append(txt_row('GuardDuty     = ML threat detection; analyses VPC Flow Logs, CloudTrail, and DNS logs'))
    lines.append(txt_row('Direct Connect= Dedicated private circuit from on-premises to AWS — bypasses public internet'))
    lines.append(txt_row('Transit Gateway= Hub-and-spoke router connecting multiple VPCs and Direct Connect/VPN links'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure',
    'docs/cloud/azure/index.md',
    'Azure Platform Stack — Entra ID, Compute, Networking, Storage, DB, Security',
)
def azure_platform_stack():
    """Azure Platform Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    ID_L, ID_R =  3, 33;  ID_MID = (ID_L + ID_R) // 2
    CP_L, CP_R = 36, 66;  CP_MID = (CP_L + CP_R) // 2
    NW_L, NW_R = 69, 99;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R =  3, 33
    DB_L, DB_R = 36, 66
    SC_L, SC_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Azure Platform Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Azure Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Portal · Azure Monitor · Log Analytics · Cost Management · Resource Manager · Policy')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Management Groups → Subscriptions → Resource Groups: hierarchical governance model')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Entra ID: cloud identity for users, apps, and workloads across the tenant')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'az CLI · Azure PowerShell · ARM templates · Bicep: infrastructure as code')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Governance and policy enforcement span all subscriptions and resource groups'))
    lines.append(txt_row())
    lines.append(R(arrow([ID_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ID_L, ID_R), bTop(CP_L, CP_R), bTop(NW_L, NW_R))))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Entra ID (Azure AD)'),
        bMid(CP_L, CP_R, 'Compute'),
        bMid(NW_L, NW_R, 'Networking'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Users · groups · app regs'),
        bMid(CP_L, CP_R, 'VMs: PAYG/reserved sizes'),
        bMid(NW_L, NW_R, 'VNet: subnets · peering'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'RBAC: role assignments'),
        bMid(CP_L, CP_R, 'VMSS: auto-scaling pool'),
        bMid(NW_L, NW_R, 'NSG: stateful FW on NICs'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'PIM: just-in-time access'),
        bMid(CP_L, CP_R, 'AKS: managed Kubernetes'),
        bMid(NW_L, NW_R, 'Azure DNS: managed DNS'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Conditional Access · MFA'),
        bMid(CP_L, CP_R, 'Functions: serverless FaaS'),
        bMid(NW_L, NW_R, 'Front Door: global CDN'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Service principals · MI'),
        bMid(CP_L, CP_R, 'App Service: PaaS host'),
        bMid(NW_L, NW_R, 'WAF · DDoS Protection'),
    )))
    lines.append(R(merge(bBot(ID_L, ID_R), bBot(CP_L, CP_R), bBot(NW_L, NW_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Entra ID controls access · VMs run inside VNets · NSGs enforce network policy'))
    lines.append(txt_row())
    lines.append(R(arrow([ID_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ST_L, ST_R), bTop(DB_L, DB_R), bTop(SC_L, SC_R))))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Storage'),
        bMid(DB_L, DB_R, 'Database'),
        bMid(SC_L, SC_R, 'Security & Monitoring'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Blob: hot/cool/archive'),
        bMid(DB_L, DB_R, 'Azure SQL: managed MSSQL'),
        bMid(SC_L, SC_R, 'Defender for Cloud: CSPM'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Managed Disks: block VMs'),
        bMid(DB_L, DB_R, 'Cosmos DB: multi-model'),
        bMid(SC_L, SC_R, 'Sentinel: SIEM + SOAR'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Azure Files: NFS/SMB'),
        bMid(DB_L, DB_R, 'PostgreSQL: managed PG'),
        bMid(SC_L, SC_R, 'Key Vault: secrets+certs'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'NetApp Files: enterprise'),
        bMid(DB_L, DB_R, 'Redis Cache: in-memory'),
        bMid(SC_L, SC_R, 'Policy: compliance scan'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'ADLS Gen2: analytics'),
        bMid(DB_L, DB_R, 'Synapse: data warehouse'),
        bMid(SC_L, SC_R, 'Monitor: metrics + logs'),
    )))
    lines.append(R(merge(bBot(ST_L, ST_R), bBot(DB_L, DB_R), bBot(SC_L, SC_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Storage, databases, and security services consumed as fully managed platform APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([ID_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Hybrid & Multi-Subscription Connectivity')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ExpressRoute: dedicated private circuit from on-premises to Azure (1/10 Gbps)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VPN Gateway: IPsec tunnels over the public internet to Azure VNets')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VNet Peering: private routing between VNets within or across regions')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Virtual WAN: hub-and-spoke WAN topology for global connectivity at scale')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure global regions and availability zones; data centres owned and operated by Microsoft'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Entra ID      = Azure Active Directory; cloud identity for users, devices, and service principals'))
    lines.append(txt_row('RBAC          = Role-Based Access Control; Azure permission model using role assignments on scopes'))
    lines.append(txt_row('PIM           = Privileged Identity Management; just-in-time privileged role activation'))
    lines.append(txt_row('VNet          = Azure Virtual Network; isolated network with subnets, NSGs, and route tables'))
    lines.append(txt_row('NSG           = Network Security Group; stateful firewall applied to subnets or individual NICs'))
    lines.append(txt_row('VMSS          = Virtual Machine Scale Set; auto-scaling pool of identical VMs'))
    lines.append(txt_row('AKS           = Azure Kubernetes Service; managed Kubernetes control plane and node pools'))
    lines.append(txt_row('Blob          = Azure Blob Storage; object store with hot, cool, and archive access tiers'))
    lines.append(txt_row('Managed Disks = Azure block volumes for VMs; Premium SSD, Standard SSD, and Ultra Disk'))
    lines.append(txt_row('ExpressRoute  = Dedicated private circuit from on-prem to Azure — bypasses public internet'))
    lines.append(txt_row('Virtual WAN   = Azure hub-and-spoke WAN; connects VNets, branches, and on-premises at scale'))
    lines.append(txt_row('Defender      = Microsoft Defender for Cloud; CSPM and workload protection for Azure resources'))
    lines.append(txt_row('Sentinel      = Azure cloud-native SIEM; ingests logs, correlates alerts, automates response'))
    lines.append(txt_row('Key Vault     = Azure managed secret store; stores keys, certificates, and connection strings'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-architecture',
    'docs/cloud/aws/architecture/index.md',
    'AWS Architecture Overview — multi-account, Organizations, SCPs, TGW, IAM Identity Center',
)
def aws_architecture_overview():
    """AWS Architecture Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Platform Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Platform Architecture — Multi-Account Organisation with Hub-and-Spoke Networking')))
    lines.append(R(bMid(IV_L, IV_R, 'Management Account: AWS Organizations root · SCPs · IAM Identity Center SSO · billing')))
    lines.append(R(bMid(IV_L, IV_R, 'Networking: Transit Gateway hub connects spoke VPCs across accounts and on-premises via')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload accounts: dedicated member accounts per environment (dev/staging/prod) or per team')))
    lines.append(R(bMid(IV_L, IV_R, 'Guardrails: SCPs (preventive) + AWS Config (detective) + Security Hub (aggregated compliance)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management account controls governance · networking hub connects spokes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Organizations: root + OUs'),
        bMid(B2_L, B2_R, 'On-prem: DirectConnect'),
        bMid(B3_L, B3_R, 'Account structure: OU layout'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM Identity Center: SSO'),
        bMid(B2_L, B2_R, 'IdP: Azure AD / Okta SAML'),
        bMid(B3_L, B3_R, 'Tagging: env+owner+team'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Transit Gateway: hub-spoke'),
        bMid(B2_L, B2_R, 'Monitoring: CloudWatch/SIEM'),
        bMid(B3_L, B3_R, 'Naming: account + resource'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SCPs: OU-level guardrails'),
        bMid(B2_L, B2_R, 'Security: GuardDuty+Hub'),
        bMid(B3_L, B3_R, 'Security baselines: CIS AWS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Config: resource inventory'),
        bMid(B2_L, B2_R, 'Billing: CUR + Cost Expl.'),
        bMid(B3_L, B3_R, 'No workloads in mgmt acct'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines OU layout and networking · Integrations connect IdP and on-prem'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Account Layer', 'Networking', 'Identity', 'Guardrails', 'Observability'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mgmt account', 'Transit Gateway', 'IAM Identity Ctr', 'SCPs on OUs', 'CloudTrail org'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Audit account', 'VPC per account', 'SSO groups', 'AWS Config', 'CloudWatch logs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Log archive acct', 'DirectConnect', 'Permission sets', 'Security Hub', 'Cost Explorer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workload accounts', 'VPC Endpoints', 'MFA enforced', 'GuardDuty org', 'Budgets+alerts'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · Availability Zones · Data Centres · Global backbone · DirectConnect physical ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Organizations = AWS service for multi-account management; root contains management account and OUs'))
    lines.append(txt_row('OU            = Organisational Unit; logical grouping of accounts; SCPs applied at OU level'))
    lines.append(txt_row('SCP           = Service Control Policy; preventive guardrail; restricts what actions accounts can'))
    lines.append(txt_row('IAM Identity Center= AWS SSO service; assigns permission sets to users/groups in member accounts'))
    lines.append(txt_row('Transit Gateway= Regional hub router; connects VPCs across accounts and to on-premises via DX/VPN'))
    lines.append(txt_row('DirectConnect = Dedicated private network connection from on-premises to AWS; bypasses internet'))
    lines.append(txt_row('AWS Config    = Tracks resource configuration history; evaluates rules; records compliance state'))
    lines.append(txt_row('Security Hub  = Aggregates findings from GuardDuty, Inspector, Config; scores security posture'))
    lines.append(txt_row('GuardDuty     = Threat detection service; analyses CloudTrail, VPC Flow Logs, DNS logs for threats'))
    lines.append(txt_row('CUR           = Cost and Usage Report; detailed billing data for chargeback and FinOps analysis'))
    lines.append(txt_row('Permission set= IAM Identity Center policy assigned to a user/group for a specific member account'))
    lines.append(txt_row('Management account= Root of the AWS Organization; no workloads; used for billing and org-level policy'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-backup',
    'docs/cloud/aws/backup/index.md',
    'AWS Backup Overview — Backup Plans, Vaults, Vault Lock, jobs, restore testing, compliance',
)
def aws_backup_overview():
    """AWS Backup Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Backup Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Backup — Centralised Backup Management Across AWS Services')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup Plans: define schedules, lifecycle, copy rules, and resource assignments per service')))
    lines.append(R(bMid(IV_L, IV_R, 'Supported resources: EC2 · EBS · RDS · Aurora · DynamoDB · EFS · FSx · S3 · Storage Gateway')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup Vaults: encrypted storage for recovery points; Vault Lock enforces immutable retention')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance: backup reports via Audit Manager; cross-region and cross-account copy supported')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Backup Plans trigger jobs · Jobs produce recovery points in Vaults · compliance validates coverage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Backup Plans'),
        bMid(B2_L, B2_R, 'Backup Vaults'),
        bMid(B3_L, B3_R, 'Backup Jobs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rules: schedule + window'),
        bMid(B2_L, B2_R, 'KMS-encrypted storage'),
        bMid(B3_L, B3_R, 'Status: Completed/Failed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lifecycle: warm → cold'),
        bMid(B2_L, B2_R, 'Vault Lock: WORM policy'),
        bMid(B3_L, B3_R, 'Monitor: EventBridge events'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resource assignment: tag'),
        bMid(B2_L, B2_R, 'Cross-region copy vault'),
        bMid(B3_L, B3_R, 'Alerts: CloudWatch alarms'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Copy rules: X-region/acct'),
        bMid(B2_L, B2_R, 'Access policy: IAM+vault'),
        bMid(B3_L, B3_R, 'Restore testing: monthly'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Retention: daily/wk/mo/yr'),
        bMid(B2_L, B2_R, 'Recovery point: RPO time'),
        bMid(B3_L, B3_R, 'Compliance: Audit Manager'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Plans define schedules · Vaults store recovery points securely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Backup Plans', 'Backup Vaults', 'Backup Jobs', 'Restore Testing', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Daily + weekly', 'KMS key assign', 'Monitor status', 'Restore by RPO', 'Audit reports'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cold lifecycle', 'Vault Lock WORM', 'Failed: retry?', 'Test validation', 'Coverage gaps'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tag-based assign', 'X-region vault', 'EventBridge hook', 'RTO verify', 'Backup report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Org-level plan', 'Access policy', 'Alert on failure', 'Compliance test', 'Org framework'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · S3-backed Backup Vaults · EC2/EBS/RDS source resources · KMS key infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Plan    = Policy that defines backup rules: schedule, lifecycle, copy destinations, retention'))
    lines.append(txt_row('Backup Vault   = Encrypted container for recovery points; access controlled by vault policy + IAM'))
    lines.append(txt_row('Vault Lock     = WORM protection on a vault; prevents deletion even by account root; compliance mode'))
    lines.append(txt_row('Recovery Point = Snapshot/backup of a resource at a point in time; stored in vault; restorable'))
    lines.append(txt_row('Backup Job     = Single backup execution; status tracked as Pending/Running/Completed/Failed/Aborted'))
    lines.append(txt_row('Restore Job    = Recovery of a resource from a recovery point; creates a new resource copy'))
    lines.append(txt_row('RPO            = Recovery Point Objective; maximum age of backup acceptable for restore after failure'))
    lines.append(txt_row('RTO            = Recovery Time Objective; maximum acceptable time to restore service after failure'))
    lines.append(txt_row('Lifecycle rule = Moves recovery points from warm (standard) to cold (cheaper) storage after N days'))
    lines.append(txt_row('X-region copy  = Cross-region replication of recovery points for DR; configured in backup plan rule'))
    lines.append(txt_row('Audit Manager  = AWS service generating backup compliance reports against defined frameworks'))
    lines.append(txt_row('Backup Compliance Report= scheduled report showing backup coverage, job success rates, and gaps'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-cli',
    'docs/cloud/aws/cli-reference/index.md',
    'AWS CLI Reference — CLI v2, profiles, assume-role, ec2/s3/iam/rds/eks commands',
)
def aws_cli_reference():
    """AWS CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS CLI Reference'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS CLI — Command-Line Interface for AWS Service Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Structured as: aws <service> <command> [--options] — e.g. aws ec2 describe-instances')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth: profiles in ~/.aws/credentials; assume-role; IAM Identity Center SSO login')))
    lines.append(R(bMid(IV_L, IV_R, 'Output formats: --output json (default) | table | text | yaml | yaml-stream')))
    lines.append(R(bMid(IV_L, IV_R, 'Pagination: --max-items / --starting-token; or --no-paginate for full result sets')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  AWS CLI organises commands by service — EC2, S3, IAM, RDS, EKS, SSM, CloudFormation, CloudWatch'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Compute (EC2/Lambda)'),
        bMid(B2_L, B2_R, 'Storage (S3/EBS/EFS)'),
        bMid(B3_L, B3_R, 'Identity (IAM/SSO)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ec2 describe-instances'),
        bMid(B2_L, B2_R, 's3 ls / cp / sync / rm'),
        bMid(B3_L, B3_R, 'iam list-users/roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ec2 start/stop-instances'),
        bMid(B2_L, B2_R, 'ec2 describe-volumes'),
        bMid(B3_L, B3_R, 'iam get-policy/document'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ec2 create-snapshot'),
        bMid(B2_L, B2_R, 'ec2 create-volume/attach'),
        bMid(B3_L, B3_R, 'sts assume-role'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'lambda invoke/list'),
        bMid(B2_L, B2_R, 'efs describe-filesystems'),
        bMid(B3_L, B3_R, 'sso login / logout'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ssm start-session'),
        bMid(B2_L, B2_R, 's3api head-bucket'),
        bMid(B3_L, B3_R, 'iam simulate-principal'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute CLI manages instances · Storage CLI handles S3/EBS/EFS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2 / SSM', 'S3', 'IAM', 'RDS / EKS', 'CloudWatch'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['describe-instances', 's3 sync src dst', 'list-roles', 'rds describe-db', 'get-metric-data'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ssm start-session', 's3api list-obj', 'assume-role', 'eks get-token', 'put-metric-alarm'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['run-instances', 'cp --recursive', 'create-policy', 'eks list-clusters', 'describe-alarms'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['send-command', 'rb --force', 'delete-role', 'rds failover-db', 'logs filter-log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · API endpoints (HTTPS) · IAM authentication layer · CloudShell or local workstation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AWS CLI v2     = Current CLI version; install via pip or official pkg; aws --version to verify'))
    lines.append(txt_row('Named profile  = ~/.aws/credentials named section; use --profile name or AWS_PROFILE env var'))
    lines.append(txt_row('assume-role    = sts assume-role --role-arn ... --role-session-name; exports temp credentials'))
    lines.append(txt_row('--query        = JMESPath filter on JSON output; e.g. --query "Instances[*].InstanceId"'))
    lines.append(txt_row('--filter       = Server-side filter; e.g. --filters "Name=tag:Env,Values=prod" on describe calls'))
    lines.append(txt_row('--output table = Formats JSON output as ASCII table for human-readable inspection in terminal'))
    lines.append(txt_row('aws configure  = Interactive setup; writes region, key ID, secret, and output format to ~/.aws'))
    lines.append(txt_row('sso login      = Initiates browser-based IAM Identity Center login; caches SSO token locally'))
    lines.append(txt_row('--dry-run      = Validates permissions without executing; useful for IAM policy troubleshooting'))
    lines.append(txt_row('CloudShell     = Browser-based shell in AWS console; pre-authenticated, no local install needed'))
    lines.append(txt_row('--no-paginate  = Retrieves all pages of a paginated result in a single command call'))
    lines.append(txt_row('--region       = Overrides default region for a single command; or set AWS_DEFAULT_REGION env var'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-compute',
    'docs/cloud/aws/compute/index.md',
    'AWS Compute Overview — EC2, AMI, instance types, Auto Scaling, Lambda, SSM',
)
def aws_compute_overview():
    """AWS Compute Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Compute Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Compute — EC2, Auto Scaling, Lambda, and Systems Manager Fleet Management')))
    lines.append(R(bMid(IV_L, IV_R, 'EC2: virtual machines in 400+ instance types across general, compute, memory, storage families')))
    lines.append(R(bMid(IV_L, IV_R, 'Auto Scaling: launch templates + scaling policies maintain desired capacity across AZs')))
    lines.append(R(bMid(IV_L, IV_R, 'Systems Manager: fleet management without SSH — session manager, patch manager, run command')))
    lines.append(R(bMid(IV_L, IV_R, 'Lambda: serverless functions; event-driven; up to 15 min timeout; 10 GB RAM; no servers to')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Compute spans persistent VMs (EC2), elastic fleets (ASG), and serverless (Lambda) managed by SSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EC2'),
        bMid(B2_L, B2_R, 'Auto Scaling'),
        bMid(B3_L, B3_R, 'Systems Manager'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Instance types: t/m/c/r/x'),
        bMid(B2_L, B2_R, 'Launch template: AMI+type'),
        bMid(B3_L, B3_R, 'Session Manager: no SSH'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AMI: OS + config snapshot'),
        bMid(B2_L, B2_R, 'Min / desired / max count'),
        bMid(B3_L, B3_R, 'Patch Manager: baselines'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EBS: root + data volumes'),
        bMid(B2_L, B2_R, 'Scaling policies: CPU/SQS'),
        bMid(B3_L, B3_R, 'Run Command: remote exec'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Instance profile: IAM role'),
        bMid(B2_L, B2_R, 'Health check: EC2 or ELB'),
        bMid(B3_L, B3_R, 'Inventory: installed SW'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metadata: IMDSv2 only'),
        bMid(B2_L, B2_R, 'Instance refresh: rolling'),
        bMid(B3_L, B3_R, 'Parameter Store: config'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  EC2 provides persistent VMs · Auto Scaling elastically manages fleets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2', 'Auto Scaling', 'Lambda', 'Systems Manager', 'Patch Manager'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Start / stop', 'Desired capacity', 'Runtime: py/js/go', 'Session: connect', 'Baseline: rules'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AMI: launch cfg', 'Scale in/out', 'Trigger: events', 'Run command', 'Patch: schedule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Snapshot: EBS', 'Launch template', 'CW Logs output', 'Inventory: list', 'Compliance: view'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resize: change typ', 'Instance refresh', 'X-acct trigger', 'Param Store: get', 'Reboot: post'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS bare-metal hosts · Nitro hypervisor · Availability Zones · VPC network · EBS storage fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EC2            = Elastic Compute Cloud; virtual machines running on AWS Nitro hypervisor'))
    lines.append(txt_row('AMI            = Amazon Machine Image; snapshot of OS + config used to launch new EC2 instances'))
    lines.append(txt_row('Instance type  = Defines vCPU, RAM, network, and storage; families: t (burstable), m (general), c'))
    lines.append(txt_row('Launch template= Versioned EC2 config (AMI, type, SG, IAM, user-data) used by ASG and manual launches'))
    lines.append(txt_row('Auto Scaling Group= Maintains desired instance count; replaces unhealthy; scales on policies or'))
    lines.append(txt_row('Instance profile= IAM role attached to EC2; grants AWS API permissions to the instance itself'))
    lines.append(txt_row('IMDSv2         = Instance Metadata Service v2; token-based; required; prevents SSRF metadata theft'))
    lines.append(txt_row('Session Manager= SSM feature replacing SSH; browser or CLI access; no inbound ports needed on SG'))
    lines.append(txt_row('Patch Manager  = SSM feature applying OS patches on schedule; records compliance per instance'))
    lines.append(txt_row('Run Command    = SSM feature executing scripts/commands on fleets without SSH; output to CloudWatch'))
    lines.append(txt_row('Lambda         = Serverless compute; no servers to manage; billed per invocation and duration (ms)'))
    lines.append(txt_row('EBS            = Elastic Block Store; persistent block volumes attached to EC2; survives instance'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-cost',
    'docs/cloud/aws/cost/index.md',
    'AWS Cost Management — Cost Explorer, Budgets, Reserved Instances, Savings Plans',
)
def aws_cost_management():
    """AWS Cost Management — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Cost Management'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Cost Management — Visibility, Optimisation, and Governance')))
    lines.append(R(bMid(IV_L, IV_R, 'Cost Explorer: historical and forecasted spend by service, account, region, and tag')))
    lines.append(R(bMid(IV_L, IV_R, 'Budgets: threshold alerts via email or SNS; action budgets can auto-apply IAM policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Reserved Instances + Savings Plans: commit to 1 or 3 years for up to 72% discount on EC2/RDS')))
    lines.append(R(bMid(IV_L, IV_R, 'Cost Anomaly Detection: ML-based; detects unexpected spend spikes and notifies immediately')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Visibility (Explorer/CUR) feeds optimisation (RI/SP) and governance (Budgets/Anomaly/Tags)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cost Explorer'),
        bMid(B2_L, B2_R, 'Budgets'),
        bMid(B3_L, B3_R, 'Optimisation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service breakdowns: daily'),
        bMid(B2_L, B2_R, 'Cost threshold: $+alert'),
        bMid(B3_L, B3_R, 'Reserved Instances: 1/3yr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Account + region filters'),
        bMid(B2_L, B2_R, 'Usage budget: unit+alert'),
        bMid(B3_L, B3_R, 'Savings Plans: compute'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Tag-based chargeback'),
        bMid(B2_L, B2_R, 'Action budget: IAM deny'),
        bMid(B3_L, B3_R, 'Spot Instances: -90% cost'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rightsizing: recommendations'),
        bMid(B2_L, B2_R, 'Forecast: alert at 80%'),
        bMid(B3_L, B3_R, 'Anomaly Detection: ML'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CUR: hourly cost detail'),
        bMid(B2_L, B2_R, 'SNS: alert notification'),
        bMid(B3_L, B3_R, 'Cost alloc tags: billing'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Cost Explorer provides visibility · Budgets alert on thresholds · Optimisation reduces total spend'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cost Explorer', 'Budgets', 'RI / Savings', 'Anomaly', 'Tags'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['By service: EC2', 'Monthly limit', 'RI coverage %', 'ML alert: spike', 'Activate tags'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['By account: all', 'Forecast alert', 'SP utilisation', 'Investigate: who', 'Cost alloc tag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Rightsizing recs', 'Action budget', 'RI renewal: when', 'Anomaly report', 'Chargeback: team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Forecast: 3mo', 'SNS notify', 'Spot: savings', 'Suppress: known', 'Tagging policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS billing infrastructure · CUR data in S3 · Cost Explorer API · Budget notifications via SNS/email'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cost Explorer   = AWS console and API tool for analysing spend trends by service, account, tag,'))
    lines.append(txt_row('CUR             = Cost and Usage Report; detailed hourly billing data exported to S3 for FinOps tools'))
    lines.append(txt_row('Budget          = Spend threshold with alert and optional action; types: cost, usage, RI, Savings'))
    lines.append(txt_row('Action budget   = Budget that auto-applies SCPs or IAM policies when spend threshold is crossed'))
    lines.append(txt_row('Reserved Instance= 1 or 3-year commitment to EC2/RDS capacity; up to 72% discount vs on-demand'))
    lines.append(txt_row('Savings Plan    = Flexible commitment to $/hr compute spend; applies to EC2, Fargate, Lambda'))
    lines.append(txt_row('Spot Instance   = Unused EC2 capacity at up to 90% discount; can be reclaimed with 2-min notice'))
    lines.append(txt_row('RI Coverage     = Percentage of eligible usage hours covered by Reserved Instances; target >80%'))
    lines.append(txt_row('Cost alloc tag  = Resource tag activated in billing console; appears as column in Cost Explorer/CUR'))
    lines.append(txt_row('Chargeback      = Attributing AWS costs to business units or teams using cost allocation tags'))
    lines.append(txt_row('Anomaly Detection= ML model that learns normal spend patterns and alerts on statistically unexpected'))
    lines.append(txt_row('Rightsizing     = Cost Explorer recommendation to downsize underutilised EC2 or RDS instances'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-governance',
    'docs/cloud/aws/governance/index.md',
    'AWS Governance — Organizations, OUs, SCPs, AWS Config, tag policies, compliance',
)
def aws_governance_overview():
    """AWS Governance Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Governance Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Governance — Organizations, SCPs, Config, and Compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Organizations: root account > OUs > member accounts; SCPs enforced at each OU level')))
    lines.append(R(bMid(IV_L, IV_R, 'Service Control Policies: preventive guardrails; deny actions before IAM even evaluates them')))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Config: detective compliance; records every resource config change; evaluates rules')))
    lines.append(R(bMid(IV_L, IV_R, 'Tagging standards: mandatory tags enforced by Config rules; used for cost and compliance')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Organizations provides structure · SCPs prevent violations · Config detects drift'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AWS Organizations'),
        bMid(B2_L, B2_R, 'Service Control Policies'),
        bMid(B3_L, B3_R, 'AWS Config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Root: management acct'),
        bMid(B2_L, B2_R, 'JSON policy: allow/deny'),
        bMid(B3_L, B3_R, 'Config recorder: all types'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OUs: env / team / app'),
        bMid(B2_L, B2_R, 'OU-level attachment'),
        bMid(B3_L, B3_R, 'Rules: managed + custom'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Member accounts: isolated'),
        bMid(B2_L, B2_R, 'Deny: regions, services'),
        bMid(B3_L, B3_R, 'Compliance: pass/fail/N/A'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Consolidated billing'),
        bMid(B2_L, B2_R, 'Allow-list pattern: safe'),
        bMid(B3_L, B3_R, 'Remediation: auto/manual'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Account structure std.'),
        bMid(B2_L, B2_R, 'Guardrail: no root key'),
        bMid(B3_L, B3_R, 'Config: S3 delivery dest'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Organizations structures accounts · SCPs prevent bad actions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Organizations', 'SCPs', 'AWS Config', 'Tagging', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Create account', 'Attach to OU', 'Enable recorder', 'Mandatory tags', 'Audit reports'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Move to OU', 'Deny: eu-west', 'Add managed rule', 'Tag policy: org', 'Non-compliant?'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Invite accounts', 'Test: SCP sim', 'Remediation auto', 'Tagging standard', 'Security Hub'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Consolidated bill', 'Exception: allow', 'Delivery: S3+SNS', 'Cost alloc tags', 'Frameworks: CIS'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global infrastructure · Organizations API · Config delivery to S3 · CloudTrail audit trail'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Organizations   = AWS multi-account management service; enforces billing and governance hierarchy'))
    lines.append(txt_row('OU              = Organisational Unit; logical account grouping; SCPs attach at this level'))
    lines.append(txt_row('SCP             = Service Control Policy; max permission boundary for all IAM in attached accounts'))
    lines.append(txt_row('Preventive guardrail= SCP that blocks actions before IAM policy is evaluated; hard boundary'))
    lines.append(txt_row('Detective guardrail = Config rule that detects non-compliant resources after they exist'))
    lines.append(txt_row('Config recorder = Tracks configuration snapshots and changes for all or selected resource types'))
    lines.append(txt_row('Config rule     = Evaluates resource configs against defined conditions; managed or custom Lambda'))
    lines.append(txt_row('Remediation action= Auto-fix triggered by Config rule non-compliance; e.g. delete public S3 bucket'))
    lines.append(txt_row('Tag policy      = Organizations policy enforcing consistent tag keys/values across accounts'))
    lines.append(txt_row('Consolidated billing= Single bill for all accounts in org; volume discounts and RI sharing applies'))
    lines.append(txt_row('Account structure = Pattern of management/audit/log-archive/workload accounts following landing zone'))
    lines.append(txt_row('SCP allow-list   = Deny-all-except pattern; safer than deny-list; only permits explicitly listed'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-identity',
    'docs/cloud/aws/identity/index.md',
    'AWS Identity — IAM, roles, policies, IAM Identity Center SSO, Access Analyzer',
)
def aws_identity_overview():
    """AWS Identity Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Identity Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Identity — IAM, IAM Identity Center, and Permission Management')))
    lines.append(R(bMid(IV_L, IV_R, 'IAM: every AWS API call is authenticated via IAM; roles preferred over long-lived user keys')))
    lines.append(R(bMid(IV_L, IV_R, 'IAM Identity Center: SSO for AWS console and CLI; groups mapped to permission sets in accounts')))
    lines.append(R(bMid(IV_L, IV_R, 'Least privilege: customer-managed policies + Permission Boundaries limit blast radius')))
    lines.append(R(bMid(IV_L, IV_R, 'Review cycle: Access Analyzer, Access Advisor, Credential Report — quarterly permission review')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  IAM authenticates every API call · Identity Center enables SSO'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM'),
        bMid(B2_L, B2_R, 'IAM Identity Center'),
        bMid(B3_L, B3_R, 'Access Control'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Roles: EC2, Lambda, X-acct'),
        bMid(B2_L, B2_R, 'SSO: browser + CLI login'),
        bMid(B3_L, B3_R, 'Permission Boundary'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policies: managed+inline'),
        bMid(B2_L, B2_R, 'Groups → permission sets'),
        bMid(B3_L, B3_R, 'Resource policies: S3/KMS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Trust policy: who assumes'),
        bMid(B2_L, B2_R, 'IdP: Azure AD / Okta'),
        bMid(B3_L, B3_R, 'Access Analyzer: external'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Access keys: rotate/delete'),
        bMid(B2_L, B2_R, 'Permission sets: scoped'),
        bMid(B3_L, B3_R, 'Access Advisor: last used'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cross-acct: sts assume'),
        bMid(B2_L, B2_R, 'Assignment: user+acct+set'),
        bMid(B3_L, B3_R, 'Credential Report: audit'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  IAM manages roles and policies · Identity Center enables SSO'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IAM', 'IAM Roles', 'IAM Policies', 'Access Keys', 'Cross-Account'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['List users', 'Trust policy', 'Managed: AWS', 'Rotate 90d', 'Trust: sts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Password policy', 'EC2 profile', 'Managed: custom', 'Delete unused', 'assume-role'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: enforce', 'X-acct assume', 'Inline: tight', 'Inventory: all', 'External ID'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Credential report', 'Lambda role', 'Boundary: max', 'Cred report', 'Session tags'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS IAM global service · IAM Identity Center in management account · STS regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IAM Role       = Identity with trust policy; assumed by services, users, or other accounts for temp'))
    lines.append(txt_row('Trust policy   = JSON document on a role defining who can call sts:AssumeRole on it'))
    lines.append(txt_row('Permission Boundary= IAM policy limiting maximum permissions a role or user can have; reduces blast'))
    lines.append(txt_row('IAM Identity Center= AWS SSO; centralises human access to accounts via groups and permission sets'))
    lines.append(txt_row('Permission set = Collection of IAM policies assigned to a user/group for one or more accounts via SSO'))
    lines.append(txt_row('Access Analyzer= Identifies resources shared outside the account or org; detects unintended external'))
    lines.append(txt_row('Access Advisor  = Shows last service access dates per role; helps prune unused permissions'))
    lines.append(txt_row('Credential Report= CSV listing all IAM users, key age, MFA status, and last login per account'))
    lines.append(txt_row('Instance profile= IAM role wrapper for EC2; metadata endpoint exposes temporary credentials to the OS'))
    lines.append(txt_row('Cross-account role= Role in account B trusted by account A; enables resource sharing without key'))
    lines.append(txt_row('STS            = Security Token Service; issues temporary credentials for assume-role and federation'))
    lines.append(txt_row('External ID    = Secret added to cross-account trust policy; prevents confused deputy attacks'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-monitoring',
    'docs/cloud/aws/monitoring/index.md',
    'AWS Monitoring — CloudWatch metrics/logs/alarms, CloudTrail, EventBridge, AWS Health',
)
def aws_monitoring_overview():
    """AWS Monitoring Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Monitoring Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Monitoring — CloudWatch, CloudTrail, and EventBridge')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudWatch: metrics, logs, alarms, dashboards — native to every AWS service; no agent for')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudWatch Agent: installs on EC2 for OS-level metrics (memory, disk) and custom log forwarding')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudTrail: API audit log; every AWS API call recorded; multi-region trail ships to S3 +')))
    lines.append(R(bMid(IV_L, IV_R, 'EventBridge: event bus routing rules to targets (Lambda, SNS, SQS, Step Functions,')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  CloudWatch collects metrics/logs · CloudTrail audits API calls'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CloudWatch'),
        bMid(B2_L, B2_R, 'CloudTrail'),
        bMid(B3_L, B3_R, 'EventBridge'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metrics: service built-in'),
        bMid(B2_L, B2_R, 'API calls: all services'),
        bMid(B3_L, B3_R, 'Event bus: default + custom'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Logs: groups + retention'),
        bMid(B2_L, B2_R, 'Multi-region trail: org'),
        bMid(B3_L, B3_R, 'Rules: event pattern match'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alarms: threshold → SNS'),
        bMid(B2_L, B2_R, 'S3: log delivery + lock'),
        bMid(B3_L, B3_R, 'Targets: Lambda/SQS/SNS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboards: metric tiles'),
        bMid(B2_L, B2_R, 'Log integrity validation'),
        bMid(B3_L, B3_R, 'Schedule: cron-like rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metric filters: log→metric'),
        bMid(B2_L, B2_R, 'Athena: query trail logs'),
        bMid(B3_L, B3_R, 'X-acct event bus pipe'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  CloudWatch collects and alerts · CloudTrail records who did what · EventBridge automates responses'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CloudWatch', 'CW Logs', 'CW Alarms', 'CloudTrail', 'EventBridge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Metric: CPUUtil', 'Log group: 30d', 'Alarm: CPU>80%', 'Org trail: all', 'Rule: EC2 stop'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Dashboard: ops', 'Metric filter', 'Action: SNS', 'S3 delivery', 'Target: Lambda'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Agent: mem/disk', 'Insights: query', 'Composite alarm', 'Athena query', 'Schedule rule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AWS Health: svc', 'Subscription flt', 'OK → ALARM', 'Integrity check', 'X-acct pipe'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS CloudWatch backend · S3 for CloudTrail · EventBridge event bus infrastructure · SNS topics'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CloudWatch metrics = Time-series data from AWS services; 1-min granularity; stored 15 months'))
    lines.append(txt_row('Log group         = CloudWatch Logs container for streams; retention 1 day–10 years or indefinite'))
    lines.append(txt_row('Metric filter     = Extracts numeric values from log events and publishes them as CloudWatch metrics'))
    lines.append(txt_row('CW Alarm          = Watches a metric or expression; transitions OK/ALARM/INSUFFICIENT; triggers'))
    lines.append(txt_row('Composite alarm   = AND/OR combination of alarms; reduces alert noise from correlated conditions'))
    lines.append(txt_row('CloudTrail        = Records management events (API calls) and optionally data events (S3/Lambda)'))
    lines.append(txt_row('Org trail         = Single CloudTrail covering all accounts in the AWS Organization; recommended'))
    lines.append(txt_row('Log file integrity= CloudTrail SHA-256 hash validation; detects tampered or deleted log files'))
    lines.append(txt_row('EventBridge rule  = Pattern-matches incoming events and routes them to one or more targets'))
    lines.append(txt_row('AWS Health        = Service health and scheduled events for your specific AWS account and resources'))
    lines.append(txt_row('CloudWatch Agent  = Daemon on EC2/on-prem; collects OS metrics (memory, disk) and custom log files'))
    lines.append(txt_row('Logs Insights     = Interactive CloudWatch Logs query engine; KQL-like syntax; serverless execution'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-networking',
    'docs/cloud/aws/networking/index.md',
    'AWS Networking — VPC, subnets, SGs, NACLs, TGW, DirectConnect, VPC Endpoints, ALB',
)
def aws_networking_overview():
    """AWS Networking Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Networking Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Networking — VPC, Transit Gateway, Security, and Connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'VPC: isolated virtual network per account+region; CIDR block /16–/28; multi-AZ subnet design')))
    lines.append(R(bMid(IV_L, IV_R, 'Transit Gateway: regional hub connecting VPCs + DirectConnect + VPN; route tables per TGW')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: Security Groups (stateful, per-resource) + NACLs (stateless, per-subnet)')))
    lines.append(R(bMid(IV_L, IV_R, 'VPC Endpoints: private access to S3, DynamoDB, and 150+ services without internet gateway')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VPC is the foundation · TGW connects VPCs and on-prem · SGs+NACLs protect resources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VPC & Subnets'),
        bMid(B2_L, B2_R, 'Security Controls'),
        bMid(B3_L, B3_R, 'Connectivity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VPC: CIDR /16-/28'),
        bMid(B2_L, B2_R, 'Security Groups: stateful'),
        bMid(B3_L, B3_R, 'Internet Gateway: public'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Public subnet: IGW route'),
        bMid(B2_L, B2_R, 'NACLs: stateless + order'),
        bMid(B3_L, B3_R, 'NAT Gateway: private out'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Private subnet: no IGW'),
        bMid(B2_L, B2_R, 'Flow Logs: VPC traffic'),
        bMid(B3_L, B3_R, 'Transit Gateway: hub'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Route tables: subnet assoc'),
        bMid(B2_L, B2_R, 'Network Firewall: L7'),
        bMid(B3_L, B3_R, 'DirectConnect: private'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VPC Endpoints: private SVC'),
        bMid(B2_L, B2_R, 'WAF: ALB / CloudFront'),
        bMid(B3_L, B3_R, 'VPN: site-to-site IPsec'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VPC/subnets define the network · Security controls filter traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VPC', 'Subnets', 'Security Groups', 'Routing', 'Load Balancer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CIDR: plan /16', 'Public: AZ-a/b/c', 'Inbound rules', 'IGW route: 0/0', 'ALB: L7 HTTP/S'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow Logs: S3', 'Private: no IGW', 'Outbound rules', 'NAT: 0/0 priv', 'NLB: L4 TCP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DNS: enableDNS', 'Multi-AZ design', 'Ref by SG ID', 'TGW attachment', 'Route 53: DNS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Endpoint: S3/SVC', 'NACL: stateless', 'All-outbound: no', 'VPN: DX backup', 'Health checks'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS network fabric · Availability Zones · DirectConnect physical ports · Transit Gateway routers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VPC            = Virtual Private Cloud; logically isolated network within a region; one CIDR block'))
    lines.append(txt_row('Subnet         = CIDR subdivision of a VPC; lives in one AZ; public if route to IGW exists'))
    lines.append(txt_row('Security Group = Stateful firewall attached to ENI; return traffic automatically allowed'))
    lines.append(txt_row('NACL           = Network Access Control List; stateless; rules evaluated in order; both in and out'))
    lines.append(txt_row('Internet Gateway= Allows resources in public subnets to reach the internet; 1:1 to a VPC'))
    lines.append(txt_row('NAT Gateway    = Allows private subnet resources to initiate outbound internet; blocks inbound'))
    lines.append(txt_row('Transit Gateway= Regional router connecting VPCs and on-premises networks; route tables per TGW'))
    lines.append(txt_row('VPC Endpoint   = Private connection to AWS services (S3, DynamoDB, etc.) without leaving AWS network'))
    lines.append(txt_row('VPC Flow Logs  = Captures network flow metadata for VPC, subnet, or ENI; written to S3 or CW Logs'))
    lines.append(txt_row('DirectConnect  = Dedicated 1/10/100 Gbps private link from on-premises to AWS; lower latency than VPN'))
    lines.append(txt_row('ALB            = Application Load Balancer; Layer 7; supports path/host routing, WAF integration'))
    lines.append(txt_row('Route 53       = AWS managed DNS; supports public/private zones, health checks, failover routing'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-operations',
    'docs/cloud/aws/operations/index.md',
    'AWS Operations — health checks, procedures, Patch Manager, backup/restore, automation',
)
def aws_operations_overview():
    """AWS Operations Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Operations Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Operations — Health Checks, Procedures, Patching, and Automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Health Checks: EC2 status checks · RDS availability · CloudWatch alarm state · AWS Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Procedures: instance lifecycle, AMI management, EBS expansion, ASG scaling, RDS failover')))
    lines.append(R(bMid(IV_L, IV_R, 'Patching: Systems Manager Patch Manager applies OS patches on schedule; compliance reporting')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup/Restore: AWS Backup jobs · EBS snapshot restore · RDS point-in-time recovery')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks prevent failures · Procedures execute changes safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Health Checks'),
        bMid(B2_L, B2_R, 'Procedures'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EC2 status: 2/2 checks'),
        bMid(B2_L, B2_R, 'Start/stop/reboot EC2'),
        bMid(B3_L, B3_R, 'SSM Run Command: fleet'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RDS: available + IOPS'),
        bMid(B2_L, B2_R, 'Resize: instance type'),
        bMid(B3_L, B3_R, 'EventBridge: auto-trigger'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CW Alarms: OK vs ALARM'),
        bMid(B2_L, B2_R, 'EBS: extend + resize fs'),
        bMid(B3_L, B3_R, 'Lambda: remediation fn'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AWS Health: svc events'),
        bMid(B2_L, B2_R, 'ASG: refresh instances'),
        bMid(B3_L, B3_R, 'CloudFormation: IaC drift'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TGW + VPN: BGP sessions'),
        bMid(B2_L, B2_R, 'RDS failover: promote'),
        bMid(B3_L, B3_R, 'Step Functions: workflow'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks detect issues · Procedures resolve them'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Health Checks', 'Procedures', 'Patching', 'Backup/Restore', 'Scripts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2 2/2 OK?', 'AMI: create', 'Patch baseline', 'Backup job: run', 'CLI: describe'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CW alarms: OK', 'EBS: extend', 'Patch window', 'EBS snap restore', 'Boto3: boto3'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RDS: available', 'ASG: refresh', 'Compliance: view', 'RDS PITR', 'SSM scripts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AWS Health: evts', 'RDS failover', 'Reboot if needed', 'Cross-region: cp', 'CDK / TF'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 hosts on Nitro · EBS storage fabric · RDS managed infrastructure · AZs for HA · VPC networking'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 status checks = System check (AWS infra) + instance check (OS/app); both must pass (2/2)'))
    lines.append(txt_row('AWS Health        = Personalised service health and maintenance events for your account and resources'))
    lines.append(txt_row('Patch Manager     = SSM feature; applies OS patches per baseline; records compliance per instance'))
    lines.append(txt_row('Patch baseline    = Defines which patches to install; AWS-managed or custom per OS and severity'))
    lines.append(txt_row('AMI               = Amazon Machine Image; golden image snapshot; used for ASG instance refresh'))
    lines.append(txt_row('ASG instance refresh= Rolling replacement of instances in an ASG with a new launch template version'))
    lines.append(txt_row('EBS expansion     = Increase volume size; then extend filesystem (growpart + resize2fs or diskpart)'))
    lines.append(txt_row('RDS PITR          = Point-in-time recovery; restore RDS to any second within the retention window'))
    lines.append(txt_row('CloudFormation drift= Detects manual changes to stack resources not captured in the template'))
    lines.append(txt_row('Step Functions    = AWS serverless workflow orchestrator; chains Lambda, SSM, ECS tasks with retries'))
    lines.append(txt_row('Run Command       = SSM feature executing commands/scripts on EC2 fleet; no SSH or VPN needed'))
    lines.append(txt_row('EventBridge rule  = Triggers Lambda/SSM/SQS on schedule or event pattern; enables auto-remediation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-security',
    'docs/cloud/aws/security/index.md',
    'AWS Security — IAM IC SSO, MFA, KMS, Secrets Manager, ACM, GuardDuty, Security Hub',
)
def aws_security_overview():
    """AWS Security Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Security Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Security — Authentication, Encryption, and Threat Detection')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: IAM Identity Center SSO · MFA enforcement · no shared credentials; roles only')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: KMS for data-at-rest · ACM for TLS certificates · Secrets Manager for credentials')))
    lines.append(R(bMid(IV_L, IV_R, 'Threat detection: GuardDuty (ML-based) · Security Hub (posture) · Inspector (vulnerability')))
    lines.append(R(bMid(IV_L, IV_R, 'Preventive guardrails: SCPs limit service/region access · Config rules detect drift · WAF')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls access · Encryption protects data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Encryption'),
        bMid(B3_L, B3_R, 'Threat Detection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM Identity Center SSO'),
        bMid(B2_L, B2_R, 'KMS: CMK + AWS managed'),
        bMid(B3_L, B3_R, 'GuardDuty: ML threat'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'MFA: virtual or hardware'),
        bMid(B2_L, B2_R, 'Secrets Manager: rotate'),
        bMid(B3_L, B3_R, 'Security Hub: score'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Roles: no long-lived keys'),
        bMid(B2_L, B2_R, 'ACM: TLS certs managed'),
        bMid(B3_L, B3_R, 'Inspector: CVE scanning'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SCP: deny root actions'),
        bMid(B2_L, B2_R, 'S3: SSE-S3 / SSE-KMS'),
        bMid(B3_L, B3_R, 'Config: drift detection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Access Analyzer: review'),
        bMid(B2_L, B2_R, 'EBS/RDS: encrypt at rest'),
        bMid(B3_L, B3_R, 'WAF: ALB + CloudFront'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication + SCPs prevent access · Encryption protects data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Authentication', 'Access Control', 'Encryption', 'Hardening', 'Certificate Mgr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSO: IAM IC', 'Roles: least priv', 'KMS: CMK create', 'GuardDuty: org', 'ACM: request'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: enforce all', 'SCP: deny risky', 'Secrets: rotate', 'Security Hub', 'Auto-renew: yes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['No shared keys', 'Boundary: set', 'S3 SSE-KMS', 'Inspector: scan', 'ALB: TLS 1.2+'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IdP: SAML 2.0', 'Access Analyzer', 'EBS: encrypted', 'Config: rules', 'DNS valid: txt'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS security regions · KMS hardware security modules · CloudFront edge for WAF'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('KMS             = Key Management Service; create and manage CMKs for encryption across AWS services'))
    lines.append(txt_row('CMK             = Customer Managed Key; KMS key you control; used for S3, EBS, RDS, Secrets Manager'))
    lines.append(txt_row('Secrets Manager = Manages credentials, API keys, and passwords; auto-rotates via Lambda integration'))
    lines.append(txt_row('ACM             = AWS Certificate Manager; provisions and auto-renews TLS certificates for ALB/CF'))
    lines.append(txt_row('GuardDuty       = ML-based threat detection; analyses CloudTrail, VPC Flow Logs, and DNS logs'))
    lines.append(txt_row('Security Hub    = Aggregates findings; computes security score against CIS, PCI-DSS, AWS Foundational'))
    lines.append(txt_row('Inspector       = Automated vulnerability scanner for EC2 OS CVEs and container image vulnerabilities'))
    lines.append(txt_row('WAF             = Web Application Firewall; Layer 7 rules for ALB, API Gateway, and CloudFront'))
    lines.append(txt_row('SSE-KMS         = Server-side encryption with KMS CMK; allows key policy + CloudTrail audit of usage'))
    lines.append(txt_row('Permission Boundary= IAM policy capping maximum permissions; limits blast radius of over-provisioned'))
    lines.append(txt_row('Access Analyzer = IAM service that finds externally-accessible resources; generates least-priv'))
    lines.append(txt_row('IAM Identity Center= SSO for human access; enforces MFA; integrates with Okta/Azure AD via SAML/SCIM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-storage',
    'docs/cloud/aws/storage/index.md',
    'AWS Storage — EBS (gp3/io2), S3 (classes/lifecycle/replication), EFS, FSx',
)
def aws_storage_overview():
    """AWS Storage Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Storage Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Storage — EBS, S3, EFS, and FSx')))
    lines.append(R(bMid(IV_L, IV_R, 'EBS: persistent block volumes attached to EC2; types gp3/io2/sc1/st1; AZ-locked; snapshots to')))
    lines.append(R(bMid(IV_L, IV_R, 'S3: unlimited object storage; 11 nines durability; lifecycle, versioning, replication, and')))
    lines.append(R(bMid(IV_L, IV_R, 'EFS: managed NFS for Linux; multi-AZ shared filesystem; provisioned or bursting throughput')))
    lines.append(R(bMid(IV_L, IV_R, 'FSx: managed Windows SMB (FSx for Windows) and HPC Lustre (FSx for Lustre) file systems')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  EBS serves block I/O for EC2 · S3 stores objects durably · EFS/FSx serve shared file workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EBS'),
        bMid(B2_L, B2_R, 'S3'),
        bMid(B3_L, B3_R, 'EFS / FSx'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Types: gp3/io2/st1/sc1'),
        bMid(B2_L, B2_R, 'Buckets: region-scoped'),
        bMid(B3_L, B3_R, 'EFS: NFS v4.1 + 4.2'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IOPS: gp3=3K, io2=64K'),
        bMid(B2_L, B2_R, 'Storage classes: S/IA/GDA'),
        bMid(B3_L, B3_R, 'FSx Windows: SMB AD'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Encrypt: CMK default'),
        bMid(B2_L, B2_R, 'Versioning: protect objs'),
        bMid(B3_L, B3_R, 'FSx Lustre: HPC Gbps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Snapshots: S3-backed copy'),
        bMid(B2_L, B2_R, 'Lifecycle: tier+expire'),
        bMid(B3_L, B3_R, 'EFS: bursting throughput'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resize: online (no reboot)'),
        bMid(B2_L, B2_R, 'Replication: X-region'),
        bMid(B3_L, B3_R, 'Mount: NFS or DFS-N'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  EBS for EC2 block I/O · S3 for durable objects and lifecycle'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EBS', 'EBS Snapshots', 'S3', 'S3 Lifecycle', 'EFS / FSx'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['gp3: baseline', 'Create snap', 'Bucket: create', 'Transition rule', 'Mount target'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['io2: 64K IOPS', 'AMI from snap', 'Block public', 'Expire: delete', 'EFS SG rules'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resize: no stop', 'Cross-region cp', 'Object lock', 'IA: 30d+ infreq', 'FSx: AD join'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Encrypt at rest', 'Retention: policy', 'Replication: CRR', 'GDA: 90d+ cold', 'FSx backup'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EBS storage fabric (AZ-local) · S3 distributed storage (region) · EFS/FSx managed NAS infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EBS            = Elastic Block Store; persistent block volumes; AZ-locked; attach to one EC2 at a'))
    lines.append(txt_row('gp3            = General Purpose SSD v3; 3,000 IOPS and 125 MiB/s baseline; independently'))
    lines.append(txt_row('io2            = Provisioned IOPS SSD; up to 64,000 IOPS; 99.999% durability; multi-attach supported'))
    lines.append(txt_row('EBS Snapshot   = Incremental S3-backed copy of a volume; used for backup, AMI creation, region copy'))
    lines.append(txt_row('S3             = Simple Storage Service; object storage; buckets in a region; 11 nines durability'))
    lines.append(txt_row('S3 Storage Class= Tiers: Standard / Standard-IA / Glacier Instant / Glacier DA / Glacier Deep Archive'))
    lines.append(txt_row('S3 Lifecycle   = Rules transitioning objects between classes or expiring them after N days'))
    lines.append(txt_row('S3 Replication = CRR (cross-region) or SRR (same-region); requires versioning on source bucket'))
    lines.append(txt_row('EFS            = Elastic File System; serverless NFS; multi-AZ; auto-scales; mount via EFS mount'))
    lines.append(txt_row('FSx for Windows= Managed SMB file share with Active Directory integration; DFS namespace support'))
    lines.append(txt_row('FSx for Lustre = High-performance parallel file system; used for ML training and HPC workloads'))
    lines.append(txt_row('Object Lock    = S3 WORM; Governance or Compliance mode; prevents delete/overwrite for retention'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aws-troubleshooting',
    'docs/cloud/aws/troubleshooting/index.md',
    'AWS Troubleshooting — common issues, Policy Simulator, Reachability Analyzer, CloudTrail',
)
def aws_troubleshooting_overview():
    """AWS Troubleshooting Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Troubleshooting Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Troubleshooting — Common Issues, Diagnostics, and Escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: IAM permission denied · SG/NACL blocking traffic · EC2 instance unreachable')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: CloudWatch Logs · CloudTrail event history · VPC Flow Logs · EC2 serial console')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: AWS CLI describe commands · Policy Simulator · Reachability Analyzer · CloudShell')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: AWS Support cases; collect account ID, region, resource ARN, error message + time')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide investigation · Diagnostics locate root cause · Escalation engages AWS support'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EC2: 2/2 status fail'),
        bMid(B2_L, B2_R, 'CW Logs: app errors'),
        bMid(B3_L, B3_R, 'Account ID + region'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SG: port not open'),
        bMid(B2_L, B2_R, 'CloudTrail: API history'),
        bMid(B3_L, B3_R, 'Resource ARN: include'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM: Access Denied'),
        bMid(B2_L, B2_R, 'VPC Flow Logs: traffic'),
        bMid(B3_L, B3_R, 'Error message + time'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RDS: conn refused'),
        bMid(B2_L, B2_R, 'Policy Simulator: test'),
        bMid(B3_L, B3_R, 'Severity: P1-P4'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'S3: 403 on object'),
        bMid(B2_L, B2_R, 'Reachability Analyzer'),
        bMid(B3_L, B3_R, 'TAM: strategic issues'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Identify issue category → gather diagnostics (logs + trail + flow) → resolve or escalate with data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Escalation', 'CLI Tools', 'Console Tools'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2 unreachable', 'CW Logs: filter', 'P1: 24/7 phone', 'describe-sgs', 'Policy Simulator'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SG: missing rule', 'CloudTrail: who?', 'Case: open now', 'flow-logs: get', 'Reach Analyzer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IAM: denied', 'VPC Flow Logs', 'ARN + error msg', 'sts get-caller', 'EC2 serial con'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['S3: bucket ACL', 'Serial console', 'Trusted Advisor', 'ec2 describe', 'AWS Health evt'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 Nitro hosts · VPC network fabric · AWS Support infrastructure · CloudTrail S3 log delivery'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 status check = System check (infra) + instance check (OS); failure triggers alarm or'))
    lines.append(txt_row('Policy Simulator = IAM console tool; tests IAM policies to check if an action would be allowed/denied'))
    lines.append(txt_row('Reachability Analyzer= VPC tool; traces packet path between source and destination; finds blocking'))
    lines.append(txt_row('VPC Flow Logs   = Captures accepted/rejected traffic metadata for subnets, VPCs, or ENIs'))
    lines.append(txt_row('CloudTrail      = Records every AWS API call; start with event history for the last 90 days in'))
    lines.append(txt_row('EC2 Serial Console= Out-of-band console access; useful when SSH/SSM unreachable; OS-level triage'))
    lines.append(txt_row('Trusted Advisor  = AWS checks across cost, security, performance, fault tolerance, and service limits'))
    lines.append(txt_row('P1 case          = Production down; 24/7 response; call +1-800-xxx alongside opening console case'))
    lines.append(txt_row('TAM              = Technical Account Manager; named AWS contact for strategic and critical escalation'))
    lines.append(txt_row('sts get-caller-identity= CLI command returning current identity; first step when debugging IAM issues'))
    lines.append(txt_row('Session Manager  = SSM feature; connect to EC2 without SSH when networking is broken but SSM agent'))
    lines.append(txt_row('Access Denied    = IAM error; check CloudTrail for the denied call; use Policy Simulator to trace'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Azure sub-section diagrams ─────────────────────────────────────────────────

@kb_diagram(
    'azure-architecture',
    'docs/cloud/azure/architecture/index.md',
    'Azure Architecture Overview — tenant hierarchy, hub-spoke VNet, Entra ID, Availability Zones',
)
def azure_architecture_overview():
    """Azure Architecture Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Platform Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Platform Architecture — Management Hierarchy, Networking, and Identity')))
    lines.append(R(bMid(IV_L, IV_R, 'Hierarchy: Tenant > Management Groups > Subscriptions > Resource Groups > Resources')))
    lines.append(R(bMid(IV_L, IV_R, 'Networking: hub-and-spoke VNet peering; hub holds shared services (firewall, DNS, VPN gateway)')))
    lines.append(R(bMid(IV_L, IV_R, 'Identity: Entra ID (formerly Azure AD); SSO, MFA, Conditional Access, PIM for privileged roles')))
    lines.append(R(bMid(IV_L, IV_R, 'Guardrails: Azure Policy (detective + preventive) · RBAC · Management Group scope policies')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Hierarchy provides scope · Hub-spoke networking connects workloads · Entra ID governs all identity'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mgmt Groups: org scope'),
        bMid(B2_L, B2_R, 'ExpressRoute: on-prem'),
        bMid(B3_L, B3_R, 'Naming: RG + resource std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Subscriptions: isolation'),
        bMid(B2_L, B2_R, 'IdP: on-prem AD + Entra'),
        bMid(B3_L, B3_R, 'Tagging: env+owner+team'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hub VNet: shared services'),
        bMid(B2_L, B2_R, 'Monitoring: Azure Monitor'),
        bMid(B3_L, B3_R, 'Subscription design: prod'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Spoke VNets: workloads'),
        bMid(B2_L, B2_R, 'Security: Defender + SIEM'),
        bMid(B3_L, B3_R, 'Security baseline: CIS Az'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Availability Zones: 3 per'),
        bMid(B2_L, B2_R, 'Billing: Cost Management'),
        bMid(B3_L, B3_R, 'HA: zone + region pattern'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines hierarchy and networking · Integrations connect on-prem'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Hierarchy', 'Networking', 'Identity', 'Guardrails', 'Availability'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tenant: root', 'Hub VNet: fw', 'Entra ID: IdP', 'Policy: deny', 'Zones: 3 AZ'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mgmt Groups', 'Spoke: app', 'RBAC: scope', 'Initiative', 'Regions: pair'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Subscriptions', 'Peering: hub', 'PIM: JIT', 'Compliance', 'ASR: failover'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resource Groups', 'ExpressRoute', 'Cond. Access', 'RBAC assign', 'LB + AG: HA'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Regions · Availability Zones · Data Centres · Global WAN backbone · ExpressRoute physical ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Management Group  = Scope above subscriptions; policies and RBAC applied here cascade to all children'))
    lines.append(txt_row('Subscription      = Billing unit and access boundary; resources live inside subscriptions'))
    lines.append(txt_row('Resource Group    = Logical container for resources; lifecycle boundary; RBAC and policy scope'))
    lines.append(txt_row('Entra ID          = Microsoft cloud identity (formerly Azure AD); directory for users, groups, apps'))
    lines.append(txt_row('Hub-spoke VNet    = Hub has shared services (firewall, DNS); spokes peer to hub for connectivity'))
    lines.append(txt_row('VNet peering      = Private connectivity between VNets; traffic stays on Microsoft backbone'))
    lines.append(txt_row('ExpressRoute      = Dedicated private circuit from on-premises to Azure; Layer 2/3; bypasses internet'))
    lines.append(txt_row('Azure Policy      = Governance service; defines and enforces compliance rules across resource configs'))
    lines.append(txt_row('RBAC              = Role-Based Access Control; Owner/Contributor/Reader built-in + custom roles'))
    lines.append(txt_row('PIM               = Privileged Identity Management; just-in-time role activation; approval + audit'))
    lines.append(txt_row('Availability Zone = Physically separate DC within a region; independent power/cooling/networking'))
    lines.append(txt_row('Conditional Access = Entra ID policy engine; evaluates sign-in context to enforce MFA, block, or'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-backup-dr',
    'docs/cloud/azure/backup-dr/index.md',
    'Azure Backup & DR — Azure Backup, RSV, ASR replication, failover/failback, test failover',
)
def azure_backup_dr_overview():
    """Azure Backup and DR Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Backup and DR Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Backup and DR — Recovery Services Vault, Azure Backup, and Azure Site Recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Backup: VM, SQL, SAP, files, blobs — all via Recovery Services Vault; policy-driven')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Site Recovery (ASR): continuous replication; orchestrated failover + failback for VMs')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery Services Vault: central container for backup items and ASR replication configs')))
    lines.append(R(bMid(IV_L, IV_R, 'Restore testing: mandatory for RTO/RPO validation; test failover in isolated network (ASR)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Backup policies protect data · ASR replicates VMs for DR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Azure Backup'),
        bMid(B2_L, B2_R, 'Recovery Svc Vault'),
        bMid(B3_L, B3_R, 'Azure Site Recovery'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VM: daily + weekly'),
        bMid(B2_L, B2_R, 'GRS: geo-redundant'),
        bMid(B3_L, B3_R, 'Replication: Azure→Az'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SQL/SAP: log backup'),
        bMid(B2_L, B2_R, 'Soft delete: 14d'),
        bMid(B3_L, B3_R, 'RPO: ~30 seconds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Files/blobs: policy'),
        bMid(B2_L, B2_R, 'Immutability: WORM'),
        bMid(B3_L, B3_R, 'Failover: 1-click plan'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Backup jobs: monitor'),
        bMid(B2_L, B2_R, 'Access policy: RBAC'),
        bMid(B3_L, B3_R, 'Test failover: isolated'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Restore: disk or full VM'),
        bMid(B2_L, B2_R, 'Reports: backup health'),
        bMid(B3_L, B3_R, 'Failback: re-protect'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Backup protects point-in-time data · Vault stores recovery points · ASR enables DR orchestration'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Azure Backup', 'RSV', 'ASR', 'Restore Test', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VM: enable', 'GRS setting', 'Enable repltn', 'Test failover', 'Backup report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Policy: daily', 'Soft delete', 'RPO: monitor', 'Validate: app', 'Policy coverage'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Job: monitor', 'Immutability', 'Failover plan', 'RTO measured', 'Gaps: alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Restore: VM', 'RBAC: ops', 'Re-protect', 'Cleanup test', 'Audit: vault'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Storage (GRS vaults) · ASR replication infrastructure · paired regions · VM host fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Recovery Services Vault= Azure container for backup items and ASR replication configs; scoped per'))
    lines.append(txt_row('Azure Backup    = Managed backup for VMs, SQL, SAP, files, blobs; policy-driven; encrypted at rest'))
    lines.append(txt_row('Backup Policy   = Defines schedule (daily/weekly) and retention (daily/weekly/monthly/yearly)'))
    lines.append(txt_row('Soft delete     = 14-day recovery window after accidental backup item deletion; default enabled'))
    lines.append(txt_row('Immutability    = WORM policy on vault; prevents deletion of recovery points; compliance requirement'))
    lines.append(txt_row('GRS             = Geo-Redundant Storage; vault data replicated to paired region; 6 copies total'))
    lines.append(txt_row('Azure Site Recovery= Continuous replication of VMs to another region; orchestrated failover/failback'))
    lines.append(txt_row('RPO             = Recovery Point Objective; ASR achieves ~30s RPO for Azure-to-Azure VM replication'))
    lines.append(txt_row('Test failover   = ASR feature; spins up replica VM in isolated VNet; validates app without affecting'))
    lines.append(txt_row('Failback        = Re-protecting and reversing replication direction after a failover test or real'))
    lines.append(txt_row('Recovery plan   = ASR orchestration of failover order, scripts, and timing for multi-VM workloads'))
    lines.append(txt_row('Replication health= ASR metric; monitors churn rate, RPO breach, and agent connectivity on source VM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-cli',
    'docs/cloud/azure/cli-reference/index.md',
    'Azure CLI Reference — az login, az vm/storage/network/backup/identity commands',
)
def azure_cli_reference():
    """Azure CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure CLI Reference'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure CLI — az command-line tool for managing Azure resources')))
    lines.append(R(bMid(IV_L, IV_R, 'Structured as: az <group> <command> [--options] — e.g. az vm list --resource-group myRG')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth: az login (browser) · az login --service-principal · az account set --subscription <id>')))
    lines.append(R(bMid(IV_L, IV_R, 'Output formats: --output json (default) | table | tsv | yaml | none')))
    lines.append(R(bMid(IV_L, IV_R, 'Query: --query uses JMESPath; e.g. --query "[?powerState==`VM running`].name" -o tsv')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  az CLI organises by resource type — vm, network, storage, account, backup, monitor, identity, aks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Compute (VM/AKS)'),
        bMid(B2_L, B2_R, 'Storage / Disks'),
        bMid(B3_L, B3_R, 'Identity / Network'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm list/show/start'),
        bMid(B2_L, B2_R, 'az storage account ls'),
        bMid(B3_L, B3_R, 'az ad user/group list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm stop/deallocate'),
        bMid(B2_L, B2_R, 'az disk list/create'),
        bMid(B3_L, B3_R, 'az role assignment list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm resize/create'),
        bMid(B2_L, B2_R, 'az snapshot create'),
        bMid(B3_L, B3_R, 'az network vnet list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az aks get-credentials'),
        bMid(B2_L, B2_R, 'az storage blob up/down'),
        bMid(B3_L, B3_R, 'az network nsg rule list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm run-command'),
        bMid(B2_L, B2_R, 'az keyvault secret get'),
        bMid(B3_L, B3_R, 'az monitor alert list'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute CLI manages VMs/AKS · Storage CLI handles blobs and disks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Account', 'Virtual Machines', 'Storage', 'Networking', 'Backup / KV'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['az login', 'vm list --rg', 'blob upload', 'vnet list', 'backup item ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['account set', 'vm start/stop', 'blob download', 'nsg rule add', 'kv secret get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['account list', 'vm resize', 'disk create', 'lb list', 'backup protect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['sp create', 'vm run-cmd', 'snapshot cp', 'vnet peering', 'kv key list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Resource Manager API · Azure AD token endpoint · Azure CloudShell or local workstation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure CLI v2     = Current az CLI; install via Homebrew/apt/pip; az --version to verify'))
    lines.append(txt_row('az login         = Browser-based interactive login; stores token in ~/.azure/; expires after 1 hour'))
    lines.append(txt_row('Service principal= Non-human identity; use az login --service-principal for automation'))
    lines.append(txt_row('az account set   = Switch active subscription; use with --subscription <name or id>'))
    lines.append(txt_row('--resource-group = Required for most resource commands; shorthand --g; targets RG scope'))
    lines.append(txt_row('--query          = JMESPath filter on JSON output; e.g. [].name for list of resource names'))
    lines.append(txt_row('--output table   = Renders JSON as a formatted table; useful for terminal readability'))
    lines.append(txt_row('az vm run-command= Execute a script inside a VM via VM agent; works without SSH or port access'))
    lines.append(txt_row('az configure     = Set default resource group, output format, and location for the CLI session'))
    lines.append(txt_row('CloudShell       = Browser-based shell in Azure portal; pre-authenticated; az available by default'))
    lines.append(txt_row('--no-wait        = Submits a long-running operation without blocking the terminal; async execution'))
    lines.append(txt_row('az find          = AI-powered CLI helper; suggests relevant commands for a given scenario'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-compute',
    'docs/cloud/azure/compute/index.md',
    'Azure Compute Overview — VMs, Availability Sets/Zones, VMSS, Update Manager, extensions',
)
def azure_compute_overview():
    """Azure Compute Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Compute Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Compute — Virtual Machines, Scale Sets, Availability, and Fleet Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Virtual Machines: Windows and Linux VMs; 800+ sizes; Availability Zones for HA deployment')))
    lines.append(R(bMid(IV_L, IV_R, 'VM Scale Sets: auto-scaling fleet; uniform or flexible orchestration; custom or platform images')))
    lines.append(R(bMid(IV_L, IV_R, 'Availability: Zones (physically isolated) and Sets (fault/update domains) for redundancy')))
    lines.append(R(bMid(IV_L, IV_R, 'Fleet ops: Azure Update Manager (patching) · Extensions (monitoring, DSC) · Boot diagnostics')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VMs provide compute · Scale Sets enable elasticity · Availability features ensure HA deployments'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Virtual Machines'),
        bMid(B2_L, B2_R, 'Availability'),
        bMid(B3_L, B3_R, 'Fleet Management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sizes: B/D/E/F families'),
        bMid(B2_L, B2_R, 'Availability Zones: 3'),
        bMid(B3_L, B3_R, 'Update Manager: patch'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OS disk: managed Premium'),
        bMid(B2_L, B2_R, 'Availability Sets: FD/UD'),
        bMid(B3_L, B3_R, 'Extensions: agent+script'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image: custom gallery'),
        bMid(B2_L, B2_R, 'VM Scale Sets: VMSS'),
        bMid(B3_L, B3_R, 'Boot diagnostics: serial'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Identity: managed identity'),
        bMid(B2_L, B2_R, 'Zone: PPG for low lat'),
        bMid(B3_L, B3_R, 'Serial console: OOB'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resize: without data loss'),
        bMid(B2_L, B2_R, 'VMSS: instance refresh'),
        bMid(B3_L, B3_R, 'Inventory: ASC + Defender'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VMs provide individual compute · Availability features distribute load'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Virtual Machines', 'Avail. Sets', 'Avail. Zones', 'Scale Sets', 'Patching'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Start/stop VM', 'FD: 2-3 racks', 'Zone 1/2/3', 'Min/max count', 'Update Manager'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resize: portal', 'UD: rolling', 'Zone balance', 'Scale rule: CPU', 'Patch schedule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Image: capture', 'Use: SAP/SQL', 'Use: web tier', 'Rolling upgrade', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Boot diag: log', 'SLA: 99.95%', 'SLA: 99.99%', 'Instance refresh', 'Reboot: sched'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure host servers · Availability Zones (physical DCs) · Managed Disk storage fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Availability Set  = Groups VMs across fault domains (rack) and update domains (patch group)'))
    lines.append(txt_row('Availability Zone = Physically separate DC in a region; each with independent power, cooling, network'))
    lines.append(txt_row('VM Scale Set      = VMSS; fleet of identical VMs with auto-scaling; uniform or flexible orchestration'))
    lines.append(txt_row('Managed Identity  = Auto-managed service principal for a VM; used to authenticate to Azure services'))
    lines.append(txt_row('Proximity Placement Group= PPG; co-locates VMs in same data centre for lowest latency between VMs'))
    lines.append(txt_row('Fault Domain      = Rack-level isolation in an Availability Set; typically 2 or 3 per set'))
    lines.append(txt_row('Update Domain     = Rolling maintenance group; Azure updates one UD at a time during planned'))
    lines.append(txt_row('Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-booting VMs'))
    lines.append(txt_row('Serial Console    = Out-of-band console access to VM; works when SSH/RDP unreachable'))
    lines.append(txt_row('Azure Update Manager= Replaces Azure Automation Update Management; patches VMs on schedule at scale'))
    lines.append(txt_row('VM Extension      = Agent-based add-ons; installs monitoring agents, DSC, custom scripts on VMs'))
    lines.append(txt_row('Shared Image Gallery= Azure Compute Gallery; stores versioned custom VM images shared across'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-cost',
    'docs/cloud/azure/cost/index.md',
    'Azure Cost Management — Cost Management, budgets, Reservations, Savings Plans, Advisor',
)
def azure_cost_management():
    """Azure Cost Management — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Cost Management'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Cost Management — Visibility, Budgets, Reservations, and Optimisation')))
    lines.append(R(bMid(IV_L, IV_R, 'Cost Management + Billing: analyse spend by subscription, RG, service, tag, and location')))
    lines.append(R(bMid(IV_L, IV_R, 'Budgets: cost or usage threshold alerts; linked to action groups for email or automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Reservations: 1 or 3-year committed use for VMs, SQL, Storage; up to 72% discount')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Advisor: right-sizing, RI recommendations, idle resources, and cost savings estimates')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Cost visibility feeds budget alerts · Advisor finds savings · Reservations commit for discounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cost Analysis'),
        bMid(B2_L, B2_R, 'Budgets'),
        bMid(B3_L, B3_R, 'Optimisation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'By service: monthly'),
        bMid(B2_L, B2_R, 'Threshold: $ alert'),
        bMid(B3_L, B3_R, 'Reservations: 1/3yr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'By tag: team/env'),
        bMid(B2_L, B2_R, 'Forecast: 80% alert'),
        bMid(B3_L, B3_R, 'Savings Plans: flex'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'By subscription: trend'),
        bMid(B2_L, B2_R, 'Action group: email'),
        bMid(B3_L, B3_R, 'Advisor: rightsizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Export: storage account'),
        bMid(B2_L, B2_R, 'Anomaly alerts: ML'),
        bMid(B3_L, B3_R, 'Spot VMs: -90% cost'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cost alloc: tags billing'),
        bMid(B2_L, B2_R, 'Budget: scope mgmt grp'),
        bMid(B3_L, B3_R, 'Idle: deallocate + del'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Cost analysis provides visibility · Budgets alert on thresholds'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cost Analysis', 'Budgets', 'Reservations', 'Savings Plans', 'Azure Advisor'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['By service view', 'Monthly limit', 'VM: 1yr save%', 'Compute flex', 'Resize: -30%'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tag: chargeback', 'Forecast alert', 'SQL: 3yr 72%', 'DB flexible', 'Idle: terminate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Export: daily', 'Action grp', 'Coverage: view', 'Storage flex', 'RI: recommend'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Anomaly: detect', 'Scope: sub/RG', 'Utilise: >80%', 'Spend commit', 'Cost: estimate'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure billing infrastructure · Cost Management API · Export storage account · Action Group SNS/email'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cost Management + Billing= Azure portal blade for analysing and controlling Azure spend'))
    lines.append(txt_row('Budget          = Spending threshold; types: cost (£/$) or usage; alerts at % of limit'))
    lines.append(txt_row('Action Group    = Named set of actions (email, SMS, webhook, Logic App) triggered by alerts'))
    lines.append(txt_row('Reservation     = 1 or 3-year committed use purchase; applies to specific VM size or service'))
    lines.append(txt_row('Savings Plan    = Flexible spend commitment ($/hr); applies across regions and eligible services'))
    lines.append(txt_row('Spot VM         = Low-priority VM using spare Azure capacity; up to 90% cheaper; can be evicted'))
    lines.append(txt_row('Azure Advisor   = Personalised recommendations for cost, security, performance, and reliability'))
    lines.append(txt_row('Cost allocation = Attributing Azure costs to teams/apps via resource tags; chargeback enablement'))
    lines.append(txt_row('Cost export     = Scheduled export of usage data to Azure Blob Storage; feeds BI tools / Power BI'))
    lines.append(txt_row('Anomaly alert   = AI-detected unexpected spend spike on subscription, resource group, or service'))
    lines.append(txt_row('Reserved capacity= Azure Reservation; pre-purchase a discount for predictable workloads'))
    lines.append(txt_row('Rightsizing     = Advisor recommendation to reduce VM SKU when CPU/memory consistently underused'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-governance',
    'docs/cloud/azure/governance/index.md',
    'Azure Governance — Management Groups, Azure Policy (Audit/Deny/DINE), initiatives, compliance',
)
def azure_governance_overview():
    """Azure Governance Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Governance Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Governance — Policy, Initiatives, Compliance, and Management Groups')))
    lines.append(R(bMid(IV_L, IV_R, 'Management Groups: policy and RBAC applied at MG scope cascade to all subscriptions below')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Policy: define rules for resource configs; effects: Audit, Deny, DeployIfNotExists')))
    lines.append(R(bMid(IV_L, IV_R, 'Initiatives: group multiple policy definitions; assign as one unit (e.g. CIS Azure Benchmark)')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance review: policy state dashboard; non-compliant resources; remediation tasks')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management Groups scope policies · Policy defines rules · Initiatives bundle them'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Management Groups'),
        bMid(B2_L, B2_R, 'Azure Policy'),
        bMid(B3_L, B3_R, 'Compliance'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Root: tenant root MG'),
        bMid(B2_L, B2_R, 'Effect: Audit/Deny/DINE'),
        bMid(B3_L, B3_R, 'Dashboard: compliant %'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Custom MG hierarchy'),
        bMid(B2_L, B2_R, 'Scope: MG/sub/RG/res'),
        bMid(B3_L, B3_R, 'Non-compliant: list/fix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inheritance: sub → RG'),
        bMid(B2_L, B2_R, 'Initiatives: CIS/NIST'),
        bMid(B3_L, B3_R, 'Remediation: auto task'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policy scope: inherited'),
        bMid(B2_L, B2_R, 'Parameters: reuse policy'),
        bMid(B3_L, B3_R, 'Exemption: time-bound'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Tag policy: org-wide'),
        bMid(B2_L, B2_R, 'Assignment: + params'),
        bMid(B3_L, B3_R, 'Audit log: activity log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Management Groups establish hierarchy · Policy defines rules · Compliance validates and remediates'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mgmt Groups', 'Azure Policy', 'Initiatives', 'Compliance', 'Exemptions'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Create MG', 'New definition', 'Assign init', 'View %: pass', 'Create exemp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Move sub to MG', 'Assign policy', 'CIS Az 1.4', 'Non-compliant', 'Waiver: reason'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Policy: inherit', 'Effect: Deny', 'NIST SP800-53', 'Remediation', 'Expiry: date'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RBAC at MG', 'DeployIfNotEx', 'Custom bundled', 'Mitigate task', 'Scope: RG/res'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Resource Manager · Policy engine · Management Group hierarchy · Activity Log infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Management Group   = Container above subscriptions; scoping boundary for policy and RBAC'))
    lines.append(txt_row('Azure Policy       = Service for defining, assigning, and evaluating compliance rules on resources'))
    lines.append(txt_row('Policy definition  = JSON rule with conditions and effects; built-in or custom; parameterised'))
    lines.append(txt_row('Policy assignment  = Applies a definition or initiative to a scope with specific parameter values'))
    lines.append(txt_row('Effect: Audit      = Logs non-compliant resources without blocking; compliance reporting only'))
    lines.append(txt_row('Effect: Deny       = Blocks creation or update of non-compliant resources; hard enforcement'))
    lines.append(txt_row('Effect: DINE       = DeployIfNotExists; deploys remediation resource when policy condition is met'))
    lines.append(txt_row('Initiative         = Collection of policy definitions assigned together; simplifies compliance sets'))
    lines.append(txt_row('Remediation task   = Auto-runs the DINE effect on existing non-compliant resources in scope'))
    lines.append(txt_row('Exemption          = Excludes a resource or scope from a policy assignment; time-bound or permanent'))
    lines.append(txt_row('Compliance state   = Per-resource evaluation result: Compliant / Non-compliant / Not started / Exempt'))
    lines.append(txt_row('Tagging policy     = Policy enforcing required tags (e.g. Owner, Environment) on all resource'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-identity',
    'docs/cloud/azure/identity/index.md',
    'Azure Identity — Entra ID, RBAC, managed identities, PIM, conditional access',
)
def azure_identity_overview():
    """Azure Identity Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Identity Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Identity — Entra ID, RBAC, Managed Identities, and PIM')))
    lines.append(R(bMid(IV_L, IV_R, 'Entra ID: cloud identity directory; users, groups, B2B guests, and app registrations')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: Owner / Contributor / Reader built-in roles + custom; scope: MG, sub, RG, resource')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed Identities: system or user-assigned; auto-managed SP for Azure services to authenticate')))
    lines.append(R(bMid(IV_L, IV_R, 'PIM: just-in-time role activation; approval workflow; time-limited privileged access')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Entra ID is the identity source · RBAC grants access · Managed Identities remove secrets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Entra ID'),
        bMid(B2_L, B2_R, 'RBAC'),
        bMid(B3_L, B3_R, 'Privileged Access'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Users: UPN + MFA'),
        bMid(B2_L, B2_R, 'Owner: full control'),
        bMid(B3_L, B3_R, 'PIM: JIT activate'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Groups: security+M365'),
        bMid(B2_L, B2_R, 'Contributor: no RBAC'),
        bMid(B3_L, B3_R, 'Approval: manager'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'App registrations: SPN'),
        bMid(B2_L, B2_R, 'Reader: read-only'),
        bMid(B3_L, B3_R, 'Time-limit: 8 hours'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Conditional Access: MFA'),
        bMid(B2_L, B2_R, 'Custom roles: JSON def'),
        bMid(B3_L, B3_R, 'Audit: PIM history'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Managed identities: MI'),
        bMid(B2_L, B2_R, 'Scope: sub/RG/resource'),
        bMid(B3_L, B3_R, 'Access review: quarterly'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Entra ID manages identities · RBAC controls access at scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Entra ID', 'App Reg.', 'RBAC', 'Managed ID', 'PIM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['User: create', 'Register app', 'Assign: sub', 'System-assign', 'Activate: JIT'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Group: add mem', 'Client secret', 'Assign: RG', 'User-assign', 'Approve: MFA'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: enforce', 'API permission', 'Custom role', 'RBAC to MI', 'Expiry: 8h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cond. Access', 'Enterprise app', 'Review: list', 'No secrets', 'Access review'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Entra ID global service · Azure RBAC control plane · PIM service · ARM token endpoint'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Entra ID         = Microsoft cloud identity directory (formerly Azure AD); users, groups, apps,'))
    lines.append(txt_row('App registration = Entra ID object representing an application; has client ID, secret or certificate'))
    lines.append(txt_row('Service principal= Instance of an app registration in a tenant; has identity and can be assigned'))
    lines.append(txt_row('Managed Identity = Azure-managed service principal; no secrets; system (tied to resource) or'))
    lines.append(txt_row('System-assigned MI= Identity tied to one resource; deleted when resource is deleted; most common'))
    lines.append(txt_row('User-assigned MI = Standalone identity; assigned to multiple resources; survives resource deletion'))
    lines.append(txt_row('RBAC             = Role-Based Access Control; assigns built-in or custom roles at a defined scope'))
    lines.append(txt_row('RBAC scope       = Hierarchy: Management Group > Subscription > Resource Group > Resource'))
    lines.append(txt_row('PIM              = Privileged Identity Management; manages just-in-time access to sensitive roles'))
    lines.append(txt_row('Conditional Access= Policy evaluating sign-in signals (location, device, risk) to grant, block, or'))
    lines.append(txt_row('Access review    = Periodic review of group membership or role assignments; remove stale access'))
    lines.append(txt_row('B2B              = Business-to-business; inviting external users (guests) to your Entra ID tenant'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-monitoring',
    'docs/cloud/azure/monitoring/index.md',
    'Azure Monitoring — Azure Monitor, Log Analytics (KQL), alerts, action groups',
)
def azure_monitoring_overview():
    """Azure Monitoring Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Monitoring Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Monitor — Metrics, Logs, Alerts, and Observability')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Monitor: platform for all metrics, logs, alerts, and dashboards across Azure services')))
    lines.append(R(bMid(IV_L, IV_R, 'Log Analytics: workspace stores logs; KQL query language; used for dashboards and alert rules')))
    lines.append(R(bMid(IV_L, IV_R, 'Alerts: metric, log, and activity log alert rules; action groups for notification and')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostic settings: route resource logs and metrics to Log Analytics, Storage, or Event Hub')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Metrics and logs feed alert rules · Alerts trigger action groups · Dashboards provide visibility'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Azure Monitor'),
        bMid(B2_L, B2_R, 'Log Analytics'),
        bMid(B3_L, B3_R, 'Alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metrics: platform native'),
        bMid(B2_L, B2_R, 'Workspace: per region'),
        bMid(B3_L, B3_R, 'Metric alert: threshold'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Activity log: ctrl-plane'),
        bMid(B2_L, B2_R, 'KQL: query + transform'),
        bMid(B3_L, B3_R, 'Log alert: KQL query'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Diagnostic settings'),
        bMid(B2_L, B2_R, 'Retention: 30-730d'),
        bMid(B3_L, B3_R, 'Activity alert: ops'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Health: events'),
        bMid(B2_L, B2_R, 'Workbooks: dashboards'),
        bMid(B3_L, B3_R, 'Action group: email/web'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboards: pin metrics'),
        bMid(B2_L, B2_R, 'Saved queries: reuse'),
        bMid(B3_L, B3_R, 'Alert rule: severity 0-4'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Azure Monitor collects metrics/logs · Log Analytics stores and queries · Alerts notify and automate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Azure Monitor', 'Log Analytics', 'Alerts', 'Activity Log', 'Service Health'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Metrics: CPU', 'KQL: query', 'Metric: CPU>80', 'Who changed?', 'Planned maint'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Diag settings', 'Workspace: RG', 'Log: KQL rule', 'Activity alert', 'Incidents: svc'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Dashboard: pin', 'Retention: 90d', 'Action: email', 'Export: LA', 'Health alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workbooks', 'Saved query', 'Severity 0-4', 'ARM events', 'Subscr events'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Monitor backend · Log Analytics workspace storage · Action Group notification services'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure Monitor     = Platform service aggregating all metrics, logs, alerts, and traces from Azure'))
    lines.append(txt_row('Log Analytics workspace= Storage and query engine for Azure Monitor logs; uses KQL; one or more per'))
    lines.append(txt_row('KQL               = Kusto Query Language; used in Log Analytics, Application Insights, and Data'))
    lines.append(txt_row('Diagnostic settings= Resource-level config routing logs/metrics to Log Analytics, Storage, or Event'))
    lines.append(txt_row('Activity Log      = Subscription-level control-plane audit log; who did what, when; 90 days retention'))
    lines.append(txt_row('Metric alert      = Fires when a metric (CPU, memory, latency) crosses a threshold for N minutes'))
    lines.append(txt_row('Log alert         = Fires when a KQL query returns rows; evaluated on a schedule (5 min – 1 day)'))
    lines.append(txt_row('Activity alert    = Fires on specific control-plane events (e.g. VM deleted, RBAC assigned)'))
    lines.append(txt_row('Action group      = Reusable set of notification actions (email, SMS, webhook, Logic App, ITSM)'))
    lines.append(txt_row('Alert severity    = Sev 0 (Critical) to Sev 4 (Verbose); used to route and prioritise alerts'))
    lines.append(txt_row('Service Health    = Azure-side health events and planned maintenance for your subscriptions/services'))
    lines.append(txt_row('Workbook          = Azure Monitor interactive report combining metrics, logs, and parameters in one'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-networking',
    'docs/cloud/azure/networking/index.md',
    'Azure Networking — VNet, subnets, NSGs, Azure Firewall, Private Endpoints, ExpressRoute',
)
def azure_networking_overview():
    """Azure Networking Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Networking Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Networking — VNet, NSG, Load Balancer, DNS, and Hybrid Connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'VNet: isolated network; CIDR /8–/29; subnets per AZ; hub-and-spoke via VNet peering')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: NSG (stateful L4 rules per subnet/NIC) · Azure Firewall (stateful L4/L7 in hub)')))
    lines.append(R(bMid(IV_L, IV_R, 'Load balancing: Load Balancer (L4) · Application Gateway (L7 + WAF) · Traffic Manager (DNS)')))
    lines.append(R(bMid(IV_L, IV_R, 'Hybrid: ExpressRoute (private circuit) · VPN Gateway (IPsec) · Private Endpoints (PaaS)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VNet defines the network · NSG/Firewall secure it · Load Balancer distributes traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VNet & Subnets'),
        bMid(B2_L, B2_R, 'Security Controls'),
        bMid(B3_L, B3_R, 'Connectivity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VNet: CIDR /16 plan'),
        bMid(B2_L, B2_R, 'NSG: allow/deny rules'),
        bMid(B3_L, B3_R, 'ExpressRoute: private'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Subnets: per AZ/tier'),
        bMid(B2_L, B2_R, 'Firewall: hub central'),
        bMid(B3_L, B3_R, 'VPN Gateway: IPsec'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Peering: hub ↔ spoke'),
        bMid(B2_L, B2_R, 'Network Watcher: diag'),
        bMid(B3_L, B3_R, 'Private Endpoint: PaaS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Route tables: UDR'),
        bMid(B2_L, B2_R, 'DDoS: Basic or std'),
        bMid(B3_L, B3_R, 'Azure DNS: pub + priv'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service endpoints'),
        bMid(B2_L, B2_R, 'Flow logs: NSG → LA'),
        bMid(B3_L, B3_R, 'LB: internal+public'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VNet/subnets form the base · NSG/Firewall protect traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VNet', 'Subnets', 'NSG', 'Load Balancer', 'App Gateway'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CIDR: plan', 'App subnet', 'Inbound rules', 'Backend pool', 'L7: path route'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Peering: hub', 'DB subnet', 'Outbound rules', 'Health probe', 'WAF: OWASP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow logs: LA', 'GW subnet: /27', 'Priority: 100', 'LB rule: port', 'SSL termination'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DNS: custom', 'Service endpt', 'NSG flow logs', 'Internal LB', 'Autoscale: min'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure SDN fabric · Availability Zones · ExpressRoute physical circuits · VPN Gateway hardware'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VNet           = Virtual Network; isolated private network in a region; one or more CIDR address'))
    lines.append(txt_row('Subnet         = Address range within a VNet; services and NSGs attached per subnet'))
    lines.append(txt_row('NSG            = Network Security Group; stateful L4 ACL; priority-ordered allow/deny rules on'))
    lines.append(txt_row('VNet peering   = Private connectivity between VNets in same or different regions; low latency'))
    lines.append(txt_row('UDR            = User Defined Route; custom route table overriding Azure defaults; force to firewall'))
    lines.append(txt_row('Azure Firewall = Managed stateful L4/L7 firewall in hub VNet; centralises egress and spoke traffic'))
    lines.append(txt_row('Private Endpoint= Private IP in a VNet for accessing PaaS (Storage, SQL, Key Vault) without internet'))
    lines.append(txt_row('Service Endpoint= Optimised route from VNet to PaaS service; not a private IP; firewall-accessible'))
    lines.append(txt_row('Application Gateway= L7 load balancer with URL routing, SSL offload, and optional WAF integration'))
    lines.append(txt_row('Network Watcher = Diagnostics for connectivity, packet capture, NSG flow logs, and topology view'))
    lines.append(txt_row('ExpressRoute   = Dedicated private 50 Mbps–10 Gbps circuit between on-premises and Azure'))
    lines.append(txt_row('Azure DNS      = Managed DNS for public zones (internet) and private zones (VNet resolution)'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-operations',
    'docs/cloud/azure/operations/index.md',
    'Azure Operations — health checks, VM procedures, Update Manager, backup/restore, automation',
)
def azure_operations_overview():
    """Azure Operations Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Operations Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Operations — Health Checks, Procedures, Patching, and Automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Health Checks: VM status · Load Balancer health probes · Monitor alert state · Service Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Procedures: VM lifecycle, disk expansion, scale set refresh, RG cleanup, ASR failover tests')))
    lines.append(R(bMid(IV_L, IV_R, 'Patching: Azure Update Manager; scheduled patch runs; compliance reporting per VM fleet')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup/Restore: Azure Backup jobs · RSV restore · disk snapshot restore · ASR test failover')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks detect issues · Procedures resolve them · Automation prevents recurrence'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Health Checks'),
        bMid(B2_L, B2_R, 'Procedures'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VM: running + health'),
        bMid(B2_L, B2_R, 'Start/stop/restart VM'),
        bMid(B3_L, B3_R, 'az CLI: scripted ops'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LB health probe: pass'),
        bMid(B2_L, B2_R, 'Resize VM SKU'),
        bMid(B3_L, B3_R, 'Logic App: workflow'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Monitor alerts: OK?'),
        bMid(B2_L, B2_R, 'Disk: expand + extend'),
        bMid(B3_L, B3_R, 'ARM / Bicep: IaC'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Health: events'),
        bMid(B2_L, B2_R, 'VMSS: instance refresh'),
        bMid(B3_L, B3_R, 'Event Grid: auto-trigger'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Backup jobs: success?'),
        bMid(B2_L, B2_R, 'ASR: test failover'),
        bMid(B3_L, B3_R, 'Azure Automation: run'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks prevent failures · Procedures execute changes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Health Checks', 'Procedures', 'Patching', 'Backup/Restore', 'Scripts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VM: running?', 'Start/stop VM', 'Update Manager', 'Backup: enable', 'az vm list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LB probe: pass', 'Resize: dealoc', 'Patch schedule', 'RSV: restore', 'az disk create'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alerts: OK', 'Disk: expand', 'Compliance', 'Snap: restore', 'Bicep: deploy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Svc Health: evt', 'VMSS refresh', 'Reboot: sched', 'ASR: test fail', 'Automation RB'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure VM host fabric · Managed Disk storage · Load Balancer health infrastructure · VNet networking'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure Update Manager = Replaces Automation Update Management; patches OS at scale per schedule'))
    lines.append(txt_row('Service Health      = Azure health dashboard for your subscriptions; planned and unplanned events'))
    lines.append(txt_row('LB health probe     = TCP or HTTP check sent to backend pool members; failure removes VM from'))
    lines.append(txt_row('VM resize           = Change VM SKU; requires deallocation first (downtime); no data loss'))
    lines.append(txt_row('Disk expansion      = Increase managed disk size in portal/CLI; then extend partition inside OS'))
    lines.append(txt_row('VMSS instance refresh= Rolling replacement of scale set instances with updated image or config'))
    lines.append(txt_row('ASR test failover   = Spins up replica VM in isolated VNet; validates recovery without affecting prod'))
    lines.append(txt_row('Azure Automation    = Runbooks (PowerShell/Python) executed on schedule or on demand at scale'))
    lines.append(txt_row('Logic App           = Low-code workflow automation; triggered by events, HTTP, or schedule'))
    lines.append(txt_row('Event Grid          = Event routing service; triggers Logic Apps, Functions, or webhooks on resource'))
    lines.append(txt_row('Bicep              = ARM template DSL; cleaner syntax for deploying Azure resources as IaC'))
    lines.append(txt_row('az vm run-command   = Execute script inside VM via agent; works when RDP/SSH is blocked'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-security',
    'docs/cloud/azure/security/index.md',
    'Azure Security — Entra ID SSO/MFA, Key Vault, CMK, Defender for Cloud, Secure Score, Sentinel',
)
def azure_security_overview():
    """Azure Security Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Security Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Security — Authentication, Encryption, and Threat Detection')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: Entra ID SSO · MFA · Conditional Access · PIM for just-in-time admin access')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: Key Vault (keys+secrets+certs) · Customer-Managed Keys · Private Link for PaaS')))
    lines.append(R(bMid(IV_L, IV_R, 'Threat detection: Defender for Cloud (posture + CSPM) · Secure Score · Defender plans per svc')))
    lines.append(R(bMid(IV_L, IV_R, 'Network security: NSGs · Azure Firewall in hub · WAF on App Gateway · DDoS Protection')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls access · Encryption protects data · Defender detects and remediates threats'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Encryption'),
        bMid(B3_L, B3_R, 'Threat Detection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Entra ID: SSO+MFA'),
        bMid(B2_L, B2_R, 'Key Vault: keys/certs'),
        bMid(B3_L, B3_R, 'Defender for Cloud'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Conditional Access'),
        bMid(B2_L, B2_R, 'CMK: storage+SQL+disk'),
        bMid(B3_L, B3_R, 'Secure Score: target'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PIM: JIT privileged'),
        bMid(B2_L, B2_R, 'TLS: App GW + APIM'),
        bMid(B3_L, B3_R, 'Defender plans: VMs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RBAC: least privilege'),
        bMid(B2_L, B2_R, 'Private Link: no pub IP'),
        bMid(B3_L, B3_R, 'Microsoft Sentinel: SIEM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Access reviews: quarterly'),
        bMid(B2_L, B2_R, 'Disk: SSE + CMK'),
        bMid(B3_L, B3_R, 'NSG + Firewall: network'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication + RBAC prevent access · Encryption protects data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Authentication', 'Access Control', 'Encryption', 'Hardening', 'Key Vault'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Entra ID: SSO', 'RBAC: Contrib', 'KV: key create', 'Defender plans', 'Key: rotate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: all users', 'PIM: JIT role', 'CMK: storage', 'Secure Score', 'Secret: get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cond. Access', 'MI: no secret', 'TLS: 1.2+ only', 'Policy: audit', 'Cert: import'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Access review', 'Custom role', 'Disk: SSE-CMK', 'NSG + FW', 'RBAC: Key Vault'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure HSM for Key Vault · Defender for Cloud backend · Entra ID global service'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Key Vault        = Managed secrets, keys, and certificates; RBAC + access policy; HSM-backed option'))
    lines.append(txt_row('CMK              = Customer-Managed Key; encryption key you control in Key Vault; used for Azure'))
    lines.append(txt_row('SSE              = Server-Side Encryption; Azure encrypts managed disks at rest using PME or CMK'))
    lines.append(txt_row('Private Link     = Private Endpoint mapping PaaS service to VNet IP; eliminates public internet'))
    lines.append(txt_row('Defender for Cloud= CSPM + CWPP; security posture management and workload protection across Azure'))
    lines.append(txt_row('Secure Score     = Numeric score (0-100) of security posture; improvements mapped to recommendations'))
    lines.append(txt_row('Defender plans   = Per-resource workload protection: VMs, SQL, Storage, Containers, Key Vault, DNS'))
    lines.append(txt_row('Microsoft Sentinel= Cloud-native SIEM + SOAR; ingests logs, detects threats, automates response'))
    lines.append(txt_row('Conditional Access= Entra ID engine; blocks, MFAs, or allows sign-in based on device, location, risk'))
    lines.append(txt_row('PIM              = Privileged Identity Management; JIT admin access with approval and time limits'))
    lines.append(txt_row('TLS validation   = Enforce minimum TLS 1.2 on Storage accounts, App Gateway, and API Management'))
    lines.append(txt_row('Access review    = Periodic audit of who has what access; approvers confirm or remove assignments'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-storage',
    'docs/cloud/azure/storage/index.md',
    'Azure Storage — Blob tiers, lifecycle, Managed Disks (Premium/Ultra/ZRS), Azure Files',
)
def azure_storage_overview():
    """Azure Storage Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Storage Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Storage — Blob, Managed Disks, Files, and Storage Accounts')))
    lines.append(R(bMid(IV_L, IV_R, 'Blob Storage: Hot / Cool / Cold / Archive access tiers; lifecycle management; immutable WORM')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed Disks: Premium SSD / Standard SSD / Ultra; ZRS for zone redundancy; snapshots')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Files: managed SMB and NFS shares; AD integration for Windows shares; Azure File Sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage accounts: replication LRS/ZRS/GRS/GZRS; encryption at rest by default; private')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Blob serves objects · Managed Disks serve VM block I/O · Files serve shared mounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blob Storage'),
        bMid(B2_L, B2_R, 'Managed Disks'),
        bMid(B3_L, B3_R, 'Azure Files'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hot: frequent access'),
        bMid(B2_L, B2_R, 'Premium SSD: low lat'),
        bMid(B3_L, B3_R, 'SMB 2.1/3.0 shares'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cool/Cold: infreq'),
        bMid(B2_L, B2_R, 'Standard SSD: gen use'),
        bMid(B3_L, B3_R, 'NFS 4.1: Linux'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Archive: offline store'),
        bMid(B2_L, B2_R, 'Ultra: 160K IOPS'),
        bMid(B3_L, B3_R, 'AD auth: Windows'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lifecycle: tier rules'),
        bMid(B2_L, B2_R, 'ZRS: zone redundant'),
        bMid(B3_L, B3_R, 'File Sync: on-prem'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Immutability: WORM'),
        bMid(B2_L, B2_R, 'Snapshots: incremental'),
        bMid(B3_L, B3_R, 'Backup: RSV policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Blob for unstructured objects · Managed Disks for VM boot/data · Files for shared SMB/NFS workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blob Storage', 'Managed Disks', 'Azure Files', 'Storage Accts', 'Snapshots'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upload: AzCopy', 'Create: P10/P30', 'Create share', 'LRS/ZRS/GRS', 'Disk snap: incr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Lifecycle: rule', 'Attach to VM', 'Mount: Windows', 'Private endpt', 'Blob snap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Immutability', 'Expand: no stop', 'Mount: Linux', 'SAS token', 'Restore: snap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tier: archive', 'ZRS: 3-zone', 'File Sync', 'CMK encrypt', 'Copy to region'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Storage clusters (LRS/ZRS/GRS) · Managed Disk fabric per AZ · Storage account endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Storage account  = Top-level namespace for Blob, Files, Queue, Table; controls replication and access'))
    lines.append(txt_row('LRS              = Locally Redundant Storage; 3 copies in one data centre; cheapest option'))
    lines.append(txt_row('ZRS              = Zone-Redundant Storage; 3 copies across 3 AZs; survives zone failure'))
    lines.append(txt_row('GRS              = Geo-Redundant Storage; 6 copies across 2 regions; async replication to secondary'))
    lines.append(txt_row('GZRS             = Geo-Zone-Redundant Storage; ZRS in primary + LRS in secondary region'))
    lines.append(txt_row('Blob access tier  = Hot (frequent), Cool (infrequent), Cold (rare), Archive (offline); cost tiers'))
    lines.append(txt_row('Lifecycle policy = Automatically transitions or deletes blobs based on age and last-modified date'))
    lines.append(txt_row('Immutable storage= WORM policy on container; Legal hold or time-based; prevents delete/overwrite'))
    lines.append(txt_row('Managed Disk     = Azure-managed block storage for VMs; types: Premium SSD, Standard SSD, Ultra'))
    lines.append(txt_row('ZRS disk         = Zone-Redundant disk; synchronously replicates across 3 AZs; no AZ downtime impact'))
    lines.append(txt_row('Azure File Sync  = Syncs Azure Files share to on-premises Windows Server; cloud tiering option'))
    lines.append(txt_row('SAS token        = Shared Access Signature; time-limited URL token for scoped blob/container access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'azure-troubleshooting',
    'docs/cloud/azure/troubleshooting/index.md',
    'Azure Troubleshooting — common issues, Boot Diagnostics, Serial Console, Network Watcher',
)
def azure_troubleshooting_overview():
    """Azure Troubleshooting Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Troubleshooting Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Troubleshooting — Common Issues, Diagnostics, and Escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: VM unreachable · NSG blocking · RBAC access denied · Storage auth error')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: Boot diagnostics · Serial Console · Network Watcher · Activity Log · Monitor')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: az CLI describe · Azure portal diagnostics · Connection Troubleshoot · Resource Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: Azure Support cases; collect sub ID, region, resource ID, error, and timeframe')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide investigation · Diagnostics locate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VM: RDP/SSH fails'),
        bMid(B2_L, B2_R, 'Boot diagnostics: log'),
        bMid(B3_L, B3_R, 'Sub ID + resource ID'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSG: port blocked'),
        bMid(B2_L, B2_R, 'Serial Console: OOB'),
        bMid(B3_L, B3_R, 'Error + timestamp'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RBAC: access denied'),
        bMid(B2_L, B2_R, 'Network Watcher: path'),
        bMid(B3_L, B3_R, 'Severity: Crit/High'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Storage: 403 auth'),
        bMid(B2_L, B2_R, 'Activity Log: who/when'),
        bMid(B3_L, B3_R, 'Sev A: production down'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DNS: resolution fail'),
        bMid(B2_L, B2_R, 'Resource Health: state'),
        bMid(B3_L, B3_R, 'Premium support: TAM'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Identify symptom → collect diagnostics (logs, Network Watcher, health) → resolve or escalate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Escalation', 'CLI Tools', 'Portal Tools'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VM: no RDP', 'Boot diag log', 'Sev A: call', 'az vm list', 'Resource Health'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSG: miss rule', 'Serial console', 'Sub ID + error', 'az network nsg', 'Net Watcher'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RBAC: denied', 'Activity Log', 'Premium: TAM', 'az role assign', 'Boot Diag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Storage: 403', 'Net Watcher', 'Collect: all', 'az storage ls', 'Diagn settings'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure VM host fabric · Azure networking SDN · Microsoft Support infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-starting VMs'))
    lines.append(txt_row('Serial Console    = Out-of-band terminal access to VM; works when RDP/SSH unreachable'))
    lines.append(txt_row('Network Watcher   = Diagnoses connectivity; Connection Troubleshoot traces hop-by-hop path'))
    lines.append(txt_row('Connection Troubleshoot= Network Watcher tool; tests TCP reachability from source VM to destination'))
    lines.append(txt_row('Resource Health   = Per-resource health history; shows Azure platform events affecting the resource'))
    lines.append(txt_row('Activity Log      = Control-plane audit; search for who made a change and when in the last 90 days'))
    lines.append(txt_row('NSG flow logs     = Accepted/denied traffic metadata; route to Log Analytics for KQL queries'))
    lines.append(txt_row('Severity A case   = Production down; 24/7 response; phone callback + online case together'))
    lines.append(txt_row('Severity B case   = Degraded function; business-hours response; online case sufficient'))
    lines.append(txt_row('TAM               = Technical Account Manager; named Microsoft contact for Premier/Unified support'))
    lines.append(txt_row('RBAC denied       = Check Activity Log for the 403; look for missing role or wrong scope'))
    lines.append(txt_row('Storage 403       = Check access key vs SAS vs RBAC; check firewall rules and private endpoint config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── VMware product diagrams — batch 1 of 2 ────────────────────────────────────


@kb_diagram('aws-arch-how', 'docs/cloud/aws/architecture/how-it-works/index.md', 'AWS Architecture — How It Works')
def _aws_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Architecture — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('Multi-account org: management root governs OUs; workload accounts isolated by purpose.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Account Layer'), bMid(L2, R2, 'Networking Layer'))))
    lines.append(R(merge(bMid(L1, R1, 'Management: org root + billing'), bMid(L2, R2, 'Transit Gateway: hub-spoke'))))
    lines.append(R(merge(bMid(L1, R1, 'Log Archive: central logs'), bMid(L2, R2, 'VPC per account: isolation'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: security tooling'), bMid(L2, R2, 'DirectConnect: on-prem link'))))
    lines.append(R(merge(bMid(L1, R1, 'Workload: env/team accounts'), bMid(L2, R2, 'VPC endpoints: private S3/SSM'))))
    lines.append(R(merge(bMid(L1, R1, 'SCPs: OU-level guardrails'), bMid(L2, R2, 'Route 53: DNS across accounts'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Accounts provide blast-radius isolation; Transit Gateway connects without peering mesh'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity and Access'), bMid(L2, R2, 'Observability'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM Identity Center: SSO'), bMid(L2, R2, 'CloudTrail: org-wide API log'))))
    lines.append(R(merge(bMid(L1, R1, 'Permission sets → member accts'), bMid(L2, R2, 'CloudWatch: metrics + logs'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML federation: IdP → AWS'), bMid(L2, R2, 'Config: resource inventory'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM roles: cross-account'), bMid(L2, R2, 'Security Hub: aggregated'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: enforced org-wide SCP'), bMid(L2, R2, 'GuardDuty: threat detection'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · Availability Zones · data centres · DirectConnect physical ports · backbone'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OU             = Organisational Unit; logical grouping of accounts with shared SCPs'))
    lines.append(txt_row('SCP            = Service Control Policy; preventive guardrail at OU or account level'))
    lines.append(txt_row('Transit Gateway= Regional hub router connecting multiple VPCs without full mesh'))
    lines.append(txt_row('IAM Identity Center= AWS SSO; assigns permission sets to users in member accounts'))
    lines.append(txt_row('Permission set = IAM policy bundle assigned to user/group for specific account'))
    lines.append(txt_row('DirectConnect  = Dedicated private link from on-premises to AWS; bypasses internet'))
    lines.append(txt_row('VPC endpoint   = Private connection to AWS services without internet traversal'))
    lines.append(txt_row('CloudTrail org = Management-account trail capturing all API calls across every account'))
    lines.append(txt_row('AWS Config     = Records resource configuration changes; evaluates compliance rules'))
    lines.append(txt_row('Security Hub   = Aggregates findings from GuardDuty, Inspector, Config across accounts'))
    lines.append(txt_row('GuardDuty      = Threat detection; analyses CloudTrail, VPC Flow Logs, DNS queries'))
    lines.append(txt_row('Log archive    = Dedicated account receiving all central logs; immutable S3 bucket'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-arch-int', 'docs/cloud/aws/architecture/integrations/index.md', 'AWS Architecture — Integrations')
def _aws_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Architecture — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('AWS platform integrates with on-prem identity, monitoring, ITSM, and CI/CD tooling.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity Integrations'), bMid(L2, R2, 'Network Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'Azure AD / Okta: SAML IdP'), bMid(L2, R2, 'DirectConnect: dedicated WAN'))))
    lines.append(R(merge(bMid(L1, R1, 'SCIM: user provisioning'), bMid(L2, R2, 'Site-to-site VPN: backup'))))
    lines.append(R(merge(bMid(L1, R1, 'AD Connector: on-prem AD'), bMid(L2, R2, 'Route 53 resolver: hybrid DNS'))))
    lines.append(R(merge(bMid(L1, R1, 'CyberArk: privileged access'), bMid(L2, R2, 'ELB: external load balancing'))))
    lines.append(R(merge(bMid(L1, R1, 'Venafi: certificate lifecycle'), bMid(L2, R2, 'WAF: edge protection'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Identity and network integrations established first; tooling integrations built on top'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitoring Integrations'), bMid(L2, R2, 'Automation Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'Datadog/Splunk: CloudWatch'), bMid(L2, R2, 'Terraform: IaC provisioning'))))
    lines.append(R(merge(bMid(L1, R1, 'PagerDuty: CloudWatch alarms'), bMid(L2, R2, 'GitHub Actions: OIDC deploy'))))
    lines.append(R(merge(bMid(L1, R1, 'ServiceNow: CMDB AWS sync'), bMid(L2, R2, 'Ansible: Systems Manager'))))
    lines.append(R(merge(bMid(L1, R1, 'Security Hub → Jira tickets'), bMid(L2, R2, 'CloudFormation: IaC native'))))
    lines.append(R(merge(bMid(L1, R1, 'Cost alerts: SNS → Slack'), bMid(L2, R2, 'EventBridge: event routing'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS backbone · DirectConnect port · on-prem IdP server · CI/CD runner · ITSM server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SCIM           = System for Cross-domain Identity Management; auto-provisions users'))
    lines.append(txt_row('AD Connector   = AWS proxy to on-prem Active Directory; no user sync required'))
    lines.append(txt_row('Route 53 resolver= Hybrid DNS: resolves on-prem names from VPC and vice versa'))
    lines.append(txt_row('WAF            = Web Application Firewall; deployed at CloudFront or ALB edge'))
    lines.append(txt_row('OIDC deploy    = GitHub Actions assumes IAM role via OIDC without static keys'))
    lines.append(txt_row('EventBridge    = Serverless event bus routing AWS events to targets or 3rd parties'))
    lines.append(txt_row('SSM            = AWS Systems Manager; fleet management without SSH/RDP'))
    lines.append(txt_row('CyberArk       = PAM tool; brokers privileged AWS console/CLI access'))
    lines.append(txt_row('Venafi         = Certificate lifecycle manager; issues and renews ACM/EC2 certs'))
    lines.append(txt_row('SNS → Slack    = Cost alerts published to SNS topic then forwarded to Slack webhook'))
    lines.append(txt_row('CMDB AWS sync  = ServiceNow discovery pulling AWS resource inventory via API'))
    lines.append(txt_row('CloudFormation = AWS native IaC; stack-based resource provisioning and updates'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-arch-design', 'docs/cloud/aws/architecture/design-standards/index.md', 'AWS Architecture — Design Standards')
def _aws_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Architecture — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Standards covering account structure, tagging, naming, networking, and security baseline.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Account Standards'), bMid(L2, R2, 'Tagging Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'One workload per account'), bMid(L2, R2, 'Required: env, owner, team'))))
    lines.append(R(merge(bMid(L1, R1, 'No production in mgmt acct'), bMid(L2, R2, 'Required: cost-centre, app'))))
    lines.append(R(merge(bMid(L1, R1, 'OU hierarchy: env-based'), bMid(L2, R2, 'Enforce: SCP deny untagged'))))
    lines.append(R(merge(bMid(L1, R1, 'Separate audit + log accts'), bMid(L2, R2, 'Naming: kebab-case standard'))))
    lines.append(R(merge(bMid(L1, R1, 'Email alias per account'), bMid(L2, R2, 'Automation: tag on create'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Account and tagging standards enforced via SCPs and AWS Config rules'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Networking Standards'), bMid(L2, R2, 'Security Baseline'))))
    lines.append(R(merge(bMid(L1, R1, 'Non-overlapping VPC CIDRs'), bMid(L2, R2, 'MFA: enforced by SCP'))))
    lines.append(R(merge(bMid(L1, R1, 'Private subnets for workloads'), bMid(L2, R2, 'Root: no programmatic keys'))))
    lines.append(R(merge(bMid(L1, R1, 'Public: only LB + NAT GW'), bMid(L2, R2, 'CloudTrail: always on'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC flow logs: enabled'), bMid(L2, R2, 'GuardDuty: org-wide on'))))
    lines.append(R(merge(bMid(L1, R1, 'TGW: centralised egress'), bMid(L2, R2, 'CIS AWS Benchmark: target'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · Availability Zones · data centres · DirectConnect · internet edge'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS AWS Benchmark= Center for Internet Security prescriptive AWS security controls'))
    lines.append(txt_row('Non-overlapping CIDR= VPC address ranges that do not conflict; required for TGW'))
    lines.append(txt_row('Private subnet = No internet gateway route; workloads access internet via NAT GW'))
    lines.append(txt_row('Public subnet  = Has internet gateway route; only load balancers and NAT GW placed here'))
    lines.append(txt_row('Centralised egress= All internet-bound traffic routed through shared inspection VPC'))
    lines.append(txt_row('Email alias    = Shared mailbox per account; avoids personal email ownership'))
    lines.append(txt_row('Kebab-case     = Naming convention using lowercase words separated by hyphens'))
    lines.append(txt_row('SCP deny untagged= Preventive control blocking resource creation without required tags'))
    lines.append(txt_row('Cost-centre tag= Tag linking resources to financial cost allocation unit'))
    lines.append(txt_row('VPC flow logs  = Network traffic metadata logs; required for security investigations'))
    lines.append(txt_row('Audit account  = Dedicated account for security tooling (Security Hub, Config agg.)'))
    lines.append(txt_row('OU hierarchy   = Organizational Unit tree: Root → Security → Workloads → env OUs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-backup-aws-backup', 'docs/cloud/aws/backup/aws-backup/index.md', 'AWS Backup — AWS Backup Service')
def _aws_backup_aws_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Backup — AWS Backup Service'))
    lines.append(txt_row())
    lines.append(txt_row('Centralised backup service managing policies, jobs, and vaults across AWS services.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Overview'), bMid(L2, R2, 'Supported Resources'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup plans: schedule + rules'), bMid(L2, R2, 'EC2: AMI + EBS snapshots'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup vault: encrypted store'), bMid(L2, R2, 'RDS: automated snapshots'))))
    lines.append(R(merge(bMid(L1, R1, 'Recovery points: per resource'), bMid(L2, R2, 'EFS: file system backups'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-region: copy rule'), bMid(L2, R2, 'DynamoDB: on-demand backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account: OU copy'), bMid(L2, R2, 'S3: continuous backup'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Backup plans target resources via tags; vaults hold recovery points with lifecycle'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Vault Configuration'), bMid(L2, R2, 'Compliance Controls'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS: customer-managed key'), bMid(L2, R2, 'AWS Backup Audit Manager'))))
    lines.append(R(merge(bMid(L1, R1, 'Vault lock: WORM policy'), bMid(L2, R2, 'Config rule: backup exists'))))
    lines.append(R(merge(bMid(L1, R1, 'Access policy: cross-acct'), bMid(L2, R2, 'Report: coverage + jobs'))))
    lines.append(R(merge(bMid(L1, R1, 'Lifecycle: cold storage tier'), bMid(L2, R2, 'Alert: SNS on job failure'))))
    lines.append(R(merge(bMid(L1, R1, 'Notifications: SNS topic'), bMid(L2, R2, 'Org backup policy: SCP'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS S3 Glacier (cold tier) · KMS HSMs · SNS · AWS Regions for cross-region copy'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup plan     = Policy defining schedule, retention, and lifecycle for backups'))
    lines.append(txt_row('Backup vault    = Encrypted container storing recovery points; access-controlled'))
    lines.append(txt_row('Recovery point  = Snapshot of a resource at a specific point in time'))
    lines.append(txt_row('Vault lock      = WORM policy preventing deletion of recovery points; compliance'))
    lines.append(txt_row('Cross-region copy= Rule copying backup to another AWS region for DR'))
    lines.append(txt_row('Cross-account copy= Copies recovery points to a separate AWS account for isolation'))
    lines.append(txt_row('Audit Manager   = AWS service verifying backup compliance against control framework'))
    lines.append(txt_row('KMS CMK         = Customer-Managed Key encrypting the backup vault'))
    lines.append(txt_row('Cold storage    = Cheaper long-term tier (Glacier); lower cost, higher restore time'))
    lines.append(txt_row('Lifecycle rule  = Transitions recovery points to cold storage after N days'))
    lines.append(txt_row('Org backup policy= Backup plan deployed org-wide via AWS Organizations'))
    lines.append(txt_row('WORM            = Write Once Read Many; immutable storage preventing modification'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-backup-compliance', 'docs/cloud/aws/backup/backup-compliance/index.md', 'AWS Backup — Compliance')
def _aws_backup_compliance():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Backup — Compliance'))
    lines.append(txt_row())
    lines.append(txt_row('Backup compliance enforced via Audit Manager controls, Config rules, and vault lock.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Audit Manager Controls'), bMid(L2, R2, 'Config Rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Framework: custom or managed'), bMid(L2, R2, 'backup-plan-min-frequency'))))
    lines.append(R(merge(bMid(L1, R1, 'Control: backup freq policy'), bMid(L2, R2, 'backup-recovery-point-exists'))))
    lines.append(R(merge(bMid(L1, R1, 'Control: retention >= N days'), bMid(L2, R2, 'backup-recovery-point-encrypted'))))
    lines.append(R(merge(bMid(L1, R1, 'Report: daily compliance pdf'), bMid(L2, R2, 'rds-in-backup-plan'))))
    lines.append(R(merge(bMid(L1, R1, 'Dashboard: pass/fail per acct'), bMid(L2, R2, 'dynamodb-in-backup-plan'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Audit Manager reports compliance; Config rules detect non-compliant resources'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Vault Lock Compliance'), bMid(L2, R2, 'Reporting'))))
    lines.append(R(merge(bMid(L1, R1, 'Governance mode: adjustable'), bMid(L2, R2, 'S3: compliance reports stored'))))
    lines.append(R(merge(bMid(L1, R1, 'Compliance mode: immutable'), bMid(L2, R2, 'SNS: alert on non-compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Min retention: enforced'), bMid(L2, R2, 'Security Hub: findings ingest'))))
    lines.append(R(merge(bMid(L1, R1, 'Deletion blocked: during lock'), bMid(L2, R2, 'Org-level: aggregated view'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: who accessed vault'), bMid(L2, R2, 'Annual review: retention policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Backup vaults · S3 (report storage) · KMS · Security Hub · SNS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Audit Manager  = AWS service mapping backup controls to compliance frameworks'))
    lines.append(txt_row('Governance mode= Vault lock allowing admin override; not fully immutable'))
    lines.append(txt_row('Compliance mode= Vault lock that cannot be changed after applied; truly immutable'))
    lines.append(txt_row('Config rule    = AWS Config check detecting resources not covered by backup plan'))
    lines.append(txt_row('backup-plan-min-frequency= Config rule ensuring backups run at least daily'))
    lines.append(txt_row('Recovery point encrypted= Config rule ensuring all backup data is KMS-encrypted'))
    lines.append(txt_row('Min retention  = Vault lock enforces recovery points cannot expire before N days'))
    lines.append(txt_row('Security Hub   = Receives Config non-compliance findings as security findings'))
    lines.append(txt_row('Org-level view = Cross-account aggregation of backup compliance across all accounts'))
    lines.append(txt_row('Compliance PDF = Daily report generated by Audit Manager summarising pass/fail'))
    lines.append(txt_row('rds-in-backup-plan= Config rule confirming every RDS instance has a backup plan'))
    lines.append(txt_row('Vault access audit= CloudTrail records who accessed or restored from vault'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-backup-jobs', 'docs/cloud/aws/backup/backup-jobs/index.md', 'AWS Backup — Backup Jobs')
def _aws_backup_jobs():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Backup — Backup Jobs'))
    lines.append(txt_row())
    lines.append(txt_row('Backup jobs execute on schedule or on-demand; monitor status, duration, and failures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Job Lifecycle'), bMid(L2, R2, 'Job Types'))))
    lines.append(R(merge(bMid(L1, R1, 'Created: plan triggers job'), bMid(L2, R2, 'Backup: resource to vault'))))
    lines.append(R(merge(bMid(L1, R1, 'Running: snapshot in progress'), bMid(L2, R2, 'Copy: vault to vault/region'))))
    lines.append(R(merge(bMid(L1, R1, 'Completed: recovery point saved'), bMid(L2, R2, 'Restore: point to resource'))))
    lines.append(R(merge(bMid(L1, R1, 'Failed: SNS alert + retry'), bMid(L2, R2, 'On-demand: manual trigger'))))
    lines.append(R(merge(bMid(L1, R1, 'Expired: retention lifecycle'), bMid(L2, R2, 'Continuous: S3/SAP HANA'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Jobs created by plan schedule; status monitored via console, CLI, or EventBridge'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitoring'), bMid(L2, R2, 'Troubleshooting'))))
    lines.append(R(merge(bMid(L1, R1, 'Console: Jobs dashboard'), bMid(L2, R2, 'IAM: BackupRole missing perms'))))
    lines.append(R(merge(bMid(L1, R1, 'CLI: list-backup-jobs'), bMid(L2, R2, 'KMS: key access denied'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudWatch: BackupJobsFailed'), bMid(L2, R2, 'Resource busy: snapshot limit'))))
    lines.append(R(merge(bMid(L1, R1, 'EventBridge: job state change'), bMid(L2, R2, 'Service quota: job concurrency'))))
    lines.append(R(merge(bMid(L1, R1, 'SNS: failure notification'), bMid(L2, R2, 'Retry: on-demand after fix'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Backup service · KMS HSM · SNS · CloudWatch · target resource (EBS/RDS/EFS)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Recovery point  = Immutable snapshot stored in vault; created on job completion'))
    lines.append(txt_row('BackupRole      = IAM role AWS Backup assumes to access resources for backup'))
    lines.append(txt_row('BackupJobsFailed= CloudWatch metric counting failed backup jobs in a period'))
    lines.append(txt_row('EventBridge     = Routes backup job state-change events to Lambda or SNS'))
    lines.append(txt_row('Continuous backup= Point-in-time recovery for S3; RPO of 1 hour'))
    lines.append(txt_row('Copy job        = Replicates recovery point to another vault or region'))
    lines.append(txt_row('Restore job     = Creates new resource from a recovery point'))
    lines.append(txt_row('On-demand job   = Manual one-off backup outside of plan schedule'))
    lines.append(txt_row('Service quota   = AWS limit on concurrent backup jobs per account'))
    lines.append(txt_row('Snapshot limit  = EBS limit on concurrent snapshots per volume'))
    lines.append(txt_row('SNS notification= Alert sent to subscribed email/Slack/Lambda on job failure'))
    lines.append(txt_row('list-backup-jobs= AWS CLI command to query job history and status'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-backup-plans', 'docs/cloud/aws/backup/backup-plans/index.md', 'AWS Backup — Backup Plans')
def _aws_backup_plans():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Backup — Backup Plans'))
    lines.append(txt_row())
    lines.append(txt_row('Backup plans define schedule, lifecycle, vault, and copy rules for targeted resources.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Plan Structure'), bMid(L2, R2, 'Rule Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'Rules: one or more per plan'), bMid(L2, R2, 'Schedule: cron or rate'))))
    lines.append(R(merge(bMid(L1, R1, 'Resources: tag-based select'), bMid(L2, R2, 'Start window: 60 min default'))))
    lines.append(R(merge(bMid(L1, R1, 'Vault: destination for points'), bMid(L2, R2, 'Completion window: 8 hr'))))
    lines.append(R(merge(bMid(L1, R1, 'Plan versions: track changes'), bMid(L2, R2, 'Retention: days to keep'))))
    lines.append(R(merge(bMid(L1, R1, 'Org policy: deploy org-wide'), bMid(L2, R2, 'Copy: region or account'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Tag-based selection targets resources; rules define when and where backups go'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Lifecycle Configuration'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'Warm tier: standard storage'), bMid(L2, R2, '3-2-1: 3 copies, 2 media, 1 offsite'))))
    lines.append(R(merge(bMid(L1, R1, 'Cold tier: after N days'), bMid(L2, R2, 'Prod: daily + weekly + monthly'))))
    lines.append(R(merge(bMid(L1, R1, 'Expire: delete after M days'), bMid(L2, R2, 'Dev: daily 7-day retention'))))
    lines.append(R(merge(bMid(L1, R1, 'Min 90 days in cold storage'), bMid(L2, R2, 'Cross-region: DR account'))))
    lines.append(R(merge(bMid(L1, R1, 'Cold storage saves ~60% cost'), bMid(L2, R2, 'Test restore: quarterly'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Backup service · S3 Glacier (cold tier) · target resources · KMS · SNS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup plan     = Policy containing rules that define backup schedule and lifecycle'))
    lines.append(txt_row('Backup rule     = Single schedule+lifecycle+vault combination within a plan'))
    lines.append(txt_row('Tag-based select= Backup plan assigns resources matching specified tag key/value'))
    lines.append(txt_row('Start window    = Time after scheduled start within which job must begin'))
    lines.append(txt_row('Completion window= Max time allowed for backup job before it is marked failed'))
    lines.append(txt_row('Warm tier       = Standard S3 storage class; fast restore, higher cost'))
    lines.append(txt_row('Cold tier       = Glacier storage; lower cost but 12-hour restore time'))
    lines.append(txt_row('3-2-1 rule      = 3 copies, 2 storage types, 1 offsite; standard DR practice'))
    lines.append(txt_row('Org policy      = Backup plan deployed to all accounts via AWS Organizations'))
    lines.append(txt_row('Plan version    = Immutable snapshot of plan configuration for audit trail'))
    lines.append(txt_row('Retention days  = How long recovery points are kept before automatic deletion'))
    lines.append(txt_row('Quarterly test  = Best practice: restore from backup to verify recoverability'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-backup-vaults', 'docs/cloud/aws/backup/backup-vaults/index.md', 'AWS Backup — Backup Vaults')
def _aws_backup_vaults():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Backup — Backup Vaults'))
    lines.append(txt_row())
    lines.append(txt_row('Backup vaults store recovery points; secured with KMS, access policies, and vault lock.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Vault Configuration'), bMid(L2, R2, 'Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'Default vault: per account'), bMid(L2, R2, 'KMS CMK: customer-managed'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom vaults: by purpose'), bMid(L2, R2, 'Key policy: who can decrypt'))))
    lines.append(R(merge(bMid(L1, R1, 'Regional: data sovereignty'), bMid(L2, R2, 'Separate key per vault'))))
    lines.append(R(merge(bMid(L1, R1, 'Logical container: IAM gated'), bMid(L2, R2, 'Key rotation: annual'))))
    lines.append(R(merge(bMid(L1, R1, 'Naming: env-purpose-region'), bMid(L2, R2, 'Cross-acct: key grant needed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Vault KMS key controls who can restore; access policy controls who can list/delete'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Access Policy'), bMid(L2, R2, 'Vault Lock'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource policy on vault'), bMid(L2, R2, 'Governance: admin override'))))
    lines.append(R(merge(bMid(L1, R1, 'Allow: specific IAM roles'), bMid(L2, R2, 'Compliance: immutable lock'))))
    lines.append(R(merge(bMid(L1, R1, 'Deny: public access'), bMid(L2, R2, 'Min retention enforced'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-acct: explicit allow'), bMid(L2, R2, 'Max retention: optional'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: CloudTrail API calls'), bMid(L2, R2, 'Compliance mode: immutable'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Backup storage (S3-backed) · KMS HSM · CloudTrail · IAM policy engine'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Default vault   = Auto-created vault per account; uses AWS-managed key'))
    lines.append(txt_row('Custom vault    = Admin-created vault with specific CMK and access policy'))
    lines.append(txt_row('CMK             = Customer-Managed Key in KMS; gives explicit control over access'))
    lines.append(txt_row('Key grant       = Permission allowing cross-account backup to use CMK for decryption'))
    lines.append(txt_row('Access policy   = Resource-based IAM policy on vault; controls list/restore/delete'))
    lines.append(txt_row('Vault lock      = Feature preventing recovery point deletion before retention expires'))
    lines.append(txt_row('Governance mode = Vault lock allowing admin to remove lock before 72-hour grace'))
    lines.append(txt_row('Compliance mode = Vault lock permanent after grace period; cannot be unlocked'))
    lines.append(txt_row('Min retention   = Vault lock rule ensuring recovery points cannot expire early'))
    lines.append(txt_row('Max retention   = Optional lock rule capping maximum retention to limit cost'))
    lines.append(txt_row('Regional vault  = Vault exists in one region; cross-region requires copy rule'))
    lines.append(txt_row('Key rotation    = Annual CMK rotation; old key versions retained for decryption'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-backup-restore-testing', 'docs/cloud/aws/backup/restore-testing/index.md', 'AWS Backup — Restore Testing')
def _aws_backup_restore_testing():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Backup — Restore Testing'))
    lines.append(txt_row())
    lines.append(txt_row('Automated restore testing validates recoverability on schedule without manual effort.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Testing Plans'), bMid(L2, R2, 'Test Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: daily/weekly test'), bMid(L2, R2, 'Recovery point selection'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource types: EC2/RDS/EFS'), bMid(L2, R2, 'Latest or random point'))))
    lines.append(R(merge(bMid(L1, R1, 'Isolated test account'), bMid(L2, R2, 'Validation: Lambda hook'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-delete after test'), bMid(L2, R2, 'Start window: 1-8 hours'))))
    lines.append(R(merge(bMid(L1, R1, 'Report: per-test result'), bMid(L2, R2, 'IAM: restore test role'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Test plan restores to isolated account; Lambda validates; resource auto-deleted'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Validation Logic'), bMid(L2, R2, 'Reporting'))))
    lines.append(R(merge(bMid(L1, R1, 'Lambda: post-restore check'), bMid(L2, R2, 'Console: test history'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2: SSM run-command ping'), bMid(L2, R2, 'CloudWatch: test metrics'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: query connectivity test'), bMid(L2, R2, 'SNS: failure alert'))))
    lines.append(R(merge(bMid(L1, R1, 'EFS: mount + read check'), bMid(L2, R2, 'Audit Manager: compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Pass/fail: status to report'), bMid(L2, R2, 'Quarterly review: RTO met'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Backup · isolated test account · Lambda · SNS · CloudWatch · target resource'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Restore testing = AWS Backup feature automating periodic restore validation'))
    lines.append(txt_row('Isolated account= Separate AWS account used for test restores; no prod impact'))
    lines.append(txt_row('Lambda hook     = Function invoked post-restore to validate resource is functional'))
    lines.append(txt_row('Auto-delete     = Test resource deleted automatically after validation completes'))
    lines.append(txt_row('Recovery point  = Snapshot used for restore test; latest or randomly selected'))
    lines.append(txt_row('RTO validation  = Test confirms restore completes within target recovery time'))
    lines.append(txt_row('SSM run-command = Execute script on EC2 without SSH; validates post-restore state'))
    lines.append(txt_row('Start window    = Allowed time after scheduled start before test is abandoned'))
    lines.append(txt_row('Restore test role= IAM role with permissions to restore resources in test account'))
    lines.append(txt_row('Audit Manager   = Records restore test results for compliance reporting'))
    lines.append(txt_row('CloudWatch metric= Tracks test success/failure counts over time'))
    lines.append(txt_row('Quarterly review= Manual review of test history to confirm RPO/RTO targets met'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-cloudformation', 'docs/cloud/aws/cli-reference/cloudformation/index.md', 'AWS CLI — CloudFormation')
def _aws_cli_cloudformation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — CloudFormation'))
    lines.append(txt_row())
    lines.append(txt_row('Key CloudFormation CLI commands for stack management, drift detection, and StackSets.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Stack Operations'), bMid(L2, R2, 'Stack Inspection'))))
    lines.append(R(merge(bMid(L1, R1, 'create-stack: deploy template'), bMid(L2, R2, 'describe-stacks: status'))))
    lines.append(R(merge(bMid(L1, R1, 'update-stack: apply changes'), bMid(L2, R2, 'list-stacks: all stacks'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-stack: teardown'), bMid(L2, R2, 'describe-stack-events: log'))))
    lines.append(R(merge(bMid(L1, R1, 'create-change-set: preview'), bMid(L2, R2, 'describe-stack-resources'))))
    lines.append(R(merge(bMid(L1, R1, 'execute-change-set: apply'), bMid(L2, R2, 'get-template: fetch yaml'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Always preview via change-set before executing; describe-stack-events for failures'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Drift and Validation'), bMid(L2, R2, 'StackSets'))))
    lines.append(R(merge(bMid(L1, R1, 'detect-stack-drift: check'), bMid(L2, R2, 'create-stack-set: define'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-stack-drift-result'), bMid(L2, R2, 'create-stack-instances: deploy'))))
    lines.append(R(merge(bMid(L1, R1, 'validate-template: lint'), bMid(L2, R2, 'update-stack-instances'))))
    lines.append(R(merge(bMid(L1, R1, 'cfn-lint: local pre-check'), bMid(L2, R2, 'list-stack-instances'))))
    lines.append(R(merge(bMid(L1, R1, 'package: upload S3 artifacts'), bMid(L2, R2, 'delete-stack-instances'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS CloudFormation service · S3 (template storage) · IAM · target AWS resources'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Stack           = CloudFormation deployment unit; collection of AWS resources'))
    lines.append(txt_row('Change set      = Preview of changes before applying; shows add/modify/remove'))
    lines.append(txt_row('Stack drift     = Resource has been modified outside of CloudFormation'))
    lines.append(txt_row('StackSet        = Multi-account/region CloudFormation deployment'))
    lines.append(txt_row('Stack instance  = Single stack deployment within a StackSet target'))
    lines.append(txt_row('validate-template= Checks CloudFormation YAML/JSON syntax before deployment'))
    lines.append(txt_row('cfn-lint        = Open-source linter; checks CloudFormation best practices'))
    lines.append(txt_row('package         = Uploads local artifacts to S3 and rewrites template references'))
    lines.append(txt_row('describe-stack-events= Chronological log of resource operations during deploy'))
    lines.append(txt_row('get-template    = Retrieves the template used to create or update the stack'))
    lines.append(txt_row('DELETE_FAILED   = Stack deletion failed; manual resource cleanup then retry'))
    lines.append(txt_row('ROLLBACK        = Failed update reverts to last known good configuration'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-cloudwatch', 'docs/cloud/aws/cli-reference/cloudwatch/index.md', 'AWS CLI — CloudWatch')
def _aws_cli_cloudwatch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — CloudWatch'))
    lines.append(txt_row())
    lines.append(txt_row('CloudWatch CLI commands for metrics, alarms, log groups, dashboards, and insights.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Metrics Commands'), bMid(L2, R2, 'Alarm Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'list-metrics: available'), bMid(L2, R2, 'describe-alarms: list'))))
    lines.append(R(merge(bMid(L1, R1, 'get-metric-statistics: query'), bMid(L2, R2, 'put-metric-alarm: create'))))
    lines.append(R(merge(bMid(L1, R1, 'put-metric-data: publish'), bMid(L2, R2, 'set-alarm-state: test'))))
    lines.append(R(merge(bMid(L1, R1, 'get-metric-data: bulk query'), bMid(L2, R2, 'delete-alarms: remove'))))
    lines.append(R(merge(bMid(L1, R1, 'list-dashboards: overview'), bMid(L2, R2, 'describe-alarm-history'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Metrics queried with namespace+dimension; alarms reference metric and threshold'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Logs Commands'), bMid(L2, R2, 'Insights Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-log-groups: list'), bMid(L2, R2, 'start-query: run query'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-log-streams: list'), bMid(L2, R2, 'get-query-results: fetch'))))
    lines.append(R(merge(bMid(L1, R1, 'get-log-events: raw events'), bMid(L2, R2, 'describe-queries: history'))))
    lines.append(R(merge(bMid(L1, R1, 'filter-log-events: search'), bMid(L2, R2, 'stop-query: cancel run'))))
    lines.append(R(merge(bMid(L1, R1, 'put-log-events: write logs'), bMid(L2, R2, 'create-log-group: setup'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('CloudWatch service · S3 (log export) · SNS (alarm action) · Lambda (alarm action)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Namespace       = Grouping for metrics, e.g. AWS/EC2, AWS/RDS, Custom/App'))
    lines.append(txt_row('Dimension       = Key-value pair identifying metric source, e.g. InstanceId=i-xxx'))
    lines.append(txt_row('get-metric-data = Bulk metric query with math expressions; preferred over statistics'))
    lines.append(txt_row('put-metric-data = Publishes custom application metrics to CloudWatch'))
    lines.append(txt_row('set-alarm-state = Forces alarm state for testing SNS/Lambda alarm actions'))
    lines.append(txt_row('filter-log-events= Searches log streams with pattern filter and time range'))
    lines.append(txt_row('Insights query  = SQL-like syntax for querying structured log data'))
    lines.append(txt_row('Log group       = Container for log streams; has retention policy'))
    lines.append(txt_row('Log stream      = Sequence of log events from one source (EC2 instance, Lambda)'))
    lines.append(txt_row('Retention policy= Days to keep log events before automatic deletion'))
    lines.append(txt_row('describe-alarm-history= Shows state transitions for debugging alarm behavior'))
    lines.append(txt_row('put-metric-alarm= Creates/updates alarm; defines threshold, period, evaluation count'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-ec2-instances', 'docs/cloud/aws/cli-reference/ec2-instances/index.md', 'AWS CLI — EC2 Instances')
def _aws_cli_ec2_instances():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — EC2 Instances'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 instance CLI commands for lifecycle, metadata, connect, and troubleshooting.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Instance Lifecycle'), bMid(L2, R2, 'Instance Inspection'))))
    lines.append(R(merge(bMid(L1, R1, 'run-instances: launch'), bMid(L2, R2, 'describe-instances: list'))))
    lines.append(R(merge(bMid(L1, R1, 'start-instances: power on'), bMid(L2, R2, 'describe-instance-status'))))
    lines.append(R(merge(bMid(L1, R1, 'stop-instances: graceful'), bMid(L2, R2, 'describe-instance-attribute'))))
    lines.append(R(merge(bMid(L1, R1, 'reboot-instances: restart'), bMid(L2, R2, 'get-console-output: log'))))
    lines.append(R(merge(bMid(L1, R1, 'terminate-instances: delete'), bMid(L2, R2, 'get-console-screenshot'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('run-instances launches; describe-instances filters by state, tag, or instance ID'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Connect and Manage'), bMid(L2, R2, 'Metadata and Tags'))))
    lines.append(R(merge(bMid(L1, R1, 'ssm start-session: shell'), bMid(L2, R2, 'describe-tags: list tags'))))
    lines.append(R(merge(bMid(L1, R1, 'ec2-instance-connect: SSH'), bMid(L2, R2, 'create-tags: add tag'))))
    lines.append(R(merge(bMid(L1, R1, 'send-ssh-public-key: temp'), bMid(L2, R2, 'delete-tags: remove'))))
    lines.append(R(merge(bMid(L1, R1, 'modify-instance-attribute'), bMid(L2, R2, 'describe-instance-types'))))
    lines.append(R(merge(bMid(L1, R1, 'monitor-instances: enable'), bMid(L2, R2, 'describe-availability-zones'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 host hardware · Nitro hypervisor · VPC network · EBS storage · SSM service'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('run-instances   = Launches one or more EC2 instances from an AMI'))
    lines.append(txt_row('ssm start-session= Opens interactive shell via SSM without SSH or key pair'))
    lines.append(txt_row('ec2-instance-connect= Pushes temporary SSH public key and opens SSH session'))
    lines.append(txt_row('get-console-output= Retrieves serial console log; useful when instance unreachable'))
    lines.append(txt_row('get-console-screenshot= Screenshot of instance display; diagnose stuck boot'))
    lines.append(txt_row('describe-instance-status= Shows system and instance reachability check results'))
    lines.append(txt_row('modify-instance-attribute= Changes instance type, user data, or termination protection'))
    lines.append(txt_row('monitor-instances= Enables detailed 1-minute CloudWatch monitoring'))
    lines.append(txt_row('Nitro hypervisor= AWS-built hypervisor providing performance and security isolation'))
    lines.append(txt_row('Termination protection= Setting preventing accidental terminate-instances call'))
    lines.append(txt_row('Instance metadata= EC2 service at 169.254.169.254 providing IAM role credentials'))
    lines.append(txt_row('User data       = Script or cloud-init config executed on first boot'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-ec2-storage', 'docs/cloud/aws/cli-reference/ec2-storage/index.md', 'AWS CLI — EC2 Storage')
def _aws_cli_ec2_storage():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — EC2 Storage'))
    lines.append(txt_row())
    lines.append(txt_row('EBS volume and snapshot CLI commands for provisioning, attaching, and DR operations.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Volume Operations'), bMid(L2, R2, 'Volume Inspection'))))
    lines.append(R(merge(bMid(L1, R1, 'create-volume: provision'), bMid(L2, R2, 'describe-volumes: list'))))
    lines.append(R(merge(bMid(L1, R1, 'attach-volume: mount to EC2'), bMid(L2, R2, 'describe-volume-status'))))
    lines.append(R(merge(bMid(L1, R1, 'detach-volume: unmount'), bMid(L2, R2, 'describe-volume-attribute'))))
    lines.append(R(merge(bMid(L1, R1, 'modify-volume: resize/type'), bMid(L2, R2, 'describe-volumes-modifications'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-volume: remove'), bMid(L2, R2, 'enable-volume-io: recover'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Volumes created and attached; modify-volume resizes without downtime on Nitro'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshot Operations'), bMid(L2, R2, 'Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'create-snapshot: point-in-time'), bMid(L2, R2, 'create-volume --encrypted'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-snapshots: list'), bMid(L2, R2, 'copy-snapshot: encrypt copy'))))
    lines.append(R(merge(bMid(L1, R1, 'copy-snapshot: cross-region'), bMid(L2, R2, 'modify-ebs-default-encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-snapshot: purge'), bMid(L2, R2, '--kms-key-id: specify CMK'))))
    lines.append(R(merge(bMid(L1, R1, 'restore-snapshot-tier: thaw'), bMid(L2, R2, 'describe-ebs-encryption-default'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EBS storage hardware · Nitro hypervisor · KMS HSM · S3 (snapshot storage)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EBS             = Elastic Block Store; persistent block storage for EC2'))
    lines.append(txt_row('modify-volume   = Online resize or type change; no detach needed on Nitro instances'))
    lines.append(txt_row('enable-volume-io= Re-enables I/O on a volume after a potential data inconsistency'))
    lines.append(txt_row('Snapshot        = Incremental backup of EBS volume stored in S3'))
    lines.append(txt_row('copy-snapshot   = Copies snapshot to another region for DR'))
    lines.append(txt_row('restore-snapshot-tier= Restores archived snapshot from S3 Glacier to standard tier'))
    lines.append(txt_row('CMK             = Customer-Managed Key in KMS; used to encrypt EBS volumes'))
    lines.append(txt_row('modify-ebs-default-encryption= Sets account-level default to encrypt all new volumes'))
    lines.append(txt_row('Volume type     = gp3 (general), io2 (IOPS), st1 (throughput), sc1 (cold)'))
    lines.append(txt_row('gp3             = Default SSD volume; baseline 3000 IOPS, 125 MB/s throughput'))
    lines.append(txt_row('io2             = High-performance SSD; up to 64,000 IOPS; provisioned IOPS'))
    lines.append(txt_row('Nitro           = AWS hypervisor; allows online volume modifications without reboot'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-eks', 'docs/cloud/aws/cli-reference/eks/index.md', 'AWS CLI — EKS')
def _aws_cli_eks():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — EKS'))
    lines.append(txt_row())
    lines.append(txt_row('EKS CLI commands for cluster management, node groups, add-ons, and kubeconfig.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Operations'), bMid(L2, R2, 'Node Group Operations'))))
    lines.append(R(merge(bMid(L1, R1, 'create-cluster: provision'), bMid(L2, R2, 'create-nodegroup'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-cluster: status'), bMid(L2, R2, 'describe-nodegroup'))))
    lines.append(R(merge(bMid(L1, R1, 'list-clusters: all in region'), bMid(L2, R2, 'update-nodegroup-config'))))
    lines.append(R(merge(bMid(L1, R1, 'update-cluster-version: upgrade'), bMid(L2, R2, 'update-nodegroup-version'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-cluster: teardown'), bMid(L2, R2, 'delete-nodegroup'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Cluster upgraded first; then node groups updated to matching Kubernetes version'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Access and Auth'), bMid(L2, R2, 'Add-ons'))))
    lines.append(R(merge(bMid(L1, R1, 'update-kubeconfig: merge'), bMid(L2, R2, 'create-addon: install'))))
    lines.append(R(merge(bMid(L1, R1, 'create-access-entry: IAM map'), bMid(L2, R2, 'describe-addon: version'))))
    lines.append(R(merge(bMid(L1, R1, 'associate-access-policy'), bMid(L2, R2, 'update-addon: upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'list-access-entries', ), bMid(L2, R2, 'delete-addon: remove'))))
    lines.append(R(merge(bMid(L1, R1, 'create-fargate-profile'), bMid(L2, R2, 'describe-addon-versions'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EKS control plane (AWS-managed) · EC2 worker nodes · VPC · IAM · EBS/EFS storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EKS             = Elastic Kubernetes Service; managed Kubernetes control plane'))
    lines.append(txt_row('Node group      = Managed group of EC2 worker nodes; auto-scaling enabled'))
    lines.append(txt_row('update-kubeconfig= Adds EKS cluster to local ~/.kube/config for kubectl access'))
    lines.append(txt_row('Access entry    = EKS API method mapping IAM principal to Kubernetes RBAC role'))
    lines.append(txt_row('Associate policy= Binds a predefined EKS access policy to an access entry'))
    lines.append(txt_row('Add-on          = Managed EKS component: CoreDNS, kube-proxy, VPC CNI, EBS CSI'))
    lines.append(txt_row('Fargate profile = Runs pods serverlessly without managing EC2 node groups'))
    lines.append(txt_row('update-cluster-version= Upgrades EKS control plane to next minor version'))
    lines.append(txt_row('update-nodegroup-version= Replaces node group nodes with new Kubernetes AMI version'))
    lines.append(txt_row('VPC CNI         = AWS VPC Container Network Interface plugin; assigns pod IPs from VPC'))
    lines.append(txt_row('EBS CSI driver  = Kubernetes CSI driver for provisioning EBS volumes as PVs'))
    lines.append(txt_row('IRSA            = IAM Roles for Service Accounts; pods assume IAM roles via OIDC'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-iam', 'docs/cloud/aws/cli-reference/iam/index.md', 'AWS CLI — IAM')
def _aws_cli_iam():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — IAM'))
    lines.append(txt_row())
    lines.append(txt_row('IAM CLI commands for users, roles, policies, MFA, and access key management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'User Management'), bMid(L2, R2, 'Role Management'))))
    lines.append(R(merge(bMid(L1, R1, 'create-user: new IAM user'), bMid(L2, R2, 'create-role: with trust policy'))))
    lines.append(R(merge(bMid(L1, R1, 'list-users: all users'), bMid(L2, R2, 'list-roles: all roles'))))
    lines.append(R(merge(bMid(L1, R1, 'get-user: user details'), bMid(L2, R2, 'assume-role: get credentials'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-user: remove'), bMid(L2, R2, 'update-assume-role-policy'))))
    lines.append(R(merge(bMid(L1, R1, 'update-login-profile: passwd'), bMid(L2, R2, 'list-attached-role-policies'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Users for human access; roles for service and cross-account access'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy and Key Management'), bMid(L2, R2, 'MFA and Security'))))
    lines.append(R(merge(bMid(L1, R1, 'create-policy: new managed'), bMid(L2, R2, 'enable-mfa-device: attach'))))
    lines.append(R(merge(bMid(L1, R1, 'attach-user-policy: assign'), bMid(L2, R2, 'deactivate-mfa-device'))))
    lines.append(R(merge(bMid(L1, R1, 'create-access-key: new key'), bMid(L2, R2, 'get-credential-report'))))
    lines.append(R(merge(bMid(L1, R1, 'update-access-key: disable'), bMid(L2, R2, 'generate-credential-report'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-access-key: remove'), bMid(L2, R2, 'get-account-summary: stats'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('IAM service (global) · AWS STS (assume-role) · CloudTrail (API logging)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('assume-role     = Requests temporary credentials for a role via STS'))
    lines.append(txt_row('Trust policy    = JSON policy on a role defining who can assume it'))
    lines.append(txt_row('Managed policy  = Standalone IAM policy; attached to multiple users/roles'))
    lines.append(txt_row('Inline policy   = Policy embedded directly in user/role; not reusable'))
    lines.append(txt_row('Access key      = Long-term programmatic credentials; rotate every 90 days'))
    lines.append(txt_row('update-access-key= Disables or activates an access key without deleting'))
    lines.append(txt_row('Credential report= CSV of all IAM users with last-used dates and MFA status'))
    lines.append(txt_row('enable-mfa-device= Registers a virtual or hardware MFA token for a user'))
    lines.append(txt_row('STS             = Security Token Service; issues temporary credentials'))
    lines.append(txt_row('get-account-summary= Returns counts of users, roles, policies, groups'))
    lines.append(txt_row('Permission boundary= IAM policy limiting max permissions a principal can have'))
    lines.append(txt_row('update-login-profile= Changes console password for an IAM user'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-lambda', 'docs/cloud/aws/cli-reference/lambda/index.md', 'AWS CLI — Lambda')
def _aws_cli_lambda():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — Lambda'))
    lines.append(txt_row())
    lines.append(txt_row('Lambda CLI commands for function deploy, invoke, configuration, and log retrieval.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Function Management'), bMid(L2, R2, 'Invocation'))))
    lines.append(R(merge(bMid(L1, R1, 'create-function: deploy'), bMid(L2, R2, 'invoke: synchronous call'))))
    lines.append(R(merge(bMid(L1, R1, 'update-function-code: redeploy'), bMid(L2, R2, 'invoke --invocation-type Event'))))
    lines.append(R(merge(bMid(L1, R1, 'update-function-configuration'), bMid(L2, R2, 'invoke --log-type Tail'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-function: remove'), bMid(L2, R2, 'list-event-source-mappings'))))
    lines.append(R(merge(bMid(L1, R1, 'list-functions: all funcs'), bMid(L2, R2, 'create-event-source-mapping'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('update-function-code deploys new zip/ECR; invoke tests synchronously or async'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Versions and Aliases'), bMid(L2, R2, 'Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'publish-version: snapshot'), bMid(L2, R2, 'get-function-configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'create-alias: named pointer'), bMid(L2, R2, 'put-function-concurrency'))))
    lines.append(R(merge(bMid(L1, R1, 'update-alias: shift traffic'), bMid(L2, R2, 'put-function-event-invoke-config'))))
    lines.append(R(merge(bMid(L1, R1, 'list-versions-by-function'), bMid(L2, R2, 'add-permission: resource policy'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-function (--qualifier)', ), bMid(L2, R2, 'get-policy: show permissions'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Lambda execution environment · VPC (if configured) · CloudWatch Logs · SQS/SNS/S3'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('invoke          = Executes function synchronously; response returned in CLI output'))
    lines.append(txt_row('--invocation-type Event= Asynchronous invocation; no response body returned'))
    lines.append(txt_row('--log-type Tail = Returns last 4KB of execution log in Base64 in response'))
    lines.append(txt_row('publish-version = Creates immutable numbered version from current $LATEST code'))
    lines.append(txt_row('Alias           = Named pointer to specific version; used for blue/green traffic split'))
    lines.append(txt_row('Event source mapping= Connects Lambda to SQS/Kinesis/DynamoDB stream as trigger'))
    lines.append(txt_row('Concurrency     = Max simultaneous Lambda executions; reserved or unreserved'))
    lines.append(txt_row('add-permission  = Grants another service (S3, SNS) permission to invoke function'))
    lines.append(txt_row('put-function-event-invoke-config= Sets max retries and DLQ for async invocations'))
    lines.append(txt_row('DLQ             = Dead Letter Queue; receives failed async events after retries'))
    lines.append(txt_row('$LATEST         = Mutable latest version; always updated by update-function-code'))
    lines.append(txt_row('ECR             = Elastic Container Registry; source for Lambda container image'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-rds', 'docs/cloud/aws/cli-reference/rds/index.md', 'AWS CLI — RDS')
def _aws_cli_rds():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — RDS'))
    lines.append(txt_row())
    lines.append(txt_row('RDS CLI commands for instance lifecycle, snapshots, parameter groups, and failover.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Instance Management'), bMid(L2, R2, 'Instance Inspection'))))
    lines.append(R(merge(bMid(L1, R1, 'create-db-instance: provision'), bMid(L2, R2, 'describe-db-instances'))))
    lines.append(R(merge(bMid(L1, R1, 'modify-db-instance: change'), bMid(L2, R2, 'describe-db-log-files'))))
    lines.append(R(merge(bMid(L1, R1, 'reboot-db-instance: restart'), bMid(L2, R2, 'download-db-log-file-portion'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-db-instance: remove'), bMid(L2, R2, 'describe-pending-maintenance'))))
    lines.append(R(merge(bMid(L1, R1, 'start/stop-db-instance'), bMid(L2, R2, 'describe-events: history'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('modify-db-instance: use --apply-immediately or --no-apply-immediately for maintenance'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshots and Restore'), bMid(L2, R2, 'High Availability'))))
    lines.append(R(merge(bMid(L1, R1, 'create-db-snapshot: manual'), bMid(L2, R2, 'failover-db-cluster: switch'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-db-snapshots: list'), bMid(L2, R2, 'create-db-cluster-snapshot'))))
    lines.append(R(merge(bMid(L1, R1, 'restore-db-instance-from-snapshot'), bMid(L2, R2, 'describe-db-clusters'))))
    lines.append(R(merge(bMid(L1, R1, 'copy-db-snapshot: cross-region'), bMid(L2, R2, 'promote-read-replica'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-db-snapshot: purge'), bMid(L2, R2, 'create-db-instance-read-replica'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('RDS managed nodes · Multi-AZ standby · EBS storage · KMS · VPC security groups'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('modify-db-instance= Changes instance class, storage, or parameter group'))
    lines.append(txt_row('--apply-immediately= Applies modification now vs next maintenance window'))
    lines.append(txt_row('Parameter group = Collection of database engine settings applied to instance'))
    lines.append(txt_row('Snapshot        = Manual or automated point-in-time copy of RDS storage'))
    lines.append(txt_row('copy-db-snapshot= Cross-region snapshot copy for DR; can re-encrypt with CMK'))
    lines.append(txt_row('Multi-AZ        = Synchronous standby in second AZ; automatic failover'))
    lines.append(txt_row('failover-db-cluster= Forces promotion of Aurora replica to writer'))
    lines.append(txt_row('promote-read-replica= Promotes MySQL/PostgreSQL read replica to standalone'))
    lines.append(txt_row('Read replica    = Asynchronous replication for read scale-out'))
    lines.append(txt_row('describe-pending-maintenance= Shows queued OS or engine maintenance tasks'))
    lines.append(txt_row('describe-events = Database event log: failovers, backups, restores'))
    lines.append(txt_row('Maintenance window= Weekly scheduled time for RDS to apply updates'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-s3', 'docs/cloud/aws/cli-reference/s3/index.md', 'AWS CLI — S3')
def _aws_cli_s3():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — S3'))
    lines.append(txt_row())
    lines.append(txt_row('S3 CLI commands for bucket management, object operations, sync, and policy config.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'High-Level S3 Commands'), bMid(L2, R2, 'Object Operations'))))
    lines.append(R(merge(bMid(L1, R1, 's3 cp: copy file/folder'), bMid(L2, R2, 's3api get-object: download'))))
    lines.append(R(merge(bMid(L1, R1, 's3 mv: move/rename'), bMid(L2, R2, 's3api put-object: upload'))))
    lines.append(R(merge(bMid(L1, R1, 's3 rm: delete object(s)'), bMid(L2, R2, 's3api delete-object'))))
    lines.append(R(merge(bMid(L1, R1, 's3 ls: list bucket/prefix'), bMid(L2, R2, 's3api list-objects-v2'))))
    lines.append(R(merge(bMid(L1, R1, 's3 sync: delta sync folder'), bMid(L2, R2, 's3api head-object: metadata'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('s3 commands wrap multipart upload; s3api gives direct REST API access'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Bucket Management'), bMid(L2, R2, 'Security and Policy'))))
    lines.append(R(merge(bMid(L1, R1, 's3api create-bucket'), bMid(L2, R2, 's3api put-bucket-policy'))))
    lines.append(R(merge(bMid(L1, R1, 's3api delete-bucket'), bMid(L2, R2, 's3api put-public-access-block'))))
    lines.append(R(merge(bMid(L1, R1, 's3api put-bucket-versioning'), bMid(L2, R2, 's3api put-bucket-encryption'))))
    lines.append(R(merge(bMid(L1, R1, 's3api put-bucket-lifecycle-configuration'), bMid(L2, R2, 's3api put-bucket-logging'))))
    lines.append(R(merge(bMid(L1, R1, 's3api put-bucket-replication'), bMid(L2, R2, 's3api put-object-lock-configuration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('S3 storage nodes (11 nines durability) · KMS · CloudTrail · CloudFront (CDN)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('s3 sync         = Transfers only new or changed objects; --delete removes extras'))
    lines.append(txt_row('Multipart upload= S3 splits large files into parts; automatic via aws s3 cp'))
    lines.append(txt_row('s3api           = Low-level REST API wrapper; all S3 operations directly'))
    lines.append(txt_row('Versioning      = Keeps all object versions; protects against accidental delete'))
    lines.append(txt_row('Object lock     = WORM: prevents object deletion during retention period'))
    lines.append(txt_row('Lifecycle rule  = Transitions objects to cheaper tiers or expires them'))
    lines.append(txt_row('Replication     = Cross-region or cross-account object copy for DR/compliance'))
    lines.append(txt_row('put-public-access-block= Blocks all public ACLs and bucket policies; account level'))
    lines.append(txt_row('head-object     = Returns metadata without downloading the object body'))
    lines.append(txt_row('Bucket policy   = Resource-based IAM policy controlling access to bucket'))
    lines.append(txt_row('Server-side encryption= SSE-S3 (managed) or SSE-KMS (CMK) encrypts stored objects'))
    lines.append(txt_row('list-objects-v2 = Paginated listing of objects in bucket with prefix filter'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-ssm', 'docs/cloud/aws/cli-reference/ssm/index.md', 'AWS CLI — SSM')
def _aws_cli_ssm():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — SSM'))
    lines.append(txt_row())
    lines.append(txt_row('Systems Manager CLI for session manager, run command, parameter store, and patching.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Session Manager'), bMid(L2, R2, 'Run Command'))))
    lines.append(R(merge(bMid(L1, R1, 'start-session: shell access'), bMid(L2, R2, 'send-command: execute script'))))
    lines.append(R(merge(bMid(L1, R1, 'terminate-session: end shell'), bMid(L2, R2, 'list-commands: history'))))
    lines.append(R(merge(bMid(L1, R1, 'list-sessions: active'), bMid(L2, R2, 'get-command-invocation'))))
    lines.append(R(merge(bMid(L1, R1, 'No SSH/RDP needed'), bMid(L2, R2, 'describe-instance-information'))))
    lines.append(R(merge(bMid(L1, R1, 'Logs: CloudWatch/S3'), bMid(L2, R2, 'list-command-invocations'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Session Manager replaces SSH bastion; run-command executes scripts fleet-wide'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Parameter Store'), bMid(L2, R2, 'Patch Manager'))))
    lines.append(R(merge(bMid(L1, R1, 'put-parameter: store secret'), bMid(L2, R2, 'describe-patch-baselines'))))
    lines.append(R(merge(bMid(L1, R1, 'get-parameter: retrieve'), bMid(L2, R2, 'get-patch-baseline: details'))))
    lines.append(R(merge(bMid(L1, R1, 'get-parameters-by-path'), bMid(L2, R2, 'describe-instance-patch-states'))))
    lines.append(R(merge(bMid(L1, R1, 'delete-parameter: remove'), bMid(L2, R2, 'describe-patch-group-state'))))
    lines.append(R(merge(bMid(L1, R1, 'SecureString: KMS-encrypted'), bMid(L2, R2, 'register-patch-baseline-for-group'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSM Agent (on EC2) · SSM endpoints (VPC) · KMS · CloudWatch · S3 (session logs)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Session Manager = Secure shell access via SSM without SSH port or key pair'))
    lines.append(txt_row('Run Command     = Execute scripts or documents on managed instances fleet-wide'))
    lines.append(txt_row('SSM Agent       = Lightweight agent installed on EC2; connects to SSM service'))
    lines.append(txt_row('Parameter Store = Hierarchical key-value store for config and secrets'))
    lines.append(txt_row('SecureString    = Parameter type encrypted with KMS key; for passwords/tokens'))
    lines.append(txt_row('get-parameters-by-path= Retrieves all parameters under a /path/ prefix'))
    lines.append(txt_row('Patch baseline  = Defines which patches are approved for auto-install'))
    lines.append(txt_row('Patch group     = Tag-based instance group assigned to a patch baseline'))
    lines.append(txt_row('describe-instance-patch-states= Shows patch compliance per instance'))
    lines.append(txt_row('SSM document    = JSON/YAML runbook defining steps for Run Command'))
    lines.append(txt_row('VPC endpoint    = Private SSM connectivity; no internet required for agent'))
    lines.append(txt_row('Managed instance= EC2 or on-prem server with SSM agent registered to account'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cli-vpc', 'docs/cloud/aws/cli-reference/vpc/index.md', 'AWS CLI — VPC')
def _aws_cli_vpc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS CLI — VPC'))
    lines.append(txt_row())
    lines.append(txt_row('VPC CLI commands for network creation, subnets, routing, security groups, and peering.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VPC and Subnet'), bMid(L2, R2, 'Routing'))))
    lines.append(R(merge(bMid(L1, R1, 'create-vpc: new VPC'), bMid(L2, R2, 'create-route-table'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-vpcs: list'), bMid(L2, R2, 'create-route: add route'))))
    lines.append(R(merge(bMid(L1, R1, 'create-subnet: segment'), bMid(L2, R2, 'associate-route-table'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-subnets: list'), bMid(L2, R2, 'create-internet-gateway'))))
    lines.append(R(merge(bMid(L1, R1, 'modify-subnet-attribute: auto-ip'), bMid(L2, R2, 'attach-internet-gateway'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('VPC and subnets created first; route tables and IGW attached to enable connectivity'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Security Groups'), bMid(L2, R2, 'Peering and Endpoints'))))
    lines.append(R(merge(bMid(L1, R1, 'create-security-group'), bMid(L2, R2, 'create-vpc-peering-connection'))))
    lines.append(R(merge(bMid(L1, R1, 'authorize-security-group-ingress'), bMid(L2, R2, 'accept-vpc-peering-connection'))))
    lines.append(R(merge(bMid(L1, R1, 'authorize-security-group-egress'), bMid(L2, R2, 'create-vpc-endpoint'))))
    lines.append(R(merge(bMid(L1, R1, 'revoke-security-group-ingress'), bMid(L2, R2, 'describe-vpc-endpoints'))))
    lines.append(R(merge(bMid(L1, R1, 'describe-security-groups'), bMid(L2, R2, 'describe-vpc-peering-connections'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS VPC hardware (Nitro cards) · internet edge (IGW) · NAT GW · Transit Gateway'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('create-vpc      = Provisions new VPC with specified CIDR; no subnets yet'))
    lines.append(txt_row('modify-subnet-attribute= Enables auto-assign public IP on instance launch'))
    lines.append(txt_row('Security group  = Stateful virtual firewall on ENI; inbound + outbound rules'))
    lines.append(txt_row('authorize-ingress= Adds inbound allow rule to security group'))
    lines.append(txt_row('VPC endpoint    = Gateway or interface endpoint for private AWS service access'))
    lines.append(txt_row('Gateway endpoint= S3 and DynamoDB only; free; route-table based'))
    lines.append(txt_row('Interface endpoint= PrivateLink ENI for other services; costs per hour'))
    lines.append(txt_row('VPC peering     = Direct routing between two VPCs; no transitive routing'))
    lines.append(txt_row('Transit Gateway = Hub router for transitive VPC connectivity'))
    lines.append(txt_row('Internet Gateway= Allows internet access for public subnet resources'))
    lines.append(txt_row('NAT Gateway     = Outbound-only internet for private subnet resources'))
    lines.append(txt_row('Nitro card      = AWS-built network card handling VPC packet forwarding'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-amis', 'docs/cloud/aws/compute/amis/index.md', 'AWS Compute — AMIs')
def _aws_compute_amis():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — AMIs'))
    lines.append(txt_row())
    lines.append(txt_row('Amazon Machine Images: golden image pipeline, lifecycle management, and sharing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'AMI Components'), bMid(L2, R2, 'AMI Types'))))
    lines.append(R(merge(bMid(L1, R1, 'Root snapshot: OS disk'), bMid(L2, R2, 'AWS-managed: Amazon Linux'))))
    lines.append(R(merge(bMid(L1, R1, 'Block device mapping: volumes'), bMid(L2, R2, 'Marketplace: vendor images'))))
    lines.append(R(merge(bMid(L1, R1, 'Launch permissions: who uses'), bMid(L2, R2, 'Custom: golden images'))))
    lines.append(R(merge(bMid(L1, R1, 'Kernel: AKI (paravirtual)'), bMid(L2, R2, 'Community: public shared'))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture: x86 or arm64'), bMid(L2, R2, 'Private: account-specific'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Golden AMIs baked via EC2 Image Builder pipeline; shared to target accounts via RAM'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Golden Image Pipeline'), bMid(L2, R2, 'Lifecycle Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Base: AWS or vendor AMI'), bMid(L2, R2, 'Deprecate: old versions'))))
    lines.append(R(merge(bMid(L1, R1, 'Harden: CIS benchmark'), bMid(L2, R2, 'Deregister: remove from list'))))
    lines.append(R(merge(bMid(L1, R1, 'Patch: SSM patch manager'), bMid(L2, R2, 'Delete snapshots: cost control'))))
    lines.append(R(merge(bMid(L1, R1, 'Test: Inspector scan'), bMid(L2, R2, 'Share: RAM cross-account'))))
    lines.append(R(merge(bMid(L1, R1, 'Publish: Image Builder'), bMid(L2, R2, 'Tag: version + build date'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 build instance · EBS (snapshot storage) · S3 (Image Builder artifacts) · KMS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AMI             = Amazon Machine Image; template for launching EC2 instances'))
    lines.append(txt_row('Golden image    = Hardened, pre-patched AMI used as approved base for all instances'))
    lines.append(txt_row('EC2 Image Builder= Managed service automating golden AMI creation and testing'))
    lines.append(txt_row('Block device map= Defines root and additional EBS volumes attached at launch'))
    lines.append(txt_row('Deprecate       = Marks AMI as outdated; still launchable but flagged for replacement'))
    lines.append(txt_row('Deregister      = Removes AMI from list; underlying snapshots must be deleted separately'))
    lines.append(txt_row('RAM             = Resource Access Manager; shares AMIs to other AWS accounts/OUs'))
    lines.append(txt_row('Launch permission= Controls which accounts can use the AMI to launch instances'))
    lines.append(txt_row('Inspector scan  = Vulnerability assessment run on AMI during Image Builder pipeline'))
    lines.append(txt_row('CIS benchmark   = Center for Internet Security OS hardening checklist'))
    lines.append(txt_row('arm64           = Graviton processor architecture; better price/performance for some'))
    lines.append(txt_row('Snapshot backing= Each AMI is backed by one or more EBS snapshots in S3'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-auto-scaling', 'docs/cloud/aws/compute/auto-scaling/index.md', 'AWS Compute — Auto Scaling')
def _aws_compute_auto_scaling():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — Auto Scaling'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 Auto Scaling adjusts fleet size based on demand using scaling policies and health.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ASG Configuration'), bMid(L2, R2, 'Launch Template'))))
    lines.append(R(merge(bMid(L1, R1, 'Min / Max / Desired capacity'), bMid(L2, R2, 'AMI: golden image version'))))
    lines.append(R(merge(bMid(L1, R1, 'AZs: multi-AZ spread'), bMid(L2, R2, 'Instance type: on-demand/spot'))))
    lines.append(R(merge(bMid(L1, R1, 'Health check: EC2 or ELB'), bMid(L2, R2, 'IAM instance profile'))))
    lines.append(R(merge(bMid(L1, R1, 'Cooldown: 300s default'), bMid(L2, R2, 'User data: bootstrap script'))))
    lines.append(R(merge(bMid(L1, R1, 'Lifecycle hooks: custom logic'), bMid(L2, R2, 'Security group assignment'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ASG maintains desired capacity; scaling policies adjust desired up or down on demand'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Scaling Policies'), bMid(L2, R2, 'Instance Refresh'))))
    lines.append(R(merge(bMid(L1, R1, 'Target tracking: CPU 70%'), bMid(L2, R2, 'Rolling replace: new AMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Step scaling: threshold bands'), bMid(L2, R2, 'Min healthy %: 90 default'))))
    lines.append(R(merge(bMid(L1, R1, 'Scheduled: predictable load'), bMid(L2, R2, 'Checkpoint: pause at N%'))))
    lines.append(R(merge(bMid(L1, R1, 'Predictive: ML-based scale'), bMid(L2, R2, 'Rollback: on failure'))))
    lines.append(R(merge(bMid(L1, R1, 'Scale-in protection: pin'), bMid(L2, R2, 'Warm pool: pre-warm instances'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 instances · ELB · CloudWatch (metrics trigger) · multiple AZs · SNS (notifications)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ASG             = Auto Scaling Group; manages a fleet of EC2 instances'))
    lines.append(txt_row('Launch template = Instance configuration used to launch new ASG members'))
    lines.append(txt_row('Target tracking = Adjusts capacity to keep metric (e.g. CPU) at target value'))
    lines.append(txt_row('Step scaling    = Adds/removes N instances per threshold band breached'))
    lines.append(txt_row('Cooldown        = Pause after scaling action to let metrics stabilise'))
    lines.append(txt_row('Lifecycle hook  = Pauses instance at launch or termination for custom processing'))
    lines.append(txt_row('Instance refresh= Replaces all ASG instances with new launch template version'))
    lines.append(txt_row('Warm pool       = Pre-started stopped instances; reduce scale-out latency'))
    lines.append(txt_row('Scale-in protection= Prevents specific instance from being terminated during scale-in'))
    lines.append(txt_row('Min healthy %   = % of instances that must stay healthy during instance refresh'))
    lines.append(txt_row('Predictive scaling= Uses ML to forecast load and pre-scale ahead of demand'))
    lines.append(txt_row('ELB health check= ASG uses ELB target health to decide if instance is unhealthy'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-ec2', 'docs/cloud/aws/compute/ec2/index.md', 'AWS Compute — EC2')
def _aws_compute_ec2():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — EC2'))
    lines.append(txt_row())
    lines.append(txt_row('Elastic Compute Cloud: instance types, purchasing options, networking, and storage.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Instance Families'), bMid(L2, R2, 'Purchasing Options'))))
    lines.append(R(merge(bMid(L1, R1, 'General: m7i, t3 (burstable)'), bMid(L2, R2, 'On-demand: pay per second'))))
    lines.append(R(merge(bMid(L1, R1, 'Compute: c7i (high CPU)'), bMid(L2, R2, 'Reserved: 1/3yr commitment'))))
    lines.append(R(merge(bMid(L1, R1, 'Memory: r7i (high RAM)'), bMid(L2, R2, 'Spot: spare capacity, -90%'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage: i4i (NVMe local)'), bMid(L2, R2, 'Savings plan: flexible RI'))))
    lines.append(R(merge(bMid(L1, R1, 'Accelerated: p4/g5 (GPU)'), bMid(L2, R2, 'Dedicated host: compliance'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Instance family chosen for workload type; purchasing model optimises cost'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Networking'), bMid(L2, R2, 'Storage'))))
    lines.append(R(merge(bMid(L1, R1, 'ENI: virtual network card'), bMid(L2, R2, 'Root EBS: OS disk'))))
    lines.append(R(merge(bMid(L1, R1, 'Public IP: auto-assign'), bMid(L2, R2, 'Data EBS: persistent block'))))
    lines.append(R(merge(bMid(L1, R1, 'Elastic IP: static public'), bMid(L2, R2, 'Instance store: ephemeral NVMe'))))
    lines.append(R(merge(bMid(L1, R1, 'Enhanced networking: SR-IOV'), bMid(L2, R2, 'EFS mount: shared NFS'))))
    lines.append(R(merge(bMid(L1, R1, 'Placement group: latency/spread'), bMid(L2, R2, 'FSx: Windows/Lustre mount'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Nitro hypervisor · Nitro cards (network/storage) · physical host · AZ data centre'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ENI             = Elastic Network Interface; virtual NIC attachable to EC2'))
    lines.append(txt_row('Elastic IP      = Static public IPv4 address; persists across stop/start'))
    lines.append(txt_row('SR-IOV          = Single Root I/O Virtualisation; enables enhanced networking'))
    lines.append(txt_row('Placement group = Cluster (low latency) or spread (fault isolation) placement'))
    lines.append(txt_row('Spot instance   = Uses spare EC2 capacity; can be interrupted with 2-min notice'))
    lines.append(txt_row('Reserved instance= 1 or 3-year commitment for up to 72% discount'))
    lines.append(txt_row('Savings plan    = Flexible commitment by $/hour; applies across instance families'))
    lines.append(txt_row('Dedicated host  = Physical server for BYOL or compliance isolation requirements'))
    lines.append(txt_row('Instance store  = NVMe SSD physically attached to host; lost on stop/terminate'))
    lines.append(txt_row('Burstable (t3)  = Accumulates CPU credits when idle; bursts above baseline'))
    lines.append(txt_row('Nitro hypervisor= AWS-built hypervisor offloading I/O to dedicated Nitro cards'))
    lines.append(txt_row('IMDS v2         = Instance Metadata Service v2; token-required for security'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-instance-recovery', 'docs/cloud/aws/compute/instance-recovery/index.md', 'AWS Compute — Instance Recovery')
def _aws_compute_instance_recovery():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — Instance Recovery'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 recovery mechanisms: CloudWatch alarm recovery, reboot, restore from AMI/snapshot.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Automatic Recovery'), bMid(L2, R2, 'Health Check Types'))))
    lines.append(R(merge(bMid(L1, R1, 'CW alarm: StatusCheckFailed'), bMid(L2, R2, 'System check: host hardware'))))
    lines.append(R(merge(bMid(L1, R1, 'Action: recover instance'), bMid(L2, R2, 'Instance check: OS/NIC'))))
    lines.append(R(merge(bMid(L1, R1, 'Retains: IP, EBS, EIP, SG'), bMid(L2, R2, 'ELB health: app-level check'))))
    lines.append(R(merge(bMid(L1, R1, 'Moves to healthy host'), bMid(L2, R2, 'Custom: CloudWatch metric'))))
    lines.append(R(merge(bMid(L1, R1, 'Notification: SNS topic'), bMid(L2, R2, 'ASG: replaces failed member'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('CW alarm triggers automatic recovery; ASG replaces terminated instances automatically'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Manual Recovery Steps'), bMid(L2, R2, 'DR Scenarios'))))
    lines.append(R(merge(bMid(L1, R1, 'Console: stop → start'), bMid(L2, R2, 'Corrupt OS: restore from AMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Reboot: keeps EBS + config'), bMid(L2, R2, 'Lost data: EBS snapshot restore'))))
    lines.append(R(merge(bMid(L1, R1, 'Detach root vol: chroot fix'), bMid(L2, R2, 'AZ failure: relaunch in new AZ'))))
    lines.append(R(merge(bMid(L1, R1, 'Serial console: no-network fix'), bMid(L2, R2, 'Region failure: cross-region AMI'))))
    lines.append(R(merge(bMid(L1, R1, 'SSM run-command: fix config'), bMid(L2, R2, 'RTO target: define per tier'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 host · Nitro hypervisor · EBS · CloudWatch · SNS · multiple AZs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('StatusCheckFailed_System= Host hardware or network issue; triggers auto-recovery'))
    lines.append(txt_row('StatusCheckFailed_Instance= OS-level failure; requires reboot or manual fix'))
    lines.append(txt_row('recover action  = CloudWatch alarm action moving instance to healthy host'))
    lines.append(txt_row('Retains EIP     = Elastic IP stays associated after automatic recovery'))
    lines.append(txt_row('Detach root vol = Mount root EBS on rescue instance to repair offline OS'))
    lines.append(txt_row('Serial console  = Out-of-band access for instances without network connectivity'))
    lines.append(txt_row('chroot          = Linux technique to access and fix a mounted OS root filesystem'))
    lines.append(txt_row('Cross-region AMI= AMI copied to DR region; launch instances there on region failure'))
    lines.append(txt_row('ASG replacement = ASG terminates failed instance and launches new one automatically'))
    lines.append(txt_row('Stop → Start    = Moves instance to new host; clears most transient failures'))
    lines.append(txt_row('RTO             = Recovery Time Objective; maximum acceptable downtime per tier'))
    lines.append(txt_row('ELB health check= Removes unhealthy instance from load balancer target group'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-lambda', 'docs/cloud/aws/compute/lambda/index.md', 'AWS Compute — Lambda')
def _aws_compute_lambda():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — Lambda'))
    lines.append(txt_row())
    lines.append(txt_row('Serverless function execution: triggers, runtimes, concurrency, VPC, and observability.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Function Configuration'), bMid(L2, R2, 'Triggers'))))
    lines.append(R(merge(bMid(L1, R1, 'Runtime: Python/Node/Java/Go'), bMid(L2, R2, 'API Gateway: HTTP invoke'))))
    lines.append(R(merge(bMid(L1, R1, 'Memory: 128MB–10GB'), bMid(L2, R2, 'S3: object events'))))
    lines.append(R(merge(bMid(L1, R1, 'Timeout: max 15 minutes'), bMid(L2, R2, 'SQS/SNS: message processing'))))
    lines.append(R(merge(bMid(L1, R1, 'Ephemeral storage: /tmp 512MB+'), bMid(L2, R2, 'EventBridge: scheduled/event'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM execution role: permissions'), bMid(L2, R2, 'DynamoDB/Kinesis: streams'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Triggers invoke function; execution role grants AWS service access during run'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Concurrency and Scaling'), bMid(L2, R2, 'Observability'))))
    lines.append(R(merge(bMid(L1, R1, 'Burst: 3000 initial, +500/min'), bMid(L2, R2, 'CloudWatch Logs: auto-stream'))))
    lines.append(R(merge(bMid(L1, R1, 'Reserved concurrency: cap'), bMid(L2, R2, 'X-Ray: distributed tracing'))))
    lines.append(R(merge(bMid(L1, R1, 'Provisioned: pre-warm exec'), bMid(L2, R2, 'Insights: cold start metric'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC: ENI in private subnet'), bMid(L2, R2, 'Errors: DLQ or on-failure'))))
    lines.append(R(merge(bMid(L1, R1, 'Cold start: init overhead'), bMid(L2, R2, 'Alarm: error rate threshold'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Lambda micro-VMs (Firecracker) · VPC ENI (if VPC mode) · CloudWatch · X-Ray'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Firecracker     = AWS micro-VM; provides isolation between Lambda executions'))
    lines.append(txt_row('Cold start      = Latency when Lambda initialises a new execution environment'))
    lines.append(txt_row('Provisioned concurrency= Pre-warms execution environments; eliminates cold start'))
    lines.append(txt_row('Reserved concurrency= Caps max executions; guarantees capacity but limits scale'))
    lines.append(txt_row('DLQ             = Dead Letter Queue; receives events that failed after retries'))
    lines.append(txt_row('Execution role  = IAM role assumed by Lambda to access S3, DynamoDB, etc.'))
    lines.append(txt_row('VPC mode        = Lambda ENI placed in VPC subnet; accesses private resources'))
    lines.append(txt_row('X-Ray           = AWS distributed tracing; shows latency across service calls'))
    lines.append(txt_row('Burst limit     = Account-level max new concurrent executions per minute'))
    lines.append(txt_row('Ephemeral /tmp  = Writable scratch space; max 10GB; not shared between invocations'))
    lines.append(txt_row('Lambda layer    = Shared libraries or runtimes attached to functions'))
    lines.append(txt_row('Event source map= Polls SQS/Kinesis/DynamoDB and invokes Lambda with batches'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-patch-manager', 'docs/cloud/aws/compute/patch-manager/index.md', 'AWS Compute — Patch Manager')
def _aws_compute_patch_manager():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — Patch Manager'))
    lines.append(txt_row())
    lines.append(txt_row('SSM Patch Manager automates OS patching across EC2 fleet using baselines and groups.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Patch Baseline'), bMid(L2, R2, 'Patch Groups'))))
    lines.append(R(merge(bMid(L1, R1, 'OS: Amazon Linux/RHEL/Windows'), bMid(L2, R2, 'Tag: Patch Group key'))))
    lines.append(R(merge(bMid(L1, R1, 'Approval: critical auto 7d'), bMid(L2, R2, 'Env: prod/staging/dev'))))
    lines.append(R(merge(bMid(L1, R1, 'Classification: Security/Bug'), bMid(L2, R2, 'Stagger: dev before prod'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom: include/exclude list'), bMid(L2, R2, 'Register baseline per group'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS default baselines: per OS'), bMid(L2, R2, 'Compliance report per group'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Baseline defines what to patch; patch group targets which instances receive it'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Patching Execution'), bMid(L2, R2, 'Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Maintenance window: schedule'), bMid(L2, R2, 'describe-patch-compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Run Command: AWS-RunPatchBaseline'), bMid(L2, R2, 'Config rule: patch compliant'))))
    lines.append(R(merge(bMid(L1, R1, 'Scan: missing patches only'), bMid(L2, R2, 'Dashboard: per-instance state'))))
    lines.append(R(merge(bMid(L1, R1, 'Install: apply + reboot'), bMid(L2, R2, 'SNS: alert on failure'))))
    lines.append(R(merge(bMid(L1, R1, 'No-reboot: --reboot-option'), bMid(L2, R2, 'Patch latency: days since avail'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSM Agent on EC2 · SSM service endpoints · CloudWatch · SNS · Config'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Patch baseline  = Policy defining which patches are approved for installation'))
    lines.append(txt_row('Patch group     = EC2 instances tagged Patch Group=<value>; mapped to baseline'))
    lines.append(txt_row('Maintenance window= Scheduled time during which patching runs; limits blast radius'))
    lines.append(txt_row('AWS-RunPatchBaseline= SSM document that scans or installs patches on instances'))
    lines.append(txt_row('Scan mode       = Reports missing patches without installing; safe for auditing'))
    lines.append(txt_row('Install mode    = Downloads and installs patches; may reboot instance'))
    lines.append(txt_row('Approval delay  = Days after patch release before it is auto-approved in baseline'))
    lines.append(txt_row('Compliance state= Compliant (all approved patches installed) or NonCompliant'))
    lines.append(txt_row('Patch latency   = Average days between patch availability and installation'))
    lines.append(txt_row('No-reboot option= Installs patches but skips reboot; manual reboot required later'))
    lines.append(txt_row('Config rule     = Detects instances with NonCompliant patch state automatically'))
    lines.append(txt_row('SSM Agent       = Software on instance that executes patch commands from SSM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-compute-systems-manager', 'docs/cloud/aws/compute/systems-manager/index.md', 'AWS Compute — Systems Manager')
def _aws_compute_systems_manager():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Compute — Systems Manager'))
    lines.append(txt_row())
    lines.append(txt_row('SSM provides fleet management: session access, patch, run-command, and parameter store.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Core Capabilities'), bMid(L2, R2, 'Fleet Manager'))))
    lines.append(R(merge(bMid(L1, R1, 'Session Manager: SSH-free'), bMid(L2, R2, 'Inventory: software + config'))))
    lines.append(R(merge(bMid(L1, R1, 'Run Command: fleet scripts'), bMid(L2, R2, 'Compliance: patch + assoc'))))
    lines.append(R(merge(bMid(L1, R1, 'Patch Manager: OS updates'), bMid(L2, R2, 'Node Management: overview'))))
    lines.append(R(merge(bMid(L1, R1, 'Parameter Store: config/secrets'), bMid(L2, R2, 'Explorer: org-wide health'))))
    lines.append(R(merge(bMid(L1, R1, 'Automation: runbook playbooks'), bMid(L2, R2, 'OpsCenter: incident tickets'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSM Agent on each instance connects outbound to SSM endpoints; no inbound ports'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Automation'), bMid(L2, R2, 'Setup Requirements'))))
    lines.append(R(merge(bMid(L1, R1, 'Runbooks: SSM documents'), bMid(L2, R2, 'SSM Agent: pre-installed AMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Trigger: EventBridge/console'), bMid(L2, R2, 'IAM role: AmazonSSMManagedInstanceCore'))))
    lines.append(R(merge(bMid(L1, R1, 'Approval step: human gate'), bMid(L2, R2, 'VPC endpoint or internet'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-account: change mgr'), bMid(L2, R2, 'Hybrid: on-prem registration'))))
    lines.append(R(merge(bMid(L1, R1, 'Rollback: stop on failure'), bMid(L2, R2, 'Tag: managed instance label'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSM service endpoints · SSM Agent · EC2/on-prem nodes · VPC endpoints · KMS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSM Agent       = Lightweight daemon on EC2 or on-prem; polls SSM for commands'))
    lines.append(txt_row('Session Manager = Secure interactive shell via SSM; no SSH port or key pair'))
    lines.append(txt_row('Run Command     = Execute SSM documents on target instances; returns output'))
    lines.append(txt_row('Parameter Store = Hierarchical config store; String, StringList, SecureString'))
    lines.append(txt_row('Automation      = Multi-step runbook; can approve, branch, loop, call APIs'))
    lines.append(txt_row('OpsCenter       = Operational issues (OpsItems) linked to AWS resources'))
    lines.append(txt_row('Explorer        = Aggregated ops dashboard across accounts in an org'))
    lines.append(txt_row('Inventory       = Collects installed software, network config, Windows registry'))
    lines.append(txt_row('AmazonSSMManagedInstanceCore= Minimum IAM policy required for SSM management'))
    lines.append(txt_row('VPC endpoint    = Allows SSM Agent to communicate without internet access'))
    lines.append(txt_row('Hybrid activation= Registers on-prem servers as managed instances in SSM'))
    lines.append(txt_row('Change Manager  = Approval workflow for SSM Automation across multiple accounts'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-budgets', 'docs/cloud/aws/cost/budgets/index.md', 'AWS Cost — Budgets')
def _aws_cost_budgets():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Budgets'))
    lines.append(txt_row())
    lines.append(txt_row('AWS Budgets sets cost and usage thresholds with alerts and optional auto-actions.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Budget Types'), bMid(L2, R2, 'Budget Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'Cost: total spend ($)'), bMid(L2, R2, 'Period: monthly/quarterly'))))
    lines.append(R(merge(bMid(L1, R1, 'Usage: units (GB, hours)'), bMid(L2, R2, 'Filter: account/service/tag'))))
    lines.append(R(merge(bMid(L1, R1, 'RI utilisation: coverage %'), bMid(L2, R2, 'Forecast: projected spend'))))
    lines.append(R(merge(bMid(L1, R1, 'Savings Plans coverage %'), bMid(L2, R2, 'Alert: actual or forecasted'))))
    lines.append(R(merge(bMid(L1, R1, 'Comparison: vs prior period'), bMid(L2, R2, 'SNS: notification target'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Alerts fire when actual or forecasted spend crosses threshold percentage'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Budget Actions'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'SCP: restrict service use'), bMid(L2, R2, 'Per account budget'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM: deny EC2 launches'), bMid(L2, R2, 'Alert at 80% + 100%'))))
    lines.append(R(merge(bMid(L1, R1, 'Require approval: SSO gate'), bMid(L2, R2, 'Forecast alert: early warning'))))
    lines.append(R(merge(bMid(L1, R1, 'Trigger: actual threshold'), bMid(L2, R2, 'Tag-based: team budgets'))))
    lines.append(R(merge(bMid(L1, R1, 'Test: manually trigger'), bMid(L2, R2, 'Review: monthly FinOps meeting'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Budgets service · SNS · SCP engine · IAM · Cost Explorer data feed'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Budget action   = Automated response when budget threshold is breached'))
    lines.append(txt_row('Forecasted alert= Fires when projected end-of-period spend will exceed threshold'))
    lines.append(txt_row('Actual alert    = Fires when real spend to date crosses threshold'))
    lines.append(txt_row('RI utilisation  = % of reserved instance hours actually consumed'))
    lines.append(txt_row('Savings Plans coverage= % of eligible spend covered by Savings Plans'))
    lines.append(txt_row('SCP action      = Budget action attaching an SCP to restrict further spending'))
    lines.append(txt_row('IAM action      = Budget action attaching IAM policy denying launch of resources'))
    lines.append(txt_row('FinOps          = Financial Operations; cloud cost management practice'))
    lines.append(txt_row('SNS target      = Budget alert publishes to SNS; subscribers get email/Slack/Lambda'))
    lines.append(txt_row('Tag filter       = Budget scoped to resources with specific tag key/value'))
    lines.append(txt_row('Period          = Evaluation window: monthly resets on 1st; quarterly on quarter start'))
    lines.append(txt_row('Cost anomaly    = Separate service; detects unexpected spend spikes via ML'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-tags', 'docs/cloud/aws/cost/cost-allocation-tags/index.md', 'AWS Cost — Cost Allocation Tags')
def _aws_cost_tags():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Cost Allocation Tags'))
    lines.append(txt_row())
    lines.append(txt_row('Cost allocation tags enable chargeback and showback by team, environment, and project.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Tag Types'), bMid(L2, R2, 'Required Tags'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS-generated: aws:createdBy'), bMid(L2, R2, 'Environment: prod/dev/test'))))
    lines.append(R(merge(bMid(L1, R1, 'User-defined: custom keys'), bMid(L2, R2, 'Owner: team or person'))))
    lines.append(R(merge(bMid(L1, R1, 'Activate: in Billing console'), bMid(L2, R2, 'CostCentre: finance code'))))
    lines.append(R(merge(bMid(L1, R1, 'Appear in CUR within 24h'), bMid(L2, R2, 'Application: workload name'))))
    lines.append(R(merge(bMid(L1, R1, 'Max 50 user-defined active'), bMid(L2, R2, 'Project: initiative tracker'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Tags must be activated in Billing console before appearing in cost reports'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Enforcement'), bMid(L2, R2, 'Reporting'))))
    lines.append(R(merge(bMid(L1, R1, 'SCP: deny without required tag'), bMid(L2, R2, 'Cost Explorer: group by tag'))))
    lines.append(R(merge(bMid(L1, R1, 'Config rule: required-tags'), bMid(L2, R2, 'CUR: raw billing CSV/Parquet'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag policy: org-level govern'), bMid(L2, R2, 'Budgets: filter by tag'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS Config remediation: auto'), bMid(L2, R2, 'Athena: query CUR in S3'))))
    lines.append(R(merge(bMid(L1, R1, 'Tagging IaC: Terraform/CFN'), bMid(L2, R2, 'QuickSight: dashboard'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Billing · S3 (CUR) · Athena · Cost Explorer · Config · Organizations'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cost allocation tag= Tag activated in Billing; appears as column in CUR and Explorer'))
    lines.append(txt_row('CUR             = Cost and Usage Report; detailed per-resource billing data'))
    lines.append(txt_row('Tag policy      = Organizations policy enforcing tag key case and allowed values'))
    lines.append(txt_row('required-tags   = AWS Config rule flagging resources missing mandatory tags'))
    lines.append(txt_row('Chargeback      = Billing teams for their actual AWS spend based on tags'))
    lines.append(txt_row('Showback        = Showing teams their spend without billing them directly'))
    lines.append(txt_row('Athena          = Serverless SQL query engine; queries CUR stored in S3'))
    lines.append(txt_row('QuickSight      = AWS BI tool; visualises CUR/Athena data as dashboards'))
    lines.append(txt_row('aws:createdBy   = AWS-generated tag showing IAM principal that created resource'))
    lines.append(txt_row('Activate in Billing= Required step to include user tag in cost reports'))
    lines.append(txt_row('Tag compliance  = % of resources with all required tags; tracked in Config'))
    lines.append(txt_row('IaC tagging     = Define required tags in Terraform/CloudFormation at resource level'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-anomaly', 'docs/cloud/aws/cost/cost-anomaly-detection/index.md', 'AWS Cost — Cost Anomaly Detection')
def _aws_cost_anomaly():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Cost Anomaly Detection'))
    lines.append(txt_row())
    lines.append(txt_row('ML-based service detecting unexpected cost spikes across services, accounts, and tags.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor Configuration'), bMid(L2, R2, 'Alert Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor: AWS service level'), bMid(L2, R2, 'Threshold: $ or % impact'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor: linked account'), bMid(L2, R2, 'Frequency: daily or weekly'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor: cost category'), bMid(L2, R2, 'SNS: email/Slack/Lambda'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor: custom tag key'), bMid(L2, R2, 'Root cause: service + usage'))))
    lines.append(R(merge(bMid(L1, R1, 'ML: learns spend patterns'), bMid(L2, R2, 'Acknowledge: mark reviewed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ML baseline takes ~10 days to establish; anomalies detected against that pattern'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Anomaly Details'), bMid(L2, R2, 'Investigation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Impact: total $ overage'), bMid(L2, R2, 'Cost Explorer: drill down'))))
    lines.append(R(merge(bMid(L1, R1, 'Root cause: top contributor'), bMid(L2, R2, 'CloudTrail: who launched'))))
    lines.append(R(merge(bMid(L1, R1, 'Duration: start/end dates'), bMid(L2, R2, 'Config: resource timeline'))))
    lines.append(R(merge(bMid(L1, R1, 'Score: confidence 0-100'), bMid(L2, R2, 'Tag: find untagged resource'))))
    lines.append(R(merge(bMid(L1, R1, 'Feedback: expected/unexpected'), bMid(L2, R2, 'Budget action: stop spend'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Cost Anomaly Detection service · SNS · Cost Explorer · CloudTrail'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Anomaly monitor = Scope definition for anomaly detection: service, account, or tag'))
    lines.append(txt_row('ML model        = Learns historical spend patterns; flags deviations as anomalies'))
    lines.append(txt_row('Anomaly score   = Confidence level 0-100; higher = more likely genuine anomaly'))
    lines.append(txt_row('Root cause      = Service and usage type contributing most to the cost spike'))
    lines.append(txt_row('Impact $        = Dollar amount by which spend exceeded expected baseline'))
    lines.append(txt_row('Acknowledge     = Mark anomaly as reviewed; improves ML model feedback'))
    lines.append(txt_row('Feedback        = Mark anomaly as expected/unexpected; trains future detection'))
    lines.append(txt_row('Alert threshold = Minimum $ or % impact before alert fires'))
    lines.append(txt_row('Daily alert     = Sends notification each day an ongoing anomaly persists'))
    lines.append(txt_row('Weekly summary  = Single weekly digest of all anomalies in the period'))
    lines.append(txt_row('Cost Explorer   = Used to drill into anomaly root cause by service/region/tag'))
    lines.append(txt_row('Budget action   = Preventive control to stop spending when anomaly is detected'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-explorer', 'docs/cloud/aws/cost/cost-explorer/index.md', 'AWS Cost — Cost Explorer')
def _aws_cost_explorer():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Cost Explorer'))
    lines.append(txt_row())
    lines.append(txt_row('Cost Explorer visualises and analyses AWS spend with filtering, grouping, and forecasts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Visualisation'), bMid(L2, R2, 'Filtering and Grouping'))))
    lines.append(R(merge(bMid(L1, R1, 'Bar/line: daily or monthly'), bMid(L2, R2, 'Group by: service, account'))))
    lines.append(R(merge(bMid(L1, R1, 'Date range: up to 13 months'), bMid(L2, R2, 'Group by: tag key'))))
    lines.append(R(merge(bMid(L1, R1, 'Granularity: daily/monthly'), bMid(L2, R2, 'Filter: region, AZ, type'))))
    lines.append(R(merge(bMid(L1, R1, 'Forecast: 12 months ahead'), bMid(L2, R2, 'Filter: linked account'))))
    lines.append(R(merge(bMid(L1, R1, 'Saved reports: share views'), bMid(L2, R2, 'API: GetCostAndUsage'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Explorer shows 13 months history; use API for programmatic cost data retrieval'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'RI and Savings Plans'), bMid(L2, R2, 'Right-Sizing'))))
    lines.append(R(merge(bMid(L1, R1, 'RI utilisation report'), bMid(L2, R2, 'Right-size: underused EC2'))))
    lines.append(R(merge(bMid(L1, R1, 'RI coverage report'), bMid(L2, R2, 'Recommendations: instance type'))))
    lines.append(R(merge(bMid(L1, R1, 'SP utilisation report'), bMid(L2, R2, 'Savings: projected savings'))))
    lines.append(R(merge(bMid(L1, R1, 'SP recommendations: buy'), bMid(L2, R2, 'CloudWatch CPU: low util flag'))))
    lines.append(R(merge(bMid(L1, R1, 'Amortised vs blended cost'), bMid(L2, R2, 'Memory: CloudWatch agent req'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Billing data pipeline · Cost Explorer service · CUR S3 bucket'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cost Explorer    = Console and API for visualising and analysing AWS spend'))
    lines.append(txt_row('Granularity      = Daily shows day-level detail; monthly aggregates per calendar month'))
    lines.append(txt_row('Amortised cost   = RI upfront fee spread across the reservation term'))
    lines.append(txt_row('Blended rate     = Average effective rate across reserved and on-demand instances'))
    lines.append(txt_row('RI utilisation   = % of purchased reserved instance hours consumed'))
    lines.append(txt_row('RI coverage      = % of eligible on-demand spend covered by reservations'))
    lines.append(txt_row('SP recommendation= Suggested Savings Plans commitment to reduce on-demand spend'))
    lines.append(txt_row('Right-sizing     = Identifying over-provisioned instances to downsize'))
    lines.append(txt_row('GetCostAndUsage  = API returning cost data with same filters as console'))
    lines.append(txt_row('Saved report     = Stored filter/group configuration; shareable via URL'))
    lines.append(txt_row('Forecast         = ML projection of future spend based on historical trends'))
    lines.append(txt_row('CUR             = Cost and Usage Report; raw billing data backing Explorer'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-explorer-billing', 'docs/cloud/aws/cost/cost-explorer-billing/index.md', 'AWS Cost — Cost Explorer Billing')
def _aws_cost_explorer_billing():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Cost Explorer Billing'))
    lines.append(txt_row())
    lines.append(txt_row('Billing console: invoices, payment methods, tax settings, and consolidated billing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Billing Console'), bMid(L2, R2, 'Consolidated Billing'))))
    lines.append(R(merge(bMid(L1, R1, 'Invoices: monthly PDF/CSV'), bMid(L2, R2, 'Org: single payer account'))))
    lines.append(R(merge(bMid(L1, R1, 'Payment: credit card/ACH'), bMid(L2, R2, 'Volume discounts: pooled'))))
    lines.append(R(merge(bMid(L1, R1, 'Tax: VAT/GST settings'), bMid(L2, R2, 'RI sharing: across accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'Credits: applied balance'), bMid(L2, R2, 'SP sharing: org-wide'))))
    lines.append(R(merge(bMid(L1, R1, 'Free tier: usage tracker'), bMid(L2, R2, 'Billing entity: per account'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Management account pays consolidated bill; member accounts see their own usage'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cost and Usage Report'), bMid(L2, R2, 'FinOps Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'CUR: granular billing CSV'), bMid(L2, R2, 'Monthly review: all teams'))))
    lines.append(R(merge(bMid(L1, R1, 'S3 bucket: daily delivery'), bMid(L2, R2, 'Chargeback: tag-based billing'))))
    lines.append(R(merge(bMid(L1, R1, 'Parquet: Athena-optimised'), bMid(L2, R2, 'Forecasting: budget vs actual'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource IDs: enabled'), bMid(L2, R2, 'Unit economics: cost per unit'))))
    lines.append(R(merge(bMid(L1, R1, 'Versioning: overwrite/create'), bMid(L2, R2, 'Waste: delete unused resources'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Billing service · S3 (CUR) · Athena · management account payment rails'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CUR             = Cost and Usage Report; most granular billing data available'))
    lines.append(txt_row('Consolidated billing= Single monthly invoice for all org accounts via management account'))
    lines.append(txt_row('RI sharing      = Reserved instances purchased in one account benefit all org accounts'))
    lines.append(txt_row('SP sharing      = Savings Plans apply to any account in the org by default'))
    lines.append(txt_row('Volume discount = AWS applies tiered pricing based on total org usage'))
    lines.append(txt_row('Chargeback      = Internally billing teams for their AWS spend via cost allocation'))
    lines.append(txt_row('Unit economics  = Cost per transaction, per user, or per API call'))
    lines.append(txt_row('Free tier tracker= Billing console shows how close each service is to free tier limit'))
    lines.append(txt_row('Tax settings    = VAT/GST registration applied to invoices by region'))
    lines.append(txt_row('Credits         = AWS promotional credits applied before charging payment method'))
    lines.append(txt_row('Parquet format  = Columnar CUR format; faster Athena queries and lower S3 cost'))
    lines.append(txt_row('Resource IDs    = CUR option adding AWS resource ARN to each billing line item'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-reserved-instances', 'docs/cloud/aws/cost/reserved-instances/index.md', 'AWS Cost — Reserved Instances')
def _aws_cost_reserved_instances():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Reserved Instances'))
    lines.append(txt_row())
    lines.append(txt_row('Reserved Instances provide up to 72% EC2 discount for 1- or 3-year commitments.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'RI Types'), bMid(L2, R2, 'Payment Options'))))
    lines.append(R(merge(bMid(L1, R1, 'Standard: fixed instance type'), bMid(L2, R2, 'All upfront: max discount'))))
    lines.append(R(merge(bMid(L1, R1, 'Convertible: change family'), bMid(L2, R2, 'Partial upfront: hybrid'))))
    lines.append(R(merge(bMid(L1, R1, 'Zonal: capacity reserve AZ'), bMid(L2, R2, 'No upfront: monthly billing'))))
    lines.append(R(merge(bMid(L1, R1, 'Regional: flexible AZ usage'), bMid(L2, R2, '1-year: ~40% discount'))))
    lines.append(R(merge(bMid(L1, R1, 'Also: RDS/ElastiCache/Redshift'), bMid(L2, R2, '3-year: up to 72% discount'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Regional RIs flexible across AZ and size; Zonal RIs reserve capacity in specific AZ'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'RI Marketplace: resell unused'), bMid(L2, R2, 'Convertible for flexibility'))))
    lines.append(R(merge(bMid(L1, R1, 'Utilisation report: coverage'), bMid(L2, R2, 'Baseline: commit stable load'))))
    lines.append(R(merge(bMid(L1, R1, 'Coverage report: % reserved'), bMid(L2, R2, 'Spiky: on-demand + spot'))))
    lines.append(R(merge(bMid(L1, R1, 'Org sharing: across accounts'), bMid(L2, R2, 'Review: quarterly utilisation'))))
    lines.append(R(merge(bMid(L1, R1, 'Modify: split or merge'), bMid(L2, R2, 'Savings Plans: often preferred'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS EC2 capacity pool · billing system · RI Marketplace · Cost Explorer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Standard RI     = Fixed instance family/size; largest discount; not exchangeable'))
    lines.append(txt_row('Convertible RI  = Can exchange for different family/size/OS; ~54% max discount'))
    lines.append(txt_row('Zonal RI        = Reserves capacity in specific AZ; smaller size flexibility'))
    lines.append(txt_row('Regional RI     = Applies to any AZ in region; size-flexible within family'))
    lines.append(txt_row('All upfront     = Entire term cost paid day 1; maximum discount'))
    lines.append(txt_row('RI Marketplace  = AWS marketplace to sell unused Standard RIs to other customers'))
    lines.append(txt_row('Utilisation     = % of reserved hours consumed; low = wasted spend'))
    lines.append(txt_row('Coverage        = % of eligible usage covered by RIs vs on-demand'))
    lines.append(txt_row('Org sharing     = RI discount applies to any account in the organisation'))
    lines.append(txt_row('Savings Plans   = More flexible alternative; recommended over RIs for most workloads'))
    lines.append(txt_row('Baseline load   = Steady minimum usage; appropriate to commit with RIs'))
    lines.append(txt_row('Modify RI       = Split one RI into smaller sizes or merge smaller into larger'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-cost-savings-plans', 'docs/cloud/aws/cost/savings-plans/index.md', 'AWS Cost — Savings Plans')
def _aws_cost_savings_plans():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Cost — Savings Plans'))
    lines.append(txt_row())
    lines.append(txt_row('Savings Plans commit $/hour across EC2, Lambda, and Fargate for up to 66% savings.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Plan Types'), bMid(L2, R2, 'Commitment Options'))))
    lines.append(R(merge(bMid(L1, R1, 'Compute SP: EC2+Lambda+Fargate'), bMid(L2, R2, 'Term: 1 or 3 years'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2 Instance SP: per family'), bMid(L2, R2, 'Payment: upfront/partial/none'))))
    lines.append(R(merge(bMid(L1, R1, 'SageMaker SP: ML workloads'), bMid(L2, R2, 'Commit: $/hour threshold'))))
    lines.append(R(merge(bMid(L1, R1, 'Compute SP: 66% max saving'), bMid(L2, R2, 'Flexible: any region/AZ/size'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2 Instance SP: 72% saving'), bMid(L2, R2, 'Org-wide: all accounts'))))
    lines.append(R(merge(bBot(L1, R1), bTop(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Compute SP most flexible; EC2 Instance SP gives highest discount for locked family'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'Recommendations: Cost Explorer'), bMid(L2, R2, 'Analyse 3 months history'))))
    lines.append(R(merge(bMid(L1, R1, 'Utilisation report: coverage %'), bMid(L2, R2, 'Commit to stable baseline'))))
    lines.append(R(merge(bMid(L1, R1, 'Coverage report: % of spend'), bMid(L2, R2, 'Spiky load: on-demand + spot'))))
    lines.append(R(merge(bMid(L1, R1, 'Inventory: purchased plans'), bMid(L2, R2, 'Quarterly review: utilisation'))))
    lines.append(R(merge(bMid(L1, R1, 'No marketplace: non-sellable'), bMid(L2, R2, 'Prefer Compute SP: flexible'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS billing system · Cost Explorer · EC2/Lambda/Fargate capacity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Compute SP      = Most flexible; applies to any EC2 family, Lambda, Fargate'))
    lines.append(txt_row('EC2 Instance SP = Locked to one instance family in one region; highest discount'))
    lines.append(txt_row('SageMaker SP    = Applies to SageMaker ML instance usage'))
    lines.append(txt_row('Commitment $/hr = Hourly spend you agree to pay; usage below = wasted'))
    lines.append(txt_row('Utilisation     = % of commitment consumed; target > 80%'))
    lines.append(txt_row('Coverage        = % of eligible spend covered by Savings Plans'))
    lines.append(txt_row('On-demand top-up= Usage above commitment charges at on-demand rate'))
    lines.append(txt_row('Org-wide sharing= SP purchased in management or any account applies org-wide'))
    lines.append(txt_row('No Marketplace  = Unlike RIs, Savings Plans cannot be resold; permanent commitment'))
    lines.append(txt_row('3-year term     = Longer commitment; higher discount; appropriate for stable services'))
    lines.append(txt_row('Baseline        = Minimum consistent usage; commit $/hr equal to baseline cost'))
    lines.append(txt_row('Cost Explorer rec= Suggests optimal SP type and amount based on usage history'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-gov-account-structure', 'docs/cloud/aws/governance/account-structure/index.md', 'AWS Governance — Account Structure')
def _aws_gov_account_structure():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Governance — Account Structure'))
    lines.append(txt_row())
    lines.append(txt_row('Multi-account structure with OU hierarchy isolating workloads by env and function.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'OU Hierarchy'), bMid(L2, R2, 'Foundation Accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'Root: org top level'), bMid(L2, R2, 'Management: billing + org'))))
    lines.append(R(merge(bMid(L1, R1, 'Security OU: tooling accts'), bMid(L2, R2, 'Log Archive: central logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Infrastructure OU: shared'), bMid(L2, R2, 'Audit/Security: tooling'))))
    lines.append(R(merge(bMid(L1, R1, 'Workloads OU: per team/env'), bMid(L2, R2, 'Network: TGW + DirectConnect'))))
    lines.append(R(merge(bMid(L1, R1, 'Sandbox OU: dev/experiment'), bMid(L2, R2, 'Shared Services: DNS/AD'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Foundation accounts built first; workload accounts provisioned per team or environment'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Account Vending'), bMid(L2, R2, 'Guardrails'))))
    lines.append(R(merge(bMid(L1, R1, 'Control Tower: automated'), bMid(L2, R2, 'SCPs: preventive at OU'))))
    lines.append(R(merge(bMid(L1, R1, 'Account Factory: template'), bMid(L2, R2, 'Config rules: detective'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM Identity Center: SSO'), bMid(L2, R2, 'Security Hub: aggregated'))))
    lines.append(R(merge(bMid(L1, R1, 'Email alias: per account'), bMid(L2, R2, 'CloudTrail: org-wide'))))
    lines.append(R(merge(bMid(L1, R1, 'CMDB: register new account'), bMid(L2, R2, 'GuardDuty: org-enabled'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Organizations · Control Tower · IAM Identity Center · CloudTrail · Config'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OU              = Organizational Unit; logical account grouping with shared SCPs'))
    lines.append(txt_row('Management account= Root of AWS Organization; no workloads; billing owner'))
    lines.append(txt_row('Log Archive     = Account receiving all org CloudTrail and Config delivery'))
    lines.append(txt_row('Control Tower   = AWS service automating multi-account setup with guardrails'))
    lines.append(txt_row('Account Factory = Control Tower feature provisioning accounts from template'))
    lines.append(txt_row('Account vending = Automated process for provisioning a new AWS account to spec'))
    lines.append(txt_row('SCP             = Service Control Policy; preventive restriction at OU level'))
    lines.append(txt_row('Network OU      = Dedicated OU for Transit Gateway and connectivity accounts'))
    lines.append(txt_row('Sandbox OU      = Isolated OU with relaxed SCPs for experimentation'))
    lines.append(txt_row('Email alias     = Shared mailbox per account; avoids personal email as owner'))
    lines.append(txt_row('CMDB            = Configuration Management Database; records account metadata'))
    lines.append(txt_row('Security Hub org= Aggregates security findings from all accounts in organisation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-gov-config', 'docs/cloud/aws/governance/aws-config/index.md', 'AWS Governance — AWS Config')
def _aws_gov_config():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Governance — AWS Config'))
    lines.append(txt_row())
    lines.append(txt_row('Config records resource inventory, tracks changes, and evaluates compliance rules.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Resource Recording'), bMid(L2, R2, 'Config Rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Recorder: all or selected types'), bMid(L2, R2, 'Managed: AWS pre-built rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Configuration item: snapshot'), bMid(L2, R2, 'Custom: Lambda-backed'))))
    lines.append(R(merge(bMid(L1, R1, 'Timeline: change history'), bMid(L2, R2, 'Trigger: change or periodic'))))
    lines.append(R(merge(bMid(L1, R1, 'Delivery: S3 bucket + SNS'), bMid(L2, R2, 'Result: Compliant/NonCompliant'))))
    lines.append(R(merge(bMid(L1, R1, 'Org aggregator: multi-acct'), bMid(L2, R2, 'Conformance pack: bundle'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Recorder captures state; rules evaluate against that state; aggregator consolidates'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Remediation'), bMid(L2, R2, 'Common Rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto: SSM Automation doc'), bMid(L2, R2, 's3-bucket-public-read-prohibited'))))
    lines.append(R(merge(bMid(L1, R1, 'Manual: console review'), bMid(L2, R2, 'ec2-instance-managed-by-ssm'))))
    lines.append(R(merge(bMid(L1, R1, 'Retry: on failure config'), bMid(L2, R2, 'encrypted-volumes'))))
    lines.append(R(merge(bMid(L1, R1, 'EventBridge: trigger action'), bMid(L2, R2, 'mfa-enabled-for-iam-console-access'))))
    lines.append(R(merge(bMid(L1, R1, 'Exceptions: suppress finding'), bMid(L2, R2, 'cloudtrail-enabled'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Config service · S3 (history) · SNS · SSM (remediation) · Security Hub (findings)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Configuration item= Point-in-time snapshot of resource state and relationships'))
    lines.append(txt_row('Recorder        = Config component capturing resource configuration changes'))
    lines.append(txt_row('Config rule     = Evaluates resources against desired configuration state'))
    lines.append(txt_row('Managed rule    = Pre-built rule maintained by AWS; parameterised'))
    lines.append(txt_row('Custom rule     = Lambda function evaluating resource config with custom logic'))
    lines.append(txt_row('Conformance pack= YAML template bundling multiple Config rules and remediations'))
    lines.append(txt_row('Aggregator      = Collects Config data from multiple accounts/regions centrally'))
    lines.append(txt_row('Auto remediation= SSM Automation document triggered on NonCompliant finding'))
    lines.append(txt_row('Compliance score= % of resources Compliant across all evaluated rules'))
    lines.append(txt_row('Change trigger  = Rule evaluates when resource configuration changes'))
    lines.append(txt_row('Periodic trigger= Rule evaluates on schedule (every 1/3/6/12/24 hours)'))
    lines.append(txt_row('Exception       = Suppresses a specific NonCompliant finding for a known reason'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-gov-organizations', 'docs/cloud/aws/governance/aws-organizations/index.md', 'AWS Governance — AWS Organizations')
def _aws_gov_organizations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Governance — AWS Organizations'))
    lines.append(txt_row())
    lines.append(txt_row('AWS Organizations manages multi-account hierarchy, SCPs, and consolidated billing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Organization Structure'), bMid(L2, R2, 'Service Control Policies'))))
    lines.append(R(merge(bMid(L1, R1, 'Root: single top-level'), bMid(L2, R2, 'Attached: to OU or account'))))
    lines.append(R(merge(bMid(L1, R1, 'OUs: nested up to 5 levels'), bMid(L2, R2, 'Effect: Deny or allow boundary'))))
    lines.append(R(merge(bMid(L1, R1, 'Accounts: leaf nodes'), bMid(L2, R2, 'Inheritance: child inherits parent'))))
    lines.append(R(merge(bMid(L1, R1, 'Management: billing root'), bMid(L2, R2, 'FullAWSAccess: default allow'))))
    lines.append(R(merge(bMid(L1, R1, 'Member: standard accounts'), bMid(L2, R2, 'MFA enforcement example'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SCPs limit maximum permissions; IAM policies still needed to grant permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Org-Wide Services'), bMid(L2, R2, 'Account Management'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudTrail: org trail'), bMid(L2, R2, 'create-account: provision'))))
    lines.append(R(merge(bMid(L1, R1, 'Config: aggregator'), bMid(L2, R2, 'move-account: change OU'))))
    lines.append(R(merge(bMid(L1, R1, 'GuardDuty: org enable'), bMid(L2, R2, 'close-account: decommission'))))
    lines.append(R(merge(bMid(L1, R1, 'Security Hub: delegated'), bMid(L2, R2, 'invite-account-to-organization'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: org backup policy'), bMid(L2, R2, 'Tag policies: enforcement'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Organizations service (global) · SCP policy engine · all member accounts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Root            = Top of OU hierarchy; SCPs here apply to every account in org'))
    lines.append(txt_row('OU              = Organizational Unit; groups accounts with common SCP requirements'))
    lines.append(txt_row('SCP             = Service Control Policy; restricts what actions accounts can perform'))
    lines.append(txt_row('FullAWSAccess   = Default SCP allowing all actions; must be paired with deny SCPs'))
    lines.append(txt_row('SCP inheritance = Child OUs and accounts inherit all SCPs from parent OUs'))
    lines.append(txt_row('Delegated admin = Member account granted admin access for specific org services'))
    lines.append(txt_row('Org trail       = CloudTrail trail in management account capturing all member API calls'))
    lines.append(txt_row('Tag policy      = Organizations policy enforcing tag key standardisation'))
    lines.append(txt_row('Backup policy   = Organizations policy deploying backup plans to member accounts'))
    lines.append(txt_row('close-account   = Initiates 90-day closure period; resources still accessible'))
    lines.append(txt_row('create-account  = Provisions new member account; email alias required'))
    lines.append(txt_row('Management account= Cannot have SCPs applied to it; exempt from OU restrictions'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-gov-compliance', 'docs/cloud/aws/governance/compliance-review/index.md', 'AWS Governance — Compliance Review')
def _aws_gov_compliance():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Governance — Compliance Review'))
    lines.append(txt_row())
    lines.append(txt_row('Periodic compliance review using Security Hub, Audit Manager, and Config dashboards.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Review Cadence'), bMid(L2, R2, 'Tools'))))
    lines.append(R(merge(bMid(L1, R1, 'Weekly: Security Hub score'), bMid(L2, R2, 'Security Hub: findings + score'))))
    lines.append(R(merge(bMid(L1, R1, 'Monthly: Config compliance %'), bMid(L2, R2, 'Audit Manager: evidence'))))
    lines.append(R(merge(bMid(L1, R1, 'Quarterly: access review'), bMid(L2, R2, 'Config: rule compliance %'))))
    lines.append(R(merge(bMid(L1, R1, 'Annual: penetration test'), bMid(L2, R2, 'Trusted Advisor: checks'))))
    lines.append(R(merge(bMid(L1, R1, 'On-demand: incident audit'), bMid(L2, R2, 'Inspector: vuln report'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Security Hub score tracked weekly; quarterly access review drives remediation'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Compliance Frameworks'), bMid(L2, R2, 'Remediation Process'))))
    lines.append(R(merge(bMid(L1, R1, 'CIS AWS Foundations v3'), bMid(L2, R2, 'Triage: severity CRITICAL/HIGH'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS Foundational Best Pract.'), bMid(L2, R2, 'Assign: team ownership'))))
    lines.append(R(merge(bMid(L1, R1, 'NIST CSF: via Security Hub'), bMid(L2, R2, 'SLA: 7d critical, 30d high'))))
    lines.append(R(merge(bMid(L1, R1, 'PCI DSS: if card data scope'), bMid(L2, R2, 'Verify: re-check rule state'))))
    lines.append(R(merge(bMid(L1, R1, 'SOC 2: Audit Manager reports'), bMid(L2, R2, 'Exception: documented suppression'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Security Hub · Audit Manager · Config · Inspector · Trusted Advisor · CloudTrail'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Security Hub score= Percentage of security checks passing; target > 90%'))
    lines.append(txt_row('CIS AWS v3      = Center for Internet Security AWS benchmark; prescriptive controls'))
    lines.append(txt_row('Audit Manager   = Maps AWS findings to SOC 2, PCI, NIST evidence requirements'))
    lines.append(txt_row('Trusted Advisor = AWS service flagging cost, security, and performance issues'))
    lines.append(txt_row('Inspector       = Vulnerability scanner for EC2 AMIs and container images'))
    lines.append(txt_row('NIST CSF        = National Institute of Standards and Technology Cybersecurity Framework'))
    lines.append(txt_row('SOC 2           = Service Organisation Control 2; trust services criteria audit'))
    lines.append(txt_row('PCI DSS         = Payment Card Industry Data Security Standard'))
    lines.append(txt_row('Penetration test= AWS permission required for external security testing'))
    lines.append(txt_row('Exception       = Suppressed finding with documented business justification'))
    lines.append(txt_row('Remediation SLA = Maximum time allowed to fix findings by severity level'))
    lines.append(txt_row('Access review   = Quarterly check of IAM users, roles, and permission sets'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-gov-scp', 'docs/cloud/aws/governance/service-control-policies/index.md', 'AWS Governance — Service Control Policies')
def _aws_gov_scp():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Governance — Service Control Policies'))
    lines.append(txt_row())
    lines.append(txt_row('SCPs define maximum permissions for OUs and accounts; deny by default override IAM.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SCP Mechanics'), bMid(L2, R2, 'Common SCP Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'Allow list: explicit permits'), bMid(L2, R2, 'Deny leave org: prevent exit'))))
    lines.append(R(merge(bMid(L1, R1, 'Deny list: explicit blocks'), bMid(L2, R2, 'Require MFA: sensitive ops'))))
    lines.append(R(merge(bMid(L1, R1, 'Deny overrides IAM allow'), bMid(L2, R2, 'Region lock: approved only'))))
    lines.append(R(merge(bMid(L1, R1, 'Root user not exempt'), bMid(L2, R2, 'Protect CloudTrail: no delete'))))
    lines.append(R(merge(bMid(L1, R1, 'Management acct exempt'), bMid(L2, R2, 'Block untagged resources'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Deny list strategy: start with FullAWSAccess then attach deny SCPs on top'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SCP Design'), bMid(L2, R2, 'Testing and Operations'))))
    lines.append(R(merge(bMid(L1, R1, 'Conditions: MFA, IP, tag'), bMid(L2, R2, 'IAM simulator: test SCP'))))
    lines.append(R(merge(bMid(L1, R1, 'NotAction: invert match'), bMid(L2, R2, 'Dry run: sandbox OU first'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource: specific ARN scope'), bMid(L2, R2, 'CloudTrail: SCP deny events'))))
    lines.append(R(merge(bMid(L1, R1, 'Principal: all (*) typical'), bMid(L2, R2, 'AccessDenied: check SCP first'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag condition: enforce tagging'), bMid(L2, R2, 'Document: why each SCP exists'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Organizations SCP engine · IAM policy evaluator · CloudTrail · all accounts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SCP             = Service Control Policy; restricts max permissions in accounts/OUs'))
    lines.append(txt_row('Allow list SCP  = Only listed actions permitted; everything else implicitly denied'))
    lines.append(txt_row('Deny list SCP   = Specific actions denied; FullAWSAccess permits everything else'))
    lines.append(txt_row('FullAWSAccess   = Default SCP allowing all actions; must be on root OU'))
    lines.append(txt_row('Root user exempt= SCP applies to root user of member accounts (not management)'))
    lines.append(txt_row('Management exempt= Management account not subject to any SCP'))
    lines.append(txt_row('Region lock     = SCP denying all actions outside approved AWS regions'))
    lines.append(txt_row('NotAction       = SCP element matching everything except listed actions'))
    lines.append(txt_row('Condition       = JSON condition block; e.g. aws:MultiFactorAuthPresent: true'))
    lines.append(txt_row('IAM simulator   = Tests SCP effect on specific API calls before applying'))
    lines.append(txt_row('Dry run         = Apply SCP to sandbox OU containing test accounts first'))
    lines.append(txt_row('AccessDenied    = Error returned when SCP blocks an action; check Organizations'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-gov-tagging', 'docs/cloud/aws/governance/tagging-standards/index.md', 'AWS Governance — Tagging Standards')
def _aws_gov_tagging():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Governance — Tagging Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Mandatory tag schema for cost allocation, compliance, ownership, and automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Mandatory Tags'), bMid(L2, R2, 'Optional Tags'))))
    lines.append(R(merge(bMid(L1, R1, 'Environment: prod/dev/test'), bMid(L2, R2, 'Version: release tag'))))
    lines.append(R(merge(bMid(L1, R1, 'Owner: team or alias email'), bMid(L2, R2, 'Backup: true/false'))))
    lines.append(R(merge(bMid(L1, R1, 'CostCentre: finance code'), bMid(L2, R2, 'Patch Group: for SSM'))))
    lines.append(R(merge(bMid(L1, R1, 'Application: workload name'), bMid(L2, R2, 'DataClassification: level'))))
    lines.append(R(merge(bMid(L1, R1, 'ManagedBy: terraform/cfn'), bMid(L2, R2, 'Expiry: sandbox TTL date'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Mandatory tags enforced by SCP and Config; optional tags enable automation'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Enforcement'), bMid(L2, R2, 'Naming Convention'))))
    lines.append(R(merge(bMid(L1, R1, 'SCP: deny without required tag'), bMid(L2, R2, 'Keys: PascalCase standard'))))
    lines.append(R(merge(bMid(L1, R1, 'Config: required-tags rule'), bMid(L2, R2, 'Values: lowercase kebab-case'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag policy: org-level case'), bMid(L2, R2, 'No spaces: use hyphens'))))
    lines.append(R(merge(bMid(L1, R1, 'IaC: tags block per resource'), bMid(L2, R2, 'Max: 50 tags per resource'))))
    lines.append(R(merge(bMid(L1, R1, 'Remediation: auto-tag Lambda'), bMid(L2, R2, 'Review: monthly compliance %'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Organizations (tag policies) · Config · SCP engine · Cost Explorer · S3 (CUR)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Tag policy      = Organizations policy enforcing allowed tag values and case'))
    lines.append(txt_row('required-tags   = Config managed rule detecting resources missing mandatory tags'))
    lines.append(txt_row('PascalCase      = Tag key convention: Environment, CostCentre, Owner'))
    lines.append(txt_row('kebab-case      = Tag value convention: prod, dev, finance-123'))
    lines.append(txt_row('ManagedBy       = Tag indicating IaC tool owning the resource lifecycle'))
    lines.append(txt_row('DataClassification= Tag indicating sensitivity: public, internal, confidential'))
    lines.append(txt_row('Expiry tag      = Date after which sandbox resource is auto-deleted by Lambda'))
    lines.append(txt_row('Patch Group     = SSM tag linking instance to patch baseline'))
    lines.append(txt_row('Auto-tag Lambda = EventBridge-triggered Lambda applying default tags on resource create'))
    lines.append(txt_row('Tag compliance  = % of resources with all required tags; tracked in Config'))
    lines.append(txt_row('Cost allocation = Tags activated in Billing console appear in CUR and Cost Explorer'))
    lines.append(txt_row('IaC tags block  = Terraform/CloudFormation resource property ensuring tags at deploy'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-identity-access-keys', 'docs/cloud/aws/identity/access-keys/index.md', 'AWS Identity — Access Keys')
def _aws_identity_access_keys():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Identity — Access Keys'))
    lines.append(txt_row())
    lines.append(txt_row('Long-term programmatic credentials: lifecycle, rotation, and replacement with roles.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Access Key Overview'), bMid(L2, R2, 'Risks'))))
    lines.append(R(merge(bMid(L1, R1, 'ID + secret: permanent creds'), bMid(L2, R2, 'Long-lived: exposure window'))))
    lines.append(R(merge(bMid(L1, R1, 'Max 2 keys per IAM user'), bMid(L2, R2, 'Leaked: GitHub/log/code'))))
    lines.append(R(merge(bMid(L1, R1, 'Used: CLI/SDK/API calls'), bMid(L2, R2, 'No MFA: bypasses console MFA'))))
    lines.append(R(merge(bMid(L1, R1, 'Status: Active or Inactive'), bMid(L2, R2, 'Root keys: highest risk'))))
    lines.append(R(merge(bMid(L1, R1, 'Rotation: 90-day policy'), bMid(L2, R2, 'No auto-expiry built-in'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Replace access keys with IAM roles wherever possible; keys only for legacy systems'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Rotation Process'), bMid(L2, R2, 'Alternatives'))))
    lines.append(R(merge(bMid(L1, R1, '1. Create new key'), bMid(L2, R2, 'IAM roles: no static keys'))))
    lines.append(R(merge(bMid(L1, R1, '2. Update all consumers'), bMid(L2, R2, 'OIDC: GitHub Actions / EKS'))))
    lines.append(R(merge(bMid(L1, R1, '3. Deactivate old key'), bMid(L2, R2, 'Instance profile: EC2 roles'))))
    lines.append(R(merge(bMid(L1, R1, '4. Monitor: no denials'), bMid(L2, R2, 'Secrets Manager: auto-rotate'))))
    lines.append(R(merge(bMid(L1, R1, '5. Delete old key'), bMid(L2, R2, 'CyberArk: PAM vault keys'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('IAM service (global) · STS · CloudTrail · Secrets Manager · GuardDuty'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Access key ID   = 20-char identifier starting with AKIA; public part of credential'))
    lines.append(txt_row('Secret access key= 40-char secret; shown once at creation; never retrievable again'))
    lines.append(txt_row('Inactive status = Key exists but rejected; use during rotation test period'))
    lines.append(txt_row('Rotation        = Creating new key, updating consumers, deleting old key'))
    lines.append(txt_row('Root access key = Key for root account; delete immediately; use roles instead'))
    lines.append(txt_row('OIDC            = OpenID Connect; allows services to assume IAM roles without keys'))
    lines.append(txt_row('Instance profile= Wrapper attaching IAM role to EC2; provides temp credentials'))
    lines.append(txt_row('Credential report= IAM report listing all keys, last-used date, and rotation age'))
    lines.append(txt_row('GuardDuty       = Detects access key use from unusual locations or TOR nodes'))
    lines.append(txt_row('Secrets Manager = Stores and auto-rotates access keys for legacy integrations'))
    lines.append(txt_row('90-day policy   = Config rule flagging keys older than 90 days as NonCompliant'))
    lines.append(txt_row('AKIA prefix     = Indicates long-term access key; ASIA prefix = temporary STS key'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-identity-cross-account', 'docs/cloud/aws/identity/cross-account-access/index.md', 'AWS Identity — Cross-Account Access')
def _aws_identity_cross_account():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Identity — Cross-Account Access'))
    lines.append(txt_row())
    lines.append(txt_row('Cross-account IAM role assumption enables multi-account access without static keys.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Role Assumption Flow'), bMid(L2, R2, 'Trust Policy'))))
    lines.append(R(merge(bMid(L1, R1, '1. Source calls AssumeRole'), bMid(L2, R2, 'Principal: source account ID'))))
    lines.append(R(merge(bMid(L1, R1, '2. STS validates trust policy'), bMid(L2, R2, 'Action: sts:AssumeRole'))))
    lines.append(R(merge(bMid(L1, R1, '3. STS returns temp creds'), bMid(L2, R2, 'Condition: ExternalId'))))
    lines.append(R(merge(bMid(L1, R1, '4. Caller uses creds in target'), bMid(L2, R2, 'Condition: MFA required'))))
    lines.append(R(merge(bMid(L1, R1, '5. Creds expire: max 12 hrs'), bMid(L2, R2, 'Condition: source IP range'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Source needs permission to call sts:AssumeRole; target role trust policy allows it'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'IAM Identity Center'), bMid(L2, R2, 'Resource-Based Policies'))))
    lines.append(R(merge(bMid(L1, R1, 'Permission set: wrapped role'), bMid(L2, R2, 'S3 bucket policy: cross-acct'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: human cross-acct login'), bMid(L2, R2, 'KMS key policy: cross-acct'))))
    lines.append(R(merge(bMid(L1, R1, 'No long-term keys needed'), bMid(L2, R2, 'SNS/SQS: cross-acct publish'))))
    lines.append(R(merge(bMid(L1, R1, 'Centralised access portal'), bMid(L2, R2, 'ECR: cross-acct pull'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: CloudTrail per account'), bMid(L2, R2, 'No assume needed: direct'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('STS (global) · IAM policy engine · CloudTrail · IAM Identity Center'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AssumeRole      = STS API call exchanging identity for temp role credentials'))
    lines.append(txt_row('Trust policy    = JSON on target role specifying who can assume it'))
    lines.append(txt_row('ExternalId      = Secret condition value preventing confused deputy attacks'))
    lines.append(txt_row('Confused deputy = Attack where trusted third party is tricked into acting on attacker'))
    lines.append(txt_row('STS             = Security Token Service; issues temporary credentials'))
    lines.append(txt_row('Temp credentials= Access key + secret + session token; expire in 15min–12hr'))
    lines.append(txt_row('Session token   = Third credential component required with temp access keys'))
    lines.append(txt_row('Permission set  = IAM Identity Center construct wrapping cross-account role'))
    lines.append(txt_row('Resource policy = Policy on resource (S3/KMS/SNS) granting cross-account access'))
    lines.append(txt_row('Max session     = AssumeRole --duration-seconds; max 43200 (12 hours)'))
    lines.append(txt_row('Org condition   = aws:PrincipalOrgID condition restricts to accounts in same org'))
    lines.append(txt_row('CloudTrail      = Both source and target account record the AssumeRole event'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-identity-iam', 'docs/cloud/aws/identity/iam/index.md', 'AWS Identity — IAM')
def _aws_identity_iam():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Identity — IAM'))
    lines.append(txt_row())
    lines.append(txt_row('IAM: users, roles, groups, and policies controlling all AWS API access.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'IAM Principals'), bMid(L2, R2, 'Policy Types'))))
    lines.append(R(merge(bMid(L1, R1, 'Users: human + programmatic'), bMid(L2, R2, 'Identity: attached to user/role'))))
    lines.append(R(merge(bMid(L1, R1, 'Roles: service or cross-acct'), bMid(L2, R2, 'Resource: on S3/KMS/SQS'))))
    lines.append(R(merge(bMid(L1, R1, 'Groups: user collections'), bMid(L2, R2, 'SCP: OU-level boundary'))))
    lines.append(R(merge(bMid(L1, R1, 'Service accounts: automation'), bMid(L2, R2, 'Permission boundary: limit'))))
    lines.append(R(merge(bMid(L1, R1, 'Root: avoid; use roles'), bMid(L2, R2, 'Session: AssumeRole context'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Effective permissions = intersection of all applicable policy types'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy Evaluation'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, '1. Explicit deny: always wins'), bMid(L2, R2, 'Least privilege: minimal perms'))))
    lines.append(R(merge(bMid(L1, R1, '2. SCP: must allow'), bMid(L2, R2, 'Roles over users: no static keys'))))
    lines.append(R(merge(bMid(L1, R1, '3. Resource policy check'), bMid(L2, R2, 'Groups: manage at group level'))))
    lines.append(R(merge(bMid(L1, R1, '4. Permission boundary'), bMid(L2, R2, 'No wildcard: specify actions'))))
    lines.append(R(merge(bMid(L1, R1, '5. Identity policy: allow'), bMid(L2, R2, 'Review: quarterly unused'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('IAM service (global, free) · STS · CloudTrail · IAM Access Analyzer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Principal       = Entity making AWS API request: user, role, service, account'))
    lines.append(txt_row('Policy          = JSON document defining allowed or denied actions on resources'))
    lines.append(txt_row('Managed policy  = Standalone reusable policy; AWS-managed or customer-managed'))
    lines.append(txt_row('Inline policy   = Embedded directly in user/role; deleted with the principal'))
    lines.append(txt_row('Permission boundary= IAM policy capping max permissions a principal can have'))
    lines.append(txt_row('IAM Access Analyzer= Identifies resources accessible from outside the account'))
    lines.append(txt_row('Explicit deny   = Deny statement that always overrides any allow'))
    lines.append(txt_row('Policy evaluation= Order: explicit deny → SCP → resource policy → boundary → identity'))
    lines.append(txt_row('Least privilege = Grant only permissions required for the specific task'))
    lines.append(txt_row('IAM group       = Collection of users inheriting same policies; simplifies management'))
    lines.append(txt_row('Service role    = IAM role a service (Lambda, EC2) assumes to call other services'))
    lines.append(txt_row('Root user       = Account owner; has full access; protect with MFA; do not use daily'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-identity-iam-policies', 'docs/cloud/aws/identity/iam-policies/index.md', 'AWS Identity — IAM Policies')
def _aws_identity_iam_policies():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Identity — IAM Policies'))
    lines.append(txt_row())
    lines.append(txt_row('IAM policy structure: Effect, Action, Resource, Condition — with evaluation logic.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy Structure'), bMid(L2, R2, 'Policy Elements'))))
    lines.append(R(merge(bMid(L1, R1, 'Version: 2012-10-17'), bMid(L2, R2, 'Effect: Allow or Deny'))))
    lines.append(R(merge(bMid(L1, R1, 'Statement: array of rules'), bMid(L2, R2, 'Action: s3:GetObject'))))
    lines.append(R(merge(bMid(L1, R1, 'Sid: optional identifier'), bMid(L2, R2, 'Resource: ARN or *'))))
    lines.append(R(merge(bMid(L1, R1, 'Principal: who (resource pol)'), bMid(L2, R2, 'Condition: context key check'))))
    lines.append(R(merge(bMid(L1, R1, 'NotAction/NotResource: invert'), bMid(L2, R2, 'Multiple statements: all eval'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('All statements evaluated; explicit deny in any statement wins over any allow'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Common Conditions'), bMid(L2, R2, 'Policy Examples'))))
    lines.append(R(merge(bMid(L1, R1, 'aws:MultiFactorAuthPresent'), bMid(L2, R2, 'S3 read-only: s3:Get* on ARN'))))
    lines.append(R(merge(bMid(L1, R1, 'aws:RequestedRegion'), bMid(L2, R2, 'EC2 start/stop: specific IDs'))))
    lines.append(R(merge(bMid(L1, R1, 'aws:PrincipalOrgID'), bMid(L2, R2, 'Require tag: StringEquals'))))
    lines.append(R(merge(bMid(L1, R1, 'aws:SourceIp: CIDR check'), bMid(L2, R2, 'Deny if no MFA: condition'))))
    lines.append(R(merge(bMid(L1, R1, 'aws:TagKeys: enforce tags'), bMid(L2, R2, 'Region lock: NotAction+Deny'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('IAM policy engine (global) · STS context · CloudTrail · IAM Access Analyzer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Statement       = Single permission rule with Effect, Action, Resource, Condition'))
    lines.append(txt_row('Action          = AWS API call: s3:PutObject, ec2:DescribeInstances'))
    lines.append(txt_row('Resource ARN    = Amazon Resource Name identifying specific resource'))
    lines.append(txt_row('Condition block = Optional; adds context constraints to when policy applies'))
    lines.append(txt_row('StringEquals    = Condition operator for exact string match'))
    lines.append(txt_row('NotAction       = Matches every action except those listed; use carefully'))
    lines.append(txt_row('aws:PrincipalOrgID= Condition key matching requesting account org membership'))
    lines.append(txt_row('aws:SourceIp    = Condition key matching caller IP; only works for direct calls'))
    lines.append(txt_row('aws:VpcSourceIp = Condition key matching caller IP when going through VPC endpoint'))
    lines.append(txt_row('IAM Access Analyzer= Scans policies for external access and validates syntax'))
    lines.append(txt_row('Policy simulator= IAM console tool testing policy effect on specific API calls'))
    lines.append(txt_row('Version 2012-10-17= Current policy language version; always include this'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-identity-iam-roles', 'docs/cloud/aws/identity/iam-roles/index.md', 'AWS Identity — IAM Roles')
def _aws_identity_iam_roles():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Identity — IAM Roles'))
    lines.append(txt_row())
    lines.append(txt_row('IAM roles provide temporary credentials for services, cross-account, and federation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Role Types'), bMid(L2, R2, 'Trust Policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Service role: EC2/Lambda/EKS'), bMid(L2, R2, 'Principal: service or account'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account: AssumeRole'), bMid(L2, R2, 'Action: sts:AssumeRole'))))
    lines.append(R(merge(bMid(L1, R1, 'Federation: SAML/OIDC'), bMid(L2, R2, 'Condition: ExternalId/MFA'))))
    lines.append(R(merge(bMid(L1, R1, 'Instance profile: EC2 wrapper'), bMid(L2, R2, 'sts:AssumeRoleWithWebIdentity'))))
    lines.append(R(merge(bMid(L1, R1, 'Linked service role: AWS mgd'), bMid(L2, R2, 'sts:AssumeRoleWithSAML'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Trust policy defines who can assume; permission policy defines what they can do'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Role Session'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'Duration: 15min–12hr max'), bMid(L2, R2, 'No static keys: use roles'))))
    lines.append(R(merge(bMid(L1, R1, 'Session name: caller identity'), bMid(L2, R2, 'Least privilege: minimal perms'))))
    lines.append(R(merge(bMid(L1, R1, 'Session tags: pass context'), bMid(L2, R2, 'IRSA: K8s pod-level role'))))
    lines.append(R(merge(bMid(L1, R1, 'Session policy: narrow scope'), bMid(L2, R2, 'Permission boundary: devs'))))
    lines.append(R(merge(bMid(L1, R1, 'Revoke: invalidate sessions'), bMid(L2, R2, 'Review: quarterly unused roles'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('STS (global) · IAM policy engine · CloudTrail · OIDC provider · SAML IdP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Trust policy    = JSON on role defining which principals can assume it'))
    lines.append(txt_row('AssumeRole      = STS call returning temporary access key + secret + token'))
    lines.append(txt_row('Service role    = Role a service (Lambda, EC2) assumes; defined in trust policy'))
    lines.append(txt_row('Instance profile= Wrapper allowing IAM role to be attached to EC2 instance'))
    lines.append(txt_row('IRSA            = IAM Roles for Service Accounts; EKS pod assumes IAM role via OIDC'))
    lines.append(txt_row('Session tag     = Key-value pair attached to role session; flows into policy conditions'))
    lines.append(txt_row('Session policy  = Additional inline policy narrowing role permissions at assume time'))
    lines.append(txt_row('Linked service role= Role created and managed by AWS for a specific service'))
    lines.append(txt_row('OIDC provider   = IAM trust configuration for GitHub Actions, EKS, or Cognito'))
    lines.append(txt_row('Revoke sessions = Add deny policy with condition on token issue time'))
    lines.append(txt_row('ExternalId      = Prevents confused deputy; required for third-party role assumptions'))
    lines.append(txt_row('Permission boundary= IAM policy capping maximum role permissions; used for delegation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-identity-permission-review', 'docs/cloud/aws/identity/permission-review/index.md', 'AWS Identity — Permission Review')
def _aws_identity_permission_review():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Identity — Permission Review'))
    lines.append(txt_row())
    lines.append(txt_row('Quarterly IAM review: remove unused principals, trim over-privileged policies.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Review Scope'), bMid(L2, R2, 'Tools'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM users: last-used date'), bMid(L2, R2, 'Credential report: all users'))))
    lines.append(R(merge(bMid(L1, R1, 'Access keys: 90-day rotation'), bMid(L2, R2, 'Access Analyzer: ext access'))))
    lines.append(R(merge(bMid(L1, R1, 'Roles: last assumed date'), bMid(L2, R2, 'IAM last-accessed data'))))
    lines.append(R(merge(bMid(L1, R1, 'Policies: unused actions'), bMid(L2, R2, 'CloudTrail: API usage data'))))
    lines.append(R(merge(bMid(L1, R1, 'Groups: membership correct'), bMid(L2, R2, 'Security Hub: IAM findings'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Last-accessed data shows unused services; trim to what was actually used'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Remediation Actions'), bMid(L2, R2, 'Automation'))))
    lines.append(R(merge(bMid(L1, R1, 'Delete: unused users/keys'), bMid(L2, R2, 'Lambda: flag stale accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable: inactive keys first'), bMid(L2, R2, 'Config: access-key-rotated'))))
    lines.append(R(merge(bMid(L1, R1, 'Trim: remove unused services'), bMid(L2, R2, 'EventBridge: 90-day trigger'))))
    lines.append(R(merge(bMid(L1, R1, 'Detach: over-broad policies'), bMid(L2, R2, 'Jira: auto-ticket per finding'))))
    lines.append(R(merge(bMid(L1, R1, 'Document: exceptions with expiry'), bMid(L2, R2, 'Review: tracked in ITSM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('IAM service · CloudTrail · Access Analyzer · Security Hub · Config · Lambda'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Credential report= CSV of all IAM users with password/key last-used dates'))
    lines.append(txt_row('Last-accessed data= Shows which AWS services a role/user has called in last 90 days'))
    lines.append(txt_row('Access Analyzer = Identifies IAM roles/S3/KMS accessible from outside the account'))
    lines.append(txt_row('Unused action   = API action granted by policy but never called in review period'))
    lines.append(txt_row('Stale account   = IAM user not logged in for > 90 days; candidate for deletion'))
    lines.append(txt_row('90-day trigger  = EventBridge rule firing when key age exceeds rotation threshold'))
    lines.append(txt_row('access-key-rotated= Config managed rule flagging keys older than specified days'))
    lines.append(txt_row('Over-privileged = Principal has more permissions than needed for their role'))
    lines.append(txt_row('Exception       = Documented justification for keeping broad permissions with expiry'))
    lines.append(txt_row('ITSM tracking   = Review findings tracked as tickets in ServiceNow or Jira'))
    lines.append(txt_row('Disable before delete= Inactivate key first; verify no breakage; then delete'))
    lines.append(txt_row('Security Hub findings= IAM-related CIS checks reported as findings in Security Hub'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-monitoring-health', 'docs/cloud/aws/monitoring/aws-health/index.md', 'AWS Health — service health events, scheduled changes, and account-specific alerts')
def _aws_monitoring_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Health — Service & Account Health'))
    lines.append(txt_row())
    lines.append(txt_row('AWS Health surfaces service events, scheduled maintenance, and account-specific issues.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Event Sources'), bMid(L2, R2, 'Health Dashboard'))))
    lines.append(R(merge(bMid(L1, R1, 'Service events: regional outages'), bMid(L2, R2, 'Personal Health Dashboard'))))
    lines.append(R(merge(bMid(L1, R1, 'Account events: limit/config issues'), bMid(L2, R2, 'AWS Status page: public view'))))
    lines.append(R(merge(bMid(L1, R1, 'Scheduled changes: maintenance windows'), bMid(L2, R2, 'EventBridge integration: alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'Operational notifications: best practice'), bMid(L2, R2, 'Organizations view: all accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'Investigations: active AWS support cases'), bMid(L2, R2, 'API: DescribeEvents, DescribeAffected'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Events flow to EventBridge rules → SNS/Lambda; org-level view requires delegated admin.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'EventBridge Rules'), bMid(L2, R2, 'Response Actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Event pattern: source=health'), bMid(L2, R2, 'SNS: notify on-call teams'))))
    lines.append(R(merge(bMid(L1, R1, 'Filter: eventTypeCategory'), bMid(L2, R2, 'Lambda: auto-remediation scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Filter: specific services/regions'), bMid(L2, R2, 'Slack/PagerDuty: incident creation'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account: org-level event bus'), bMid(L2, R2, 'ITSM: ServiceNow ticket creation'))))
    lines.append(R(merge(bMid(L1, R1, 'Archive: store all health events'), bMid(L2, R2, 'Runbook: link affected resource ARN'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global backbone · Regional control planes · Availability Zone infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Personal Health Dashboard= Account-specific view of events affecting your resources'))
    lines.append(txt_row('Service Health Dashboard = Public AWS status page showing service health per region'))
    lines.append(txt_row('eventTypeCategory    = Classification: issue, scheduledChange, or accountNotification'))
    lines.append(txt_row('eventTypeCode        = Specific event type, e.g. AWS_EC2_INSTANCE_STOP_SCHEDULED'))
    lines.append(txt_row('Affected entities    = Specific resource ARNs or account IDs impacted by the event'))
    lines.append(txt_row('Organizations view   = Aggregated health events across all accounts in the org'))
    lines.append(txt_row('Delegated admin      = Account designated to view org-wide health events via API'))
    lines.append(txt_row('EventBridge rule     = Pattern-matched rule forwarding health events to targets'))
    lines.append(txt_row('Scheduled change     = Planned AWS maintenance requiring customer action or awareness'))
    lines.append(txt_row('Investigation        = Active AWS support engagement linked to a health event'))
    lines.append(txt_row('DescribeEvents API   = Lists health events matching filters; requires Business/Enterprise'))
    lines.append(txt_row('Upcoming changes     = 14-day advance notice for planned infrastructure maintenance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-monitoring-cloudtrail', 'docs/cloud/aws/monitoring/cloudtrail/index.md', 'CloudTrail — API call logging, governance audit trail, and security investigation')
def _aws_monitoring_cloudtrail():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudTrail — API Audit Logging'))
    lines.append(txt_row())
    lines.append(txt_row('CloudTrail records all AWS API calls for governance, compliance, and security investigation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Trail Types'), bMid(L2, R2, 'Event Categories'))))
    lines.append(R(merge(bMid(L1, R1, 'Management trail: control-plane ops'), bMid(L2, R2, 'Management events: API calls'))))
    lines.append(R(merge(bMid(L1, R1, 'Data trail: S3/Lambda data-plane ops'), bMid(L2, R2, 'Data events: object read/write'))))
    lines.append(R(merge(bMid(L1, R1, 'Org trail: all accounts in org'), bMid(L2, R2, 'Insights: unusual activity detection'))))
    lines.append(R(merge(bMid(L1, R1, 'Single-region vs multi-region trail'), bMid(L2, R2, 'Read-only vs write-only filtering'))))
    lines.append(R(merge(bMid(L1, R1, 'Lake: SQL query across events'), bMid(L2, R2, 'Exclude: high-volume read events'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Events delivered to S3 within ~15 min; CloudWatch Logs for real-time analysis.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage & Integrity'), bMid(L2, R2, 'Analysis & Alerting'))))
    lines.append(R(merge(bMid(L1, R1, 'S3 bucket: log storage with SSE-KMS'), bMid(L2, R2, 'CloudWatch Logs: metric filters'))))
    lines.append(R(merge(bMid(L1, R1, 'Log file validation: SHA-256 digest'), bMid(L2, R2, 'Athena: ad-hoc SQL queries on S3'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA delete: protect log bucket'), bMid(L2, R2, 'CloudTrail Lake: managed SQL engine'))))
    lines.append(R(merge(bMid(L1, R1, 'Retention: S3 lifecycle to Glacier'), bMid(L2, R2, 'Security Hub: CloudTrail findings'))))
    lines.append(R(merge(bMid(L1, R1, 'Replication: cross-region S3 copy'), bMid(L2, R2, 'EventBridge: real-time rule triggers'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global backbone · S3 storage infrastructure · Regional CloudTrail endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Trail           = Configuration defining which events to log and where to deliver them'))
    lines.append(txt_row('Management event= Control-plane API call: CreateInstance, PutBucketPolicy, AttachRole'))
    lines.append(txt_row('Data event      = Data-plane operation: S3 GetObject/PutObject, Lambda Invoke'))
    lines.append(txt_row('Insights event  = Anomaly detected: unusual API call rate or error rate spike'))
    lines.append(txt_row('Org trail       = Single trail that captures events from all member accounts in org'))
    lines.append(txt_row('Log file validation= Digest file lets you verify logs were not tampered after delivery'))
    lines.append(txt_row('CloudTrail Lake = Managed event data store; query with SQL up to 7-year retention'))
    lines.append(txt_row('Event history   = 90-day free lookup without a trail; management events only'))
    lines.append(txt_row('userIdentity    = JSON field in each log record identifying who made the API call'))
    lines.append(txt_row('sourceIPAddress = IP or AWS service that originated the API call in the log record'))
    lines.append(txt_row('eventName       = Specific AWS API action recorded, e.g. RunInstances, DeleteBucket'))
    lines.append(txt_row('Athena query    = Ad-hoc SQL against CloudTrail JSON logs stored in S3 via Glue table'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-monitoring-cloudwatch', 'docs/cloud/aws/monitoring/cloudwatch/index.md', 'CloudWatch — metrics, dashboards, and unified observability for AWS resources')
def _aws_monitoring_cloudwatch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudWatch — Unified AWS Observability'))
    lines.append(txt_row())
    lines.append(txt_row('CloudWatch collects metrics, logs, and traces to provide observability across all AWS services.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Sources'), bMid(L2, R2, 'Core Capabilities'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS services: auto-publish metrics'), bMid(L2, R2, 'Metrics: time-series data points'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2: CloudWatch agent on instances'), bMid(L2, R2, 'Dashboards: cross-service widgets'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom: PutMetricData API'), bMid(L2, R2, 'Alarms: threshold-based alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'Logs: CloudWatch Logs groups'), bMid(L2, R2, 'Logs Insights: query log data'))))
    lines.append(R(merge(bMid(L1, R1, 'X-Ray: distributed trace segments'), bMid(L2, R2, 'Container Insights: EKS/ECS metrics'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Metrics retained 15 months; alarms evaluate period-by-period and notify via SNS/action.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Alarms & Actions'), bMid(L2, R2, 'Advanced Features'))))
    lines.append(R(merge(bMid(L1, R1, 'Threshold: static value comparison'), bMid(L2, R2, 'Anomaly detection: ML baseline'))))
    lines.append(R(merge(bMid(L1, R1, 'Composite alarms: AND/OR logic'), bMid(L2, R2, 'Metric math: cross-metric formulas'))))
    lines.append(R(merge(bMid(L1, R1, 'Actions: SNS, EC2, Auto Scaling'), bMid(L2, R2, 'Contributor Insights: top-N analysis'))))
    lines.append(R(merge(bMid(L1, R1, 'Alarm states: OK/ALARM/INSUFFICIENT'), bMid(L2, R2, 'ServiceLens: trace-metric correlation'))))
    lines.append(R(merge(bMid(L1, R1, 'Suppression: maintenance window'), bMid(L2, R2, 'Synthetics: canary endpoint tests'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS regional CloudWatch endpoints · S3 backend for log storage · Global backbone'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Namespace       = Logical grouping of metrics, e.g. AWS/EC2, AWS/RDS, Custom/App'))
    lines.append(txt_row('Dimension       = Key-value pair that identifies a metric, e.g. InstanceId=i-12345'))
    lines.append(txt_row('Period          = Granularity of metric data points: 1s, 10s, 30s, or multiples of 60'))
    lines.append(txt_row('Statistics      = Aggregation function: Average, Sum, Min, Max, SampleCount, pNN.NN'))
    lines.append(txt_row('High-resolution = Sub-minute metric with 1s/10s/30s period (custom metrics only)'))
    lines.append(txt_row('Composite alarm = Alarm that evaluates other alarms with Boolean (AND/OR/NOT) logic'))
    lines.append(txt_row('Metric math     = Formula combining multiple metrics, e.g. CPUUtilization/100'))
    lines.append(txt_row('Anomaly detection= ML model trained on metric history to define expected band'))
    lines.append(txt_row('Contributor Insights= Identifies top-N callers or keys driving a metric spike'))
    lines.append(txt_row('ServiceLens     = Integrates X-Ray traces with CloudWatch metrics and alarms'))
    lines.append(txt_row('Synthetics canary= Scripted browser/API test that checks endpoints on a schedule'))
    lines.append(txt_row('Container Insights= Enhanced metrics for EKS nodes, pods, and containers'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-monitoring-cloudwatch-alarms', 'docs/cloud/aws/monitoring/cloudwatch-alarms/index.md', 'CloudWatch Alarms — threshold configuration, composite alarms, and automated actions')
def _aws_monitoring_cloudwatch_alarms():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudWatch Alarms — Threshold Alerting'))
    lines.append(txt_row())
    lines.append(txt_row('CloudWatch Alarms evaluate metrics against thresholds and trigger automated responses.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Alarm Configuration'), bMid(L2, R2, 'Alarm Types'))))
    lines.append(R(merge(bMid(L1, R1, 'Metric: namespace + name + dims'), bMid(L2, R2, 'Static: fixed threshold value'))))
    lines.append(R(merge(bMid(L1, R1, 'Period: evaluation interval'), bMid(L2, R2, 'Anomaly detection: ML band'))))
    lines.append(R(merge(bMid(L1, R1, 'Evaluation periods: N of M breaches'), bMid(L2, R2, 'Composite: Boolean of child alarms'))))
    lines.append(R(merge(bMid(L1, R1, 'Threshold: comparison + value'), bMid(L2, R2, 'Metric math: formula-based'))))
    lines.append(R(merge(bMid(L1, R1, 'Missing data: breaching/notBreaching'), bMid(L2, R2, 'Billing alarm: account spend'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Alarms in ALARM state trigger actions; composite alarms reduce alert noise with logic.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Alarm Actions'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'SNS: notify teams via email/SMS'), bMid(L2, R2, 'Use composite to reduce noise'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2: stop/reboot/terminate/recover'), bMid(L2, R2, 'Datapoints to alarm: N of M'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto Scaling: scale-out/in policy'), bMid(L2, R2, 'Set breaching for missing data'))))
    lines.append(R(merge(bMid(L1, R1, 'Systems Manager OpsItem creation'), bMid(L2, R2, 'Tag alarms with team/service'))))
    lines.append(R(merge(bMid(L1, R1, 'Lambda: custom remediation trigger'), bMid(L2, R2, 'Test with set-alarm-state CLI'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS CloudWatch control plane · Regional endpoints · SNS delivery infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evaluation period= Time window for one metric data point comparison against threshold'))
    lines.append(txt_row('Datapoints to alarm= Number of breaching periods needed before alarm state triggers'))
    lines.append(txt_row('N of M            = Alarm triggers when N out of last M evaluation periods breach'))
    lines.append(txt_row('ALARM state       = Threshold breached for required number of consecutive/total periods'))
    lines.append(txt_row('OK state          = Metric is within acceptable range for all evaluation periods'))
    lines.append(txt_row('INSUFFICIENT_DATA = Not enough metric data points to evaluate the alarm condition'))
    lines.append(txt_row('Composite alarm   = Parent alarm whose state is computed from child alarm states'))
    lines.append(txt_row('Anomaly band      = ML-derived upper/lower bounds; alarm fires outside the band'))
    lines.append(txt_row('treat missing data= How to count missing data points: notBreaching, breaching, ignore'))
    lines.append(txt_row('EC2 recover action= Auto-recover instance on system check failure; preserves private IP'))
    lines.append(txt_row('Billing alarm     = Monitors EstimatedCharges metric; requires billing alerts enabled'))
    lines.append(txt_row('OpsItem action    = Creates Systems Manager OpsItem when alarm fires for ITSM tracking'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-monitoring-cloudwatch-logs', 'docs/cloud/aws/monitoring/cloudwatch-logs/index.md', 'CloudWatch Logs — log ingestion, retention, metric filters, and Logs Insights queries')
def _aws_monitoring_cloudwatch_logs():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudWatch Logs — Log Management'))
    lines.append(txt_row())
    lines.append(txt_row('CloudWatch Logs ingests, stores, and queries log data from AWS services and applications.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Log Ingestion'), bMid(L2, R2, 'Storage & Retention'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudWatch agent: EC2/on-prem logs'), bMid(L2, R2, 'Log groups: top-level container'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS services: auto-publish logs'), bMid(L2, R2, 'Log streams: per instance/resource'))))
    lines.append(R(merge(bMid(L1, R1, 'Lambda: stdout/stderr auto-captured'), bMid(L2, R2, 'Retention: 1 day to 10 years'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC Flow Logs: network traffic'), bMid(L2, R2, 'Encryption: KMS CMK on group'))))
    lines.append(R(merge(bMid(L1, R1, 'PutLogEvents API: custom app logs'), bMid(L2, R2, 'Export: S3 bucket for long-term'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Metric filters convert log patterns to metrics; subscriptions stream logs to destinations.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Analysis'), bMid(L2, R2, 'Destinations & Actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Logs Insights: query language'), bMid(L2, R2, 'Metric filter: pattern → metric'))))
    lines.append(R(merge(bMid(L1, R1, 'Fields, filter, stats, sort cmds'), bMid(L2, R2, 'Subscription filter: Kinesis/Lambda'))))
    lines.append(R(merge(bMid(L1, R1, 'Visualize: time-series bar charts'), bMid(L2, R2, 'Cross-account delivery: log sink'))))
    lines.append(R(merge(bMid(L1, R1, 'Save queries: reuse across sessions'), bMid(L2, R2, 'CloudWatch Alarm on metric filter'))))
    lines.append(R(merge(bMid(L1, R1, 'Live tail: real-time log streaming'), bMid(L2, R2, 'OpenSearch: subscription export'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS CloudWatch Logs storage infrastructure · Kinesis data plane · Regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Log group       = Top-level container for logs; retention and encryption set here'))
    lines.append(txt_row('Log stream      = Sequence of log events from a single source within a log group'))
    lines.append(txt_row('Log event       = Timestamped record with a message string; basic unit of log data'))
    lines.append(txt_row('Metric filter   = Pattern match on log events that increments a custom CloudWatch metric'))
    lines.append(txt_row('Subscription filter= Delivers matching log events in real time to Kinesis, Lambda, or Firehose'))
    lines.append(txt_row('Logs Insights   = Query engine for CloudWatch Logs using a purpose-built query language'))
    lines.append(txt_row('fields command  = Logs Insights: selects specific fields from JSON-structured log events'))
    lines.append(txt_row('filter command  = Logs Insights: includes/excludes events matching a pattern or condition'))
    lines.append(txt_row('stats command   = Logs Insights: aggregates field values with count, sum, avg, min, max'))
    lines.append(txt_row('Live tail       = Real-time streaming view of incoming log events in the console'))
    lines.append(txt_row('Log sink        = Cross-account/cross-region log delivery destination for centralisation'))
    lines.append(txt_row('Export to S3    = Batch export of log data to S3; not real-time; use subscription instead'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-monitoring-eventbridge', 'docs/cloud/aws/monitoring/eventbridge/index.md', 'EventBridge — event bus, rules, and serverless event-driven automation across AWS')
def _aws_monitoring_eventbridge():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'EventBridge — Event-Driven Automation'))
    lines.append(txt_row())
    lines.append(txt_row('EventBridge routes events from AWS services, custom apps, and SaaS to processing targets.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Event Sources'), bMid(L2, R2, 'Event Bus Types'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS services: state-change events'), bMid(L2, R2, 'Default bus: all AWS service events'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom apps: PutEvents API calls'), bMid(L2, R2, 'Custom bus: app/domain isolation'))))
    lines.append(R(merge(bMid(L1, R1, 'SaaS partners: Zendesk, Datadog'), bMid(L2, R2, 'Partner bus: SaaS source events'))))
    lines.append(R(merge(bMid(L1, R1, 'Scheduled: cron/rate expressions'), bMid(L2, R2, 'Pipes: filtered point-to-point'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account: resource-based policy'), bMid(L2, R2, 'Global endpoint: multi-region HA'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Rules match event patterns and route to targets; multiple targets per rule supported.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Rules & Patterns'), bMid(L2, R2, 'Targets'))))
    lines.append(R(merge(bMid(L1, R1, 'Event pattern: JSON field matching'), bMid(L2, R2, 'Lambda: invoke function'))))
    lines.append(R(merge(bMid(L1, R1, 'Prefix/suffix/exists/anything-but'), bMid(L2, R2, 'SNS/SQS: fan-out/queue'))))
    lines.append(R(merge(bMid(L1, R1, 'Input transformer: reshape payload'), bMid(L2, R2, 'Step Functions: workflow'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: cron(0 12 * * ? *) expr'), bMid(L2, R2, 'Kinesis Firehose: stream'))))
    lines.append(R(merge(bMid(L1, R1, 'DLQ: failed delivery capture'), bMid(L2, R2, 'EventBridge bus: cross-account'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS regional EventBridge endpoints · Multi-AZ event bus infrastructure · Global backbone'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Event           = JSON document with source, detail-type, detail, and metadata fields'))
    lines.append(txt_row('Event bus       = Channel receiving events; rules attached to a bus filter and route'))
    lines.append(txt_row('Rule            = Evaluates event pattern match and routes matching events to targets'))
    lines.append(txt_row('Event pattern   = JSON filter defining which events a rule matches, field by field'))
    lines.append(txt_row('Input transformer= Modifies the event payload before delivery to the target'))
    lines.append(txt_row('Schedule        = Cron or rate expression triggering a rule on a time basis'))
    lines.append(txt_row('DLQ             = Dead-letter queue capturing events that failed target delivery'))
    lines.append(txt_row('Pipes           = Point-to-point integration with filter, enrich, and transform stages'))
    lines.append(txt_row('Partner event source= SaaS provider sending events directly to EventBridge partner bus'))
    lines.append(txt_row('Global endpoint = Two-bus active-active across two regions; automatic event replication'))
    lines.append(txt_row('PutEvents API   = SDK/CLI method to send custom events to an event bus'))
    lines.append(txt_row('detail-type     = Human-readable string classifying the event, e.g. EC2 Instance State-change'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-elb', 'docs/cloud/aws/networking/elastic-load-balancer/index.md', 'Elastic Load Balancer — ALB, NLB, and GWLB routing, listeners, and target groups')
def _aws_net_elb():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Elastic Load Balancer — ALB / NLB / GWLB'))
    lines.append(txt_row())
    lines.append(txt_row('ELB distributes inbound traffic across targets; ALB for HTTP, NLB for TCP, GWLB for appliances.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ALB (Layer 7)'), bMid(L2, R2, 'NLB (Layer 4)'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTP/HTTPS listener rules'), bMid(L2, R2, 'TCP/UDP/TLS listener'))))
    lines.append(R(merge(bMid(L1, R1, 'Path/host/header routing'), bMid(L2, R2, 'Static IP per AZ; EIP support'))))
    lines.append(R(merge(bMid(L1, R1, 'WAF integration; auth with Cognito'), bMid(L2, R2, 'Ultra-low latency; millions RPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Redirect/fixed-response actions'), bMid(L2, R2, 'Preserve source IP to targets'))))
    lines.append(R(merge(bMid(L1, R1, 'Target: instance, IP, Lambda, ALB'), bMid(L2, R2, 'Target: instance, IP, ALB'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Listeners route to target groups; health checks determine which targets receive traffic.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Target Groups'), bMid(L2, R2, 'Health & Access Logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Protocol: HTTP/HTTPS/TCP/UDP'), bMid(L2, R2, 'Health check: path, interval, codes'))))
    lines.append(R(merge(bMid(L1, R1, 'Deregistration delay: drain conns'), bMid(L2, R2, 'Access logs: S3 bucket delivery'))))
    lines.append(R(merge(bMid(L1, R1, 'Stickiness: LB or app-based cookie'), bMid(L2, R2, 'Connection logs: NLB only'))))
    lines.append(R(merge(bMid(L1, R1, 'Slow start: ramp traffic to targets'), bMid(L2, R2, 'CloudWatch metrics: RequestCount'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-zone load balancing option'), bMid(L2, R2, 'Deletion protection toggle'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS regional ELB nodes per AZ · ENI attached to VPC subnets · Global backbone'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ALB             = Application Load Balancer; Layer 7; routes on HTTP attributes'))
    lines.append(txt_row('NLB             = Network Load Balancer; Layer 4; routes on TCP/UDP/TLS'))
    lines.append(txt_row('GWLB            = Gateway Load Balancer; routes traffic through third-party appliances'))
    lines.append(txt_row('Listener        = Protocol+port entry point on the load balancer; holds routing rules'))
    lines.append(txt_row('Rule            = ALB condition + action; evaluated in priority order per listener'))
    lines.append(txt_row('Target group    = Set of registered targets with a common health check configuration'))
    lines.append(txt_row('Stickiness      = Session affinity directing a client to the same target repeatedly'))
    lines.append(txt_row('Deregistration delay= Time targets drain existing connections after deregistration'))
    lines.append(txt_row('Cross-zone LB   = Distributes requests evenly across all targets in all enabled AZs'))
    lines.append(txt_row('Access logs     = Per-request records delivered to S3: time, client, target, response'))
    lines.append(txt_row('WAF integration = ALB can enforce AWS WAF web ACL on inbound HTTP requests'))
    lines.append(txt_row('EIP on NLB      = Elastic IP assigned to NLB node per AZ; stable IP for allowlisting'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-igw', 'docs/cloud/aws/networking/internet-gateway/index.md', 'Internet Gateway — public internet connectivity for VPC subnets and Elastic IPs')
def _aws_net_igw():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Internet Gateway — VPC Internet Connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('IGW provides bidirectional internet access for public subnets; performs NAT for Elastic IPs.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'IGW Function'), bMid(L2, R2, 'Requirements for Public Access'))))
    lines.append(R(merge(bMid(L1, R1, 'Horizontally scaled; HA by design'), bMid(L2, R2, 'IGW attached to the VPC'))))
    lines.append(R(merge(bMid(L1, R1, 'No bandwidth limits or single points'), bMid(L2, R2, 'Route table: 0.0.0.0/0 → IGW'))))
    lines.append(R(merge(bMid(L1, R1, '1-to-1 NAT: EIP ↔ private IPv4'), bMid(L2, R2, 'Subnet must be marked public'))))
    lines.append(R(merge(bMid(L1, R1, 'No NAT needed for IPv6 (native)'), bMid(L2, R2, 'Instance needs EIP or auto-assign'))))
    lines.append(R(merge(bMid(L1, R1, 'Supports IPv4 and IPv6 traffic'), bMid(L2, R2, 'Security group allows inbound'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('IGW enables inbound and outbound internet; Egress-only IGW for IPv6 outbound-only traffic.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Egress-Only IGW (IPv6)'), bMid(L2, R2, 'Related Components'))))
    lines.append(R(merge(bMid(L1, R1, 'Allows IPv6 outbound from VPC'), bMid(L2, R2, 'NAT Gateway: IPv4 private subnet'))))
    lines.append(R(merge(bMid(L1, R1, 'Blocks inbound IPv6 connections'), bMid(L2, R2, 'Route tables: per-subnet control'))))
    lines.append(R(merge(bMid(L1, R1, 'No EIP needed; uses instance IPv6'), bMid(L2, R2, 'Elastic IP: static public IPv4'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach to VPC; add route table rule'), bMid(L2, R2, 'Security groups + NACLs: firewall'))))
    lines.append(R(merge(bMid(L1, R1, 'Free; no hourly/data charges'), bMid(L2, R2, 'VPC Flow Logs: traffic capture'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS edge network · Regional backbone · ENIs on VPC subnet boundary infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IGW             = Internet Gateway; horizontally scaled, redundant VPC component'))
    lines.append(txt_row('Public subnet   = Subnet whose route table has a default route (0.0.0.0/0) to an IGW'))
    lines.append(txt_row('Elastic IP      = Static public IPv4 address allocated to an AWS account'))
    lines.append(txt_row('1-to-1 NAT      = IGW translates EIP ↔ private IPv4 for inbound and outbound traffic'))
    lines.append(txt_row('Egress-only IGW = IPv6-only gateway allowing outbound but blocking inbound connections'))
    lines.append(txt_row('Default route   = 0.0.0.0/0 or ::/0 route pointing to IGW for internet-bound traffic'))
    lines.append(txt_row('Attached state  = IGW must be in attached state to the VPC for traffic to flow'))
    lines.append(txt_row('Auto-assign IP  = Subnet setting that gives instances a public IP at launch from pool'))
    lines.append(txt_row('IPv6 native     = No NAT needed; instances get globally routable /128 IPv6 address'))
    lines.append(txt_row('VPC routing     = Route table entries direct traffic; longest prefix match decides'))
    lines.append(txt_row('NAT Gateway     = Managed service for private subnet IPv4 outbound; not the IGW itself'))
    lines.append(txt_row('HA design       = Single IGW is HA; do not run multiple IGWs for redundancy'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-nat', 'docs/cloud/aws/networking/nat-gateway/index.md', 'NAT Gateway — managed outbound internet access for private subnet workloads')
def _aws_net_nat():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NAT Gateway — Private Subnet Outbound Access'))
    lines.append(txt_row())
    lines.append(txt_row('NAT Gateway enables private subnet instances to reach the internet without being reachable.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NAT Gateway Types'), bMid(L2, R2, 'Traffic Flow'))))
    lines.append(R(merge(bMid(L1, R1, 'Public: EIP, routes via IGW'), bMid(L2, R2, 'Private subnet → route table'))))
    lines.append(R(merge(bMid(L1, R1, 'Private: VPC-to-VPC routing only'), bMid(L2, R2, 'Route: 0.0.0.0/0 → NAT GW'))))
    lines.append(R(merge(bMid(L1, R1, 'Managed: HA within one AZ'), bMid(L2, R2, 'NAT GW → IGW → internet'))))
    lines.append(R(merge(bMid(L1, R1, 'Up to 100 Gbps; 55,000 conns/host'), bMid(L2, R2, 'Response: IGW → NAT GW → instance'))))
    lines.append(R(merge(bMid(L1, R1, 'No port 25 (SMTP) allowed'), bMid(L2, R2, 'Inbound blocked: no unsolicited'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Deploy one NAT Gateway per AZ; route each AZ private subnet to its own NAT GW for HA.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'HA Pattern'), bMid(L2, R2, 'Costs'))))
    lines.append(R(merge(bMid(L1, R1, 'One NAT GW per AZ (3 for 3 AZs)'), bMid(L2, R2, 'Hourly charge per NAT GW'))))
    lines.append(R(merge(bMid(L1, R1, 'Each AZ private route → local NAT'), bMid(L2, R2, 'Data processing fee per GB'))))
    lines.append(R(merge(bMid(L1, R1, 'AZ failure: other AZs unaffected'), bMid(L2, R2, 'Data transfer out: standard rates'))))
    lines.append(R(merge(bMid(L1, R1, 'No cross-AZ NAT GW sharing (cost)'), bMid(L2, R2, 'Private NAT: no data transfer fee'))))
    lines.append(R(merge(bMid(L1, R1, 'NAT instance: cheaper but manual HA'), bMid(L2, R2, 'Consider VPC endpoints to reduce'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS managed network infrastructure per AZ · Elastic IP from AWS pool · Regional backbone'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Public NAT GW   = NAT Gateway with an EIP; routes outbound through IGW to internet'))
    lines.append(txt_row('Private NAT GW  = NAT Gateway without EIP; used for private VPC-to-VPC routing'))
    lines.append(txt_row('SNAT            = Source NAT; replaces instance private IP with NAT GW EIP'))
    lines.append(txt_row('Connection tracking= NAT GW maintains state table mapping flows to return traffic'))
    lines.append(txt_row('Idle timeout    = NAT GW drops TCP connections idle for 350 seconds'))
    lines.append(txt_row('Port exhaustion = >55,000 simultaneous connections to same dest IP:port causes drops'))
    lines.append(txt_row('NAT instance    = EC2-based alternative; user-managed; cheaper but no built-in HA'))
    lines.append(txt_row('Private subnet  = Subnet with no IGW route; relies on NAT GW for internet access'))
    lines.append(txt_row('AZ isolation    = Each AZ should have its own NAT GW for fault isolation'))
    lines.append(txt_row('VPC endpoint    = Alternative to NAT for AWS service access; no internet required'))
    lines.append(txt_row('Bandwidth limit = 100 Gbps max throughput; scales automatically up to limit'))
    lines.append(txt_row('Data processing = Per-GB charge applies for all traffic passing through NAT Gateway'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-nacls', 'docs/cloud/aws/networking/network-acls/index.md', 'Network ACLs — stateless subnet-level firewall rules for VPC traffic control')
def _aws_net_nacls():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Network ACLs — Stateless Subnet Firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Network ACLs provide stateless subnet-level traffic filtering; processed in rule-number order.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NACL Characteristics'), bMid(L2, R2, 'Rule Structure'))))
    lines.append(R(merge(bMid(L1, R1, 'Stateless: return traffic needs rule'), bMid(L2, R2, 'Rule number: 1–32766 (lower first)'))))
    lines.append(R(merge(bMid(L1, R1, 'Applies to whole subnet (not instance)'), bMid(L2, R2, 'Protocol: TCP/UDP/ICMP/All'))))
    lines.append(R(merge(bMid(L1, R1, 'Default NACL: allow all in and out'), bMid(L2, R2, 'Port range: single or range'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom NACL: deny all by default'), bMid(L2, R2, 'Source/dest CIDR'))))
    lines.append(R(merge(bMid(L1, R1, 'One NACL per subnet; reusable'), bMid(L2, R2, 'Action: Allow or Deny'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('NACLs evaluate each packet independently; security groups track connection state instead.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Common Use Patterns'), bMid(L2, R2, 'NACL vs Security Group'))))
    lines.append(R(merge(bMid(L1, R1, 'Block specific IPs across all VMs'), bMid(L2, R2, 'NACL: subnet boundary; stateless'))))
    lines.append(R(merge(bMid(L1, R1, 'Ephemeral return ports: 1024–65535'), bMid(L2, R2, 'SG: instance boundary; stateful'))))
    lines.append(R(merge(bMid(L1, R1, 'Explicit deny before wildcard allow'), bMid(L2, R2, 'Use both for defence in depth'))))
    lines.append(R(merge(bMid(L1, R1, 'Inbound + matching outbound rules'), bMid(L2, R2, 'NACL cannot reference SG by ID'))))
    lines.append(R(merge(bMid(L1, R1, 'Low rule numbers: highest priority'), bMid(L2, R2, 'SG: no explicit deny; default deny'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS VPC data plane · Hypervisor-enforced packet filtering at subnet boundary'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Stateless       = Each packet evaluated independently; no connection state tracked'))
    lines.append(txt_row('Rule number     = Lower numbers processed first; first match terminates evaluation'))
    lines.append(txt_row('* rule          = Implicit deny-all catch-all at the end; cannot be removed'))
    lines.append(txt_row('Ephemeral ports = 1024–65535; required in outbound rules for TCP response traffic'))
    lines.append(txt_row('Inbound rules   = Filter traffic entering the subnet from outside'))
    lines.append(txt_row('Outbound rules  = Filter traffic leaving the subnet; needed for return traffic'))
    lines.append(txt_row('Default NACL    = VPC-default NACL allows all inbound and outbound traffic'))
    lines.append(txt_row('Custom NACL     = New NACL denies all traffic until rules are explicitly added'))
    lines.append(txt_row('CIDR block      = IP address range in NACL rule; can be /32 for a single IP'))
    lines.append(txt_row('Subnet association= A subnet can only be associated with one NACL at a time'))
    lines.append(txt_row('Defence in depth= Use NACLs + security groups together for layered network security'))
    lines.append(txt_row('Allow before deny= Implicit deny; explicit allow rules required for desired traffic'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-route53', 'docs/cloud/aws/networking/route-53/index.md', 'Route 53 — DNS hosting, routing policies, health checks, and private hosted zones')
def _aws_net_route53():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Route 53 — DNS & Traffic Routing'))
    lines.append(txt_row())
    lines.append(txt_row('Route 53 provides authoritative DNS, health checks, and intelligent traffic routing policies.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Hosted Zones'), bMid(L2, R2, 'Record Types'))))
    lines.append(R(merge(bMid(L1, R1, 'Public: authoritative for internet'), bMid(L2, R2, 'A: IPv4 address'))))
    lines.append(R(merge(bMid(L1, R1, 'Private: VPC-internal resolution'), bMid(L2, R2, 'AAAA: IPv6 address'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone delegation: NS records'), bMid(L2, R2, 'CNAME: canonical name alias'))))
    lines.append(R(merge(bMid(L1, R1, 'DNSSEC: signing for public zones'), bMid(L2, R2, 'Alias: AWS resource pointer'))))
    lines.append(R(merge(bMid(L1, R1, 'Transfer lock: prevent hijacking'), bMid(L2, R2, 'MX/TXT/SRV/CAA record types'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Routing policies control how Route 53 responds; health checks remove unhealthy endpoints.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Routing Policies'), bMid(L2, R2, 'Health Checks'))))
    lines.append(R(merge(bMid(L1, R1, 'Simple: single value returned'), bMid(L2, R2, 'Endpoint: HTTP/HTTPS/TCP check'))))
    lines.append(R(merge(bMid(L1, R1, 'Weighted: percentage split'), bMid(L2, R2, 'Calculated: combine child checks'))))
    lines.append(R(merge(bMid(L1, R1, 'Failover: primary/secondary pair'), bMid(L2, R2, 'CloudWatch alarm: metric-based'))))
    lines.append(R(merge(bMid(L1, R1, 'Latency: lowest latency region'), bMid(L2, R2, 'Interval: 30s or 10s fast'))))
    lines.append(R(merge(bMid(L1, R1, 'Geolocation/Geoproximity routing'), bMid(L2, R2, 'SNS alert on health state change'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('100+ globally distributed Route 53 edge locations · Anycast IP infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Hosted zone     = Container for DNS records for a domain; public or private scoped'))
    lines.append(txt_row('Alias record    = Route 53 extension mapping a DNS name to an AWS resource endpoint'))
    lines.append(txt_row('TTL             = Time-to-live; how long resolvers cache a DNS response in seconds'))
    lines.append(txt_row('Weighted policy = Splits traffic by weight ratio, e.g. 70/30 for canary deployments'))
    lines.append(txt_row('Failover policy = Routes to primary; falls back to secondary when health check fails'))
    lines.append(txt_row('Latency policy  = Routes to AWS region with lowest latency for the client'))
    lines.append(txt_row('Geolocation     = Routes based on geographic location of the requesting resolver'))
    lines.append(txt_row('Geoproximity    = Routes based on distance; bias shifts boundary toward a region'))
    lines.append(txt_row('Private zone    = Hosted zone that resolves only within associated VPCs'))
    lines.append(txt_row('DNSSEC          = Signs zone records; resolvers validate signature chain to root'))
    lines.append(txt_row('Health check    = Route 53 probe; removes unhealthy endpoints from DNS responses'))
    lines.append(txt_row('Resolver        = Inbound/outbound endpoints for hybrid DNS query forwarding'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-route-tables', 'docs/cloud/aws/networking/route-tables/index.md', 'Route Tables — VPC routing rules, subnet associations, and inter-VPC traffic paths')
def _aws_net_route_tables():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Route Tables — VPC Traffic Routing'))
    lines.append(txt_row())
    lines.append(txt_row('Route tables control how traffic is directed within a VPC; each subnet has one route table.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Route Table Types'), bMid(L2, R2, 'Route Entry Targets'))))
    lines.append(R(merge(bMid(L1, R1, 'Main: default for unassociated subnets'), bMid(L2, R2, 'Internet Gateway: public internet'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom: explicit subnet association'), bMid(L2, R2, 'NAT Gateway: private outbound'))))
    lines.append(R(merge(bMid(L1, R1, 'Gateway: edge routing for IGW/VGW'), bMid(L2, R2, 'TGW: transit gateway routing'))))
    lines.append(R(merge(bMid(L1, R1, 'Local: VPC CIDR always present'), bMid(L2, R2, 'VPC Peering: peer VPC CIDR'))))
    lines.append(R(merge(bMid(L1, R1, 'One route table per subnet max'), bMid(L2, R2, 'Virtual Private Gateway: VPN/DX'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Longest prefix match determines which route applies; local VPC route cannot be deleted.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Common Patterns'), bMid(L2, R2, 'Route Propagation'))))
    lines.append(R(merge(bMid(L1, R1, 'Public subnet: 0.0.0.0/0 → IGW'), bMid(L2, R2, 'VGW propagation: VPN BGP routes'))))
    lines.append(R(merge(bMid(L1, R1, 'Private subnet: 0.0.0.0/0 → NAT'), bMid(L2, R2, 'TGW route tables: segment traffic'))))
    lines.append(R(merge(bMid(L1, R1, 'On-prem: 10.0.0.0/8 → VGW or TGW'), bMid(L2, R2, 'Blackhole: drop matching traffic'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC peering: specific peer CIDRs'), bMid(L2, R2, 'Active routes: propagated + static'))))
    lines.append(R(merge(bMid(L1, R1, 'Middlebox: route via appliance ENI'), bMid(L2, R2, 'Edge RT: service insertion at IGW'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS VPC hypervisor routing fabric · Transit Gateway physical nodes per region'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Route table     = Set of rules (routes) that determine where network traffic is directed'))
    lines.append(txt_row('Local route     = VPC CIDR route always present; allows inter-subnet communication'))
    lines.append(txt_row('Main route table= Default table applied to subnets not explicitly associated elsewhere'))
    lines.append(txt_row('Gateway RT      = Special route table associated with IGW or VGW for edge routing'))
    lines.append(txt_row('Longest prefix  = Most specific matching route wins; /32 beats /24 beats /0'))
    lines.append(txt_row('Route propagation= VGW or TGW automatically populates routes from BGP advertisements'))
    lines.append(txt_row('Blackhole route = Route pointing to a deleted or non-existent target; drops traffic'))
    lines.append(txt_row('Middlebox route = Traffic directed through a network appliance ENI for inspection'))
    lines.append(txt_row('TGW route table = Transit Gateway has its own route tables separate from VPC tables'))
    lines.append(txt_row('VGW             = Virtual Private Gateway; attachment point for VPN and Direct Connect'))
    lines.append(txt_row('Active route    = Route in active use; a route can be static or propagated'))
    lines.append(txt_row('Subnet association= Linking a subnet to a specific route table; overrides main table'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-security-groups', 'docs/cloud/aws/networking/security-groups/index.md', 'Security Groups — stateful instance-level firewall rules for EC2 and other resources')
def _aws_net_security_groups():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Security Groups — Stateful Instance Firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Security groups act as virtual firewalls for ENIs; stateful — return traffic is automatic.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Security Group Characteristics'), bMid(L2, R2, 'Rule Structure'))))
    lines.append(R(merge(bMid(L1, R1, 'Stateful: return traffic auto-allowed'), bMid(L2, R2, 'Protocol: TCP/UDP/ICMP/All'))))
    lines.append(R(merge(bMid(L1, R1, 'Allow rules only; no explicit deny'), bMid(L2, R2, 'Port or port range'))))
    lines.append(R(merge(bMid(L1, R1, 'Applied to ENI; multiple per ENI'), bMid(L2, R2, 'Source/dest: CIDR or SG reference'))))
    lines.append(R(merge(bMid(L1, R1, 'All rules evaluated (no ordering)'), bMid(L2, R2, 'Description field per rule'))))
    lines.append(R(merge(bMid(L1, R1, 'Default SG: allows all within group'), bMid(L2, R2, 'Inbound and outbound rule sets'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Reference another SG as source/dest to allow traffic between grouped resources.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Best Practices'), bMid(L2, R2, 'Common Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'Least privilege: minimal open ports'), bMid(L2, R2, 'Web tier SG: 443 from 0.0.0.0/0'))))
    lines.append(R(merge(bMid(L1, R1, 'SG reference instead of CIDR ranges'), bMid(L2, R2, 'App SG: port from web SG only'))))
    lines.append(R(merge(bMid(L1, R1, 'Prefix lists: managed CIDR sets'), bMid(L2, R2, 'DB SG: 5432 from app SG only'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag SGs: team, environment, purpose'), bMid(L2, R2, 'Bastion SG: 22 from corp CIDR'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit via Config rule: open rules'), bMid(L2, R2, 'ELB SG: source ALB SG to targets'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS hypervisor network layer · ENI-level enforcement per EC2 host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Security group  = Stateful virtual firewall applied to one or more ENIs'))
    lines.append(txt_row('ENI             = Elastic Network Interface; SGs attach here, not to instances directly'))
    lines.append(txt_row('Stateful        = Connection tracking; return packets allowed without explicit outbound rule'))
    lines.append(txt_row('Allow-only      = SGs have no deny rules; absence of allow = implicit deny'))
    lines.append(txt_row('SG reference    = Rule source/dest is another SG ID; allows dynamic group membership'))
    lines.append(txt_row('Default SG      = Created with each VPC; allows all inbound from same SG'))
    lines.append(txt_row('Prefix list     = Named collection of CIDRs usable as SG rule source/destination'))
    lines.append(txt_row('Rule evaluation = All rules processed; most permissive allow wins (no ordering)'))
    lines.append(txt_row('Chained SGs     = Web → app → DB using SG references creates least-privilege tiers'))
    lines.append(txt_row('Max per ENI     = Default 5 SGs per ENI; up to 16 with limit increase'))
    lines.append(txt_row('Inbound default = New custom SG has no inbound rules; all inbound denied'))
    lines.append(txt_row('Outbound default= New custom SG allows all outbound; restrict for compliance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-subnets', 'docs/cloud/aws/networking/subnets/index.md', 'Subnets — VPC subnet design, AZ placement, CIDR sizing, and public vs private')
def _aws_net_subnets():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Subnets — VPC Subnet Design'))
    lines.append(txt_row())
    lines.append(txt_row('Subnets divide a VPC CIDR into segments per AZ; public or private determined by route table.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Subnet Characteristics'), bMid(L2, R2, 'Reserved IPs (per subnet)'))))
    lines.append(R(merge(bMid(L1, R1, 'Single AZ scope; no multi-AZ subnet'), bMid(L2, R2, '.0 — network address'))))
    lines.append(R(merge(bMid(L1, R1, 'CIDR sub-block of the VPC CIDR'), bMid(L2, R2, '.1 — VPC router'))))
    lines.append(R(merge(bMid(L1, R1, 'Minimum /28 (11 usable IPs)'), bMid(L2, R2, '.2 — Route 53 DNS resolver'))))
    lines.append(R(merge(bMid(L1, R1, 'No overlapping CIDRs within VPC'), bMid(L2, R2, '.3 — future use'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-assign public IP option'), bMid(L2, R2, '.255 — broadcast (unusable)'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Public vs private determined by route table; public has IGW default route; private uses NAT.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Tier Design Pattern'), bMid(L2, R2, 'CIDR Sizing Guidance'))))
    lines.append(R(merge(bMid(L1, R1, 'Public tier: ALB, NAT GW, bastion'), bMid(L2, R2, 'Large app: /20 (4091 usable)'))))
    lines.append(R(merge(bMid(L1, R1, 'App tier: EC2, ECS, Lambda ENIs'), bMid(L2, R2, 'Medium: /22 (1019 usable)'))))
    lines.append(R(merge(bMid(L1, R1, 'Data tier: RDS, ElastiCache, MSK'), bMid(L2, R2, 'Small: /24 (251 usable)'))))
    lines.append(R(merge(bMid(L1, R1, 'Isolated: sensitive/restricted hosts'), bMid(L2, R2, 'Lambda: /28 (11 minimum)'))))
    lines.append(R(merge(bMid(L1, R1, 'Replicate tier pattern across AZs'), bMid(L2, R2, 'Always plan for Lambda ENI growth'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS AZ physical data centres · VPC fabric per region · Hypervisor network partitioning'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Subnet          = IPv4/IPv6 range within a VPC tied to one Availability Zone'))
    lines.append(txt_row('Public subnet   = Subnet whose default route points to an Internet Gateway'))
    lines.append(txt_row('Private subnet  = Subnet with no IGW route; outbound via NAT GW or VPC endpoints'))
    lines.append(txt_row('Reserved IPs    = AWS reserves 5 IPs per subnet; usable = 2^(32-prefix) - 5'))
    lines.append(txt_row('CIDR            = Classless Inter-Domain Routing; defines the IP range of the subnet'))
    lines.append(txt_row('AZ affinity     = Resources in a subnet run in the same physical AZ'))
    lines.append(txt_row('Auto-assign IP  = Subnet setting giving EC2 instances a public IP at launch'))
    lines.append(txt_row('Subnet CIDR     = Must not overlap other subnets or secondary VPC CIDRs'))
    lines.append(txt_row('Lambda ENI      = Lambda in VPC creates ENI in each AZ subnet; plan capacity'))
    lines.append(txt_row('/16 VPC         = Max VPC size; provides 65,536 IPs to sub-allocate into subnets'))
    lines.append(txt_row('Tier isolation  = Place each app tier in separate subnets for NACL-level segmentation'))
    lines.append(txt_row('Multi-AZ design = Create same-purpose subnets in 2–3 AZs for high availability'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-vpc', 'docs/cloud/aws/networking/vpc/index.md', 'VPC — Virtual Private Cloud architecture, CIDR design, and network topology')
def _aws_net_vpc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VPC — Virtual Private Cloud'))
    lines.append(txt_row())
    lines.append(txt_row('VPC is an isolated virtual network within AWS; you control CIDR, subnets, and routing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VPC Core Components'), bMid(L2, R2, 'Connectivity Options'))))
    lines.append(R(merge(bMid(L1, R1, 'CIDR block: /16 to /28 IPv4 range'), bMid(L2, R2, 'Internet Gateway: public access'))))
    lines.append(R(merge(bMid(L1, R1, 'Subnets: per-AZ CIDR sub-blocks'), bMid(L2, R2, 'NAT Gateway: private outbound'))))
    lines.append(R(merge(bMid(L1, R1, 'Route tables: traffic direction'), bMid(L2, R2, 'VPC Peering: direct VPC link'))))
    lines.append(R(merge(bMid(L1, R1, 'Security groups: stateful firewall'), bMid(L2, R2, 'Transit Gateway: hub-spoke'))))
    lines.append(R(merge(bMid(L1, R1, 'NACLs: stateless subnet firewall'), bMid(L2, R2, 'DirectConnect/VPN: on-prem'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Multi-AZ design with public + private + data tiers; TGW for cross-account connectivity.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VPC Design Decisions'), bMid(L2, R2, 'Default VPC'))))
    lines.append(R(merge(bMid(L1, R1, 'RFC1918 CIDR: avoid prod overlap'), bMid(L2, R2, 'Auto-created in every region'))))
    lines.append(R(merge(bMid(L1, R1, 'Secondary CIDR: expand if exhausted'), bMid(L2, R2, '/16 CIDR; public subnets per AZ'))))
    lines.append(R(merge(bMid(L1, R1, 'Enable DNS hostnames + resolution'), bMid(L2, R2, 'IGW attached; auto-assign IP on'))))
    lines.append(R(merge(bMid(L1, R1, 'Flow logs: capture all traffic'), bMid(L2, R2, 'Do not use for prod workloads'))))
    lines.append(R(merge(bMid(L1, R1, 'Shared VPC: RAM for multi-account'), bMid(L2, R2, 'Recreate if accidentally deleted'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS regional network fabric · Multiple physical AZ data centres · Global backbone'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VPC             = Logically isolated section of AWS cloud with its own network configuration'))
    lines.append(txt_row('CIDR block      = IP range for the VPC; primary + optional secondary blocks'))
    lines.append(txt_row('Tenancy         = Default (shared hardware) or dedicated (single-tenant physical host)'))
    lines.append(txt_row('DNS resolution  = VPC attribute enabling DNS queries to route through Route 53 resolver'))
    lines.append(txt_row('DNS hostnames   = VPC attribute giving instances public DNS names for their public IPs'))
    lines.append(txt_row('Secondary CIDR  = Additional CIDR block added to expand VPC IP address space'))
    lines.append(txt_row('Shared VPC      = VPC owned by one account; subnets shared to others via RAM'))
    lines.append(txt_row('VPC Peering     = Private routing between two VPCs; no TGW required; no transitive'))
    lines.append(txt_row('Transit Gateway = Regional hub connecting many VPCs and on-prem; supports transitive'))
    lines.append(txt_row('Default VPC     = AWS-created VPC in every region; do not use for production'))
    lines.append(txt_row('Flow Logs       = VPC-level capture of accept/reject traffic for network analysis'))
    lines.append(txt_row('RFC1918         = Private address ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-vpc-endpoints', 'docs/cloud/aws/networking/vpc-endpoints/index.md', 'VPC Endpoints — private connectivity to AWS services without internet traversal')
def _aws_net_vpc_endpoints():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VPC Endpoints — Private AWS Service Access'))
    lines.append(txt_row())
    lines.append(txt_row('VPC Endpoints connect your VPC to AWS services privately without NAT, IGW, or internet.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Gateway Endpoints'), bMid(L2, R2, 'Interface Endpoints (PrivateLink)'))))
    lines.append(R(merge(bMid(L1, R1, 'Services: S3 and DynamoDB only'), bMid(L2, R2, 'Services: most AWS APIs'))))
    lines.append(R(merge(bMid(L1, R1, 'Route table entry: no ENI created'), bMid(L2, R2, 'ENI in subnet: private IP'))))
    lines.append(R(merge(bMid(L1, R1, 'No cost: free to use'), bMid(L2, R2, 'Hourly + data processing fee'))))
    lines.append(R(merge(bMid(L1, R1, 'Policy: restrict bucket/table access'), bMid(L2, R2, 'Policy: restrict API actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Regional; DNS unchanged for S3'), bMid(L2, R2, 'Private DNS: resolve to ENI IP'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Interface endpoints use PrivateLink; traffic stays on AWS backbone; no public internet hop.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Endpoint Policies'), bMid(L2, R2, 'Use Cases'))))
    lines.append(R(merge(bMid(L1, R1, 'JSON resource policy on endpoint'), bMid(L2, R2, 'Private Lambda → S3 no NAT'))))
    lines.append(R(merge(bMid(L1, R1, 'Restrict: specific S3 buckets only'), bMid(L2, R2, 'EC2 → SSM without internet'))))
    lines.append(R(merge(bMid(L1, R1, 'Condition: aws:SourceVpc check'), bMid(L2, R2, 'Compliance: no internet egress'))))
    lines.append(R(merge(bMid(L1, R1, 'Combine with SCP to enforce use'), bMid(L2, R2, 'Reduce NAT GW data costs'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: CloudTrail endpoint events'), bMid(L2, R2, 'Cross-account via shared endpoint'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS internal backbone · PrivateLink infrastructure per AZ · Regional service endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Gateway endpoint= Route-table-based endpoint for S3 and DynamoDB; free; regional'))
    lines.append(txt_row('Interface endpoint= ENI-based PrivateLink endpoint for most AWS services; has ENI IP'))
    lines.append(txt_row('PrivateLink      = AWS technology powering interface endpoints over internal backbone'))
    lines.append(txt_row('Private DNS      = Endpoint option that resolves service FQDN to private ENI IP'))
    lines.append(txt_row('Endpoint policy  = IAM resource policy on the endpoint restricting allowed actions'))
    lines.append(txt_row('aws:SourceVpc    = Condition key used in bucket policies to enforce endpoint usage'))
    lines.append(txt_row('S3 bucket policy = Deny s3:* unless aws:SourceVpc matches your VPC endpoint'))
    lines.append(txt_row('Endpoint SG      = Security group on interface endpoint ENI controlling access'))
    lines.append(txt_row('Cross-account    = Interface endpoint can be shared to other accounts via RAM'))
    lines.append(txt_row('Cost benefit     = Eliminates NAT GW data processing fee for S3/DynamoDB traffic'))
    lines.append(txt_row('SSM endpoint     = ssm, ssmmessages, ec2messages endpoints needed for Session Manager'))
    lines.append(txt_row('Endpoint DNS     = Regional + AZ-specific DNS names provided by interface endpoints'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-net-vpc-flow-logs', 'docs/cloud/aws/networking/vpc-flow-logs/index.md', 'VPC Flow Logs — network traffic capture, analysis, and security investigation')
def _aws_net_vpc_flow_logs():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VPC Flow Logs — Network Traffic Capture'))
    lines.append(txt_row())
    lines.append(txt_row('VPC Flow Logs capture metadata about IP traffic to/from ENIs for security and troubleshooting.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Capture Scope'), bMid(L2, R2, 'Log Record Fields'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC level: all ENIs in VPC'), bMid(L2, R2, 'srcaddr, dstaddr: IP addresses'))))
    lines.append(R(merge(bMid(L1, R1, 'Subnet level: all ENIs in subnet'), bMid(L2, R2, 'srcport, dstport: port numbers'))))
    lines.append(R(merge(bMid(L1, R1, 'ENI level: specific interface'), bMid(L2, R2, 'protocol: 6=TCP 17=UDP 1=ICMP'))))
    lines.append(R(merge(bMid(L1, R1, 'Accepted, rejected, or all traffic'), bMid(L2, R2, 'action: ACCEPT or REJECT'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom fields: add/remove columns'), bMid(L2, R2, 'bytes, packets: volume metrics'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Flow logs delivered to S3 or CloudWatch Logs; query with Athena or Logs Insights.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Destinations'), bMid(L2, R2, 'Analysis Use Cases'))))
    lines.append(R(merge(bMid(L1, R1, 'S3: Athena queries; Parquet format'), bMid(L2, R2, 'Security: detect port scans'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudWatch Logs: Insights queries'), bMid(L2, R2, 'Compliance: audit traffic patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'Kinesis Firehose: real-time stream'), bMid(L2, R2, 'Troubleshoot: find rejected traffic'))))
    lines.append(R(merge(bMid(L1, R1, 'Aggregation interval: 1 or 10 min'), bMid(L2, R2, 'Optimize: identify top talkers'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account S3 delivery supported'), bMid(L2, R2, 'GuardDuty: uses flow logs input'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS VPC data plane capture agents · S3/CloudWatch Logs storage infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Flow log record = Single aggregated capture of a traffic flow over the interval'))
    lines.append(txt_row('Aggregation interval= 1 or 10 minutes; shorter captures flows faster but costs more'))
    lines.append(txt_row('action field    = ACCEPT = SG+NACL allowed; REJECT = SG or NACL denied the flow'))
    lines.append(txt_row('NODATA          = No traffic was recorded during the aggregation interval'))
    lines.append(txt_row('SKIPDATA        = Capacity constraints skipped some records during the interval'))
    lines.append(txt_row('Custom format   = Choose which fields to include; reduces storage cost'))
    lines.append(txt_row('Parquet format  = Columnar S3 delivery; faster Athena queries and lower scan cost'))
    lines.append(txt_row('Athena query    = SQL against S3 flow logs via Glue table; pay per TB scanned'))
    lines.append(txt_row('GuardDuty input = GuardDuty ingests flow logs to detect anomalous traffic patterns'))
    lines.append(txt_row('Not real-time   = Flow logs are near-real-time; not suitable for live blocking'))
    lines.append(txt_row('Cost            = Charged for data ingestion; S3 cheaper than CloudWatch Logs'))
    lines.append(txt_row('IAM role        = Required to grant VPC Flow Logs permission to deliver records'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-ops-backup-restore', 'docs/cloud/aws/operations/backup-restore/index.md', 'AWS operations backup and restore procedures — snapshot workflows and recovery')
def _aws_ops_backup_restore():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Operations — Backup & Restore Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Operational backup and restore procedures covering EC2, RDS, EBS, and S3 workflows.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Backup Procedures'), bMid(L2, R2, 'Restore Procedures'))))
    lines.append(R(merge(bMid(L1, R1, 'EBS: create snapshot via console/CLI'), bMid(L2, R2, 'EBS: restore snapshot to new volume'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: automated + manual snapshots'), bMid(L2, R2, 'RDS: restore to point-in-time'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2 AMI: image from running instance'), bMid(L2, R2, 'EC2: launch from AMI'))))
    lines.append(R(merge(bMid(L1, R1, 'S3: versioning + replication policy'), bMid(L2, R2, 'S3: restore previous version'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS Backup: vault + plan schedule'), bMid(L2, R2, 'Backup: restore job from vault'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Verify restore procedures regularly; test AMI launches and RDS PITR in non-prod accounts.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Operational Checks'), bMid(L2, R2, 'Automation'))))
    lines.append(R(merge(bMid(L1, R1, 'Verify snapshot completion status'), bMid(L2, R2, 'AWS Backup plan: cron schedule'))))
    lines.append(R(merge(bMid(L1, R1, 'Check cross-region copy completion'), bMid(L2, R2, 'Lambda: custom snapshot scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Validate retention policy compliance'), bMid(L2, R2, 'EventBridge: trigger on schedule'))))
    lines.append(R(merge(bMid(L1, R1, 'Test restore RTO: measure duration'), bMid(L2, R2, 'SNS: notify on job success/fail'))))
    lines.append(R(merge(bMid(L1, R1, 'Review cost of snapshot storage'), bMid(L2, R2, 'Lifecycle: auto-expire old snaps'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS S3 snapshot storage · Cross-region replication infrastructure · Regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EBS snapshot    = Point-in-time copy of an EBS volume stored durably in S3'))
    lines.append(txt_row('AMI             = Amazon Machine Image; snapshot + metadata needed to launch EC2'))
    lines.append(txt_row('RDS snapshot    = Database-level backup; automated (daily) or manual on demand'))
    lines.append(txt_row('PITR            = Point-in-time recovery; RDS/DynamoDB restore to any second in window'))
    lines.append(txt_row('AWS Backup vault= Encrypted container for backup recovery points with access policy'))
    lines.append(txt_row('Recovery point  = A backup copy stored in a vault; has expiry and lifecycle rules'))
    lines.append(txt_row('Cross-region copy= Backup rule that replicates snapshots to another region'))
    lines.append(txt_row('RTO             = Recovery time objective; target time to restore from backup'))
    lines.append(txt_row('RPO             = Recovery point objective; maximum acceptable data loss window'))
    lines.append(txt_row('Restore job     = AWS Backup task that re-creates a resource from a recovery point'))
    lines.append(txt_row('Snapshot lifecycle= Policy that transitions or deletes snapshots after N days'))
    lines.append(txt_row('Incremental snapshot= After first full, EBS snapshots store only changed blocks'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-ops-cli-reference', 'docs/cloud/aws/operations/cli-reference/index.md', 'AWS operations CLI reference — common operational commands and output formats')
def _aws_ops_cli_reference():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Operations — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('Common AWS CLI operational commands for day-to-day management and scripting.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity & Config'), bMid(L2, R2, 'Output & Filtering'))))
    lines.append(R(merge(bMid(L1, R1, 'aws sts get-caller-identity'), bMid(L2, R2, '--output json/text/table/yaml'))))
    lines.append(R(merge(bMid(L1, R1, 'aws configure list-profiles'), bMid(L2, R2, '--query JMESPath expression'))))
    lines.append(R(merge(bMid(L1, R1, 'aws configure set/get region'), bMid(L2, R2, '--filter Name=Value pairs'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS_PROFILE env var override'), bMid(L2, R2, '--no-cli-pager: disable pager'))))
    lines.append(R(merge(bMid(L1, R1, 'aws sso login --profile name'), bMid(L2, R2, 'jq: JSON post-processing tool'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Use --dry-run for EC2 permission checks; --no-paginate for full result sets.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Operational Commands'), bMid(L2, R2, 'Scripting Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'aws ec2 describe-instances'), bMid(L2, R2, 'for loop over aws ... output text'))))
    lines.append(R(merge(bMid(L1, R1, 'aws s3 sync src/ s3://bucket/'), bMid(L2, R2, 'aws ... wait instance-running'))))
    lines.append(R(merge(bMid(L1, R1, 'aws logs tail /group --follow'), bMid(L2, R2, 'aws ... --no-paginate | jq'))))
    lines.append(R(merge(bMid(L1, R1, 'aws cloudformation deploy ...'), bMid(L2, R2, 'AWS_DEFAULT_REGION override'))))
    lines.append(R(merge(bMid(L1, R1, 'aws ssm start-session --target'), bMid(L2, R2, 'set -e + trap for error handling'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS CLI calls regional API endpoints · TLS 1.2+ over internet or private link'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AWS CLI         = Command-line interface tool for all AWS service operations'))
    lines.append(txt_row('Profile         = Named credential set in ~/.aws/credentials + ~/.aws/config'))
    lines.append(txt_row('JMESPath        = Query language used with --query to filter/transform CLI output'))
    lines.append(txt_row('--dry-run       = EC2 flag that checks permissions without executing the action'))
    lines.append(txt_row('wait command    = CLI blocks until a resource reaches a target state (polling)'))
    lines.append(txt_row('--no-paginate   = Returns all results at once instead of paginating the output'))
    lines.append(txt_row('AWS_PROFILE     = Env var selecting the named credential profile for CLI calls'))
    lines.append(txt_row('AWS_DEFAULT_REGION= Env var overriding the configured region for CLI commands'))
    lines.append(txt_row('SSO login       = aws sso login authenticates browser-based before CLI commands'))
    lines.append(txt_row('get-caller-identity= Returns AccountId, UserId, and ARN of current credentials'))
    lines.append(txt_row('aws s3 sync     = Copies changed/new files between local and S3 (one-way)'))
    lines.append(txt_row('Session Manager = aws ssm start-session; interactive shell without SSH or bastion'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-ops-health-checks', 'docs/cloud/aws/operations/health-checks/index.md', 'AWS operational health checks — service, instance, and application health verification')
def _aws_ops_health_checks():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Operations — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Health verification procedures for EC2 instances, load balancers, RDS, and services.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'EC2 Health Checks'), bMid(L2, R2, 'ELB Health Checks'))))
    lines.append(R(merge(bMid(L1, R1, 'System status: hardware + network'), bMid(L2, R2, 'HTTP path + expected status code'))))
    lines.append(R(merge(bMid(L1, R1, 'Instance status: OS + software'), bMid(L2, R2, 'Interval: 5s or 30s (ALB/NLB)'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-recovery on system check fail'), bMid(L2, R2, 'Healthy threshold: N consecutive'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudWatch: StatusCheckFailed alarm'), bMid(L2, R2, 'Unhealthy: removed from rotation'))))
    lines.append(R(merge(bMid(L1, R1, 'SSM: run command to verify app'), bMid(L2, R2, 'Route 53 health check: DNS remove'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Failed health checks trigger alarm actions and Auto Scaling replacement of instances.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Database Health'), bMid(L2, R2, 'Service-Level Checks'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: Enhanced Monitoring metrics'), bMid(L2, R2, 'CloudWatch alarms: CPU/mem/disk'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: describe-db-instances status'), bMid(L2, R2, 'CloudWatch Synthetics canaries'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: Performance Insights queries'), bMid(L2, R2, 'Route 53: endpoint health checks'))))
    lines.append(R(merge(bMid(L1, R1, 'DynamoDB: ConsumedCapacity CW'), bMid(L2, R2, 'AWS Health: account event status'))))
    lines.append(R(merge(bMid(L1, R1, 'ElastiCache: cluster node status'), bMid(L2, R2, 'Systems Manager OpsCenter items'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS EC2 host hardware · ELB infrastructure per AZ · CloudWatch data collection agents'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('System status check= EC2 check for AWS hardware and network issues under the instance'))
    lines.append(txt_row('Instance status check= EC2 check for OS-level software and network configuration'))
    lines.append(txt_row('Auto-recovery   = EC2 action that migrates instance to healthy host on system failure'))
    lines.append(txt_row('ELB health check= Load balancer probe that marks targets healthy or unhealthy'))
    lines.append(txt_row('Healthy threshold= Number of consecutive successful checks to mark target healthy'))
    lines.append(txt_row('Unhealthy threshold= Consecutive failures before target removed from load balancer'))
    lines.append(txt_row('Synthetics canary= Scripted check that simulates user actions against an endpoint'))
    lines.append(txt_row('Enhanced Monitoring= Per-second RDS OS metrics via CloudWatch agent on the host'))
    lines.append(txt_row('Performance Insights= RDS query-level analysis tool showing wait states and top SQL'))
    lines.append(txt_row('OpsCenter item  = Systems Manager work item created from CloudWatch alarm or event'))
    lines.append(txt_row('StatusCheckFailed= CloudWatch metric: 1 if either EC2 status check is failing'))
    lines.append(txt_row('Route 53 health = External probe; fails DNS failover if endpoint unreachable'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-ops-install-upgrade', 'docs/cloud/aws/operations/install-upgrade/index.md', 'AWS install and upgrade operations — patching, agent upgrades, and AMI refresh')
def _aws_ops_install_upgrade():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Operations — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('Patching, agent upgrades, AMI refresh, and service version management procedures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'EC2 Patching'), bMid(L2, R2, 'Agent Upgrades'))))
    lines.append(R(merge(bMid(L1, R1, 'SSM Patch Manager: baseline + scan'), bMid(L2, R2, 'CloudWatch agent: SSM distributor'))))
    lines.append(R(merge(bMid(L1, R1, 'Patch groups: tag-based targeting'), bMid(L2, R2, 'SSM agent: auto-update setting'))))
    lines.append(R(merge(bMid(L1, R1, 'Maintenance window: scheduled run'), bMid(L2, R2, 'X-Ray daemon: via userdata'))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-patch: snapshot AMI first'), bMid(L2, R2, 'CodeDeploy agent: SSM distributor'))))
    lines.append(R(merge(bMid(L1, R1, 'Post-patch: compliance report in CW'), bMid(L2, R2, 'Inspector agent: auto-managed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('AMI refresh strategy: build new AMI with Packer, replace instances via Auto Scaling.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'RDS & Other Services'), bMid(L2, R2, 'Blue/Green & Immutable'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: modify engine version'), bMid(L2, R2, 'Auto Scaling: instance refresh'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: apply during maintenance window'), bMid(L2, R2, 'CodeDeploy: blue/green deployment'))))
    lines.append(R(merge(bMid(L1, R1, 'EKS: managed node group update'), bMid(L2, R2, 'Elastic Beanstalk: rolling update'))))
    lines.append(R(merge(bMid(L1, R1, 'Lambda: version + alias promotion'), bMid(L2, R2, 'CloudFormation: rolling update'))))
    lines.append(R(merge(bMid(L1, R1, 'ElastiCache: cluster version update'), bMid(L2, R2, 'Bake new AMI: never patch in place'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS EC2 host fleet · RDS managed hardware · EKS control plane infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Patch baseline  = SSM policy defining which patches to install; OS and severity filters'))
    lines.append(txt_row('Patch group     = Tag value (Patch Group) used to associate instances with a baseline'))
    lines.append(txt_row('Maintenance window= SSM scheduled time window for patch and other automation tasks'))
    lines.append(txt_row('Distributor     = SSM feature for installing and updating agent packages on instances'))
    lines.append(txt_row('Instance refresh= Auto Scaling feature replacing instances with updated launch template'))
    lines.append(txt_row('AMI bake        = Build a new AMI with all patches baked in; replace running instances'))
    lines.append(txt_row('Blue/green      = New environment deployed alongside old; traffic switched at cutover'))
    lines.append(txt_row('Rolling update  = Update subset of instances at a time; maintains partial availability'))
    lines.append(txt_row('RDS apply-immediately= Forces maintenance change immediately vs next window'))
    lines.append(txt_row('Lambda alias    = Pointer to a function version; shift traffic between versions'))
    lines.append(txt_row('Compliance report= SSM Patch Manager scan result: compliant/non-compliant per instance'))
    lines.append(txt_row('Immutable upgrade= Never patch in place; always replace with pre-patched AMI'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-ops-procedures', 'docs/cloud/aws/operations/procedures/index.md', 'AWS operational procedures — runbooks, change management, and incident response')
def _aws_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Operations — Procedures & Runbooks'))
    lines.append(txt_row())
    lines.append(txt_row('Standard operating procedures for AWS change management, incident response, and routine ops.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Change Management'), bMid(L2, R2, 'Incident Response'))))
    lines.append(R(merge(bMid(L1, R1, 'RFC: document scope and rollback'), bMid(L2, R2, 'Detect: CloudWatch alarm fires'))))
    lines.append(R(merge(bMid(L1, R1, 'CAB approval for prod changes'), bMid(L2, R2, 'Acknowledge: on-call via PagerDuty'))))
    lines.append(R(merge(bMid(L1, R1, 'Change window: low-traffic period'), bMid(L2, R2, 'Investigate: CloudTrail + CW Logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-change: snapshot + health check'), bMid(L2, R2, 'Contain: isolate affected resource'))))
    lines.append(R(merge(bMid(L1, R1, 'Post-change: validate + close RFC'), bMid(L2, R2, 'Recover: restore from backup/AMI'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSM Automation documents codify runbooks; OpsCenter tracks operational issues.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Routine Operations'), bMid(L2, R2, 'Post-Incident Review'))))
    lines.append(R(merge(bMid(L1, R1, 'Daily: review CloudWatch dashboards'), bMid(L2, R2, 'Timeline: reconstruct from CT logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Weekly: cost anomaly report review'), bMid(L2, R2, 'Root cause: 5-why analysis'))))
    lines.append(R(merge(bMid(L1, R1, 'Monthly: patch compliance report'), bMid(L2, R2, 'Action items: preventive controls'))))
    lines.append(R(merge(bMid(L1, R1, 'Quarterly: IAM access review'), bMid(L2, R2, 'Document: PIR in Confluence/Jira'))))
    lines.append(R(merge(bMid(L1, R1, 'Annual: DR test + architecture review'), bMid(L2, R2, 'Share: distribute learnings to team'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS regional infrastructure · Multi-AZ service endpoints · CloudTrail audit data'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RFC             = Request for Change; documents scope, risk, and rollback plan'))
    lines.append(txt_row('CAB             = Change Advisory Board; approves high-risk changes before execution'))
    lines.append(txt_row('Change window   = Pre-approved time slot for making infrastructure changes'))
    lines.append(txt_row('Rollback plan   = Documented steps to revert changes if post-change validation fails'))
    lines.append(txt_row('OpsCenter       = SSM feature that aggregates operational issues with context'))
    lines.append(txt_row('SSM Automation  = Document-based runbook executed against AWS resources'))
    lines.append(txt_row('PIR             = Post-Incident Review; blameless analysis after an incident'))
    lines.append(txt_row('5-why analysis  = Root cause technique: ask why 5 times to find the true cause'))
    lines.append(txt_row('On-call rotation= Schedule assigning primary/secondary responders for incident alerts'))
    lines.append(txt_row('Runbook         = Step-by-step procedure for a repeatable operational task'))
    lines.append(txt_row('IAM access review= Periodic audit of unused permissions and inactive access keys'))
    lines.append(txt_row('DR test         = Disaster recovery test validating RTO/RPO targets are achievable'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-ops-scripts', 'docs/cloud/aws/operations/scripts/index.md', 'AWS operations scripts — automation scripts for common operational tasks')
def _aws_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Operations — Scripts & Automation'))
    lines.append(txt_row())
    lines.append(txt_row('Operational scripts for resource inventory, cost reporting, and routine automation tasks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Inventory Scripts'), bMid(L2, R2, 'Cost Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'List EC2: describe-instances query'), bMid(L2, R2, 'Unattached EBS: cost recovery'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM report: credential report CSV'), bMid(L2, R2, 'Unused EIPs: identify and release'))))
    lines.append(R(merge(bMid(L1, R1, 'Security groups: find 0.0.0.0/0'), bMid(L2, R2, 'Rightsizing: low CPU instances'))))
    lines.append(R(merge(bMid(L1, R1, 'S3 bucket sizes: list-buckets loop'), bMid(L2, R2, 'Snapshot age: old snap cleanup'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag compliance: untagged resources'), bMid(L2, R2, 'Reserved vs on-demand analysis'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Lambda + EventBridge schedules operationalise scripts without managing servers.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Security Scripts'), bMid(L2, R2, 'Script Delivery'))))
    lines.append(R(merge(bMid(L1, R1, 'Rotate access keys: detect old keys'), bMid(L2, R2, 'Lambda: scheduled via EventBridge'))))
    lines.append(R(merge(bMid(L1, R1, 'GuardDuty findings: export to S3'), bMid(L2, R2, 'SSM Run Command: push to instances'))))
    lines.append(R(merge(bMid(L1, R1, 'Config non-compliant: list resources'), bMid(L2, R2, 'Step Functions: multi-step flows'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA audit: users without MFA'), bMid(L2, R2, 'S3 + Athena: output query result'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudTrail: detect root usage'), bMid(L2, R2, 'SNS: notify on script completion'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Lambda compute · EventBridge scheduling plane · S3 output storage · Regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('aws ec2 describe-instances= List all EC2 instances with attributes; filter with --query'))
    lines.append(txt_row('credential report= IAM-generated CSV of all users with last-activity timestamps'))
    lines.append(txt_row('Unattached EBS  = Volume in available state; incurring cost with no instance attached'))
    lines.append(txt_row('Unused EIP      = Elastic IP not associated with a running instance; billed hourly'))
    lines.append(txt_row('Rightsizing     = Identifying oversized instances based on CloudWatch CPU/memory data'))
    lines.append(txt_row('EventBridge schedule= Cron or rate rule triggering Lambda or SSM on a timed basis'))
    lines.append(txt_row('SSM Run Command = Execute scripts on EC2 instances without SSH access'))
    lines.append(txt_row('Step Functions  = Serverless workflow orchestrator for multi-step operational flows'))
    lines.append(txt_row('Tag compliance  = Checking resources have required tags: env, owner, team, cost-center'))
    lines.append(txt_row('GuardDuty findings= Security threat detections exported via EventBridge to S3/SIEM'))
    lines.append(txt_row('Config non-compliant= AWS Config rule evaluation returning NON_COMPLIANT for resources'))
    lines.append(txt_row('Root usage detect= CloudTrail filter for events where userIdentity.type = Root'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-access-control', 'docs/cloud/aws/security/access-control/index.md', 'AWS access control — IAM policies, SCPs, resource policies, and least-privilege design')
def _aws_sec_access_control():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Access Control — Least-Privilege IAM Design'))
    lines.append(txt_row())
    lines.append(txt_row('Layered access control using IAM policies, SCPs, permission boundaries, and resource policies.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy Types'), bMid(L2, R2, 'Evaluation Order'))))
    lines.append(R(merge(bMid(L1, R1, 'Identity: user/role/group policy'), bMid(L2, R2, '1. Explicit deny anywhere → DENY'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource: bucket/key/queue policy'), bMid(L2, R2, '2. SCP denies → DENY'))))
    lines.append(R(merge(bMid(L1, R1, 'SCP: org-level guardrail'), bMid(L2, R2, '3. Permission boundary limits'))))
    lines.append(R(merge(bMid(L1, R1, 'Permission boundary: max allowed'), bMid(L2, R2, '4. Session policy reduces scope'))))
    lines.append(R(merge(bMid(L1, R1, 'Session: temporary scoped token'), bMid(L2, R2, '5. Identity or resource allows → ALLOW'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Default deny: no explicit allow means denied; all policy types must allow for access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Least Privilege Design'), bMid(L2, R2, 'Access Analysis Tools'))))
    lines.append(R(merge(bMid(L1, R1, 'Start with managed policies'), bMid(L2, R2, 'IAM Access Analyzer: findings'))))
    lines.append(R(merge(bMid(L1, R1, 'Generate policy from CloudTrail'), bMid(L2, R2, 'CloudTrail: last-used data'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove unused permissions quarterly'), bMid(L2, R2, 'Credential report: stale keys'))))
    lines.append(R(merge(bMid(L1, R1, 'Conditions: IP, time, MFA, tag'), bMid(L2, R2, 'Config rule: no wildcard actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag-based access: aws:RequestedRegion'), bMid(L2, R2, 'Security Hub: IAM findings'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS IAM control plane · Global IAM service · Regional enforcement at API endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Explicit deny   = Deny statement that overrides any allow; highest priority in evaluation'))
    lines.append(txt_row('SCP             = Service Control Policy; org-level ceiling; cannot grant new permissions'))
    lines.append(txt_row('Permission boundary= IAM policy limiting the maximum permissions an entity can have'))
    lines.append(txt_row('Resource policy = Policy attached to a resource (S3 bucket, KMS key) controlling access'))
    lines.append(txt_row('Session policy  = Policy passed with AssumeRole to further restrict the session'))
    lines.append(txt_row('Default deny    = No explicit allow = implicit deny; AWS denies by default'))
    lines.append(txt_row('IAM condition   = Policy element adding constraints: IP, MFA, time, tag, region'))
    lines.append(txt_row('Access Analyzer = Service that identifies cross-account or public resource access'))
    lines.append(txt_row('Policy generator= Tool that analyses CloudTrail to generate least-privilege policy'))
    lines.append(txt_row('aws:RequestedRegion= Condition key restricting actions to specified AWS regions'))
    lines.append(txt_row('Credential report= CSV of all IAM users with last sign-in and key usage timestamps'))
    lines.append(txt_row('Wildcard action = iam:* or s3:* in a policy grants all actions — avoid in production'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-authentication', 'docs/cloud/aws/security/authentication/index.md', 'AWS authentication — IAM Identity Center SSO, MFA, and credential management')
def _aws_sec_authentication():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Authentication — SSO, MFA & Credentials'))
    lines.append(txt_row())
    lines.append(txt_row('Authentication to AWS via IAM Identity Center SSO, MFA enforcement, and access keys.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'IAM Identity Center (SSO)'), bMid(L2, R2, 'MFA Enforcement'))))
    lines.append(R(merge(bMid(L1, R1, 'IdP: Azure AD / Okta SAML source'), bMid(L2, R2, 'Root account: hardware MFA key'))))
    lines.append(R(merge(bMid(L1, R1, 'Permission sets → IAM roles in accts'), bMid(L2, R2, 'IAM users: TOTP or hardware MFA'))))
    lines.append(R(merge(bMid(L1, R1, 'Browser: AWS access portal login'), bMid(L2, R2, 'SCP: deny without MFA condition'))))
    lines.append(R(merge(bMid(L1, R1, 'CLI: aws sso login --profile'), bMid(L2, R2, 'Identity Center: MFA at portal level'))))
    lines.append(R(merge(bMid(L1, R1, 'Token: short-lived; no static keys'), bMid(L2, R2, 'Condition: aws:MultiFactorAuthPresent'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSO issues short-lived tokens; no long-lived access keys needed for human users.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Access Keys (Machine Identity)'), bMid(L2, R2, 'Credential Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'Use only for machine/CI workloads'), bMid(L2, R2, 'No root account access keys'))))
    lines.append(R(merge(bMid(L1, R1, 'Prefer IAM roles over access keys'), bMid(L2, R2, 'Rotate keys every 90 days'))))
    lines.append(R(merge(bMid(L1, R1, 'Store in Secrets Manager not code'), bMid(L2, R2, 'Audit with credential report'))))
    lines.append(R(merge(bMid(L1, R1, 'OIDC for GitHub Actions (no key)'), bMid(L2, R2, 'Deactivate before deleting'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS for signing; not static keys'), bMid(L2, R2, 'Alert on root usage via CT/CW'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS IAM global service · Identity Center regional portal · STS regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IAM Identity Center= AWS SSO service managing human user access across accounts'))
    lines.append(txt_row('Permission set  = IAM policy definition assigned to users/groups in member accounts'))
    lines.append(txt_row('SAML federation = Protocol connecting corporate IdP (Azure AD/Okta) to AWS SSO'))
    lines.append(txt_row('TOTP            = Time-based One-Time Password; TOTP app (e.g. Authenticator) for MFA'))
    lines.append(txt_row('Hardware MFA    = Physical YubiKey or similar device; recommended for root account'))
    lines.append(txt_row('STS             = Security Token Service; issues temporary credentials via AssumeRole'))
    lines.append(txt_row('Access key      = Long-lived AKID+secret pair; avoid for human users; use SSO instead'))
    lines.append(txt_row('OIDC            = OpenID Connect; allows GitHub Actions to assume roles without keys'))
    lines.append(txt_row('aws:MultiFactorAuthPresent= Condition key requiring MFA in the session'))
    lines.append(txt_row('Credential report= IAM CSV report listing users and their last key/password usage'))
    lines.append(txt_row('Root account    = AWS account root user; cannot be restricted by SCP; use sparingly'))
    lines.append(txt_row('Short-lived token= Temporary STS credential; expires after max 12h; no rotation needed'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-acm', 'docs/cloud/aws/security/certificate-manager/index.md', 'ACM — certificate provisioning, renewal, and deployment for AWS services')
def _aws_sec_acm():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ACM — Certificate Manager'))
    lines.append(txt_row())
    lines.append(txt_row('ACM provisions, manages, and renews TLS certificates for AWS services at no charge.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Types'), bMid(L2, R2, 'Validation Methods'))))
    lines.append(R(merge(bMid(L1, R1, 'Public: trusted by browsers'), bMid(L2, R2, 'DNS: add CNAME to hosted zone'))))
    lines.append(R(merge(bMid(L1, R1, 'Private: ACM Private CA issued'), bMid(L2, R2, 'Email: domain owner email approval'))))
    lines.append(R(merge(bMid(L1, R1, 'Imported: bring own cert/key pair'), bMid(L2, R2, 'DNS preferred: auto-renews cert'))))
    lines.append(R(merge(bMid(L1, R1, 'Wildcard: *.example.com scope'), bMid(L2, R2, 'Route 53: one-click CNAME add'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN: multi-domain single cert'), bMid(L2, R2, 'Pending validation: up to 72h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ACM auto-renews DNS-validated certs 60 days before expiry; no manual renewal needed.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Deployment Targets'), bMid(L2, R2, 'Monitoring & Alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'ALB: HTTPS listener certificate'), bMid(L2, R2, 'CloudWatch: days to expiry metric'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudFront: us-east-1 cert only'), bMid(L2, R2, 'EventBridge: cert expiry event'))))
    lines.append(R(merge(bMid(L1, R1, 'API Gateway: custom domain cert'), bMid(L2, R2, 'Config rule: acm-certificate-expiry'))))
    lines.append(R(merge(bMid(L1, R1, 'AppSync / Cognito domain cert'), bMid(L2, R2, 'SNS: alert 30 days before expiry'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2 (imported only; not ACM-managed)'), bMid(L2, R2, 'Security Hub: cert findings'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Certificate Manager infrastructure · ACM Private CA HSM hardware · Regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ACM             = AWS Certificate Manager; free TLS certs for integrated AWS services'))
    lines.append(txt_row('Public cert     = Browser-trusted cert issued by Amazon root CA; free to provision'))
    lines.append(txt_row('Private CA      = ACM Private CA; issues internal certs for private services'))
    lines.append(txt_row('DNS validation  = Proves domain ownership by adding a CNAME record to DNS'))
    lines.append(txt_row('Email validation= Sends approval email to WHOIS contacts; expires if not confirmed'))
    lines.append(txt_row('SAN             = Subject Alternative Name; multi-domain cert (up to 10 SANs in ACM)'))
    lines.append(txt_row('Wildcard cert   = Single cert for *.domain.com; covers all one-level subdomains'))
    lines.append(txt_row('Auto-renewal    = ACM renews DNS-validated certs automatically 60 days before expiry'))
    lines.append(txt_row('Imported cert   = Third-party cert uploaded to ACM; manual renewal required'))
    lines.append(txt_row('CloudFront cert = ACM certs for CloudFront must be in us-east-1 regardless of region'))
    lines.append(txt_row('DaysToExpiry    = CloudWatch metric for imported certs; monitor for upcoming expiry'))
    lines.append(txt_row('Certificate pinning= Not supported with ACM managed certs due to auto-rotation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-encryption', 'docs/cloud/aws/security/encryption/index.md', 'AWS encryption — at-rest and in-transit encryption across storage, compute, and network')
def _aws_sec_encryption():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Encryption — At Rest & In Transit'))
    lines.append(txt_row())
    lines.append(txt_row('Encryption at rest via KMS keys; in transit via TLS; key management and rotation policy.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'At-Rest Encryption'), bMid(L2, R2, 'In-Transit Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'S3: SSE-S3, SSE-KMS, SSE-C'), bMid(L2, R2, 'ALB/NLB: TLS 1.2+ policies'))))
    lines.append(R(merge(bMid(L1, R1, 'EBS: AES-256 via KMS CMK'), bMid(L2, R2, 'API calls: HTTPS/TLS enforced'))))
    lines.append(R(merge(bMid(L1, R1, 'RDS: encryption at creation only'), bMid(L2, R2, 'S3: enforce-HTTPS bucket policy'))))
    lines.append(R(merge(bMid(L1, R1, 'DynamoDB: enabled by default'), bMid(L2, R2, 'VPN: IPSec tunnel encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'EFS / FSx / ElastiCache: KMS opt'), bMid(L2, R2, 'DirectConnect: MACsec Layer 2'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Use CMKs over AWS-managed keys for full control, key policy, and cross-account access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Management'), bMid(L2, R2, 'Encryption in Practice'))))
    lines.append(R(merge(bMid(L1, R1, 'CMK: customer-managed KMS key'), bMid(L2, R2, 'S3 bucket policy: deny non-HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Key policy: who can use/admin'), bMid(L2, R2, 'EBS default encryption: account'))))
    lines.append(R(merge(bMid(L1, R1, 'Annual auto-rotation available'), bMid(L2, R2, 'RDS: encrypt before launch'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-region: copy snapshot with key'), bMid(L2, R2, 'Config rule: encrypted-volumes'))))
    lines.append(R(merge(bMid(L1, R1, 'Secrets Manager: KMS envelope enc'), bMid(L2, R2, 'Security Hub: encryption findings'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS KMS HSMs (FIPS 140-2 Level 3) · S3 encryption hardware · TLS termination nodes'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CMK             = Customer-Managed Key; KMS key fully controlled by the customer'))
    lines.append(txt_row('AWS-managed key = Managed by AWS per service; auto-rotate annually; less control'))
    lines.append(txt_row('Envelope encryption= Data encrypted with data key; data key encrypted with CMK'))
    lines.append(txt_row('SSE-KMS         = S3 server-side encryption using a KMS key; auditable in CloudTrail'))
    lines.append(txt_row('SSE-S3          = S3 server-side encryption with AWS-managed S3 key; no KMS audit'))
    lines.append(txt_row('SSE-C           = S3 encryption with customer-provided key; AWS does not store key'))
    lines.append(txt_row('Key rotation    = Annual automatic replacement of key material; aliases unchanged'))
    lines.append(txt_row('Key policy      = Resource-based policy on CMK defining who can use/manage the key'))
    lines.append(txt_row('Cross-region copy= Snapshot copied to another region must be re-encrypted with region key'))
    lines.append(txt_row('MACsec          = Layer 2 encryption on dedicated Direct Connect connections'))
    lines.append(txt_row('TLS policy      = ALB security policy selecting supported TLS versions and ciphers'))
    lines.append(txt_row('EBS default enc = Account-level setting encrypting all new EBS volumes automatically'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-guardduty', 'docs/cloud/aws/security/guardduty/index.md', 'GuardDuty — threat detection, finding types, and automated response workflows')
def _aws_sec_guardduty():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'GuardDuty — Threat Detection'))
    lines.append(txt_row())
    lines.append(txt_row('GuardDuty analyses CloudTrail, VPC Flow Logs, and DNS to detect threats with ML/signatures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Sources'), bMid(L2, R2, 'Finding Categories'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudTrail management events'), bMid(L2, R2, 'Backdoor: C2 communication'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudTrail S3 data events'), bMid(L2, R2, 'Cryptocurrency: mining activity'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC Flow Logs: network flows'), bMid(L2, R2, 'Recon: port scan / API probe'))))
    lines.append(R(merge(bMid(L1, R1, 'Route 53 DNS query logs'), bMid(L2, R2, 'Stealth: policy change detection'))))
    lines.append(R(merge(bMid(L1, R1, 'EKS audit + runtime monitoring'), bMid(L2, R2, 'Trojan: malware callback patterns'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Findings classified LOW/MED/HIGH; EventBridge routes findings to SNS/Lambda/SIEM.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-Account Management'), bMid(L2, R2, 'Response Actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Delegated admin: security account'), bMid(L2, R2, 'EventBridge rule: pattern match'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-enable for new member accounts'), bMid(L2, R2, 'Lambda: isolate EC2 instance'))))
    lines.append(R(merge(bMid(L1, R1, 'Aggregate findings centrally'), bMid(L2, R2, 'SNS: alert on-call team'))))
    lines.append(R(merge(bMid(L1, R1, 'Suppression rules: reduce noise'), bMid(L2, R2, 'Security Hub: ingest findings'))))
    lines.append(R(merge(bMid(L1, R1, 'Export: EventBridge → S3/SIEM'), bMid(L2, R2, 'Threat Intel: custom IP/domain list'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS GuardDuty ML infrastructure · Regional data processing · CloudTrail/Flow Log feeds'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Finding         = GuardDuty security alert with type, severity, and affected resource'))
    lines.append(txt_row('Finding type    = Structured name: ThreatPurpose:ResourceTypeAffected/ThreatFamilyName'))
    lines.append(txt_row('Severity        = Numeric 0.1–8.9 mapped to LOW/MEDIUM/HIGH'))
    lines.append(txt_row('Delegated admin = Member account designated to manage GuardDuty org-wide'))
    lines.append(txt_row('Suppression rule= Filter that archives matching findings automatically to reduce noise'))
    lines.append(txt_row('Trusted IP list = Whitelist of IPs that GuardDuty will not generate findings for'))
    lines.append(txt_row('Threat intel    = Custom IP/domain list uploaded to GuardDuty as threat indicator'))
    lines.append(txt_row('EKS protection  = GuardDuty monitors Kubernetes audit logs for anomalous activity'))
    lines.append(txt_row('Runtime monitoring= GuardDuty agent on EC2/ECS/EKS for process-level detection'))
    lines.append(txt_row('Malware protection= GuardDuty scans EBS volumes of flagged instances for malware'))
    lines.append(txt_row('EventBridge export= GuardDuty sends findings to EventBridge for automated routing'))
    lines.append(txt_row('30-day free trial= GuardDuty offers 30-day free trial per account per region'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-hardening', 'docs/cloud/aws/security/hardening/index.md', 'AWS security hardening — CIS benchmarks, account baseline, and preventive controls')
def _aws_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Security Hardening — CIS Baseline'))
    lines.append(txt_row())
    lines.append(txt_row('Account and resource hardening following CIS AWS Benchmark and AWS Security Best Practices.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Account-Level Controls'), bMid(L2, R2, 'IAM Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Root MFA: hardware key required'), bMid(L2, R2, 'No root access keys'))))
    lines.append(R(merge(bMid(L1, R1, 'No root access keys created'), bMid(L2, R2, 'Password policy: 14+ chars'))))
    lines.append(R(merge(bMid(L1, R1, 'CloudTrail: org trail all regions'), bMid(L2, R2, 'MFA for all IAM users'))))
    lines.append(R(merge(bMid(L1, R1, 'Config: record all resource changes'), bMid(L2, R2, 'Access keys rotated < 90 days'))))
    lines.append(R(merge(bMid(L1, R1, 'GuardDuty: enabled all accounts'), bMid(L2, R2, 'Inactive users deactivated'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SCPs enforce preventive controls; Config rules detect drift; Security Hub aggregates.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Hardening'), bMid(L2, R2, 'Monitoring Baseline'))))
    lines.append(R(merge(bMid(L1, R1, 'No 0.0.0.0/0 on sensitive ports'), bMid(L2, R2, 'CW alarm: root usage'))))
    lines.append(R(merge(bMid(L1, R1, 'Default SG: deny all traffic'), bMid(L2, R2, 'CW alarm: console login no MFA'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC Flow Logs: all VPCs enabled'), bMid(L2, R2, 'CW alarm: CloudTrail config change'))))
    lines.append(R(merge(bMid(L1, R1, 'No default VPC in use for prod'), bMid(L2, R2, 'CW alarm: unauthorised API calls'))))
    lines.append(R(merge(bMid(L1, R1, 'WAF on public-facing ALBs'), bMid(L2, R2, 'Security Hub score > 80%'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global IAM plane · CloudTrail infrastructure · Config recorders per region'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS AWS Benchmark= Center for Internet Security published hardening checklist for AWS'))
    lines.append(txt_row('Org trail       = Single CloudTrail trail capturing all accounts and all regions'))
    lines.append(txt_row('Config recorder = Regional AWS Config component tracking resource configuration history'))
    lines.append(txt_row('SCP             = Preventive guardrail; denies actions org-wide; enforces policy'))
    lines.append(txt_row('Default SG      = Harden by removing all rules; new instances should use custom SGs'))
    lines.append(txt_row('Password policy = IAM setting enforcing min length, complexity, rotation for IAM users'))
    lines.append(txt_row('Security Hub score= Percentage of enabled controls passing; target > 80%'))
    lines.append(txt_row('Preventive control= Config rule or SCP that blocks non-compliant actions before they occur'))
    lines.append(txt_row('Detective control= Config rule or GuardDuty finding that identifies non-compliance after'))
    lines.append(txt_row('WAF             = Web Application Firewall; filters HTTP requests on ALB/CloudFront'))
    lines.append(txt_row('VPC Flow Logs   = Network traffic metadata; enable on all VPCs for security audit'))
    lines.append(txt_row('Root MFA        = Hardware MFA on root is CIS level 1 requirement; highest priority'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-inspector', 'docs/cloud/aws/security/inspector/index.md', 'AWS Inspector — vulnerability scanning for EC2, ECR images, and Lambda functions')
def _aws_sec_inspector():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'AWS Inspector — Vulnerability Scanning'))
    lines.append(txt_row())
    lines.append(txt_row('Inspector continuously scans EC2, ECR container images, and Lambda for vulnerabilities.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Scan Targets'), bMid(L2, R2, 'Finding Types'))))
    lines.append(R(merge(bMid(L1, R1, 'EC2: OS packages + software CVEs'), bMid(L2, R2, 'CVE: known software vulnerability'))))
    lines.append(R(merge(bMid(L1, R1, 'ECR: container image layers scan'), bMid(L2, R2, 'Network: reachable port finding'))))
    lines.append(R(merge(bMid(L1, R1, 'Lambda: function code + packages'), bMid(L2, R2, 'Code: Lambda code vulnerability'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-enabled: no config required'), bMid(L2, R2, 'EPSS: exploit probability score'))))
    lines.append(R(merge(bMid(L1, R1, 'Continuous: rescan on new CVE pub'), bMid(L2, R2, 'Severity: CRITICAL/HIGH/MED/LOW'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Inspector scores each finding with CVSS + EPSS; prioritise by exploitability score.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-Account & Org'), bMid(L2, R2, 'Remediation Workflow'))))
    lines.append(R(merge(bMid(L1, R1, 'Delegated admin: central findings'), bMid(L2, R2, 'Security Hub: findings forwarded'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-enable on new org accounts'), bMid(L2, R2, 'EventBridge: route critical CVEs'))))
    lines.append(R(merge(bMid(L1, R1, 'Suppression rules: noise reduction'), bMid(L2, R2, 'Jira/ITSM: ticket via EventBridge'))))
    lines.append(R(merge(bMid(L1, R1, 'Export: JSON to S3 for analysis'), bMid(L2, R2, 'Patch: SSM Patch Manager'))))
    lines.append(R(merge(bMid(L1, R1, 'Coverage: track enabled resources'), bMid(L2, R2, 'Re-image: bake fixed AMI'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Inspector scanning infrastructure · SSM agent on EC2 · ECR registry endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CVE             = Common Vulnerabilities and Exposures; standardised vulnerability ID'))
    lines.append(txt_row('CVSS            = Common Vulnerability Scoring System; 0–10 severity rating'))
    lines.append(txt_row('EPSS            = Exploit Prediction Scoring System; probability of exploitation'))
    lines.append(txt_row('Inspector score = Adjusted CVSS considering exploitability and network reachability'))
    lines.append(txt_row('Network finding = Inspector detects EC2 ports reachable from 0.0.0.0/0 via SG rules'))
    lines.append(txt_row('ECR scan        = Inspector scans container images pushed to ECR automatically'))
    lines.append(txt_row('Lambda scan     = Inspector analyses Lambda function code and package dependencies'))
    lines.append(txt_row('Continuous scan = Inspector rescans whenever a new CVE is published for known packages'))
    lines.append(txt_row('Suppression rule= Filter that archives findings matching a specific pattern'))
    lines.append(txt_row('Delegated admin = Member account with org-wide Inspector visibility and management'))
    lines.append(txt_row('Coverage        = Percentage of resources successfully scanned by Inspector'))
    lines.append(txt_row('SSM agent       = Required on EC2 for Inspector to collect package inventory data'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-kms', 'docs/cloud/aws/security/kms/index.md', 'KMS — key management, CMK types, key policies, and encryption integration')
def _aws_sec_kms():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'KMS — Key Management Service'))
    lines.append(txt_row())
    lines.append(txt_row('KMS manages encryption keys used by AWS services; CMKs provide full customer control.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Types'), bMid(L2, R2, 'Key Operations'))))
    lines.append(R(merge(bMid(L1, R1, 'Symmetric: AES-256 for encryption'), bMid(L2, R2, 'Encrypt: up to 4KB directly'))))
    lines.append(R(merge(bMid(L1, R1, 'Asymmetric: RSA/ECC sign/verify'), bMid(L2, R2, 'GenerateDataKey: envelope enc'))))
    lines.append(R(merge(bMid(L1, R1, 'HMAC: message authentication'), bMid(L2, R2, 'Sign/Verify: digital signatures'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS-managed: per service; free'), bMid(L2, R2, 'CreateGrant: temporary delegation'))))
    lines.append(R(merge(bMid(L1, R1, 'Customer-managed: full control'), bMid(L2, R2, 'Decrypt: returns plaintext data key'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Key policies are the primary access control; IAM policies alone are insufficient for CMKs.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Policy'), bMid(L2, R2, 'KMS Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Root account: full admin access'), bMid(L2, R2, 'S3: SSE-KMS per bucket/object'))))
    lines.append(R(merge(bMid(L1, R1, 'Key admins: manage but not use'), bMid(L2, R2, 'EBS: CMK at volume creation'))))
    lines.append(R(merge(bMid(L1, R1, 'Key users: encrypt/decrypt ops'), bMid(L2, R2, 'RDS: CMK at database creation'))))
    lines.append(R(merge(bMid(L1, R1, 'kms:ViaService: service restriction'), bMid(L2, R2, 'Secrets Manager: auto-rotation'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account: explicit allow needed'), bMid(L2, R2, 'CloudTrail: all KMS API calls'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS KMS HSM hardware (FIPS 140-2 Level 3) · Regional KMS endpoints · CloudHSM option'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CMK             = Customer-Managed Key; KMS key managed by customer with full control'))
    lines.append(txt_row('Key policy      = Resource-based JSON policy attached to a KMS key; required for access'))
    lines.append(txt_row('Envelope encryption= Plaintext encrypted with data key; data key encrypted with CMK'))
    lines.append(txt_row('GenerateDataKey = KMS returns plaintext + encrypted data key for envelope encryption'))
    lines.append(txt_row('Key rotation    = Annual automatic rotation of key material; previous material retained'))
    lines.append(txt_row('Key alias       = Friendly name (alias/my-key) for a CMK; updatable without re-keying'))
    lines.append(txt_row('Grant           = Programmatic temporary delegation of key use to a principal'))
    lines.append(txt_row('kms:ViaService  = Condition restricting key use to calls made by a specific AWS service'))
    lines.append(txt_row('Key deletion    = 7–30 day waiting period before permanent deletion; irreversible'))
    lines.append(txt_row('Multi-region key= Replica key in another region; same key material, different ARN'))
    lines.append(txt_row('CloudHSM        = Dedicated hardware HSM; FIPS 140-2 Level 3; customer-managed cluster'))
    lines.append(txt_row('Asymmetric key  = Public key downloadable; private key never leaves KMS HSM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-secrets-manager', 'docs/cloud/aws/security/secrets-manager/index.md', 'Secrets Manager — secret storage, rotation, and cross-service credential management')
def _aws_sec_secrets_manager():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Secrets Manager — Credential Lifecycle'))
    lines.append(txt_row())
    lines.append(txt_row('Secrets Manager stores, rotates, and distributes credentials without hardcoding secrets.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Secret Storage'), bMid(L2, R2, 'Secret Types'))))
    lines.append(R(merge(bMid(L1, R1, 'JSON key-value or plaintext string'), bMid(L2, R2, 'RDS credentials: auto-rotate'))))
    lines.append(R(merge(bMid(L1, R1, 'Encrypted with KMS CMK'), bMid(L2, R2, 'API keys: manual or Lambda rotate'))))
    lines.append(R(merge(bMid(L1, R1, 'Versioned: AWSCURRENT/AWSPENDING'), bMid(L2, R2, 'SSH keys: stored encrypted'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource policy: cross-account share'), bMid(L2, R2, 'OAuth tokens: Lambda rotation'))))
    lines.append(R(merge(bMid(L1, R1, 'Replication: cross-region replicas'), bMid(L2, R2, 'Certificates: alongside ACM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Auto-rotation uses Lambda to update the secret and the target service atomically.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Rotation Workflow'), bMid(L2, R2, 'Access Patterns'))))
    lines.append(R(merge(bMid(L1, R1, '1. createSecret: AWSPENDING version'), bMid(L2, R2, 'SDK: get-secret-value API call'))))
    lines.append(R(merge(bMid(L1, R1, '2. setSecret: update the service'), bMid(L2, R2, 'Lambda env: inject at deploy'))))
    lines.append(R(merge(bMid(L1, R1, '3. testSecret: verify new creds'), bMid(L2, R2, 'ECS/EKS: secret reference'))))
    lines.append(R(merge(bMid(L1, R1, '4. finishSecret: promote to CURRENT'), bMid(L2, R2, 'CodeBuild: secret ID in buildspec'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: days interval or cron'), bMid(L2, R2, 'Cache: SDK caches for 5 minutes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS KMS HSM · Secrets Manager regional API · Lambda rotation infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Secret          = Encrypted credential or config value stored in Secrets Manager'))
    lines.append(txt_row('AWSCURRENT      = Version label for the current active version of a secret'))
    lines.append(txt_row('AWSPENDING      = Version label for the new secret during rotation; not yet current'))
    lines.append(txt_row('Rotation Lambda = Function that rotates the secret value and updates the target service'))
    lines.append(txt_row('get-secret-value= SDK/CLI API that retrieves the plaintext secret value'))
    lines.append(txt_row('Resource policy = JSON policy on the secret allowing cross-account access'))
    lines.append(txt_row('Replication     = Cross-region replica; same secret value; independent rotation'))
    lines.append(txt_row('SDK caching     = AWS SDK caches secret for 5 min; reduces API calls and cost'))
    lines.append(txt_row('RDS integration = Built-in rotation for RDS; Lambda updates both secret and DB password'))
    lines.append(txt_row('SSM Parameter Store= Simpler alternative; no auto-rotation; SecureString uses KMS'))
    lines.append(txt_row('Rotation schedule= Interval in days or cron expression for automatic rotation'))
    lines.append(txt_row('Secret ARN      = Unique identifier for the secret; used in IAM policy resource field'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-sec-security-hub', 'docs/cloud/aws/security/security-hub/index.md', 'Security Hub — aggregated security findings, compliance standards, and posture scoring')
def _aws_sec_security_hub():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Security Hub — Aggregated Security Posture'))
    lines.append(txt_row())
    lines.append(txt_row('Security Hub aggregates findings from AWS services and third parties into a central score.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Sources (Finding Integrations)'), bMid(L2, R2, 'Compliance Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'GuardDuty: threat findings'), bMid(L2, R2, 'CIS AWS Benchmark v1.4/3.0'))))
    lines.append(R(merge(bMid(L1, R1, 'Inspector: vulnerability findings'), bMid(L2, R2, 'AWS Foundational Security Best'))))
    lines.append(R(merge(bMid(L1, R1, 'Config: non-compliant resources'), bMid(L2, R2, 'PCI DSS v3.2.1'))))
    lines.append(R(merge(bMid(L1, R1, 'IAM Access Analyzer findings'), bMid(L2, R2, 'NIST SP 800-53 Rev 5'))))
    lines.append(R(merge(bMid(L1, R1, 'Macie, Firewall Manager, 3rd party'), bMid(L2, R2, 'Custom standard (self-managed)'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Security score = % controls passing; findings routed via EventBridge to SIEM/ticketing.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-Account Management'), bMid(L2, R2, 'Finding Workflow'))))
    lines.append(R(merge(bMid(L1, R1, 'Delegated admin: security account'), bMid(L2, R2, 'Status: NEW/NOTIFIED/RESOLVED'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-enable on new org members'), bMid(L2, R2, 'Workflow: assign owner/notes'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-region aggregation: one pane'), bMid(L2, R2, 'Suppression: auto-archive rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Finding aggregation region option'), bMid(L2, R2, 'EventBridge: route to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom actions: EventBridge target'), bMid(L2, R2, 'ASFF: standard finding format'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Security Hub regional service · EventBridge integration infrastructure · ASFF schema'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Security Hub    = AWS service aggregating security findings with posture scoring'))
    lines.append(txt_row('Security score  = Percentage of enabled standard controls passing across all accounts'))
    lines.append(txt_row('ASFF            = Amazon Security Finding Format; standardised JSON finding schema'))
    lines.append(txt_row('Control         = Specific check within a compliance standard; PASS/FAIL/NO_DATA'))
    lines.append(txt_row('Standard        = Collection of controls, e.g. CIS Benchmark or FSBP'))
    lines.append(txt_row('Delegated admin = Member account with org-wide Security Hub management rights'))
    lines.append(txt_row('Custom action   = User-defined action sending selected findings to EventBridge'))
    lines.append(txt_row('Finding aggregation= Option to centralise findings from all regions to one region'))
    lines.append(txt_row('Suppression rule= Auto-archive filter for expected/accepted findings'))
    lines.append(txt_row('Workflow status = Finding lifecycle: NEW → NOTIFIED → IN_PROGRESS → RESOLVED'))
    lines.append(txt_row('FSBP            = AWS Foundational Security Best Practices; AWS-maintained standard'))
    lines.append(txt_row('Macie           = Data protection service; sends S3 sensitive data findings to Hub'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-ebs', 'docs/cloud/aws/storage/ebs/index.md', 'EBS — volume types, performance tiers, multi-attach, and encryption')
def _aws_storage_ebs():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'EBS — Elastic Block Store'))
    lines.append(txt_row())
    lines.append(txt_row('EBS provides persistent block storage for EC2; volume type determines performance tier.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Volume Types'), bMid(L2, R2, 'Performance Specs'))))
    lines.append(R(merge(bMid(L1, R1, 'gp3: general SSD; default choice'), bMid(L2, R2, 'gp3: 16,000 IOPS / 1,000 MB/s'))))
    lines.append(R(merge(bMid(L1, R1, 'gp2: older general SSD; burst'), bMid(L2, R2, 'io2 Block Express: 256K IOPS'))))
    lines.append(R(merge(bMid(L1, R1, 'io2: provisioned IOPS; multi-attach'), bMid(L2, R2, 'st1: 500 MB/s throughput'))))
    lines.append(R(merge(bMid(L1, R1, 'st1: throughput HDD; big data'), bMid(L2, R2, 'sc1: 250 MB/s cold HDD'))))
    lines.append(R(merge(bMid(L1, R1, 'sc1: cold HDD; infrequent access'), bMid(L2, R2, 'gp2: burst 3,000 IOPS to credit'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('EBS volumes are AZ-scoped; use snapshots to move data across AZs or regions.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Advanced Features'), bMid(L2, R2, 'Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-attach: io1/io2 up to 16 EC2'), bMid(L2, R2, 'Enable account default encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption: AES-256 via KMS CMK'), bMid(L2, R2, 'Use gp3 over gp2 (cheaper)'))))
    lines.append(R(merge(bMid(L1, R1, 'Modify in-place: resize/type change'), bMid(L2, R2, 'Snapshots before risky changes'))))
    lines.append(R(merge(bMid(L1, R1, 'Fast snapshot restore: instant data'), bMid(L2, R2, 'CloudWatch IOPS metric alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'Nitro-based: max performance gains'), bMid(L2, R2, 'Delete volumes on termination'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS AZ SSD/HDD storage arrays · Dedicated EBS network separate from EC2 data path'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('gp3             = General Purpose SSD v3; independently set IOPS and throughput'))
    lines.append(txt_row('io2 Block Express= Highest performance SSD; up to 256K IOPS; SAP HANA workloads'))
    lines.append(txt_row('IOPS            = Input/output operations per second; determines random I/O speed'))
    lines.append(txt_row('Throughput      = Data transfer rate in MB/s; determines sequential I/O speed'))
    lines.append(txt_row('Multi-attach    = io1/io2 feature allowing up to 16 EC2 instances to share a volume'))
    lines.append(txt_row('Burst credit    = gp2 earns credits at baseline; spends at 3,000 IOPS during burst'))
    lines.append(txt_row('Modify in-place = Change volume type, size, or IOPS without stopping EC2 instance'))
    lines.append(txt_row('FSR             = Fast Snapshot Restore; initialises volume data instantly from snapshot'))
    lines.append(txt_row('AZ-scoped       = EBS volume lives in one AZ; detach and re-attach within same AZ only'))
    lines.append(txt_row('Snapshot        = Point-in-time backup of EBS volume stored durably in S3'))
    lines.append(txt_row('Nitro EC2       = Instance family required for max EBS performance (most modern types)'))
    lines.append(txt_row('Delete on term  = Volume option; if enabled, volume deleted when instance terminates'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-ebs-snapshots', 'docs/cloud/aws/storage/ebs-snapshots/index.md', 'EBS Snapshots — lifecycle, cross-region copy, Data Lifecycle Manager, and restore')
def _aws_storage_ebs_snapshots():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'EBS Snapshots — Backup & Lifecycle'))
    lines.append(txt_row())
    lines.append(txt_row('EBS snapshots are incremental S3-backed backups; DLM automates creation and retention.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshot Mechanics'), bMid(L2, R2, 'Snapshot Operations'))))
    lines.append(R(merge(bMid(L1, R1, 'Incremental: only changed blocks'), bMid(L2, R2, 'Create: from volume or running EC2'))))
    lines.append(R(merge(bMid(L1, R1, 'Stored in S3 (not visible in bucket)'), bMid(L2, R2, 'Restore: create new volume from snap'))))
    lines.append(R(merge(bMid(L1, R1, 'Regional: copy to other regions'), bMid(L2, R2, 'AMI: create image from snapshot'))))
    lines.append(R(merge(bMid(L1, R1, 'Encrypted: uses volume CMK'), bMid(L2, R2, 'Share: to account or public'))))
    lines.append(R(merge(bMid(L1, R1, 'Charged for changed blocks only'), bMid(L2, R2, 'Copy: cross-region with new key'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DLM policy automates snapshot schedules and retention; use FSR for fast restores.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DLM (Data Lifecycle Manager)'), bMid(L2, R2, 'Snapshot Archive'))))
    lines.append(R(merge(bMid(L1, R1, 'Policy: tag-based volume targeting'), bMid(L2, R2, 'Archive tier: 75% cost saving'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: frequency + retention'), bMid(L2, R2, 'Restore: 24–72h from archive'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-region copy rule in policy'), bMid(L2, R2, 'Recycle Bin: accidental delete'))))
    lines.append(R(merge(bMid(L1, R1, 'Fast snapshot restore option'), bMid(L2, R2, 'Recycle retention: 1–365 days'))))
    lines.append(R(merge(bMid(L1, R1, 'EventBridge: notify on creation'), bMid(L2, R2, 'Compliance lock: prevent early del'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS S3 snapshot storage backend · Cross-region replication infrastructure · Archive tier'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Incremental snapshot= After first full, subsequent snaps store only changed blocks'))
    lines.append(txt_row('DLM             = Data Lifecycle Manager; manages EBS snapshot automation policies'))
    lines.append(txt_row('FSR             = Fast Snapshot Restore; pre-initialises snapshot data for instant restore'))
    lines.append(txt_row('Snapshot archive= Cold tier for infrequently accessed snapshots; lower cost'))
    lines.append(txt_row('Recycle Bin     = Soft-delete retention for snapshots; recover within retention period'))
    lines.append(txt_row('Snapshot lock   = Compliance mode preventing modification or deletion of snapshots'))
    lines.append(txt_row('Cross-region copy= Create copy of snapshot in another region; re-encrypt with new key'))
    lines.append(txt_row('Shared snapshot = Owner can share snapshot to specific accounts or make public'))
    lines.append(txt_row('Encrypted snap  = Snapshot of encrypted volume is always encrypted; cannot disable'))
    lines.append(txt_row('Volume from snap= New EBS volume restored from snapshot data; any size ≥ original'))
    lines.append(txt_row('Retention count = DLM policy keeps N most recent snapshots; deletes older ones'))
    lines.append(txt_row('Tag targeting   = DLM policy targets volumes with specific tag key-value pairs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-efs', 'docs/cloud/aws/storage/efs/index.md', 'EFS — elastic NFS file system, performance modes, and access control')
def _aws_storage_efs():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'EFS — Elastic File System'))
    lines.append(txt_row())
    lines.append(txt_row('EFS provides shared NFS file storage for EC2 and Lambda; scales automatically to petabytes.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'EFS Characteristics'), bMid(L2, R2, 'Performance Modes'))))
    lines.append(R(merge(bMid(L1, R1, 'NFS v4.1/v4.0 protocol'), bMid(L2, R2, 'General Purpose: low latency'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-AZ: mount from any AZ'), bMid(L2, R2, 'Max I/O: high aggregate throughput'))))
    lines.append(R(merge(bMid(L1, R1, 'Pay per GB stored; no provisioning'), bMid(L2, R2, 'Bursting: scales with file system'))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption: KMS at rest; TLS transit'), bMid(L2, R2, 'Elastic: recommended default'))))
    lines.append(R(merge(bMid(L1, R1, 'POSIX permissions + ACLs'), bMid(L2, R2, 'Provisioned: guaranteed throughput'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Mount targets per AZ; security group on mount target controls NFS port 2049 access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage Classes'), bMid(L2, R2, 'Access Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'Standard: frequently accessed'), bMid(L2, R2, 'EC2: mount in user-data script'))))
    lines.append(R(merge(bMid(L1, R1, 'Standard-IA: infrequent access'), bMid(L2, R2, 'Lambda: /mnt/* mount config'))))
    lines.append(R(merge(bMid(L1, R1, 'One Zone: single AZ; lower cost'), bMid(L2, R2, 'ECS/EKS: persistent volume claim'))))
    lines.append(R(merge(bMid(L1, R1, 'Lifecycle: auto-tier after N days'), bMid(L2, R2, 'Access Points: per-app directory'))))
    lines.append(R(merge(bMid(L1, R1, 'Intelligent-Tiering: auto-move'), bMid(L2, R2, 'DataSync: on-prem migration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS EFS storage infrastructure per AZ · Mount target ENIs in each VPC subnet'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Mount target    = ENI in a subnet; endpoint for NFS connections from EC2 or Lambda'))
    lines.append(txt_row('Access Point    = Application-specific entry point enforcing POSIX user and root path'))
    lines.append(txt_row('General Purpose = Default performance mode; low latency for most workloads'))
    lines.append(txt_row('Max I/O         = Higher aggregate throughput; higher latency; for parallel workloads'))
    lines.append(txt_row('Elastic throughput= Auto-scales up to 10 GB/s without provisioning; recommended'))
    lines.append(txt_row('Bursting throughput= Scales with file system size; earns burst credits when idle'))
    lines.append(txt_row('Standard-IA     = Infrequent Access storage class; 92% cheaper than Standard'))
    lines.append(txt_row('Lifecycle policy= Automatically moves files to IA after 7, 14, 30, 60, or 90 days'))
    lines.append(txt_row('One Zone        = Single-AZ EFS; 47% cheaper than standard; no cross-AZ redundancy'))
    lines.append(txt_row('NFS port 2049   = TCP port used for NFS connections; allow in mount target SG'))
    lines.append(txt_row('DataSync        = AWS service for migrating on-premises NFS data to EFS'))
    lines.append(txt_row('Encryption at rest= KMS CMK encrypts all EFS file system data and metadata'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-fsx', 'docs/cloud/aws/storage/fsx/index.md', 'FSx — managed file systems for Windows (SMB), Lustre, NetApp ONTAP, and OpenZFS')
def _aws_storage_fsx():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'FSx — Managed File System Flavours'))
    lines.append(txt_row())
    lines.append(txt_row('FSx provides fully managed file systems: Windows SMB, Lustre HPC, ONTAP, and OpenZFS.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'FSx for Windows File Server'), bMid(L2, R2, 'FSx for Lustre'))))
    lines.append(R(merge(bMid(L1, R1, 'SMB protocol: Windows native share'), bMid(L2, R2, 'HPC/ML: sub-ms latency'))))
    lines.append(R(merge(bMid(L1, R1, 'AD integration: Kerberos auth'), bMid(L2, R2, 'S3 integration: data repo'))))
    lines.append(R(merge(bMid(L1, R1, 'DFS namespace: scale-out shares'), bMid(L2, R2, 'SSD: scratch or persistent tier'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-AZ HA with standby node'), bMid(L2, R2, 'Up to 1 TB/s aggregate'))))
    lines.append(R(merge(bMid(L1, R1, 'Shadow copies, VSS, DFS-R support'), bMid(L2, R2, 'EKS/ECS: CSI driver support'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('FSx for ONTAP: full NetApp features in AWS; FSx for OpenZFS: NFS with ZFS snapshots.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'FSx for ONTAP'), bMid(L2, R2, 'FSx for OpenZFS'))))
    lines.append(R(merge(bMid(L1, R1, 'NFS/SMB/iSCSI multi-protocol'), bMid(L2, R2, 'NFS v3/v4 file system'))))
    lines.append(R(merge(bMid(L1, R1, 'SnapMirror: on-prem replication'), bMid(L2, R2, 'ZFS snapshots and clones'))))
    lines.append(R(merge(bMid(L1, R1, 'FlexVols, thin provision, dedup'), bMid(L2, R2, 'Up to 12.5 GB/s throughput'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-AZ: HA primary/standby'), bMid(L2, R2, 'Low latency: SSD storage only'))))
    lines.append(R(merge(bMid(L1, R1, 'StorageVMs: multi-tenancy support'), bMid(L2, R2, 'POSIX: Linux workload lift/shift'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS managed storage infrastructure · SSD arrays per AZ · Regional file system endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FSx             = Amazon FSx; family of managed third-party file system services'))
    lines.append(txt_row('SMB             = Server Message Block; Windows file sharing protocol'))
    lines.append(txt_row('DFS namespace   = Distributed File System namespace; aggregates shares under one path'))
    lines.append(txt_row('Shadow copy     = Windows VSS snapshot; FSx supports application-consistent copies'))
    lines.append(txt_row('Lustre          = High-performance parallel file system; POSIX; used for HPC/ML'))
    lines.append(txt_row('S3 data repo    = FSx for Lustre imports from and exports to an S3 bucket'))
    lines.append(txt_row('FSx ONTAP       = NetApp ONTAP managed by AWS; supports FlexVols and SnapMirror'))
    lines.append(txt_row('StorageVM       = ONTAP SVM; logical isolation within a file system for multi-tenancy'))
    lines.append(txt_row('SnapMirror      = ONTAP replication technology; replicate to on-prem or another FSx'))
    lines.append(txt_row('OpenZFS         = Open source file system with ZFS features; NFS access; low latency'))
    lines.append(txt_row('Multi-AZ FSx    = Primary + standby in different AZs; automatic failover on failure'))
    lines.append(txt_row('CSI driver      = Container Storage Interface; allows EKS pods to mount FSx volumes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-s3', 'docs/cloud/aws/storage/s3/index.md', 'S3 — object storage, bucket configuration, access control, and storage classes')
def _aws_storage_s3():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'S3 — Object Storage'))
    lines.append(txt_row())
    lines.append(txt_row('S3 stores objects in buckets; 11 nines durability; access controlled by policies and ACLs.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Bucket Configuration'), bMid(L2, R2, 'Storage Classes'))))
    lines.append(R(merge(bMid(L1, R1, 'Global namespace: unique name'), bMid(L2, R2, 'Standard: frequent access'))))
    lines.append(R(merge(bMid(L1, R1, 'Region-bound: data stays regional'), bMid(L2, R2, 'Intelligent-Tiering: auto-move'))))
    lines.append(R(merge(bMid(L1, R1, 'Versioning: preserve all versions'), bMid(L2, R2, 'Standard-IA: infrequent access'))))
    lines.append(R(merge(bMid(L1, R1, 'Object Lock: WORM protection'), bMid(L2, R2, 'One Zone-IA: single AZ; cheaper'))))
    lines.append(R(merge(bMid(L1, R1, 'Event notification: Lambda/SNS/SQS'), bMid(L2, R2, 'Glacier/Deep Archive: archival'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Access control via bucket policy + Block Public Access; IAM for programmatic access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Access Control'), bMid(L2, R2, 'Advanced Features'))))
    lines.append(R(merge(bMid(L1, R1, 'Bucket policy: resource-based JSON'), bMid(L2, R2, 'Multipart upload: > 100MB'))))
    lines.append(R(merge(bMid(L1, R1, 'Block Public Access: 4 settings'), bMid(L2, R2, 'Transfer Acceleration: CloudFront'))))
    lines.append(R(merge(bMid(L1, R1, 'SSE-KMS: audit every API call'), bMid(L2, R2, 'Select: SQL filter in-place'))))
    lines.append(R(merge(bMid(L1, R1, 'Presigned URL: time-limited access'), bMid(L2, R2, 'Requester Pays: shift cost'))))
    lines.append(R(merge(bMid(L1, R1, 'VPC endpoint: private access'), bMid(L2, R2, 'Static website: index + error'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS S3 storage infrastructure (3+ AZ) · CloudFront edge for acceleration · Regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Bucket          = Container for objects; globally unique name; region-bound storage'))
    lines.append(txt_row('Object          = File + metadata; identified by key (full path); up to 5TB'))
    lines.append(txt_row('Versioning      = Preserves all versions of an object; delete = delete marker'))
    lines.append(txt_row('Object Lock     = WORM protection; governance or compliance mode; delete prevention'))
    lines.append(txt_row('Bucket policy   = JSON resource policy controlling access to bucket and objects'))
    lines.append(txt_row('Block Public Access= Four settings preventing public ACLs and bucket policies'))
    lines.append(txt_row('Presigned URL   = Time-limited URL granting temporary access to a private object'))
    lines.append(txt_row('Glacier         = S3 archive tier; minutes to hours retrieval; very low storage cost'))
    lines.append(txt_row('Intelligent-Tiering= Auto-moves objects between tiers based on 30-day access pattern'))
    lines.append(txt_row('Multipart upload= Parallel upload of large objects in parts; required > 5GB'))
    lines.append(txt_row('S3 Select       = SQL queries filtering object content server-side; reduces data transfer'))
    lines.append(txt_row('11 nines        = 99.999999999% durability; objects stored across 3+ AZs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-s3-lifecycle', 'docs/cloud/aws/storage/s3-lifecycle/index.md', 'S3 Lifecycle — transition and expiration rules for automated cost management')
def _aws_storage_s3_lifecycle():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'S3 Lifecycle — Automated Tiering & Expiry'))
    lines.append(txt_row())
    lines.append(txt_row('S3 lifecycle rules automate transitioning objects to cheaper tiers and expiring old data.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Rule Scoping'), bMid(L2, R2, 'Transition Rules'))))
    lines.append(R(merge(bMid(L1, R1, 'Prefix: apply to path prefix'), bMid(L2, R2, 'Standard → Standard-IA: 30 days'))))
    lines.append(R(merge(bMid(L1, R1, 'Tags: filter by object tag'), bMid(L2, R2, 'Standard-IA → Glacier: 60 days'))))
    lines.append(R(merge(bMid(L1, R1, 'Object size: min/max filters'), bMid(L2, R2, 'Glacier → Deep Archive: 180 days'))))
    lines.append(R(merge(bMid(L1, R1, 'Versioned: current or noncurrent'), bMid(L2, R2, 'Any class → Intelligent-Tiering'))))
    lines.append(R(merge(bMid(L1, R1, 'Applies to whole bucket or subset'), bMid(L2, R2, 'Min days in class before next move'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Expiration rules delete objects or delete markers; clean up incomplete multipart uploads.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Expiration Rules'), bMid(L2, R2, 'Cost Impact'))))
    lines.append(R(merge(bMid(L1, R1, 'Delete current version after N days'), bMid(L2, R2, 'Standard-IA: 58% cheaper storage'))))
    lines.append(R(merge(bMid(L1, R1, 'Delete noncurrent version after N'), bMid(L2, R2, 'Glacier: 70%+ cheaper than Std'))))
    lines.append(R(merge(bMid(L1, R1, 'Delete expired delete markers'), bMid(L2, R2, 'Deep Archive: lowest cost tier'))))
    lines.append(R(merge(bMid(L1, R1, 'Abort incomplete multipart uploads'), bMid(L2, R2, 'Minimum storage duration charges'))))
    lines.append(R(merge(bMid(L1, R1, 'Max noncurrent versions to retain'), bMid(L2, R2, 'Retrieval fees: IA and Glacier'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS S3 storage tiers · Glacier vault infrastructure · Regional S3 control plane'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Lifecycle rule  = Configuration defining when objects transition or expire'))
    lines.append(txt_row('Transition      = Lifecycle action moving object to a cheaper storage class'))
    lines.append(txt_row('Expiration      = Lifecycle action permanently deleting an object after N days'))
    lines.append(txt_row('Current version = Latest version of an object in a versioned bucket'))
    lines.append(txt_row('Noncurrent version= Previous version after a new upload overwrites; retained by versioning'))
    lines.append(txt_row('Delete marker   = Placeholder created when deleting a versioned object; no data'))
    lines.append(txt_row('Minimum storage = IA: 30 days; Glacier: 90 days; charged even if deleted earlier'))
    lines.append(txt_row('Retrieval fee   = Per-GB charge to access IA or Glacier objects; varies by speed'))
    lines.append(txt_row('Incomplete upload= Multipart upload parts accumulate cost; set expiry rule to clean up'))
    lines.append(txt_row('Tag filter      = Lifecycle rule applies only to objects with specific tag key-value'))
    lines.append(txt_row('Intelligent-Tiering= No retrieval fees; auto-moves between tiers after 30 days inactivity'))
    lines.append(txt_row('Deep Archive    = Lowest cost S3 tier; 12–48h retrieval; for compliance long-term data'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aws-storage-s3-replication', 'docs/cloud/aws/storage/s3-replication/index.md', 'S3 Replication — CRR and SRR configuration, filters, and replication status')
def _aws_storage_s3_replication():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'S3 Replication — CRR & SRR'))
    lines.append(txt_row())
    lines.append(txt_row('S3 replication copies objects asynchronously to destination buckets; versioning required.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Replication Types'), bMid(L2, R2, 'Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'CRR: Cross-Region Replication'), bMid(L2, R2, 'Versioning must be enabled both'))))
    lines.append(R(merge(bMid(L1, R1, 'SRR: Same-Region Replication'), bMid(L2, R2, 'IAM role: source assumes to dest'))))
    lines.append(R(merge(bMid(L1, R1, 'Cross-account: specify dest owner'), bMid(L2, R2, 'Prefix/tag filter: scope objects'))))
    lines.append(R(merge(bMid(L1, R1, 'Batch replication: existing objects'), bMid(L2, R2, 'Storage class: same or override'))))
    lines.append(R(merge(bMid(L1, R1, 'RTC: 99.99% replicated in 15 min'), bMid(L2, R2, 'Encryption: KMS key at dest'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('New objects replicate automatically; existing objects require Batch Replication job.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'What Does Not Replicate'), bMid(L2, R2, 'Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'Objects before rule creation'), bMid(L2, R2, 'CloudWatch: ReplicationLatency'))))
    lines.append(R(merge(bMid(L1, R1, 'Objects in Glacier or Deep Archive'), bMid(L2, R2, 'ReplicationObjects metric'))))
    lines.append(R(merge(bMid(L1, R1, 'Delete markers (by default)'), bMid(L2, R2, 'S3 Replication Dashboard'))))
    lines.append(R(merge(bMid(L1, R1, 'Lifecycle-transitioned objects'), bMid(L2, R2, 'Replication status tag on object'))))
    lines.append(R(merge(bMid(L1, R1, 'Objects already replicated'), bMid(L2, R2, 'EventBridge: replication failure'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS S3 replication infrastructure · Cross-region AWS backbone · Regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CRR             = Cross-Region Replication; copies to a bucket in another region'))
    lines.append(txt_row('SRR             = Same-Region Replication; copies within same region for log aggregation'))
    lines.append(txt_row('RTC             = Replication Time Control; SLA 99.99% replicated within 15 minutes'))
    lines.append(txt_row('Batch replication= Replicates existing objects using S3 Batch Operations job'))
    lines.append(txt_row('Replication status= Object metadata: PENDING, COMPLETED, FAILED, or REPLICA'))
    lines.append(txt_row('Delete marker replication= Optional: replicate delete markers to keep buckets in sync'))
    lines.append(txt_row('Replica ownership= Option to give replica ownership to destination account'))
    lines.append(txt_row('Bidirectional   = Two rules (A→B + B→A) creates active-active replication'))
    lines.append(txt_row('Replication role= IAM role that S3 assumes to read from source and write to dest'))
    lines.append(txt_row('Multi-destination= One source bucket replicating to multiple destination buckets'))
    lines.append(txt_row('Encryption replication= Replicated objects can be re-encrypted with destination KMS key'))
    lines.append(txt_row('Async replication= Objects replicated asynchronously; dest lags source slightly'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines

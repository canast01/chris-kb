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

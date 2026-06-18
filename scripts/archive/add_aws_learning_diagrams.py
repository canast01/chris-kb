#!/usr/bin/env python3
"""
Add AWS CLF-C02 exam-aligned learning/concept diagrams to AWS KB pages.
Run from repo root: python3 scripts/add_aws_learning_diagrams.py
"""
import os

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
AWS = os.path.join(DOCS, 'cloud', 'aws')
W = 103  # content width between the two outer-border chars

# ── Box drawing helpers ───────────────────────────────────────────────────────

def blank():
    return '│' + ' ' * W + '│'

def line(text):
    return '│  ' + text.ljust(W - 2) + '│'

def top(title):
    inner = ' ' + title + ' '
    pad = W - len(inner)
    l, r = pad // 2, pad - pad // 2
    return '┌' + '─' * l + inner + '─' * r + '┐'

def bot():
    return '└' + '─' * W + '┘'

def arrows():
    # two down-arrows at approx 1/4 and 3/4 of content width
    return '│' + ' ' * 26 + '▼' + ' ' * 49 + '▼' + ' ' * 26 + '│'

def itop():
    return '│   ┌' + '─' * 46 + '┐  ┌' + '─' * 45 + '┐   │'

def ibot():
    return '│   └' + '─' * 46 + '┘  └' + '─' * 45 + '┘   │'

def ititle(left, right):
    return '│   │' + left.center(46) + '│  │' + right.center(45) + '│   │'

def irow(left, right):
    return '│   │' + left.ljust(46) + '│  │' + right.ljust(45) + '│   │'

# ── Section builder ───────────────────────────────────────────────────────────

def section(heading, diag_lines):
    return ['\n---\n', '## ' + heading + '\n', '```'] + diag_lines + ['```\n']

def append_sections(path, sections):
    with open(path) as f:
        content = f.read()
    new_parts = []
    for sec in sections:
        h = next(x.strip() for x in sec if x.startswith('## '))
        if h in content:
            print('  SKIP: ' + h)
        else:
            new_parts.extend(sec)
    if not new_parts:
        print('  Nothing new for ' + os.path.relpath(path))
        return
    with open(path, 'a') as f:
        f.write('\n'.join(new_parts))
    print('  Updated ' + os.path.relpath(path))


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: architecture/how-it-works  (5 diagrams)
# ═══════════════════════════════════════════════════════════════════════════════

def d_global_infra():
    return section('AWS Global Infrastructure', [
        top('AWS Global Infrastructure — Regions, AZs, and Edge Locations'),
        blank(),
        line('  33+ Regions, 105+ AZs, 400+ CloudFront edge locations; foundation of all AWS services.'),
        blank(),
        itop(),
        ititle('       AWS Regions (33+)          ', '      Availability Zones (105+)      '),
        irow('  Isolated geographic area (sovereign)', '  One or more independent data centres'),
        irow('  Contains 2 to 6 Availability Zones', '  Separate power, cooling, networking'),
        irow('  Data stays in Region by default   ', '  Low-latency fibre links between AZs'),
        irow('  Choose by: latency, compliance, $  ', '  Fault-isolated; independent failure'),
        irow('  Opt-in Regions disabled by default ', '  AZ ID is consistent cross-account  '),
        ibot(),
        blank(),
        line('  Regions are data-sovereignty boundaries; AZs provide HA within a Region.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('       Edge Locations (400+)       ', '      Special Infrastructure         '),
        irow('  CloudFront PoP: cache + WAF/Shield ', '  Local Zone: sub-ms latency in city '),
        irow('  Route 53: anycast DNS resolution   ', '  Wavelength: 5G mobile edge compute '),
        irow('  Lambda@Edge: code at CloudFront PoP', '  Outposts: AWS rack in customer DC  '),
        irow('  Global Accelerator: Anycast IPs    ', '  GovCloud US: FedRAMP/ITAR compliant'),
        irow('  Shield Standard: free L3/L4 DDoS   ', '  China: separate partition, ICP req '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS data centres worldwide · submarine cables · backbone fibre · internet exchange points'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Region         = Isolated geo area; 2+ AZs; data stays in Region; 33+ globally'),
        line('  AZ             = Availability Zone; 1+ DCs with independent power/cooling/network'),
        line('  Edge Location  = CloudFront PoP; caches content; applies WAF and Shield at edge'),
        line('  Local Zone     = AWS infrastructure extension to major cities for low-latency apps'),
        line('  Wavelength     = AWS compute embedded in telecom 5G network for ultra-low latency'),
        line('  Outposts       = AWS rack on-premises; extends AWS APIs to customer data centre'),
        line('  GovCloud       = US-only Regions meeting FedRAMP High, ITAR, DoD requirements'),
        line('  Global Accelerator = Anycast IPs routing users to nearest healthy AWS endpoint'),
        line('  PoP            = Point of Presence; CloudFront edge node for caching/DDoS defence'),
        line('  AZ ID          = Consistent cross-account AZ identifier (e.g., use1-az1)'),
        line('  Opt-in Region  = Region disabled by default; must be enabled per account'),
        line('  Partition      = Isolated AWS infrastructure group: standard, GovCloud, China'),
        blank(),
        bot(),
    ])


def d_shared_responsibility():
    return section('AWS Shared Responsibility Model', [
        top('AWS Shared Responsibility Model — Security OF vs IN the Cloud'),
        blank(),
        line('  AWS secures the infrastructure; customers secure what they run on it.'),
        blank(),
        itop(),
        ititle('    AWS Responsibility (OF the cloud) ', '  Customer Responsibility (IN the cloud)'),
        irow('  Physical hardware + data centres    ', '  Data: classification and encryption'),
        irow('  Network and hypervisor layer         ', '  Identity and access management     '),
        irow('  Compute / storage / database infra  ', '  OS patches (for EC2/IaaS only)     '),
        irow('  Regions, AZs, and edge locations    ', '  Application code and configuration '),
        irow('  Managed service security (RDS/S3)   ', '  Network config: SGs, NACLs, routes '),
        ibot(),
        blank(),
        line('  For managed services (RDS, Lambda), AWS takes more responsibility; EC2 is IaaS.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  IaaS (EC2): Customer manages most  ', '  PaaS/SaaS: AWS manages most        '),
        irow('  Guest OS: customer patches/updates  ', '  RDS: OS/engine patched by AWS      '),
        irow('  Security groups: customer configures', '  S3: infra/durability managed by AWS'),
        irow('  Application: customer deploys/secures', '  Lambda: runtime managed by AWS     '),
        irow('  IAM roles: customer defines access  ', '  DynamoDB: fully managed by AWS     '),
        irow('  Encryption: customer enables/manages', '  Customer manages data and IAM only '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS-owned hardware, data centres, network; customers have no physical access'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Shared model    = AWS owns security of the cloud; customer owns security in the cloud'),
        line('  IaaS            = Infrastructure as a Service; e.g., EC2 — customer manages OS up'),
        line('  PaaS            = Platform as a Service; e.g., Elastic Beanstalk, RDS'),
        line('  SaaS            = Software as a Service; e.g., Chime, WorkMail'),
        line('  Security of     = Hardware, software, networking, facilities managed by AWS'),
        line('  Security in     = Data, platform, applications, identity managed by customer'),
        line('  Managed service = AWS handles patching, HA, backups; customer handles data/access'),
        line('  Encryption keys = Customer may manage via KMS CMK; AWS manages default keys'),
        blank(),
        bot(),
    ])


def d_well_architected():
    return section('AWS Well-Architected Framework — 6 Pillars', [
        top('AWS Well-Architected Framework — 6 Pillars'),
        blank(),
        line('  Framework guides cloud architecture decisions; assessed via Well-Architected Tool.'),
        blank(),
        itop(),
        ititle('  Operational Excellence              ', '  Security                           '),
        irow('  Run + monitor workloads effectively  ', '  Protect data, systems, and assets  '),
        irow('  Improve operations through small     ', '  Apply security at all layers       '),
        irow('  frequent reversible changes          ', '  Enable traceability via logging    '),
        irow('  Annotate docs; anticipate failure    ', '  Automate security best practices   '),
        irow('  Perform operations as code (IaC)     ', '  Protect data in transit and at rest'),
        ibot(),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Reliability                         ', '  Performance Efficiency              '),
        irow('  Recover from failures automatically  ', '  Use compute resources efficiently  '),
        irow('  Scale horizontally for availability  ', '  Select right resource types/sizes  '),
        irow('  Manage change via automation          ', '  Monitor performance; adapt/evolve  '),
        irow('  Test recovery procedures regularly   ', '  Use advanced tech democratized     '),
        irow('  Design for multi-AZ and multi-region ', '  Go global quickly with AWS Regions '),
        ibot(),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Cost Optimization                   ', '  Sustainability (6th pillar, 2021)   '),
        irow('  Avoid unnecessary costs              ', '  Minimise environmental impact      '),
        irow('  Measure efficiency; use managed svcs ', '  Understand your impact footprint   '),
        irow('  Analyse and attribute expenditure    ', '  Maximise resource utilisation      '),
        irow('  Use Reserved/Savings Plans wisely    ', '  Use managed services (lower footpt)'),
        irow('  Right-size and eliminate idle rsrcs  ', '  Choose Regions with clean energy   '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  All 6 pillars apply to services running on AWS hardware in Regions and AZs'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Well-Architected Tool  = Free AWS service to review workloads against 6 pillars'),
        line('  Well-Architected Review = Formal assessment producing improvement action plan'),
        line('  Pillar                 = One of 6 design domains; each has design principles + questions'),
        line('  High Risk Issue (HRI)  = WAF finding requiring immediate attention'),
        line('  Medium Risk Issue (MRI)= WAF finding to address in upcoming sprint'),
        line('  IaC                    = Infrastructure as Code; operations as code principle'),
        line('  Sustainability pillar  = Added 2021; focuses on energy use and carbon footprint'),
        blank(),
        bot(),
    ])


def d_caf():
    return section('AWS Cloud Adoption Framework — 6 Perspectives', [
        top('AWS Cloud Adoption Framework (CAF) — 6 Perspectives'),
        blank(),
        line('  CAF organises guidance into Business and Technology perspectives for cloud adoption.'),
        blank(),
        itop(),
        ititle('  Business Perspectives (outcomes)   ', '  Technology Perspectives (delivery)  '),
        irow('  Business: value / strategy / KPIs   ', '  Platform: architecture / IaC / CI/CD'),
        irow('  People: change mgmt / org readiness ', '  Security: IAM / detection / response'),
        irow('  Governance: risk / compliance / fin  ', '  Operations: monitoring / ITSM / DR  '),
        ibot(),
        blank(),
        line('  Business side drives why; Technology side drives how. Both needed for success.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  CAF Capabilities by Perspective     ', '  Transformation Domains              '),
        irow('  Business: portfolio mgmt, data monet ', '  Technology: modernise IT platforms  '),
        irow('  People: HR trans, leadership align   ', '  Process: digitise, automate, optimise'),
        irow('  Governance: prog mgmt, benefit real  ', '  Organisation: lead cloud teams      '),
        irow('  Platform: platform eng, data estate  ', '  Product: innovate, experiment fast  '),
        irow('  Security: threat intel, vuln mgmt    ', '  Outcomes: reduce cost + risk, speed '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  CAF is a methodology; underlying infra = AWS Regions, AZs, and managed services'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  CAF          = Cloud Adoption Framework; AWS guidance for org cloud transformation'),
        line('  Perspective  = One of 6 CAF domains grouping related capabilities'),
        line('  Capability   = Specific business or technology ability needed for cloud adoption'),
        line('  Business side= Business + People + Governance; aligned to business outcomes'),
        line('  Tech side    = Platform + Security + Operations; aligned to technical delivery'),
        line('  Transformation domain = Area of organisational change: technology, process, org, product'),
        line('  MRA          = Migration Readiness Assessment; CAF-based readiness scoring'),
        blank(),
        bot(),
    ])


def d_seven_rs():
    return section('AWS Migration Strategies — 7 Rs', [
        top('AWS Migration Strategies — The 7 Rs'),
        blank(),
        line('  7 Rs describe how an application moves to or is handled in the cloud migration.'),
        blank(),
        itop(),
        ititle('     Retire / Retain (no move)       ', '     Rehost / Relocate (lift-shift)   '),
        irow('  Retire: decommission the app         ', '  Rehost: move to EC2 with no changes '),
        irow('  No migration needed; end of life     ', '  Fastest path; no refactoring needed'),
        irow('  Retain: keep on-premises for now     ', '  Relocate: move VMware VMs to VMC   '),
        irow('  Revisit later; compliance/technical  ', '  Hyper-V/VMware to cloud via migrate'),
        irow('  Review at next migration cycle       ', '  Good for large legacy app portfolios'),
        ibot(),
        blank(),
        line('  Retire/Retain need no cloud resources; Rehost/Relocate need minimal changes.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Replatform / Repurchase             ', '  Refactor / Re-architect             '),
        irow('  Replatform: lift-tinker-shift        ', '  Refactor: re-write as cloud-native  '),
        irow('  e.g., RDS instead of self-managed DB ', '  e.g., move to Lambda/containers/EKS '),
        irow('  Minor optimisations; same app code   ', '  Highest effort; highest cloud value '),
        irow('  Repurchase: drop and shop to SaaS    ', '  Best for apps needing scale/agility '),
        irow('  e.g., CRM on-prem to Salesforce      ', '  Microservices, serverless, event-drv'),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS Regions and AZs host migrated workloads; on-prem DC remains for Retain/Retire'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Retire      = Decommission; no longer needed; remove from scope'),
        line('  Retain      = Keep on-premises; revisit later; compliance or technical blocker'),
        line('  Rehost      = Lift and shift to EC2; no application changes; fastest'),
        line('  Relocate    = Move to cloud without buying new hardware (e.g., VMware Cloud on AWS)'),
        line('  Replatform  = Lift tinker and shift; minor optimisations without code changes'),
        line('  Repurchase  = Replace with SaaS product; drop and shop; e.g., on-prem CRM to SaaS'),
        line('  Refactor    = Re-architect as cloud-native; highest effort; microservices/serverless'),
        line('  MGN         = AWS Application Migration Service; automates rehost migrations'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: networking/vpc  (3 diagrams)
# ═══════════════════════════════════════════════════════════════════════════════

def d_vpc_subnet():
    return section('VPC Subnet Architecture', [
        top('VPC Subnet Architecture — Public, Private, and Data Tiers'),
        blank(),
        line('  Multi-tier VPC: public (internet-facing), private (app), data (DB) subnets per AZ.'),
        blank(),
        itop(),
        ititle('    Public Subnet (internet-facing)  ', '    Private Subnet (app/compute tier) '),
        irow('  ALB: routes inbound internet traffic ', '  EC2, ECS, EKS workloads live here  '),
        irow('  NAT Gateway: private outbound traffic', '  No direct inbound internet path    '),
        irow('  Bastion host (if needed)             ', '  Route table: 0.0.0.0/0 via NAT GW  '),
        irow('  Route table: 0.0.0.0/0 via IGW       ', '  Security groups: allow from ALB SG  '),
        irow('  IGW: internet gateway attached to VPC', '  Connects to data tier via SG rules  '),
        ibot(),
        blank(),
        line('  IGW enables internet; NAT GW enables private outbound without public IPs.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Security Groups (instance-level)    ', '  NACLs (subnet-level)                '),
        irow('  Stateful: return traffic auto-allowed', '  Stateless: must allow both directions'),
        irow('  Attached to ENI (per-instance)       ', '  Applied to subnet boundary          '),
        irow('  Allow rules only; no explicit deny   ', '  Allow and deny rules both available '),
        irow('  Rules evaluated together (OR logic)  ', '  Rules evaluated in number order     '),
        irow('  Default SG: allows all from same SG  ', '  Default NACL: allows all traffic    '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS regional network fabric · AZ data centres · physical NICs backing ENIs'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  IGW         = Internet Gateway; allows public subnets to reach the internet'),
        line('  NAT Gateway = Managed NAT; private subnet instances can reach internet outbound only'),
        line('  Security Group = Stateful firewall at the instance (ENI) level; allow rules only'),
        line('  NACL        = Network ACL; stateless firewall at subnet boundary; allow + deny'),
        line('  Stateful    = Return traffic automatically allowed; no explicit rule needed'),
        line('  Stateless   = Every direction needs an explicit rule; no tracking'),
        line('  Route table = Per-subnet list of destinations and their targets (IGW, NAT, etc.)'),
        line('  ENI         = Elastic Network Interface; virtual NIC; SG is attached to ENI'),
        line('  Bastion host= EC2 in public subnet used as SSH jump host to private EC2 instances'),
        blank(),
        bot(),
    ])


def d_network_connectivity():
    return section('AWS Network Connectivity Options', [
        top('AWS Network Connectivity Options'),
        blank(),
        line('  Multiple options connect on-prem to AWS or VPCs to each other; choose by need.'),
        blank(),
        itop(),
        ititle('  Internet Gateway / NAT Gateway      ', '  Site-to-Site VPN                    '),
        irow('  IGW: public subnet internet access   ', '  IPSec tunnel over the public internet'),
        irow('  NAT GW: private outbound only (no in)', '  Virtual Private Gateway on VPC side '),
        irow('  Managed by AWS; HA within AZ         ', '  Customer Gateway on on-prem side    '),
        irow('  NAT GW: charged per GB + hourly       ', '  Bandwidth: up to ~1.25 Gbps per VPN '),
        irow('  Scales automatically; no maintenance  ', '  Low cost; quick to set up; encrypted'),
        ibot(),
        blank(),
        line('  VPN is encrypted but uses shared internet; Direct Connect is dedicated private link.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  AWS Direct Connect (DX)             ', '  PrivateLink / Transit Gateway        '),
        irow('  Dedicated physical link to AWS        ', '  PrivateLink: expose service to VPC   '),
        irow('  1 Gbps or 10 Gbps ports available    ', '  No internet; no peering; private IP  '),
        irow('  Lower latency + consistent bandwidth  ', '  Endpoint in consumer VPC; NLB backed '),
        irow('  DX Gateway: one DX to many Regions   ', '  Transit Gateway: hub-spoke for VPCs  '),
        irow('  Not encrypted by default; use IPSec  ', '  TGW: transitive routing; centrally   '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS backbone fibre · DX colocation partner facilities · physical DX ports'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Site-to-Site VPN = IPSec encrypted tunnel from on-prem to VPC via internet'),
        line('  Direct Connect   = Dedicated private physical connection; bypasses internet'),
        line('  VGW              = Virtual Private Gateway; VPN/DX attachment point on VPC'),
        line('  CGW              = Customer Gateway; on-prem router configuration in AWS'),
        line('  DX Gateway       = Connect one Direct Connect to VPCs in multiple Regions'),
        line('  Transit Gateway  = Regional hub; connects many VPCs and on-prem via single hub'),
        line('  PrivateLink      = Expose a service privately; no internet traversal; NLB-backed'),
        line('  VPC Peering      = Direct 1:1 routing between two VPCs; not transitive'),
        line('  Transitive routing= Traffic A→B→C; TGW supports it; VPC Peering does not'),
        blank(),
        bot(),
    ])


def d_route53():
    return section('Route 53 Routing Policies', [
        top('Route 53 Routing Policies — Comparison'),
        blank(),
        line('  Route 53 supports 7 routing policies; choose based on traffic distribution goal.'),
        blank(),
        itop(),
        ititle('    Policy                            ', '  Use Case / Behaviour                '),
        irow('  Simple                               ', '  Single record; basic DNS; no health '),
        irow('  Weighted                             ', '  Split traffic by % (A/B testing)    '),
        irow('  Latency                              ', '  Route to lowest-latency AWS Region  '),
        irow('  Failover                             ', '  Primary + secondary with health chk '),
        irow('  Geolocation                          ', '  Route by user country or continent  '),
        ibot(),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('    Policy (continued)                ', '  Use Case / Behaviour                '),
        irow('  Geoproximity                         ', '  Route by geographic proximity; bias '),
        irow('  Multivalue Answer                    ', '  Return up to 8 healthy records      '),
        irow('  Health checks                        ', '  Monitor endpoints; failover if down '),
        irow('  Alias records                        ', '  Point to AWS resources (ALB, CF, S3)'),
        irow('  Private hosted zone                  ', '  DNS inside VPC; internal resolution '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  Route 53 anycast infrastructure · 100+ edge PoPs globally · DNSSEC support'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Simple routing     = Single resource; multiple values returned randomly (no health)'),
        line('  Weighted routing   = Assign weights (0-255) to split traffic; A/B testing'),
        line('  Latency routing    = Measure latency to AWS Regions; send user to lowest latency'),
        line('  Failover routing   = Active/passive; primary serves traffic; secondary if unhealthy'),
        line('  Geolocation        = Route based on user geographic location (country, continent)'),
        line('  Geoproximity       = Route by proximity to resource; bias shifts boundary'),
        line('  Multivalue         = Up to 8 healthy records returned; basic load distribution'),
        line('  Health check       = HTTP/HTTPS/TCP probe; marks record unhealthy if failing'),
        line('  Alias record       = Native Route 53 record type pointing to AWS service endpoints'),
        line('  Private hosted zone= DNS zone only resolvable inside VPC or associated VPCs'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: identity/iam  (2 diagrams)
# ═══════════════════════════════════════════════════════════════════════════════

def d_iam_model():
    return section('IAM Identity Model', [
        top('IAM Identity Model — Users, Groups, Roles, Policies, and Identity Center'),
        blank(),
        line('  IAM controls all API access; prefer roles over users; use Identity Center for humans.'),
        blank(),
        itop(),
        ititle('  IAM Principals                      ', '  Policy Types                        '),
        irow('  User: human or programmatic access   ', '  Identity policy: on user/role/group '),
        irow('  Group: users collection (no nesting) ', '  Resource policy: on S3/KMS/SQS      '),
        irow('  Role: temporary creds via STS        ', '  SCP: OU-level max permission cap    '),
        irow('  Service role: assumed by AWS service ', '  Permission boundary: per-principal  '),
        irow('  Root user: full access; protect+avoid', '  Session policy: AssumeRole context  '),
        ibot(),
        blank(),
        line('  Effective permissions = intersection of all applicable policy types; deny wins.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  IAM Identity Center (SSO)           ', '  MFA and Credential Types            '),
        irow('  Central SSO for human access         ', '  Virtual MFA: Google Authenticator   '),
        irow('  SAML 2.0 federation to external IdP  ', '  Hardware MFA: YubiKey, hardware key '),
        irow('  Permission sets map to IAM roles     ', '  TOTP code required at login         '),
        irow('  No long-lived keys for humans        ', '  Root MFA: mandatory best practice   '),
        irow('  AWS SSO replaces creating IAM users  ', '  Access keys: programmatic; rotate   '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  IAM is a global service (no Region) · STS issues temporary tokens · free service'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  IAM User        = Long-lived identity; access key + secret or console password'),
        line('  IAM Role        = Assumable identity; temp creds via STS; no long-lived keys'),
        line('  IAM Group       = Collection of users sharing policies; groups cannot be nested'),
        line('  Trust policy    = Defines who can assume the role (Principal in trust document)'),
        line('  Managed policy  = Standalone JSON document; reusable across principals'),
        line('  Inline policy   = Embedded in user/role/group; deleted with the principal'),
        line('  Identity Center = AWS SSO; preferred for human access; replaces IAM users'),
        line('  Permission set  = Bundle of IAM policies assigned to user/group in an account'),
        line('  SAML 2.0        = Federation standard; links IdP (Okta/AD) to AWS'),
        line('  STS             = Security Token Service; issues temporary credentials for roles'),
        blank(),
        bot(),
    ])


def d_policy_evaluation():
    return section('IAM Policy Evaluation Order', [
        top('IAM Policy Evaluation — Decision Flow'),
        blank(),
        line('  Every AWS API call follows this exact evaluation order; explicit deny always wins.'),
        blank(),
        itop(),
        ititle('  Evaluation Steps (in order)         ', '  Details                             '),
        irow('  1. Explicit Deny in any policy       ', '  Any deny = DENY; no override        '),
        irow('  2. AWS Organizations SCP             ', '  Must allow the action at OU level   '),
        irow('  3. Resource-based policy             ', '  S3 bucket/KMS key/SQS policy check  '),
        irow('  4. IAM Permission Boundary           ', '  Sets maximum allowed permissions    '),
        irow('  5. Session Policy (AssumeRole)       ', '  Further limits role session          '),
        ibot(),
        blank(),
        line('  After step 5: if no explicit allow found in identity policy, default = DENY.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Common Deny Scenarios               ', '  Common Allow Scenarios              '),
        irow('  SCP blocks action in OU              ', '  SCP allows + identity policy allows '),
        irow('  Explicit Deny in identity policy     ', '  Resource policy grants cross-account '),
        irow('  Permission boundary excludes action  ', '  Role trust policy allows AssumeRole '),
        irow('  No identity policy allows action     ', '  Session + identity policy both allow '),
        irow('  KMS key policy denies user access    ', '  Least privilege: narrowest allow set '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  IAM policy engine (global service) · STS · CloudTrail logging all API decisions'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Explicit Deny   = Deny statement in any policy; overrides all allows; step 1'),
        line('  SCP             = Service Control Policy; restricts max perms at OU/account level'),
        line('  Resource policy = Policy attached to a resource (S3, KMS); can allow cross-account'),
        line('  Permission boundary = IAM policy capping the maximum perms a principal can have'),
        line('  Session policy  = Passed during AssumeRole; further restricts session permissions'),
        line('  Identity policy = Policy attached to user/group/role via managed or inline'),
        line('  Default deny    = Implicit deny when no explicit allow is found; not logged'),
        line('  Cross-account   = Resource policy can grant access from another AWS account'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: compute/ec2  (4 diagrams)
# ═══════════════════════════════════════════════════════════════════════════════

def d_ec2_purchase():
    return section('EC2 Purchase Options', [
        top('EC2 Purchase Options — Discount and Commitment Comparison'),
        blank(),
        line('  Six purchase options balance cost, flexibility, and availability guarantees.'),
        blank(),
        itop(),
        ititle('  On-Demand and Reserved               ', '  Savings Plans                       '),
        irow('  On-Demand: no commitment, per-second  ', '  Compute SP: EC2+Fargate+Lambda      '),
        irow('  Full price; start/stop anytime         ', '  Any instance type/family/Region     '),
        irow('  Standard Reserved: 1 or 3 yr commit   ', '  Up to 66% discount; most flexible   '),
        irow('  Same type only; up to 72% discount    ', '  EC2 Instance SP: same family/Region '),
        irow('  Convertible Reserved: exchange allowed ', '  Up to 72% discount; less flexible   '),
        ibot(),
        blank(),
        line('  Savings Plans and Reserved Instances both require upfront commitment for discount.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Spot Instances                       ', '  Dedicated Options                   '),
        irow('  Uses spare AWS capacity               ', '  Dedicated Host: physical server     '),
        irow('  Up to 90% discount off On-Demand      ', '  BYOL licensing; full host control   '),
        irow('  2-minute interruption notice from AWS ', '  Dedicated Instance: on dedicated HW '),
        irow('  Not for critical/persistent workloads  ', '  Capacity Reservation: guarantee AZ  '),
        irow('  Spot Fleets: mix types for target cap  ', '  No discount; ensures capacity avail '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  EC2 runs on Nitro hypervisor · Nitro cards offload I/O · physical hosts in AZs'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  On-Demand         = Full price; no commitment; billed per second after first minute'),
        line('  Standard RI       = 1/3yr commit to specific type; up to 72% off; not exchangeable'),
        line('  Convertible RI    = 1/3yr commit; can exchange instance family/OS/tenancy; 66% off'),
        line('  Compute Savings Plan = $/hr commitment; applies to EC2/Fargate/Lambda; 66% off'),
        line('  EC2 Instance SP   = $/hr for a specific family and Region; up to 72% off'),
        line('  Spot              = Spare capacity; up to 90% off; can be reclaimed with 2-min notice'),
        line('  Spot interruption = AWS reclaims Spot with 2-minute warning; use checkpointing'),
        line('  Dedicated Host    = Physical server; BYOL; see sockets/cores; compliance isolation'),
        line('  Capacity Reservation= Reserve EC2 capacity in a specific AZ; no commitment discount'),
        blank(),
        bot(),
    ])


def d_instance_families():
    return section('EC2 Instance Type Families', [
        top('EC2 Instance Type Families — Workload Optimisation'),
        blank(),
        line('  Instance family letter tells you the workload optimisation; generation number follows.'),
        blank(),
        itop(),
        ititle('  General Purpose                      ', '  Compute Optimised                   '),
        irow('  m: balanced CPU/memory (m7i, m6i)    ', '  c: high compute-to-memory (c7i,c6i) '),
        irow('  t: burstable with CPU credits (t3)   ', '  HPC, batch jobs, ML inference       '),
        irow('  Web servers, app servers, dev/test    ', '  Gaming, ad serving, media encode    '),
        irow('  a: ARM-based Graviton (cost-efficient)', '  c7g: Graviton3; best $/vCPU compute '),
        irow('  mac: macOS dev environments (M1/M2)  ', '  Prefix c = compute optimised family '),
        ibot(),
        blank(),
        line('  Family letter = optimisation type; generation = newer hardware; suffix = features.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Memory Optimised                     ', '  Storage / Accelerated Computing     '),
        irow('  r: high RAM (r7i up to 768 GiB)      ', '  i: NVMe SSD storage (i4i, i3en)     '),
        irow('  x: extra large memory (x2idn)        ', '  d: dense HDD storage (d3en)         '),
        irow('  z: high-freq core + memory (z1d)     ', '  p: GPU for ML training (p4d, p5)    '),
        irow('  In-memory DB, Redis, SAP HANA         ', '  g: GPU for ML inference (g5, g4dn) '),
        irow('  Real-time big data analytics          ', '  trn: Trainium (AWS ML chip)         '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  Nitro hypervisor · Nitro cards · physical CPUs (Intel/AMD/Graviton) · NVMe/GPU'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Family          = Letter prefix (m, c, r, i, p, g) indicating workload optimisation'),
        line('  Generation      = Number after family (e.g., 7 in m7i); higher = newer hardware'),
        line('  Processor       = Suffix: i=Intel, a=AMD, g=Graviton (AWS ARM); no suffix=any'),
        line('  Size            = nano, micro, small, medium, large, xlarge, 2xlarge, etc.'),
        line('  Burstable (t)   = Earns CPU credits when idle; bursts above baseline when credits exist'),
        line('  Graviton        = AWS-designed ARM chips (g suffix); up to 40% better price/performance'),
        line('  Nitro hypervisor= AWS-built hypervisor offloading storage/network to dedicated silicon'),
        line('  Bare metal       = Physical host access; no hypervisor; for licensing or performance'),
        blank(),
        bot(),
    ])


def d_compute_services():
    return section('Compute Services Comparison', [
        top('AWS Compute Services — EC2 vs Containers vs Serverless'),
        blank(),
        line('  Choose compute based on control needed, workload type, and management overhead.'),
        blank(),
        itop(),
        ititle('  EC2 (IaaS — full control)           ', '  Lambda (FaaS — serverless)          '),
        irow('  Launch VMs; choose OS and instance    ', '  Event-driven; run code, not servers '),
        irow('  You manage OS, patches, agents        ', '  15 minute max timeout per invocation'),
        irow('  Persistent; auto scaling groups       ', '  Auto-scales to thousands instantly  '),
        irow('  Any workload: persistent, stateful    ', '  Pay per request + duration (ms)     '),
        irow('  Most control; most management effort  ', '  Supports Python, Node, Java, Go, etc'),
        ibot(),
        blank(),
        line('  EC2 = most control; Lambda = least management; containers sit in the middle.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  ECS / Fargate / EKS (containers)    ', '  Other Compute Services               '),
        irow('  ECS: Docker on AWS; AWS control plane', '  Elastic Beanstalk: PaaS; deploy code'),
        irow('  Fargate: serverless containers (ECS)  ', '  Lightsail: simple VPS for small apps'),
        irow('  No EC2 management in Fargate mode     ', '  App Runner: deploy web app from code '),
        irow('  EKS: managed Kubernetes on AWS        ', '  Batch: managed batch HPC computing  '),
        irow('  ECR: private container image registry ', '  Outposts: EC2 + ECS on-premises     '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  Nitro hypervisor · container runtime on EC2 hosts · Lambda micro-VMs (Firecracker)'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  EC2             = Elastic Compute Cloud; virtual server; IaaS; full OS control'),
        line('  Lambda          = Serverless function; event-triggered; no server management'),
        line('  ECS             = Elastic Container Service; run Docker containers on AWS'),
        line('  Fargate         = Serverless compute engine for ECS/EKS; no EC2 to manage'),
        line('  EKS             = Elastic Kubernetes Service; managed K8s control plane on AWS'),
        line('  Elastic Beanstalk= PaaS; upload code; AWS provisions EC2/LB/ASG/RDS automatically'),
        line('  Lightsail       = Simple VPS with fixed monthly pricing; good for small workloads'),
        line('  Firecracker     = AWS micro-VM technology powering Lambda and Fargate isolation'),
        blank(),
        bot(),
    ])


def d_autoscaling_lb():
    return section('EC2 Auto Scaling and Load Balancing', [
        top('EC2 Auto Scaling + Elastic Load Balancing — Architecture'),
        blank(),
        line('  ALB/NLB distribute traffic; Auto Scaling Group adjusts capacity automatically.'),
        blank(),
        itop(),
        ititle('  Elastic Load Balancers               ', '  Load Balancer Selection              '),
        irow('  ALB: Layer 7 HTTP/HTTPS/gRPC          ', '  ALB: path/host routing; microservices'),
        irow('  Path routing: /api to API target grp  ', '  ALB: WAF integration; TLS termination'),
        irow('  Host routing: api.x.com to target grp ', '  NLB: TCP/UDP/TLS; ultra-low latency '),
        irow('  NLB: Layer 4 TCP/UDP; static Elastic  ', '  NLB: static IPs; for firewall rules  '),
        irow('  GWLB: inline L3 for virtual appliances', '  GWLB: transparent for IDS/IPS/FW    '),
        ibot(),
        blank(),
        line('  ALB is preferred for HTTP workloads; NLB for extreme performance or static IPs.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Auto Scaling Group (ASG)             ', '  Scaling Policies                    '),
        irow('  Min / Desired / Max capacity settings ', '  Target Tracking: maintain CPU at 60%'),
        irow('  Launch template: AMI + type + SGs     ', '  Step Scaling: scale by steps on alrm'),
        irow('  Health check: LB or EC2 status        ', '  Scheduled: scale at known times      '),
        irow('  Multi-AZ: instances spread across AZs ', '  Predictive: ML forecast future load  '),
        irow('  Warm pools: pre-warm instances quickly ', '  Cool-down: prevent scale thrashing   '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  ALB/NLB nodes in each AZ · EC2 instances on Nitro hosts · Route 53 DNS'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  ALB             = Application Load Balancer; Layer 7; path/host/header routing'),
        line('  NLB             = Network Load Balancer; Layer 4; static IPs; ultra-low latency'),
        line('  GWLB            = Gateway Load Balancer; transparent inline Layer 3 for appliances'),
        line('  Target Group    = Set of targets (EC2/Lambda/IP) that LB routes requests to'),
        line('  Auto Scaling Group = EC2 fleet with min/desired/max; replaces unhealthy instances'),
        line('  Launch Template = EC2 config snapshot (AMI, type, SG, user data) used by ASG'),
        line('  Target Tracking = Scaling policy that adjusts capacity to hit a target metric'),
        line('  Warm Pool       = Pool of pre-initialised instances to reduce scale-out latency'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: storage/s3  (2 diagrams)
# ═══════════════════════════════════════════════════════════════════════════════

def d_s3_classes():
    return section('S3 Storage Classes', [
        top('S3 Storage Classes — Availability, Retrieval, and Cost'),
        blank(),
        line('  Seven storage classes balance retrieval latency, availability, and storage cost.'),
        blank(),
        itop(),
        ititle('  Frequent Access Classes              ', '  Infrequent Access Classes           '),
        irow('  Standard: 99.99% avail; 3+ AZ        ', '  Standard-IA: 99.9%; 3+ AZ; fee/get '),
        irow('  Standard: no retrieval fee; default   ', '  Standard-IA: 30-day minimum storage '),
        irow('  Intelligent-Tiering: auto-moves tiers ', '  One Zone-IA: 99.5%; 1 AZ; cheaper  '),
        irow('  IT: monitoring fee; no retrieval fee  ', '  One Zone-IA: re-creatable data only '),
        irow('  IT: moves after 30 days of no access  ', '  Both: per-GB retrieval fee applies  '),
        ibot(),
        blank(),
        line('  Standard for frequent access; IA tiers for data accessed less than once a month.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Glacier Archive Classes              ', '  Retrieval Comparison                '),
        irow('  Glacier Instant: ms retrieval; 90-day', '  Standard: ms; no retrieval fee      '),
        irow('  Glacier Flexible: mins-hrs; 90-day   ', '  Standard-IA: ms; retrieval fee/GB   '),
        irow('  Glacier Deep Archive: 12-hr; 180-day  ', '  Glacier Instant: ms; per GB fee     '),
        irow('  Deep Archive: cheapest storage class  ', '  Glacier Flexible: bulk=5-12h, free  '),
        irow('  All Glacier: 11-nines durability; 3AZ ', '  Deep Archive: standard=12h retrieval'),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  S3 stores objects across 3+ AZs in a Region; 11 nines (99.999999999%) durability'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  S3 Standard     = Default; frequent access; 3+ AZ; 99.99% availability'),
        line('  Intelligent-Tiering = Auto-moves objects between tiers; monitoring fee per 1000'),
        line('  Standard-IA     = Infrequent Access; 3+ AZ; lower storage cost; retrieval fee'),
        line('  One Zone-IA     = Single AZ; 20% cheaper than Standard-IA; risk of AZ loss'),
        line('  Glacier Instant = Archive; millisecond retrieval; 90-day minimum; per-GB fee'),
        line('  Glacier Flexible= Archive; expedited(1-5min)/standard(3-5h)/bulk(5-12h) retrieval'),
        line('  Deep Archive    = Cheapest; 12-hour standard retrieval; 180-day minimum'),
        line('  Minimum duration= Classes have minimum storage billing periods; charged even if deleted'),
        blank(),
        bot(),
    ])


def d_storage_comparison():
    return section('AWS Storage Services Comparison', [
        top('AWS Storage Services — S3 vs EBS vs EFS vs FSx vs Instance Store'),
        blank(),
        line('  Five main storage types; choose by access pattern, sharing, and persistence needs.'),
        blank(),
        itop(),
        ititle('  S3 (Object Storage)                 ', '  EBS (Block Storage)                 '),
        irow('  Objects in buckets; unlimited scale   ', '  Persistent block volumes for EC2    '),
        irow('  Globally unique bucket name           ', '  Bound to a single AZ                '),
        irow('  HTTP API (PUT/GET); not mountable     ', '  Mountable like a local disk (ext4)  '),
        irow('  11 nines durability; 3+ AZ by default ', '  SSD (gp3/io2) or HDD (st1/sc1)     '),
        irow('  Use: backups, static web, data lake   ', '  Use: OS disk, DB, boot volume       '),
        ibot(),
        blank(),
        line('  EBS is block (like a hard drive); EFS is shared NFS; S3 is object (HTTP API).'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  EFS (Elastic File System)            ', '  Instance Store / FSx                '),
        irow('  NFSv4 shared file system              ', '  Instance Store: ephemeral local NVMe'),
        irow('  Multi-AZ; automatically scales        ', '  Lost on stop/terminate/host failure '),
        irow('  Mount simultaneously to many EC2       ', '  Highest I/O throughput; no extra $  '),
        irow('  Linux only; no Windows                ', '  FSx for Windows: SMB, AD-integrated '),
        irow('  Standard + Infrequent Access tiers    ', '  FSx for Lustre: HPC parallel FS     '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  S3 infrastructure (3+ AZ) · EBS volumes in AZ · NFS cluster (EFS) · local NVMe'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  S3         = Object storage; buckets + keys; unlimited scale; HTTP GET/PUT API'),
        line('  EBS        = Elastic Block Store; like a virtual hard drive; attached to one EC2'),
        line('  EFS        = Elastic File System; NFS v4; shared across many Linux EC2 instances'),
        line('  Instance Store = Local NVMe on the physical host; ephemeral; fastest raw IOPS'),
        line('  FSx for Windows= Fully managed Windows file server; SMB protocol; AD integration'),
        line('  FSx for Lustre = High-performance parallel file system; integrates with S3'),
        line('  Storage Gateway= Hybrid storage; connects on-prem to S3/EBS/Tape via iSCSI/NFS'),
        line('  Snow Family    = Physical devices (Snowcone/Snowball/Snowmobile) for data transfer'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: cost  (2 diagrams)
# ═══════════════════════════════════════════════════════════════════════════════

def d_pricing_models():
    return section('EC2 Pricing Models', [
        top('EC2 Pricing Models — Commitment vs Discount'),
        blank(),
        line('  Longer commitment = larger discount; Spot gives biggest saving with interruption risk.'),
        blank(),
        itop(),
        ititle('  Model                               ', '  Key Facts                           '),
        irow('  On-Demand                            ', '  No commitment; full price; per second'),
        irow('  Standard Reserved (1 year)           ', '  Up to 72% off; same config only     '),
        irow('  Standard Reserved (3 year)           ', '  Maximum RI discount; locked config  '),
        irow('  Convertible Reserved (1/3 yr)        ', '  Up to 66% off; can exchange family  '),
        irow('  Compute Savings Plan                 ', '  Up to 66% off; EC2+Fargate+Lambda  '),
        ibot(),
        blank(),
        line('  Reserved and Savings Plans are billed whether you use the capacity or not.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Model (continued)                  ', '  Key Facts                           '),
        irow('  EC2 Instance Savings Plan            ', '  Up to 72% off; same family + Region '),
        irow('  Spot Instances                       ', '  Up to 90% off; 2-min interruption   '),
        irow('  Dedicated Host                       ', '  Physical server; BYOL; compliance   '),
        irow('  Dedicated Instance                   ', '  On dedicated HW; per-instance charge'),
        irow('  Free Tier (12 months new accounts)   ', '  750 hrs/mo t2/t3.micro; then billed '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  EC2 billing infrastructure · AWS Cost Explorer API · CUR exported to S3'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  On-Demand     = No commitment; highest per-unit cost; most flexible'),
        line('  Reserved RI   = 1 or 3-year commitment to capacity; up to 72% discount'),
        line('  Savings Plan  = $/hr flexible commitment; applies across instance families'),
        line('  Spot          = Unused EC2 capacity auction; up to 90% off; interruptible'),
        line('  Dedicated Host= Physical server commitment; BYOL compliant; socket/core visibility'),
        line('  Free Tier     = 750 hrs/mo t2.micro or t3.micro for 12 months on new accounts'),
        line('  RI Marketplace= Sell unused Standard RIs to other AWS customers'),
        line('  Utilisation   = Percentage of purchased Reserved/Savings Plan capacity actually used'),
        blank(),
        bot(),
    ])


def d_support_tiers():
    return section('AWS Support Tiers', [
        top('AWS Support Plans — Features and Response Times'),
        blank(),
        line('  Five support tiers; higher tiers add TAMs, faster response, and architectural guidance.'),
        blank(),
        itop(),
        ititle('  Basic / Developer Plans              ', '  Business / Enterprise On-Ramp       '),
        irow('  Basic: free; documentation only       ', '  Business: $100/mo or 10% of charges '),
        irow('  Basic: AWS Health Dashboard + forums  ', '  Business: all contacts; 24/7 phone  '),
        irow('  Developer: $29/mo or 3% of charges    ', '  Business: <1h critical response      '),
        irow('  Developer: 1 contact; biz-hours email ', '  Enterprise On-Ramp: $5500/mo min    '),
        irow('  Developer: general guidance + sandbox ', '  Ent On-Ramp: TAM pool; <30 min crit '),
        ibot(),
        blank(),
        line('  Business adds 24/7 support + full Trusted Advisor; Enterprise adds dedicated TAM.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Enterprise Plan                      ', '  Trusted Advisor Checks by Tier      '),
        irow('  Enterprise: $15000/mo or % of charges ', '  Basic: 6 core security checks only  '),
        irow('  Enterprise: dedicated Technical Acct  ', '  Developer: same 6 checks as Basic   '),
        irow('  Enterprise: <15 min business-critical  ', '  Business: ALL ~500+ Trusted Advisor  '),
        irow('  Enterprise: Well-Architected Reviews  ', '  Enterprise: ALL checks + API access '),
        irow('  Enterprise: Concierge; billing review  ', '  Proactive recommendations: Ent only '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS Support infrastructure · TAM communication channels · Trusted Advisor service'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  TAM            = Technical Account Manager; dedicated expert in Enterprise plan'),
        line('  Trusted Advisor= Automated checks across cost, performance, security, fault tolerance'),
        line('  Basic          = Free; 7 Trusted Advisor checks; Health Dashboard; community forums'),
        line('  Developer      = $29/mo or 3% of monthly charges; 1 primary contact; 12-24h response'),
        line('  Business       = $100+/mo; unlimited contacts; 24/7 phone+chat; <1h prod-down response'),
        line('  Enterprise On-Ramp= $5500/mo; TAM pool; 30-min critical response; WAR reviews'),
        line('  Enterprise     = $15000/mo; dedicated TAM; 15-min critical; Concierge team access'),
        line('  Infrastructure Event Mgmt = Enterprise only; AWS support during launches/migrations'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: security  (1 diagram)
# ═══════════════════════════════════════════════════════════════════════════════

def d_security_services():
    return section('AWS Security Services Map', [
        top('AWS Security Services — Prevention, Detection, and Response'),
        blank(),
        line('  Security services span prevention, detection, and response; many can be centralised.'),
        blank(),
        itop(),
        ititle('  Prevention Services                  ', '  Detection Services                  '),
        irow('  Shield Standard: free L3/L4 DDoS     ', '  GuardDuty: ML threat detection      '),
        irow('  Shield Advanced: L7 + cost protection ', '  GuardDuty: CloudTrail+FlowLogs+DNS  '),
        irow('  WAF: Layer 7 rules (ALB/CF/API GW)   ', '  Inspector: EC2 CVE + container scan '),
        irow('  KMS: CMK key management + encryption  ', '  Macie: S3 PII/sensitive data finding'),
        irow('  SCP: restrict max perms at OU level  ', '  Config: resource drift + rules eval  '),
        ibot(),
        blank(),
        line('  Prevent access and encrypt first; detect threats; respond and investigate.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Monitoring and Audit                 ', '  Aggregation and Response            '),
        irow('  CloudTrail: all API calls logged      ', '  Security Hub: aggregates all findings'),
        irow('  CloudTrail Org: captures all accounts ', '  Security Hub: CIS/PCI compliance score'),
        irow('  Config: inventory + config history    ', '  Detective: graph-based investigation '),
        irow('  Trusted Advisor: security checks      ', '  Incident Manager: runbooks + alerts  '),
        irow('  Access Analyzer: finds external access', '  Systems Manager: patch + run command '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  KMS HSMs · GuardDuty ML infra · CloudFront edge for WAF · CloudTrail S3 storage'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Shield Standard = Free DDoS protection at L3/L4 for all AWS customers'),
        line('  Shield Advanced = $3000/mo; L7 DDoS; cost protection; dedicated response team'),
        line('  WAF             = Web Application Firewall; rules on ALB/CloudFront/API Gateway'),
        line('  GuardDuty       = ML-based threat detection; analyses CloudTrail/VPC logs/DNS'),
        line('  Inspector       = Automated CVE scanner for EC2 instances and container images'),
        line('  Macie           = Machine learning to discover PII and sensitive data in S3'),
        line('  Config          = Resource configuration recorder; evaluates compliance rules'),
        line('  Security Hub    = Aggregates GuardDuty/Inspector/Macie/Config findings; scores'),
        line('  Detective       = Investigates security incidents using graph analysis of logs'),
        line('  KMS CMK         = Customer Managed Key; full control; CloudTrail logs all usage'),
        line('  Access Analyzer = Identifies resources accessible from outside the account'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: governance/aws-organizations  (1 diagram)
# ═══════════════════════════════════════════════════════════════════════════════

def d_organizations():
    return section('AWS Organizations Multi-Account Hierarchy', [
        top('AWS Organizations — Multi-Account Hierarchy and Consolidated Billing'),
        blank(),
        line('  Organizations enables account governance, SCP guardrails, and consolidated billing.'),
        blank(),
        itop(),
        ititle('  Organization Hierarchy               ', '  Service Control Policies (SCPs)     '),
        irow('  Root: single top; SCPs here = all    ', '  Attached to Root, OU, or account    '),
        irow('  OUs: nested up to 5 levels deep      ', '  Limits maximum allowed permissions  '),
        irow('  Accounts: leaf nodes; leaf or in OUs ', '  Does NOT grant permissions itself   '),
        irow('  Management account: billing root only ', '  FullAWSAccess SCP: default allow all'),
        irow('  Management: exempt from SCPs          ', '  Inheritance: child inherits parent  '),
        ibot(),
        blank(),
        line('  SCPs are guardrails, not grants; IAM policies still needed to allow actions.'),
        blank(),
        arrows(),
        blank(),
        itop(),
        ititle('  Consolidated Billing                 ', '  Org-Wide Service Enablement         '),
        irow('  Single invoice for all member accts  ', '  CloudTrail: org trail, all accounts '),
        irow('  Combined usage for volume discounts  ', '  Config: aggregated compliance view  '),
        irow('  RI and Savings Plans shared across   ', '  GuardDuty: one click all accounts   '),
        irow('  Payer account = management account   ', '  Security Hub: delegated admin acct  '),
        irow('  Cost allocation tags: per account     ', '  Backup: org backup plans to members '),
        ibot(),
        blank(),
        line('  Physical Infrastructure (the hardware everything above runs on):'),
        line('  AWS Organizations global service · SCP engine · consolidated billing infrastructure'),
        blank(),
        line('  Key terms:'),
        blank(),
        line('  Root           = Top of OU tree; SCPs applied here affect every account in org'),
        line('  OU             = Organizational Unit; groups accounts with similar SCP requirements'),
        line('  SCP            = Service Control Policy; restricts actions regardless of IAM grants'),
        line('  Management account = Account that created org; cannot have SCPs applied to it'),
        line('  Consolidated billing= All accounts billed to management account; combined discounts'),
        line('  Delegated admin= Member account granted org-level admin for a specific service'),
        line('  AWS Control Tower= Landing zone service using Organizations; guardrails + Account Factory'),
        line('  Payer account  = Synonym for management account in billing context'),
        line('  Tag policy     = Enforces tag key and value standardisation across accounts'),
        blank(),
        bot(),
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# Main execution
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    targets = [
        (
            os.path.join(AWS, 'architecture', 'how-it-works', 'index.md'),
            [d_global_infra(), d_shared_responsibility(), d_well_architected(),
             d_caf(), d_seven_rs()],
        ),
        (
            os.path.join(AWS, 'networking', 'vpc', 'index.md'),
            [d_vpc_subnet(), d_network_connectivity(), d_route53()],
        ),
        (
            os.path.join(AWS, 'identity', 'iam', 'index.md'),
            [d_iam_model(), d_policy_evaluation()],
        ),
        (
            os.path.join(AWS, 'compute', 'ec2', 'index.md'),
            [d_ec2_purchase(), d_instance_families(), d_compute_services(),
             d_autoscaling_lb()],
        ),
        (
            os.path.join(AWS, 'storage', 's3', 'index.md'),
            [d_s3_classes(), d_storage_comparison()],
        ),
        (
            os.path.join(AWS, 'cost', 'index.md'),
            [d_pricing_models(), d_support_tiers()],
        ),
        (
            os.path.join(AWS, 'security', 'index.md'),
            [d_security_services()],
        ),
        (
            os.path.join(AWS, 'governance', 'aws-organizations', 'index.md'),
            [d_organizations()],
        ),
    ]

    for path, sections in targets:
        if not os.path.exists(path):
            print('MISSING: ' + path)
            continue
        print(path)
        append_sections(path, sections)

    print('\nDone.')


if __name__ == '__main__':
    main()

# AWS Cloud Practitioner CLF-C02 — 14-Day Study Plan

**3 hrs/day · 50 Q&A per day · May 2026**

AWS CLOUD PRACTITIONER CLF-C02
14-DAY STUDY PLAN  |  3 HRS/DAY  |  50 Q&A PER DAY
Christos Anastasiadis  |  May 2026

## Exam Facts

| | |
|---|---|
| **Exam code** | CLF-C02 |
| **Questions** | 65 (50 scored, 15 unscored) |
| **Time** | 90 minutes |
| **Pass score** | 700/1000 |
| **Format** | Multiple choice, multiple response |
| **Cost** | $100 USD |
| **Schedule** | https://www.aws.training/certification |

## Exam Domains

| Domain | Weight |
|---|---|
| Domain 1 — Cloud Concepts | 24% |
| Domain 2 — Security and Compliance | 30% |
| Domain 3 — Cloud Technology | 34% |
| Domain 4 — Billing and Pricing | 12% |

## Day 1 — CLOUD CONCEPTS & AWS GLOBAL INFRASTRUCTURE

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 1)

| Acronym | Definition |
|---|---|
| `IaaS` | Infrastructure as a Service |
| `PaaS` | Platform as a Service |
| `SaaS` | Software as a Service |
| `EC2` | Elastic Compute Cloud (virtual servers) |
| `RDS` | Relational Database Service (managed databases) |
| `S3` | Simple Storage Service (object storage) |
| `VPC` | Virtual Private Cloud (your private network) |
| `IAM` | Identity and Access Management |
| `CDN` | Content Delivery Network |
| `AZ` | Availability Zone |
| `DC` | Data Center |
| `CapEx` | Capital Expenditure (upfront investment) |
| `OpEx` | Operational Expenditure (ongoing costs) |
| `VM` | Virtual Machine |
| `HA` | High Availability |
| `DR` | Disaster Recovery |
| `VPN` | Virtual Private Network |
| `DNS` | Domain Name System |

#### Hour 1: Cloud Concepts

**What is cloud computing?**
- On-demand delivery of IT resources over the internet
- Pay-as-you-go pricing. No need to buy or maintain physical DCs.

**6 Advantages of cloud computing (memorize all 6):**
- 1. Trade fixed expense for variable expense
- 2. Benefit from massive economies of scale
- 3. Stop guessing capacity
- 4. Increase speed and agility
- 5. Stop spending money running and maintaining data centers
- 6. Go global in minutes

**3 Cloud computing models:**
- IaaS — You manage: OS, middleware, runtime, data, apps
- AWS manages: virtualization, servers, storage, networking
- Example: EC2
- PaaS — You manage: data and applications only
- AWS manages: everything else
- Example: Elastic Beanstalk, RDS
- SaaS — You manage: nothing (just use the software)
- AWS manages: everything
- Example: Gmail, Salesforce, ServiceNow, Jira

**3 Cloud deployment models:**
- Public cloud   — All resources on AWS
- Private cloud  — Resources on your own data center (T. Rowe today)
- Hybrid cloud   — Mix of public and private


#### Hour 2: Aws Global Infrastructure

**Regions:**
- A geographic area with 2+ Availability Zones
- Currently 30+ regions worldwide
- How to choose: compliance, latency, services, cost

**Availability Zones (AZs):**
- One or more discrete data centers within a region
- Each AZ has independent power, cooling, and networking
- Connected by high-bandwidth, low-latency fiber
- Best practice: deploy across multiple AZs for HA

**Edge Locations:**
- Used by CloudFront (CDN) to cache content closer to users
- 400+ edge locations worldwide — more than Regions or AZs

**Local Zones:**
- AWS infrastructure deployed closer to large population centers
- For workloads requiring single-digit millisecond latency

**Wavelength Zones:**
- AWS infrastructure embedded in telecom 5G networks
- Ultra-low latency for mobile applications

**AWS Outposts:**
- AWS hardware installed in YOUR data center
- Run AWS services on-premises (relevant to T. Rowe environment)


### Questions & Answers — Day 1

| **Q1** | What is the definition of cloud computing? |
|:---|:---|
| **A** | On-demand delivery of IT (Information Technology) resources<br>over the internet with pay-as-you-go pricing.<br><br>NEW ACRONYM: IT = Information Technology<br>Everything digital: servers, storage, networking, databases. |

```
TRADITIONAL IT                    CLOUD (AWS)
┌─────────────────┐               ┌─────────────────┐
│  Buy servers     │               │  Request online  │
│  Wait weeks      │     vs        │  Ready in mins   │
│  Pay upfront     │               │  Pay per use     │
│  Guess capacity  │               │  Scale anytime   │
└─────────────────┘               └─────────────────┘
```

| **Q2** | Which cloud advantage eliminates the need to guess how much infrastructure capacity you need? |
|:---|:---|
| **A** | Stop guessing capacity. AWS scales automatically<br>using Auto Scaling.<br><br>NEW ACRONYM: Auto Scaling = AWS service that automatically<br>adds or removes servers based on real-time demand. |

```
TRADITIONAL (guessing)            CLOUD (auto-match)
┌──────────────────┐              ┌──────────────────┐
│ Buy too much?    │              │  Auto Scaling    │
│  wasted capacity │   vs         │  scales UP/DOWN  │
│ Buy too little?  │              │  Always matches  │
│  crashes!        │              │  actual demand   │
└──────────────────┘              └──────────────────┘
```

| **Q3** | What does "trade fixed expense for variable expense" mean? |
|:---|:---|
| **A** | Instead of investing upfront (CapEx), you pay only for<br>what you consume (OpEx).<br><br>CapEx = Capital Expenditure: Big upfront purchase<br>        Example: buying 500 servers for $2M<br>OpEx  = Operational Expenditure: Ongoing costs<br>        Example: paying $50K/month AWS bill |

```
CAPEX (Traditional)               OPEX (Cloud)
┌───────────────────┐             ┌───────────────────┐
│ Jan: $2,000,000    │             │ Jan:  $45,000      │
│ (buy servers)      │    vs       │ Feb:  $48,000      │
│ Feb-Dec: maintain  │             │ (matches usage)    │
└───────────────────┘             └───────────────────┘
```

| **Q4** | Which cloud model gives the most control over infrastructure? |
|:---|:---|
| **A** | IaaS (Infrastructure as a Service) — you manage OS and above. |

```
RESPONSIBILITY STACK
┌──────────────────────────────────────────────┐
│           IaaS        PaaS        SaaS       │
│        ┌────────┐  ┌────────┐  ┌────────┐   │
│  YOU → │  App   │  │  App   │  │        │   │
│  YOU → │  Data  │  │  Data  │  │  AWS   │   │
│  YOU → │  OS    │  │        │  │manages │   │
│  AWS → │  Virt  │  │  AWS   │  │  ALL   │   │
│  AWS → │  HW/DC │  │manages │  │        │   │
│        └────────┘  └────────┘  └────────┘   │
│  Control: HIGH         MID          LOW      │
└──────────────────────────────────────────────┘
```

| **Q5** | EC2 is an example of which cloud model? |
|:---|:---|
| **A** | IaaS — you manage the OS, AWS manages physical infra.<br><br>NEW ACRONYM: EC2 = Elastic Compute Cloud<br>Elastic = can grow/shrink. Compute = CPU+RAM. Cloud = hosted on AWS.<br>= Virtual servers you rent on AWS. Like a VM on your VMware cluster<br>  except AWS owns the physical hardware. |

```
┌──────────────────────────────────┐
│  EC2 (Elastic Compute Cloud)     │
│  YOU manage: OS, apps, data, SGs │
│  AWS manages: hardware, hypervisor│
└──────────────────────────────────┘
```

| **Q6** | Elastic Beanstalk is an example of which model? |
|:---|:---|
| **A** | PaaS — you deploy code, AWS manages everything else.<br><br>NEW ACRONYM: PaaS = Platform as a Service<br>AWS provides complete platform. You bring the code. |

```
┌──────────────────────────────────────┐
│  Elastic Beanstalk (PaaS)            │
│  YOU → Upload your code              │
│  AWS → Provisions EC2, OS, LB, ASG   │
│  App is running! (you did nothing)   │
└──────────────────────────────────────┘
```

| **Q7** | Which cloud model requires managing the least infrastructure? |
|:---|:---|
| **A** | SaaS — provider manages everything, you just use it.<br><br>NEW ACRONYM: SaaS = Software as a Service<br>Like a streaming service for software. Just log in and use it.<br>Examples: Gmail, Salesforce, ServiceNow (T. Rowe uses this!), Jira |

```
┌──────────────────────────────────────┐
│  SaaS: Open browser → Log in → Use  │
│  Provider manages: code, DB, servers │
│  You manage: NOTHING                 │
└──────────────────────────────────────┘
```

| **Q8** | A company wants to keep sensitive data on-premises while using AWS for other workloads. Which deployment model? |
|:---|:---|
| **A** | Hybrid cloud — mix of on-premises and cloud. |

```
YOUR DATA CENTER          AWS CLOUD
┌──────────────┐          ┌──────────────┐
│  Sensitive   │◄────────►│  Web servers │
│  financial   │  VPN /   │  Dev/test    │
│  records     │  Direct  │  Analytics   │
│  (on-prem)   │  Connect │  Backups     │
└──────────────┘          └──────────────┘
THIS IS EXACTLY T. Rowe Price today.
```

| **Q9** | Which deployment model uses only AWS with no on-premises? |
|:---|:---|
| **A** | Public cloud (all-in cloud). |

```
┌────────────────────────────────────┐
│  INTERNET → AWS Region             │
│  EC2, S3, RDS, Lambda — 100% cloud │
│  No servers you own anywhere       │
└────────────────────────────────────┘
```

| **Q10** | What is an AWS Region? |
|:---|:---|
| **A** | A geographical area with 2+ AZs, isolated from other regions.<br><br>NEW ACRONYM: AZ = Availability Zone<br>Physically separate data center(s) within a Region with<br>independent power, cooling, and networking. |

```
┌──────────────────────────────────────┐
│  30+ Regions worldwide               │
│  Examples: us-east-1 (N. Virginia)   │
│            eu-west-1 (Ireland)       │
│  Data stays IN region unless you     │
│  explicitly move it                  │
└──────────────────────────────────────┘
```

| **Q11** | How many AZs does each AWS Region have at minimum? |
|:---|:---|
| **A** | At least two. Most have three or more. |

```
AWS REGION (e.g. us-east-1)
┌─────────────────────────────────────┐
│  ┌─────────┐  ┌─────────┐  ┌─────┐  │
│  │   AZ-1  │  │   AZ-2  │  │AZ-3 │  │
│  │(min req)│  │(min req)│  │     │  │
│  └─────────┘  └─────────┘  └─────┘  │
│       └────────────┴────────────┘    │
│         High-bandwidth private fiber  │
└─────────────────────────────────────┘
```

| **Q12** | What is an Availability Zone? |
|:---|:---|
| **A** | One or more discrete data centers with redundant power,<br>networking, and connectivity within a region. |

```
AVAILABILITY ZONE
┌──────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐      │
│  │  Data    │  │  Data    │      │
│  │ Center A │  │ Center B │      │
│  └──────────┘  └──────────┘      │
│  Independent power and cooling    │
│  Connected to other AZs via       │
│  private high-bandwidth fiber     │
└──────────────────────────────────┘
Like a separate building in your DC campus
with its own power feed.
```

| **Q13** | Why deploy applications across multiple AZs? |
|:---|:---|
| **A** | High availability — if one AZ fails, app continues in others.<br><br>NEW ACRONYM: HA = High Availability<br>Like your dual-fabric SAN — if Fabric A fails, Fabric B runs. |

```
SINGLE AZ (bad)          MULTI-AZ (good)
┌─────────────┐          ┌─────────────────────┐
│     AZ-1    │          │  AZ-1    │  AZ-2    │
│  ┌────────┐ │          │ ┌──────┐ │ ┌──────┐ │
│  │  App   │ │          │ │ App  │ │ │ App  │ │
│  └────────┘ │          │ └──────┘ │ └──────┘ │
│  AZ fails   │          │ AZ fails │ Still UP!│
│  OUTAGE!    │          │          │    ✓     │
└─────────────┘          └─────────────────────┘
```

| **Q14** | What are Edge Locations used for? |
|:---|:---|
| **A** | Caching content via CloudFront CDN to reduce latency.<br><br>NEW ACRONYM: CDN = Content Delivery Network<br>Network of servers worldwide caching content close to users.<br>CloudFront = AWS's CDN service. |

```
WITHOUT EDGE: [User: Tokyo] →→→→→ [Origin: us-east-1] ~150ms
WITH EDGE:    [User: Tokyo] → [Edge: Tokyo] ~5ms (cached)
```

| **Q15** | Which has more locations — Regions or Edge Locations? |
|:---|:---|
| **A** | Edge Locations (400+) vs Regions (30+). |

```
Regions:         ██  30+
AZs:             █████  90+
Edge Locations:  ████████████████  400+
Rule: Edge > AZs > Regions
```

| **Q16** | What is an AWS Local Zone? |
|:---|:---|
| **A** | An extension of an AWS Region placed closer to large<br>population centers for single-digit millisecond latency.<br><br>NEW ACRONYM: ms = milliseconds (1/1000 of a second) |

```
REGION (N. Virginia) ──extends──► [LA Local Zone]
User in LA: ~20ms to VA vs ~1ms to Local Zone
```

| **Q17** | What is AWS Wavelength? |
|:---|:---|
| **A** | AWS infrastructure embedded in 5G telecom networks for<br>ultra-low latency mobile applications.<br><br>NEW ACRONYMS: 5G = Fifth Generation mobile network<br>              IoT = Internet of Things |

```
STANDARD: [Mobile] → [5G Tower] → [Internet] → [AWS] ~15ms
WAVELENGTH:[Mobile] → [5G Tower + AWS compute] ~1-2ms
```

| **Q18** | What is AWS Outposts? |
|:---|:---|
| **A** | AWS-managed hardware installed in YOUR data center to run<br>AWS services on-premises. |

```
YOUR DATA CENTER
┌──────────────────────────────────┐
│  AWS Outposts Rack:              │
│  EC2 | EBS | RDS | ECS           │
│  AWS hardware in YOUR building   │
│  Connects to AWS via Direct Connect│
└──────────────────────────────────┘
Relevant to T. Rowe — extend on-prem to AWS.
```

| **Q19** | Which AWS service runs AWS infrastructure in your own DC? |
|:---|:---|
| **A** | AWS Outposts. |

| **Q20** | A company needs data to stay in a specific country. What should they consider? |
|:---|:---|
| **A** | Select an AWS Region in that country. AWS never moves<br>data out of a region without your explicit action.<br><br>NEW ACRONYM: GDPR = General Data Protection Regulation<br>EU law requiring personal data of EU citizens stays in EU. |

| **Q21** | Which is NOT a cloud advantage? A) Go global in minutes  B) Eliminate all security concerns C) Stop guessing capacity  D) Trade fixed for variable |
|:---|:---|
| **A** | B — Cloud does NOT eliminate security concerns.<br>Security is a SHARED responsibility.<br><br>THE REAL 6 ADVANTAGES:<br>1. Trade CapEx for OpEx<br>2. Economies of scale<br>3. Stop guessing capacity<br>4. Speed and agility<br>5. Stop spending on data centers<br>6. Go global in minutes |

| **Q22** | What does "go global in minutes" mean? |
|:---|:---|
| **A** | Deploy in multiple AWS Regions worldwide quickly.<br><br>WITHOUT CLOUD: Find DC, sign lease, order hardware → 6 months<br>WITH AWS: Open console, select region, deploy → 10 minutes |

| **Q23** | Which deployment model is most like traditional IT? |
|:---|:---|
| **A** | Private cloud — your own hardware, your own DC.<br>Like T. Rowe's VMware/VxRail environment today. |

| **Q24** | How are AZs connected within a region? |
|:---|:---|
| **A** | High-bandwidth, low-latency PRIVATE fiber — NOT internet.<br>Similar to your dual-fabric SAN ISLs between buildings. |

| **Q25** | A startup wants global launch with minimal upfront cost. Which cloud advantage? |
|:---|:---|
| **A** | Trade fixed expense (CapEx) for variable expense (OpEx).<br>Pay $0 upfront. Pay only when users arrive. |

| **Q26** | What factor is NOT used when choosing a Region? A) Compliance  B) Proximity  C) Services  D) Logo color |
|:---|:---|
| **A** | D. Real factors: Compliance first, then proximity,<br>available services, then cost. |

| **Q27** | Which is correct about AWS Regions? A) All same services  B) Connected by public internet C) Each region isolated  D) One region only allowed |
|:---|:---|
| **A** | C — Regions are geographically isolated.<br>If us-east-1 fails, eu-west-1 is NOT affected. |

| **Q28** | What is the primary purpose of multiple AZs? |
|:---|:---|
| **A** | Fault tolerance and HA — apps survive individual AZ failures.<br><br>ELB = Elastic Load Balancer (routes traffic to healthy AZs)<br>SYNC = Synchronous replication (data written to both at once) |

| **Q29** | Which component reduces content delivery latency globally? |
|:---|:---|
| **A** | Edge Locations used by CloudFront CDN. |

| **Q30** | A healthcare company must ensure EU patient data stays in EU. |
|:---|:---|
| **A** | AWS Regions — data stays in the region you choose.<br>Deploy in eu-west-1 or eu-central-1. |

| **Q31** | What best describes economies of scale? |
|:---|:---|
| **A** | AWS aggregates usage from millions of customers → lower costs<br>→ passes savings to customers through lower prices. |

| **Q32** | What type of expense is a monthly AWS bill? |
|:---|:---|
| **A** | OpEx (Operational Expenditure) — variable, pay-as-you-go. |

| **Q33** | What type of expense is buying physical servers? |
|:---|:---|
| **A** | CapEx (Capital Expenditure) — large upfront investment.<br>Goes on balance sheet, depreciated over years. |

| **Q34** | T. Rowe Price has on-premises + AWS pilot. Which model? |
|:---|:---|
| **A** | Hybrid cloud. |

| **Q35** | How many edge locations does AWS have approximately? |
|:---|:---|
| **A** | 400+ edge locations worldwide. |

| **Q36** | Which is a characteristic of ALL cloud models? A) No security mgmt  B) On-demand self-service C) Requires on-prem  D) Fixed monthly pricing |
|:---|:---|
| **A** | B — On-demand self-service (NIST characteristic).<br><br>NIST = National Institute of Standards and Technology<br>5 cloud characteristics: On-demand self-service, broad network<br>access, resource pooling, rapid elasticity, measured service. |

| **Q37** | What makes Wavelength different from AZs? |
|:---|:---|
| **A** | Wavelength is embedded in 5G telecom networks (~1-2ms).<br>AZs are standalone data center facilities (~10-20ms). |

| **Q38** | Which for single-digit ms latency near a specific city? |
|:---|:---|
| **A** | AWS Local Zone if available near that city. |

| **Q39** | Which about AWS global infrastructure is TRUE? A) One region only  B) Edge = region locations C) AZs are physically separate  D) Same services everywhere |
|:---|:---|
| **A** | C — AZs are physically separate with independent<br>power and networking. |

| **Q40** | What is the main benefit of "increase speed and agility"? |
|:---|:---|
| **A** | Access new resources in minutes. New EC2 in 60 seconds<br>vs 6-8 weeks for physical server procurement.<br><br>SSH = Secure Shell (how you remotely access Linux servers) |

| **Q41** | In IaaS, what does the customer manage? |
|:---|:---|
| **A** | OS, middleware, runtime, data, and applications.<br><br>IaaS boundary: Customer owns OS and above.<br>AWS owns: virtualization, hardware, data center. |

| **Q42** | In PaaS, what does AWS manage? |
|:---|:---|
| **A** | Everything except customer data and applications.<br>OS, middleware, runtime, hardware — all AWS. |

| **Q43** | Gmail is an example of which model? |
|:---|:---|
| **A** | SaaS — Google manages everything. |

| **Q44** | What does Outposts allow that standard Regions do not? |
|:---|:---|
| **A** | Run AWS services on your own on-premises hardware<br>inside your building. |

| **Q45** | Which advantage for expanding to new countries? |
|:---|:---|
| **A** | Go global in minutes — deploy in new regions in minutes<br>vs months of physical DC build-out. |

| **Q46** | How does AWS achieve massive economies of scale? |
|:---|:---|
| **A** | Aggregating usage from hundreds of thousands of customers,<br>achieving lower costs and passing savings to customers.<br>AWS has dropped prices 100+ times since 2006. |

| **Q47** | Minimum AZs required for a Region to exist? |
|:---|:---|
| **A** | Two. Most regions have three. us-east-1 has six. |

| **Q48** | Which is SaaS? A) EC2  B) RDS  C) Salesforce CRM  D) Elastic Beanstalk |
|:---|:---|
| **A** | C — Salesforce. Log in via browser, use it.<br>TRICK: RDS is PaaS (you still manage schema and data).<br>CRM = Customer Relationship Management software. |

| **Q49** | Moving 500 servers to AWS changes from which expense to which? |
|:---|:---|
| **A** | From CapEx (owning servers) to OpEx (paying for usage). |

| **Q50** | Correct order of AWS infrastructure from largest to smallest? |
|:---|:---|
| **A** |  |

```
Region → Availability Zone → Data Center.
(Edge locations exist separately for CloudFront CDN only.)
```

DAY 1 COMPLETE
*Tomorrow: Day 2 — Shared Responsibility Model & IAM*

## Day 2 — SHARED RESPONSIBILITY MODEL & IAM

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 2)

| Acronym | Definition |
|---|---|
| `IAM` | Identity and Access Management |
| `MFA` | Multi-Factor Authentication |
| `SRM` | Shared Responsibility Model |
| `ARN` | Amazon Resource Name (unique ID for every AWS resource) |
| `JSON` | JavaScript Object Notation (text format for policies) |
| `SSO` | Single Sign-On |
| `STS` | Security Token Service (issues temporary credentials) |
| `AD` | Active Directory (Microsoft's user directory system) |
| `SAML` | Security Assertion Markup Language (federation standard) |
| `KMS` | Key Management Service |
| `SCP` | Service Control Policy |
| `OU` | Organizational Unit |
| `CloudTrail` | AWS API audit logging service |
| `CloudWatch` | AWS monitoring and metrics service |

#### Hour 1: Shared Responsibility Model

**AWS IS RESPONSIBLE FOR — "Security OF the Cloud":**
- Physical data centers, hardware, hypervisor/virtualization,
- managed service infrastructure, global network

**CUSTOMER IS RESPONSIBLE FOR — "Security IN the Cloud":**
- Customer data + encryption, IAM users/groups/roles/policies,
- MFA, OS patching on EC2, application security,
- Security group rules, NACL rules, VPC configuration

**KEY EXAM SPECIFICS:**
- EC2:    Customer manages OS patching and security groups
- RDS:    AWS manages OS and DB engine patching
- S3:     AWS secures infrastructure; customer manages bucket policies
- Lambda: AWS manages all infrastructure; customer manages code and IAM


#### Hour 2: Iam

**IAM is FREE and GLOBAL (not region-specific).**

**Root user: Created when account opens. Full access. DO NOT use daily.**
- Enable MFA immediately. Only use for billing/close account.
**IAM Users: Individual identities. No permissions by default.**
**IAM Groups: Collection of users. Attach policies to groups.**
- A user can belong to multiple groups.
- Groups CANNOT contain other groups.
**IAM Roles: Temporary identity for services (EC2, Lambda, cross-account).**
- Best practice for EC2 — never store access keys on EC2.
**IAM Policies: JSON documents. Allow or Deny. Principle of least privilege.**
**MFA: Password + device. Virtual (Google Authenticator) or hardware key.**

**DENY ALWAYS OVERRIDES ALLOW — the golden IAM rule.**


### Questions & Answers — Day 2

| **Q1** | What is the AWS Shared Responsibility Model? |
|:---|:---|
| **A** | AWS = Security OF the cloud (physical infra, hardware, hypervisor).<br>Customer = Security IN the cloud (data, IAM, OS, apps, network config). |

```
CUSTOMER: Your data, IAM, OS patching, app code, security groups
═══════════════════════════════════ THE LINE
AWS: Physical facilities, hardware, hypervisor, global network
```

| **Q2** | Who patches the OS on an EC2 instance? |
|:---|:---|
| **A** | The CUSTOMER. On EC2 you manage the guest OS including patching.<br><br>Guest OS = OS running INSIDE your VM (Windows/Linux you installed).<br>Host OS = AWS hypervisor layer (Nitro/Xen — AWS manages this). |

```
┌──────────────────────────────────────────┐
│  EC2 Instance                            │
│  GUEST OS (Windows/Linux) ← YOU patch   │
│  ─────────────────────────────────────   │
│  HYPERVISOR (Nitro)       ← AWS patches  │
│  PHYSICAL SERVER          ← AWS manages  │
└──────────────────────────────────────────┘
```

| **Q3** | Who patches the database engine on RDS? |
|:---|:---|
| **A** | AWS. RDS is a managed service — AWS handles OS and DB patching.<br><br>RDS vs EC2 DATABASE:<br>RDS: AWS patches OS + DB engine. YOU manage data, schema, access.<br>EC2: YOU patch everything. More control, more work. |

| **Q4** | Who is responsible for physical security of AWS data centers? |
|:---|:---|
| **A** | AWS. Always AWS. You never visit or touch AWS hardware.<br>AWS uses: armed guards, biometrics, cameras, unmarked buildings. |

| **Q5** | Customer stores sensitive data in S3. Who encrypts it? |
|:---|:---|
| **A** | The CUSTOMER. AWS provides encryption OPTIONS (SSE-S3, SSE-KMS, SSE-C)<br>but YOU must enable and configure encryption.<br><br>SSE = Server-Side Encryption<br>KMS = Key Management Service (manages encryption keys)<br>Encryption = Converting readable data to scrambled form. |

| **Q6** | Who configures security group rules on EC2? |
|:---|:---|
| **A** | The CUSTOMER. Network configuration is always customer responsibility. |

| **Q7** | What does "security OF the cloud" mean? |
|:---|:---|
| **A** | AWS responsibility — physical facilities, hardware, hypervisor,<br>global infrastructure, managed service underlying infrastructure. |

| **Q8** | What does "security IN the cloud" mean? |
|:---|:---|
| **A** | Customer responsibility — data, IAM, OS patching, app code,<br>security groups, NACLs, VPC config, encryption choices. |

| **Q9** | For Lambda, what is the customer responsible for? |
|:---|:---|
| **A** | Function code and IAM roles/permissions.<br>AWS manages all infrastructure, OS, runtime, scaling.<br><br>Lambda = AWS serverless compute. You upload code, AWS runs it.<br>Serverless = no servers for YOU to manage. |

| **Q10** | Which is ALWAYS AWS's responsibility? A) Encrypting customer data  B) Managing IAM passwords C) Physical decommissioning of storage hardware D) Patching guest OS on EC2 |
|:---|:---|
| **A** | C — Physical decommissioning. AWS wipes/destroys old disks.<br>DoD = Department of Defense (military-grade data wiping standard). |

| **Q11** | What is the AWS root user? |
|:---|:---|
| **A** | The identity created when account first opens.<br>Complete unrestricted access to everything. Cannot be deleted.<br><br>Like "sa" in SQL Server or "root" in Linux — don't use daily. |

| **Q12** | Best practice for AWS root user? |
|:---|:---|
| **A** | Enable MFA immediately. Create IAM admin user for daily work.<br>Only use root for tasks that specifically require it. |

| **Q13** | Which tasks require root user? |
|:---|:---|
| **A** | Change account settings/email, close account, change support plan,<br>restore deleted IAM admin, enable MFA delete on S3.<br>Everything else: use IAM users or roles. |

| **Q14** | What does IAM stand for? |
|:---|:---|
| **A** | Identity and Access Management.<br>Identity = WHO are you?  Access Management = WHAT can you do?<br>FREE service. GLOBAL (not region-specific). |

| **Q15** | Is IAM regional or global? |
|:---|:---|
| **A** | GLOBAL. IAM users, groups, roles, policies work across all regions.<br><br>GLOBAL services: IAM, Route 53, CloudFront, WAF<br>REGIONAL services: EC2, S3, RDS, VPC, Lambda |

| **Q16** | What permissions does a new IAM user have by default? |
|:---|:---|
| **A** | NONE. Zero permissions. Must be explicitly granted.<br>Principle of least privilege: start with nothing, add only what's needed. |

| **Q17** | What is the principle of least privilege? |
|:---|:---|
| **A** | Grant users only the minimum permissions needed for their job.<br>If credentials are stolen: minimal damage possible. |

| **Q18** | What is an IAM Group? |
|:---|:---|
| **A** |  |

```
Collection of IAM users. Attach policies to groups, not individuals.
New person joins → add to group → instantly gets all permissions.
Person leaves → remove from group → instantly loses permissions.
```

| **Q19** | Can an IAM group contain other IAM groups? |
|:---|:---|
| **A** | NO. Groups contain only users, never other groups.<br>A user CAN belong to multiple groups simultaneously. |

| **Q20** | What is an IAM Role? |
|:---|:---|
| **A** | Temporary identity not tied to a specific person.<br>Assumed by: EC2 instances, Lambda functions, cross-account access.<br>Best practice: use roles for EC2 apps instead of access keys.<br><br>USER = permanent identity for a specific person.<br>ROLE = like a hat anyone can put on temporarily. |

| **Q21** | When to use IAM Role vs access keys for EC2? |
|:---|:---|
| **A** | ALWAYS use IAM Role. Never store access keys on EC2.<br>Roles: no credentials stored, auto-rotate, easy to update.<br>Access keys on EC2: security risk if instance compromised. |

| **Q22** | What is an IAM Policy? |
|:---|:---|
| **A** | JSON document defining permissions — Allow or Deny specific<br>actions on specific resources.<br><br>Example: {"Effect":"Allow","Action":"s3:GetObject","Resource":"*"}<br>ARN = Amazon Resource Name (unique identifier for every AWS resource) |

| **Q23** | Three types of IAM policies? |
|:---|:---|
| **A** | AWS managed (created by AWS), customer managed (created by you),<br>inline (embedded directly in a user/role, not reusable). |

| **Q24** | What is MFA? |
|:---|:---|
| **A** | Multi-Factor Authentication.<br>Multi = more than one. Factor = proof of identity.<br>= Password (something you know) + Device (something you have).<br>Even if password stolen, attacker needs your physical device. |

| **Q25** | Which MFA type uses a smartphone app? |
|:---|:---|
| **A** | Virtual MFA device — Google Authenticator or Authy generates<br>TOTP = Time-based One-Time Password (6-digit code, changes every 30s). |

| **Q26** | Developer needs to make API calls from laptop. What credentials? |
|:---|:---|
| **A** | Access keys — Access Key ID (like username) +<br>Secret Access Key (like password, shown ONCE at creation).<br><br>CLI = Command Line Interface  SDK = Software Development Kit<br>API = Application Programming Interface |

| **Q27** | Best practice for access keys? |
|:---|:---|
| **A** | Never share. Never put in code. Never commit to Git.<br>Use IAM roles instead when possible. Rotate every 90 days.<br>Git = version control system (code repository). |

| **Q28** | All developers need S3 read access. Most efficient approach? |
|:---|:---|
| **A** | Create Developers IAM group, attach S3 read policy to group,<br>add all developers to group. One policy update affects all. |

| **Q29** | Which is TRUE about IAM? A) $0.01/user/month  B) Regional service C) New users have no permissions  D) Use root daily |
|:---|:---|
| **A** | C — new IAM users have ZERO permissions by default. |

| **Q30** | EC2 app needs to read from DynamoDB. Correct approach? |
|:---|:---|
| **A** | Create IAM Role with DynamoDB read permissions, attach to EC2.<br>DynamoDB = AWS's managed NoSQL database (serverless, ms performance).<br>NoSQL = Not only SQL (flexible schema, key-value store). |

| **Q31** | Difference between authentication and authorization? |
|:---|:---|
| **A** | Authentication = verifying WHO you are (login/identity).<br>Authorization = determining WHAT you can do (permissions). |

| **Q32** | Which is correct about IAM policies? A) Deny always overrides Allow  B) Allow overrides Deny C) They cancel each other  D) Users have Allow by default |
|:---|:---|
| **A** | A — DENY ALWAYS OVERRIDES ANY ALLOW. The golden IAM rule. |

| **Q33** | User in two groups: one allows S3, one denies S3. Can user access? |
|:---|:---|
| **A** | NO. Explicit Deny always wins. S3 access denied. |

| **Q34** | What is federated identity in IAM? |
|:---|:---|
| **A** | External identity providers (like Active Directory, Google) can<br>assume IAM roles via SAML. No separate IAM users needed per person.<br>SSO = Single Sign-On (log in once, access multiple systems).<br>AD = Active Directory (Microsoft's user directory). |

| **Q35** | Which service provides SSO across multiple AWS accounts? |
|:---|:---|
| **A** | AWS IAM Identity Center (formerly AWS SSO). |

| **Q36** | Lost MFA device for root account? |
|:---|:---|
| **A** | Contact AWS Support to recover access. Can take DAYS.<br>This is why storing root credentials safely is critical. |

| **Q37** | IMMEDIATELY after creating a new AWS account? A) Create 10 IAM users  B) Enable MFA on root C) Delete root  D) Create S3 buckets |
|:---|:---|
| **A** | B — Enable MFA on root IMMEDIATELY. |

| **Q38** | What is an access key composed of? |
|:---|:---|
| **A** | Access Key ID (starts with AKIA, 20 chars, like username) +<br>Secret Access Key (40 chars random, like password, shown ONCE).<br>If secret key lost: create new key pair, cannot retrieve old one. |

| **Q39** | Can you retrieve a Secret Access Key after creation? |
|:---|:---|
| **A** | NO. Only viewable once at creation. If lost, create new key pair. |

| **Q40** | Best IAM entity to grant third party temporary access? |
|:---|:---|
| **A** | IAM Role with cross-account trust policy.<br>STS = Security Token Service (issues temporary credentials).<br>They assume the role, get temp creds that expire automatically. |

| **Q41** | What is AWS Organizations? |
|:---|:---|
| **A** | Manage multiple AWS accounts centrally with consolidated billing,<br>volume discounts, and Service Control Policies (SCPs).<br>OU = Organizational Unit (folder for grouping accounts). |

| **Q42** | What are Service Control Policies (SCPs)? |
|:---|:---|
| **A** | IAM policies at organizational level setting MAXIMUM permission<br>limits for accounts. SCPs can only RESTRICT, never GRANT permissions. |

| **Q43** | Who manages the hypervisor in EC2? |
|:---|:---|
| **A** | AWS. The virtualization layer is always AWS's responsibility.<br>AWS uses Nitro hypervisor (like VMware ESXi but AWS's own). |

| **Q44** | IAM feature that enforces strong passwords? |
|:---|:---|
| **A** | IAM Password Policy — set minimum length, complexity, expiry,<br>rotation period, password history (prevent reuse). |

| **Q45** | Which is customer's responsibility for RDS? A) Patching DB engine  B) Managing EC2 instance C) Configuring security group rules  D) Physical security |
|:---|:---|
| **A** | C — Customer configures security groups and network access for RDS. |

| **Q46** | Type of policy to grant EC2 permission to write to S3? |
|:---|:---|
| **A** | IAM Role with S3 write policy, attached to EC2 as instance profile.<br>Instance Profile = container that passes IAM Role to EC2. |

| **Q47** | Can you attach multiple IAM policies to one user? |
|:---|:---|
| **A** | YES. All policies combined. Any DENY = final answer DENY. |

| **Q48** | Difference between IAM user and IAM role? |
|:---|:---|
| **A** | User = permanent identity for a specific person.<br>Role = temporary identity assumed by services or users. |

| **Q49** | Which service logs all API calls in your AWS account? |
|:---|:---|
| **A** | AWS CloudTrail — WHO made what API call, when, from where.<br>CloudTrail answers: WHO, WHAT, WHEN, WHERE for every action. |

| **Q50** | Who is responsible for enabling CloudTrail? |
|:---|:---|
| **A** | The CUSTOMER. AWS provides the service but YOU must enable it.<br>AWS never monitors your account FOR you — you set it up. |

DAY 2 COMPLETE
*Tomorrow: Day 3 — Core Compute Services*

## Day 3 — CORE COMPUTE SERVICES

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 3)

| Acronym | Definition |
|---|---|
| `EC2` | Elastic Compute Cloud (virtual servers) |
| `AMI` | Amazon Machine Image (OS template for EC2) |
| `EBS` | Elastic Block Store (block storage for EC2) |
| `ELB` | Elastic Load Balancer |
| `ALB` | Application Load Balancer (HTTP/HTTPS, Layer 7) |
| `NLB` | Network Load Balancer (TCP/UDP, Layer 4) |
| `GLB` | Gateway Load Balancer (third-party appliances) |
| `ASG` | Auto Scaling Group |
| `vCPU` | Virtual CPU (portion of physical CPU core) |
| `GPU` | Graphics Processing Unit (for ML/graphics) |
| `HPC` | High Performance Computing |
| `BYOL` | Bring Your Own License |
| `CI/CD` | Continuous Integration / Continuous Delivery |
| `K8s` | Kubernetes (container orchestration, 8 letters between K and s) |

#### Hour 1: Ec2

**EC2 INSTANCE FAMILIES:**
- General Purpose (T3, M5):    Balanced CPU/memory/network
- Compute Optimized (C5):      High CPU, batch processing, gaming
- Memory Optimized (R5, X1):   High RAM, in-memory databases, SAP HANA
- Storage Optimized (I3, D2):  High I/O, data warehousing
- Accelerated (P3, G4):        GPU, machine learning, AI

**EC2 PURCHASING OPTIONS (most tested):**
- On-Demand:         Pay per hour, no commitment, most expensive/hr
- Best for: unpredictable, short-term, testing
- Reserved (RI):     1 or 3 year commit, up to 72% discount
- Best for: steady-state predictable workloads
- Spot:              Use spare capacity, up to 90% off
- Can be terminated with 2-min warning
- Best for: fault-tolerant batch jobs, NOT databases
- Savings Plans:     Commit to $/hr for 1-3 years, flexible
- Applies to EC2, Lambda, Fargate
- Dedicated Hosts:   Physical server for you, BYOL compliance
- Dedicated Instances: Dedicated hardware, share with same account only


#### Hour 2: Other Compute

**Auto Scaling Group (ASG): Add/remove EC2 based on demand**
**ELB types: ALB (Layer 7, HTTP/HTTPS), NLB (Layer 4, TCP/UDP), GLB (appliances)**
**Lambda: Serverless, event-driven, max 15 min, pay per execution**
**Elastic Beanstalk: PaaS, upload code, AWS manages infra**
**ECS: AWS container orchestration (Docker)**
**EKS: Managed Kubernetes on AWS**
**Fargate: Serverless containers, no EC2 to manage**
**Lightsail: Simple VPS, fixed pricing, beginners**


### Questions & Answers — Day 3

| **Q1** | What is Amazon EC2? |
|:---|:---|
| **A** | Elastic Compute Cloud — virtual servers in the cloud.<br>Like a VM on your VMware cluster but AWS owns the hardware.<br>YOU manage: OS, apps, data, security groups.<br>AWS manages: physical servers, hypervisor, network hardware. |

| **Q2** | EC2 family for in-memory databases like SAP HANA? |
|:---|:---|
| **A** | Memory Optimized (R5, X1 family).<br>SAP HANA = SAP's enterprise database that keeps data in RAM.<br>RAM is 1,000x faster than SSD — memory-optimized maximizes this. |

| **Q3** | EC2 family for machine learning with GPUs? |
|:---|:---|
| **A** | Accelerated Computing (P3, G4 family).<br>GPU = Graphics Processing Unit: thousands of small cores for<br>parallel math — perfect for ML/AI matrix operations. |

| **Q4** | Which EC2 option has no upfront commitment and highest hourly cost? |
|:---|:---|
| **A** | On-Demand Instances. Maximum flexibility, maximum per-hour price.<br>Best for: testing, unknown workloads, short-term experiments. |

| **Q5** | Which EC2 option offers up to 90% discount but can be interrupted? |
|:---|:---|
| **A** |  |

```
Spot Instances. AWS needs capacity back → 2-min warning → terminated.
GOOD: batch jobs, big data, CI/CD, rendering (can restart).
BAD: production databases, real-time apps (cannot interrupt).
```

| **Q6** | When would you NOT use Spot Instances? |
|:---|:---|
| **A** | Critical workloads that cannot be interrupted: databases, real-time<br>apps. If Spot is terminated at 11 PM → production DOWN. |

| **Q7** | Best option for steady-state workload running 24/7 for 3 years? |
|:---|:---|
| **A** | Reserved Instances — 3-year commitment = up to 72% savings.<br>3yr m5.xlarge: $5,046 On-Demand vs ~$1,413 Reserved = 72% off. |

| **Q8** | Difference between Standard and Convertible Reserved Instances? |
|:---|:---|
| **A** | Standard RI: biggest discount (72%), cannot change instance type.<br>Convertible RI: smaller discount (~66%), CAN change instance family. |

| **Q9** | Company needs dedicated physical servers for software licensing. |
|:---|:---|
| **A** | Dedicated Hosts. BYOL = Bring Your Own License.<br>You see exact socket/core count for Oracle/Windows licensing. |

| **Q10** | Difference between Dedicated Hosts and Dedicated Instances? |
|:---|:---|
| **A** | Dedicated Host: you control and see the physical server.<br>Dedicated Instance: dedicated hardware but AWS manages the host. |

| **Q11** | What is Auto Scaling? |
|:---|:---|
| **A** | Automatically adjusts EC2 instance count based on demand.<br>Scale out (add instances) when demand rises.<br>Scale in (remove instances) when demand drops. |

```
┌──────────────────────────────────────────┐
│  ASG: Min=2, Max=10, Desired=2           │
│  CPU > 70%: launch more instances        │
│  CPU < 30%: terminate some instances     │
│  Always right-sized, never over-paying   │
└──────────────────────────────────────────┘
```

| **Q12** | Difference between scaling out and scaling up? |
|:---|:---|
| **A** | Scale OUT (horizontal): add more instances. No downtime. Preferred.<br>Scale UP (vertical): increase size of existing instance. Requires restart. |

| **Q13** | Which ELB operates at Layer 7 and supports HTTP/HTTPS routing? |
|:---|:---|
| **A** |  |

```
Application Load Balancer (ALB).
Layer 7 = Application layer. Can route by URL path, hostname, headers.
Example: /api/* → Server Group A, /web/* → Server Group B
```

| **Q14** | Which ELB for ultra-low latency TCP/UDP traffic? |
|:---|:---|
| **A** | Network Load Balancer (NLB).<br>Layer 4 = Transport layer. Handles millions of requests/second.<br>Use for: gaming (UDP), financial trading (TCP), IoT. |

| **Q15** | What is AWS Lambda? |
|:---|:---|
| **A** | Serverless compute — run code without managing servers.<br>Event-driven: triggers from S3, API Gateway, SQS, CloudWatch, etc.<br>Pay ONLY when code runs. Free tier: 1M requests/month forever. |

| **Q16** | Maximum execution time for a Lambda function? |
|:---|:---|
| **A** | 15 minutes (900 seconds). If > 15 min needed: use EC2 or ECS. |

| **Q17** | How are you charged for Lambda? |
|:---|:---|
| **A** | Number of requests + duration of execution.<br>Pay $0 when not running. 3 AM with no requests = $0 cost. |

| **Q18** | What is Elastic Beanstalk? |
|:---|:---|
| **A** | PaaS — deploy your application, AWS handles everything else.<br>Upload code → Beanstalk creates EC2, ELB, ASG, security groups.<br>Supported: Java, .NET, PHP, Python, Ruby, Go, Node.js, Docker. |

| **Q19** | Compute service for Docker containers without managing servers? |
|:---|:---|
| **A** | AWS Fargate — serverless containers. No EC2 instances to manage.<br>Docker = platform for building/running containers.<br>Container = lightweight VM-like unit packaging app and dependencies. |

| **Q20** | Difference between ECS and EKS? |
|:---|:---|
| **A** | ECS = AWS's own container orchestration (simpler, AWS-native).<br>EKS = Managed Kubernetes on AWS (for teams already using K8s).<br>K8s = Kubernetes (industry standard container orchestration). |

| **Q21** | Startup wants to deploy web app without managing any servers? |
|:---|:---|
| **A** | Lambda (backend functions) + Elastic Beanstalk (full app deployment).<br>Fargate also valid for containerized apps.<br>REST API = Representational State Transfer API (web standard). |

| **Q22** | Which option commits to $/hr across EC2, Lambda, and Fargate? |
|:---|:---|
| **A** | Savings Plans — more flexible than Reserved Instances.<br>Compute Savings Plans: apply across EC2, Lambda, Fargate.<br>EC2 Instance Savings Plans: specific family/region, higher discount. |

| **Q23** | Batch processing jobs that can be interrupted. Best option? |
|:---|:---|
| **A** | Spot Instances — up to 90% savings, batch jobs can restart. |

| **Q24** | What happens to Spot Instance when AWS needs capacity back? |
|:---|:---|
| **A** | 2-minute warning, then terminated. Unsaved data = LOST.<br>Save checkpoints to S3 regularly for restartable jobs. |

| **Q25** | Which load balancer for third-party virtual firewall appliances? |
|:---|:---|
| **A** | Gateway Load Balancer (GWLB/GLB).<br>Intercepts all traffic, routes through Palo Alto/Fortinet, returns. |

| **Q26** | Two services that handle traffic spikes automatically? |
|:---|:---|
| **A** | Auto Scaling (adjusts instance count) +<br>Elastic Load Balancing (distributes traffic to healthy instances). |

| **Q27** | Best EC2 family for a web server with balanced requirements? |
|:---|:---|
| **A** | General Purpose (T3, M5 family).<br>Memory trick: M5 = "Medium/balanced", C5 = "CPU", R5 = "RAM". |

| **Q28** | What is an EC2 instance profile? |
|:---|:---|
| **A** | Container that passes an IAM Role to an EC2 instance so it can<br>make AWS API calls. App retrieves temp credentials automatically<br>from http://169.254.169.254 (instance metadata service). |

| **Q29** | Company wants Java web app deployed without managing EC2? |
|:---|:---|
| **A** | AWS Elastic Beanstalk — supports Java (WAR files) and manages<br>all underlying infrastructure automatically.<br>JDK = Java Development Kit. WAR = Web Application Archive. |

| **Q30** | How does serverless differ from traditional compute? |
|:---|:---|
| **A** | Serverless: don't provision, manage, or pay for idle servers.<br>Pay only when code actually runs. Lambda, Fargate, DynamoDB, S3. |

| **Q31** | Which is correct about Reserved Instances? A) Change types freely  B) 1 or 3 year commitment C) More expensive than On-Demand  D) One region only |
|:---|:---|
| **A** | B — RI requires 1 or 3 year commitment. |

| **Q32** | HPC simulations. Which EC2 family? |
|:---|:---|
| **A** | Compute Optimized (C5/C5n for CPU) or Accelerated (P3/P4 for GPU).<br>HPC = High Performance Computing (scientific simulations).<br>EFA = Elastic Fabric Adapter (low-latency HPC networking). |

| **Q33** | Relationship between ECS and Fargate? |
|:---|:---|
| **A** | Fargate is a LAUNCH TYPE for ECS (and EKS) that removes need<br>to manage underlying EC2 infrastructure for containers. |

| **Q34** | Which service automatically replaces unhealthy EC2 instances? |
|:---|:---|
| **A** | Auto Scaling — health checks detect failure, terminate, replace.<br>Self-healing infrastructure with no human intervention needed. |

| **Q35** | Media company processes video in 6-hour nightly batch jobs? |
|:---|:---|
| **A** | Spot Instances — batch jobs can tolerate interruption, 90% savings. |

| **Q36** | Benefit of multiple AZs with Application Load Balancer? |
|:---|:---|
| **A** | High availability — if one AZ fails, ELB routes to healthy AZs.<br>ALB automatically discovers new instances added by Auto Scaling. |

| **Q37** | Best option for a 3-day experiment? |
|:---|:---|
| **A** | On-Demand — no commitment, pay hourly, stop when done. |

| **Q38** | Which is a valid Lambda trigger? A) S3 object upload  B) DynamoDB change  C) EC2 launch D) All of the above |
|:---|:---|
| **A** | D — Lambda can be triggered by hundreds of AWS events. |

| **Q39** | What type of scaling does a load balancer support? |
|:---|:---|
| **A** | Horizontal scaling (scale out) — distributing traffic across<br>multiple instances instead of one large server. |

| **Q40** | Migrate VMware workloads to AWS. Which service? |
|:---|:---|
| **A** | VMware Cloud on AWS — same vCenter, NSX, vSAN tools in AWS.<br>vMotion/HCX for live VM migration with no application changes.<br>HCX = Hybrid Cloud Extension (VMware migration tool). |

| **Q41** | What does EC2 stand for? |
|:---|:---|
| **A** | Elastic Compute Cloud.<br>Elastic = scales on demand. Compute = CPU+RAM. Cloud = AWS hosted. |

| **Q42** | Which is NOT a valid EC2 purchasing option? A) On-Demand  B) Spot  C) Perpetual License  D) Savings Plans |
|:---|:---|
| **A** | C — Perpetual License is not an EC2 pricing model. |

| **Q43** | How much can Reserved Instances save vs On-Demand? |
|:---|:---|
| **A** | Up to 72% with 3-year all-upfront commitment. |

| **Q44** | How much can Spot Instances save? |
|:---|:---|
| **A** | Up to 90% vs On-Demand pricing. |

| **Q45** | Compute Savings Plans vs EC2 Instance Savings Plans? |
|:---|:---|
| **A** | Compute SP: applies to EC2+Lambda+Fargate, any region (66% off).<br>EC2 Instance SP: specific instance family in specific region (72% off). |

| **Q46** | Which service for a serverless REST API backend? |
|:---|:---|
| **A** | AWS Lambda with API Gateway — standard serverless API pattern. |

| **Q47** | Company wants to never over-provision compute. Which feature? |
|:---|:---|
| **A** | Auto Scaling — automatically adjusts capacity to match actual demand.<br>Never paying for idle capacity. Never running short either. |

| **Q48** | What makes Fargate different from containers on EC2? |
|:---|:---|
| **A** | With Fargate you don't manage underlying EC2 instances at all.<br>Just define container CPU/memory requirements, AWS handles the rest. |

| **Q49** | Which model for new app with completely unknown usage pattern? |
|:---|:---|
| **A** | On-Demand — no commitment. Observe actual usage for 3 months,<br>then buy Reserved Instances or Savings Plans based on real data. |

| **Q50** | Financial company needs EC2 physically isolated from other customers? |
|:---|:---|
| **A** | Dedicated Hosts or Dedicated Instances — hardware not shared with<br>other AWS customer accounts.<br>Tenancy = who shares physical hardware. |

DAY 3 COMPLETE
*Tomorrow: Day 4 — Storage Services*

## Day 4 — STORAGE SERVICES

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 4)

| Acronym | Definition |
|---|---|
| `S3` | Simple Storage Service (object storage) |
| `EBS` | Elastic Block Store (block storage for EC2) |
| `EFS` | Elastic File System (managed NFS) |
| `NFS` | Network File System (Linux shared file protocol) |
| `SMB` | Server Message Block (Windows file sharing) |
| `IOPS` | Input/Output Operations Per Second |
| `SSD` | Solid State Drive (fast flash storage) |
| `HDD` | Hard Disk Drive (slower spinning disk) |
| `WORM` | Write Once Read Many (immutable storage compliance) |
| `CRR` | Cross-Region Replication |
| `SRR` | Same-Region Replication |
| `SSE` | Server-Side Encryption |
| `AES` | Advanced Encryption Standard (AES-256 = 256-bit encryption) |
| `RTO` | Recovery Time Objective (max downtime allowed) |
| `RPO` | Recovery Point Objective (max data loss allowed) |
| `NAS` | Network Attached Storage |
| `VTL` | Virtual Tape Library |
| `LTO` | Linear Tape-Open (tape format) |
| `PB` | Petabyte (1,000 TB) |

STUDY NOTES — HOURS 1 & 2: ALL STORAGE SERVICES
S3 STORAGE CLASSES (memorize all 7):
Standard:              Frequent access, $0.023/GB, no minimum
Intelligent-Tiering:   Unknown patterns, auto-moves between tiers
Standard-IA:           Infrequent access, $0.0125/GB, 30-day min, retrieval fee
One Zone-IA:           Infrequent, ONE AZ only, $0.010/GB, data lost if AZ fails
Glacier Instant:       Archive, quarterly access, millisecond retrieval, 90-day min
Glacier Flexible:      Archive, minutes-hours retrieval, 90-day min
Glacier Deep Archive:  CHEAPEST ($0.00099/GB), 12-hr retrieval, 180-day min

EBS VOLUME TYPES:
gp3: General Purpose SSD — most common, up to 16,000 IOPS
io2: Provisioned IOPS SSD — high-performance databases, up to 256,000 IOPS
st1: Throughput HDD — big data, sequential workloads
sc1: Cold HDD — cheapest, infrequently accessed data

EFS: Managed NFS, multiple Linux EC2 instances simultaneously, auto-scales
Instance Store: Temporary, physically attached NVMe, fastest, LOST on stop
Storage Gateway: Hybrid — File Gateway (NFS/SMB→S3), Volume (iSCSI→S3), Tape (VTL→Glacier)
Snow Family: Snowcone (8TB), Snowball Edge (80TB), Snowmobile (100PB truck)
FSx: Windows File Server (SMB/AD), Lustre (HPC), NetApp ONTAP, OpenZFS

### Questions & Answers — Day 4

| **Q1** | What type of storage is Amazon S3? |
|:---|:---|
| **A** | Object storage. Files stored as objects with key, data, and metadata.<br>Unlimited storage. Objects up to 5 TB each. Globally unique bucket names.<br>99.999999999% (11 nines) durability — stored across 3+ AZs automatically. |

| **Q2** | Maximum size of a single S3 object? |
|:---|:---|
| **A** | 5 TB. Files > 5 GB must use Multipart Upload (uploads in parallel chunks). |

| **Q3** | S3 durability? |
|:---|:---|
| **A** | 99.999999999% (11 nines). Store 10 billion objects, expect to lose 1/year.<br>Automatically stores across minimum 3 AZs within the region. |

| **Q4** | Most cost-effective for data rarely accessed with 12-hour retrieval? |
|:---|:---|
| **A** | S3 Glacier Deep Archive. $0.00099/GB/month. 180-day minimum retention. |

| **Q5** | Which S3 class for unknown or changing access patterns? |
|:---|:---|
| **A** | S3 Intelligent-Tiering — auto-moves objects between tiers.<br>Small monthly monitoring fee. Access object → moves back to frequent tier. |

| **Q6** | Minimum storage duration for S3 Glacier Deep Archive? |
|:---|:---|
| **A** | 180 days. Delete before 180 days = still charged for 180. |

| **Q7** | Which S3 class stores data in ONLY ONE Availability Zone? |
|:---|:---|
| **A** | S3 One Zone-IA. Cheaper but data permanently LOST if that AZ fails.<br>Use only for recreatable data (thumbnails, processed outputs). |

| **Q8** | What is an S3 bucket? |
|:---|:---|
| **A** | Container for storing objects. Names must be GLOBALLY UNIQUE across all AWS.<br>URL: https://[bucket-name].s3.amazonaws.com/[key] |

| **Q9** | How to automatically move S3 objects between classes over time? |
|:---|:---|
| **A** |  |

```
S3 Lifecycle Rules — define policies to transition or expire objects.
Example: Standard → Standard-IA (day 30) → Glacier (day 90) → Delete (day 365)
```

| **Q10** | Store compliance archives for 7 years, rarely accessed? |
|:---|:---|
| **A** | S3 Glacier Deep Archive. Most cost-effective. 12-hour retrieval fine for audit. |

| **Q11** | What is Amazon EBS? |
|:---|:---|
| **A** | Elastic Block Store — persistent block storage volumes for EC2.<br>Like a virtual hard drive. Network-attached (not physically attached).<br>Persists when EC2 stops. Must be in same AZ as EC2 instance. |

| **Q12** | How many EC2 instances can an EBS volume attach to? |
|:---|:---|
| **A** | ONE (standard volumes). io2 Multi-Attach allows up to 16 in same AZ.<br>Like a SAN LUN — one host maps to one LUN (normally). |

| **Q13** | What happens to EBS data when EC2 terminates? |
|:---|:---|
| **A** | Root EBS volume: deleted by default.<br>Additional volumes: persist by default.<br>STOPPED (not terminated): all EBS data intact. |

| **Q14** | What is an EBS Snapshot? |
|:---|:---|
| **A** | Point-in-time backup stored in S3. Incremental (only changed blocks).<br>Use to: restore in same AZ, create in different AZ, copy cross-region. |

| **Q15** | Difference between EBS and Instance Store? |
|:---|:---|
| **A** | EBS: persistent — survives stop/terminate (network-attached).<br>Instance Store: temporary — LOST when stopped/terminated/fails.<br>Instance Store: physically attached NVMe, much faster than EBS. |

| **Q16** | Which storage is fastest and physically attached? |
|:---|:---|
| **A** | Instance Store — directly attached NVMe SSD.<br>NVMe = Non-Volatile Memory Express (fastest SSD interface).<br>Speed order: Instance Store > EBS gp3 > EFS > S3 |

| **Q17** | What is Amazon EFS? |
|:---|:---|
| **A** | Elastic File System — managed NFS that multiple EC2 instances can<br>mount SIMULTANEOUSLY. Auto-scales. Linux only.<br>For Windows shared files: use FSx for Windows File Server. |

| **Q18** | How does EFS differ from EBS? |
|:---|:---|
| **A** | EFS: shared across MULTIPLE instances and AZs. Auto-scales. NFS.<br>EBS: attached to SINGLE instance. Manual sizing. Block storage.<br>Use EFS: shared content management, web farm (100 servers same files).<br>Use EBS: database volumes, OS boot drives. |

| **Q19** | Shared filesystem for 100 Linux EC2 instances simultaneously? |
|:---|:---|
| **A** | Amazon EFS — designed for shared access across many instances. |

| **Q20** | What is AWS Storage Gateway? |
|:---|:---|
| **A** |  |

```
Hybrid cloud storage — connects on-premises environments to AWS.
Apps see local interface; data actually stored in S3/Glacier.
Types: File Gateway (NFS/SMB→S3), Volume (iSCSI→S3), Tape (VTL→Glacier)
```

| **Q21** | Which Storage Gateway type presents NFS/SMB interface to S3? |
|:---|:---|
| **A** | File Gateway — apps write to NFS/SMB share, data goes to S3. |

| **Q22** | Which Storage Gateway type presents iSCSI block storage? |
|:---|:---|
| **A** | Volume Gateway. iSCSI = Internet Small Computer Systems Interface<br>(block storage over IP/TCP — like SAN but over Ethernet). |

| **Q23** | Which Storage Gateway type replaces tape libraries? |
|:---|:---|
| **A** | Tape Gateway — VTL (Virtual Tape Library) backed by S3/Glacier.<br>Same backup software (NetBackup/TSM) unchanged. No physical tapes. |

| **Q24** | When to use Snowball Edge instead of internet transfer? |
|:---|:---|
| **A** | When data is too large (>10TB generally) or bandwidth is insufficient.<br>1 PB over 100 Mbps internet = ~3 years. Snowball = weeks. |

| **Q25** | Capacity of AWS Snowmobile? |
|:---|:---|
| **A** | 100 petabytes — 45-foot semi-truck. Armed guards, GPS, encrypted.<br>AWS drives the truck to your DC. Plug in fiber, transfer data. |

| **Q26** | Best FSx for Windows SMB file shares? |
|:---|:---|
| **A** | Amazon FSx for Windows File Server — fully managed, AD integration,<br>DFS namespaces, SMB protocol. AD = Active Directory. |

| **Q27** | Which FSx is relevant to NetApp ONTAP users? |
|:---|:---|
| **A** | Amazon FSx for NetApp ONTAP — same SVM, NFS/CIFS/iSCSI, SnapMirror.<br>Migrate NetApp workloads to AWS with no application changes. |

| **Q28** | Which S3 feature protects against accidental deletion? |
|:---|:---|
| **A** | S3 Versioning — keeps multiple versions. Delete adds a delete marker<br>(versions still exist). Remove marker = file restored. |

| **Q29** | Replicate S3 data to another region for DR? |
|:---|:---|
| **A** | S3 Cross-Region Replication (CRR). Requires versioning on both buckets.<br>SRR = Same-Region Replication (for log aggregation, test sync). |

| **Q30** | What is an S3 presigned URL? |
|:---|:---|
| **A** | Time-limited URL granting temporary access to private S3 object.<br>No AWS credentials needed. Configurable expiry (seconds to days). |

| **Q31** | Best EBS type for high-performance databases needing high IOPS? |
|:---|:---|
| **A** | io2 (Provisioned IOPS SSD) — up to 256,000 IOPS. For SAP HANA, Oracle, SQL Server. |

| **Q32** | Best EBS type for general purpose at lowest cost? |
|:---|:---|
| **A** | gp3 (General Purpose SSD) — 3,000 baseline IOPS, $0.08/GB.<br>Replaced gp2 as default. IOPS independent of volume size. |

| **Q33** | Can EBS volumes be in a different AZ than EC2? |
|:---|:---|
| **A** | NO. Must be in same AZ. To move: take snapshot, create volume<br>from snapshot in target AZ. |

| **Q34** | How to move EBS volume to a different AZ? |
|:---|:---|
| **A** | Snapshot the volume → create new volume from snapshot in target AZ<br>→ attach to EC2 in that AZ. Cannot directly "move" a volume. |

| **Q35** | Which S3 encryption uses AWS-managed keys requiring no customer work? |
|:---|:---|
| **A** | SSE-S3 — AWS manages keys entirely. AES-256. Free. No audit trail. |

| **Q36** | Which S3 encryption lets you use KMS for key control? |
|:---|:---|
| **A** | SSE-KMS — you control key policies, can audit all key usage via CloudTrail.<br>Better for compliance requiring separation of duties. |

| **Q37** | S3 Standard-IA minimum storage duration? |
|:---|:---|
| **A** | 30 days. Delete before 30 days = still charged for 30. |

| **Q38** | S3 Glacier Instant Retrieval minimum storage duration? |
|:---|:---|
| **A** | 90 days. Millisecond retrieval (vs minutes-hours for Flexible). |

| **Q39** | Host a static website (HTML/CSS/JS) with no servers? |
|:---|:---|
| **A** | Amazon S3 static website hosting. Extremely cheap. No EC2 needed.<br>Add CloudFront for HTTPS and custom domain. |

| **Q40** | Difference between S3 Standard and S3 Standard-IA? |
|:---|:---|
| **A** | Standard: $0.023/GB, no retrieval fee, for frequent daily access.<br>Standard-IA: $0.0125/GB + retrieval fee, for monthly/occasional access. |

| **Q41** | Snow Family for migrating 50TB with no internet access? |
|:---|:---|
| **A** | Snowball Edge — up to 80TB usable, works offline. |

| **Q42** | Which storage auto-grows and shrinks based on usage? |
|:---|:---|
| **A** | Amazon EFS — no pre-provisioning. Start at 0 GB. Pay per GB used. |

| **Q43** | Can S3 bucket names be reused after deletion? |
|:---|:---|
| **A** | YES — name becomes globally available again. Security risk: old URLs<br>could serve attacker's content if they register the name. |

| **Q44** | What is S3 Object Lock? |
|:---|:---|
| **A** | Prevents deletion/overwriting for set time — WORM compliance.<br>Governance Mode: privileged users can override.<br>Compliance Mode: NOBODY can delete (not even root!) during retention.<br>WORM = Write Once Read Many. Use for SEC, FINRA, HIPAA compliance. |

| **Q45** | Extend on-premises NAS to AWS while maintaining local access? |
|:---|:---|
| **A** | AWS Storage Gateway File Gateway — local NFS/SMB interface backed by S3.<br>NAS = Network Attached Storage (Isilon/PowerScale, NetApp, etc.) |

| **Q46** | What happens to Instance Store data if host fails? |
|:---|:---|
| **A** | Data is PERMANENTLY LOST. Instance Store has zero durability guarantees.<br>Good for: temporary cache, scratch space, swap files. |

| **Q47** | Company has 2PB to migrate. Internet would take years? |
|:---|:---|
| **A** | AWS Snowmobile — 100PB semi-truck.<br>2PB over Snowmobile: ~27 minutes of data transfer. Plus shipping weeks. |

| **Q48** | Best S3 class for frequently accessed data with highest performance? |
|:---|:---|
| **A** | S3 Standard. 99.99% availability, no retrieval fee, no minimum duration. |

| **Q49** | What is S3 Transfer Acceleration? |
|:---|:---|
| **A** | Uses CloudFront edge locations to speed up S3 uploads worldwide.<br>Upload to mybucket.s3-accelerate.amazonaws.com instead of s3.amazonaws.com. |

| **Q50** | DR scenario with RTO of 12 hours, data accessed less than once/year? |
|:---|:---|
| **A** | S3 Glacier Deep Archive — 12-hour retrieval matches 12-hour RTO.<br>Cheapest option. 180-day minimum retention.<br>RTO = Recovery Time Objective (max acceptable downtime).<br>RPO = Recovery Point Objective (max acceptable data loss). |

DAY 4 COMPLETE
*Tomorrow: Day 5 — Databases*

## Day 5 — DATABASES

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 5)

| Acronym | Definition |
|---|---|
| `RDS` | Relational Database Service |
| `SQL` | Structured Query Language (database query language) |
| `OLTP` | Online Transaction Processing (many small fast transactions) |
| `OLAP` | Online Analytical Processing (complex queries on large data) |
| `BI` | Business Intelligence (data analysis and reporting) |
| `ETL` | Extract, Transform, Load (data pipeline process) |
| `DMS` | Database Migration Service |
| `SCT` | Schema Conversion Tool |
| `DAX` | DynamoDB Accelerator (in-memory cache for DynamoDB) |
| `RCU` | Read Capacity Unit |
| `WCU` | Write Capacity Unit |
| `CDC` | Change Data Capture |
| `GSI` | Global Secondary Index |
| `LSI` | Local Secondary Index |
| `PITR` | Point-In-Time Recovery |

STUDY NOTES — HOURS 1 & 2: ALL DATABASE SERVICES
RDS: Managed relational DB. Engines: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora.
AWS manages: OS patching, DB engine patching, backups, scaling, hardware.
Multi-AZ: SYNCHRONOUS standby → HIGH AVAILABILITY (automatic failover).
Read Replica: ASYNCHRONOUS copy → PERFORMANCE (read scaling only, not failover).
EXAM: Multi-AZ = HA. Read Replica = Performance. Know the difference!

Aurora: AWS cloud-native, MySQL/PostgreSQL compatible. 5x faster than MySQL.
6 copies across 3 AZs automatically. Storage auto-grows 10GB increments to 128TB.
Aurora Serverless: auto-scales capacity. Aurora Global: cross-region replication.

DynamoDB: Fully managed NoSQL. Serverless. Single-digit ms at ANY scale.
Key-value + document. Flexible schema. DynamoDB Global Tables: multi-region.
DAX: in-memory cache for DynamoDB → microsecond latency.

ElastiCache: In-memory caching. Redis (persistence, pub/sub, sorted sets) or
Memcached (simple, multi-threaded). Sub-millisecond latency.

Redshift: Data warehouse. OLAP/BI. COLUMNAR storage. Petabyte-scale analytics.

DocumentDB: MongoDB-compatible managed document database.
Neptune: Graph database. Social networks, fraud detection, knowledge graphs.
QLDB: Immutable cryptographically verifiable ledger. Financial compliance.
Timestream: Time-series database for IoT and operational metrics.
DMS: Database Migration Service. Homogeneous (Oracle→Oracle) and heterogeneous.
Athena: Serverless SQL queries directly on S3 data. $5/TB scanned.

### Questions & Answers — Day 5

| **Q1** | What does RDS manage for you vs running DB on EC2? |
|:---|:---|
| **A** | RDS manages: OS patching, DB engine patching, backups, scaling, hardware.<br>You manage: data, schema, queries, access, security groups.<br>EC2 DB: YOU manage everything above plus OS and DB patching. |

| **Q2** | Which database engines does RDS support? |
|:---|:---|
| **A** | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Amazon Aurora. |

| **Q3** | Difference between RDS Multi-AZ and Read Replicas? |
|:---|:---|
| **A** |  |

```
Multi-AZ: SYNCHRONOUS replication → HIGH AVAILABILITY → automatic failover.
Read Replica: ASYNCHRONOUS replication → PERFORMANCE → read scaling only.
Multi-AZ standby: CANNOT be read from (failover only).
Read Replica: CAN be read from. Can be in different region.
EXAM TRAP: Read Replicas ≠ failover. Only Multi-AZ = failover.
```

| **Q4** | Can you use Read Replica for automatic failover? |
|:---|:---|
| **A** | NO. Read Replicas are for read scaling only. Multi-AZ handles failover.<br>Failover time for Multi-AZ: ~1-2 minutes (DNS updates automatically). |

| **Q5** | What is Amazon Aurora? |
|:---|:---|
| **A** | AWS cloud-native relational DB. MySQL + PostgreSQL compatible.<br>5x faster than MySQL, 3x faster than PostgreSQL.<br>6 copies across 3 AZs. Storage auto-grows in 10GB increments to 128TB. |

| **Q6** | How much faster is Aurora vs MySQL? |
|:---|:---|
| **A** | Up to 5x faster than standard MySQL. |

| **Q7** | What is Aurora Serverless? |
|:---|:---|
| **A** | Aurora that auto-starts, scales capacity, and pauses based on demand.<br>Paused = $0 cost. Good for: dev/test, variable/unpredictable load.<br>ACU = Aurora Capacity Unit (unit of compute for Serverless). |

| **Q8** | What is DynamoDB? |
|:---|:---|
| **A** | Fully managed NoSQL key-value + document database.<br>Serverless. Single-digit millisecond performance at ANY scale.<br>From 1 item to 10 petabytes — same ms latency. |

| **Q9** | What type of database is DynamoDB? |
|:---|:---|
| **A** | NoSQL — key-value and document store.<br>NoSQL = Not only SQL. Flexible schema. No rigid table structure. |

| **Q10** | Which DB service requires no server management and scales automatically? |
|:---|:---|
| **A** | DynamoDB — fully serverless NoSQL. Also Aurora Serverless. |

| **Q11** | What is DynamoDB DAX? |
|:---|:---|
| **A** | DynamoDB Accelerator — in-memory cache for DynamoDB.<br>Microsecond response times (vs ms for DynamoDB).<br>Cache HIT: serve from DAX, no DynamoDB charge.<br>Cache MISS: fetch from DynamoDB, cache it, serve. |

| **Q12** | DAX vs ElastiCache — when to use each? |
|:---|:---|
| **A** | DAX: ONLY for DynamoDB caching. Same API as DynamoDB.<br>ElastiCache: for RDS, MySQL, or any other general caching needs. |

| **Q13** | What is Amazon ElastiCache? |
|:---|:---|
| **A** | Managed in-memory caching (Redis or Memcached).<br>Sub-millisecond latency. Reduces database load for repeated queries. |

| **Q14** | What is Amazon Redshift? |
|:---|:---|
| **A** | Data warehouse for analytics. OLAP workloads. Columnar storage.<br>Petabyte-scale. Use for BI and complex analytical queries.<br>NOT for transactional workloads (use RDS/DynamoDB for OLTP). |

| **Q15** | Difference between OLTP and OLAP? |
|:---|:---|
| **A** | OLTP: many small fast transactions (INSERT/UPDATE). Use RDS/DynamoDB.<br>     Example: ATM, e-commerce orders, trading transactions.<br>OLAP: complex queries on large historical datasets. Use Redshift.<br>     Example: revenue by region, risk analysis, regulatory reporting. |

| **Q16** | Which database for MongoDB workloads? |
|:---|:---|
| **A** | Amazon DocumentDB — MongoDB-compatible managed document database. |

| **Q17** | What is Amazon Neptune? |
|:---|:---|
| **A** | Graph database. Data stored as nodes and edges.<br>Use for: social networks, fraud detection, knowledge graphs.<br>Graph queries are 100x faster than relational JOINs at scale. |

| **Q18** | Which DB for immutable cryptographically verifiable transactions? |
|:---|:---|
| **A** |  |

```
Amazon QLDB — Quantum Ledger Database.
Hash chain: change old record → hash chain breaks → tampering detected.
Use for: banking ledgers, supply chain, insurance, financial compliance.
```

| **Q19** | IoT sensors sending data every second. Which DB? |
|:---|:---|
| **A** | Amazon Timestream — purpose-built time-series database.<br>Auto-tiering: recent data hot, older data cold. Built-in time functions. |

| **Q20** | What is AWS DMS? |
|:---|:---|
| **A** | Database Migration Service — migrate DBs to AWS with minimal downtime.<br>Full Load (copy existing) + CDC (capture ongoing changes) = near-zero downtime.<br>CDC = Change Data Capture. |

| **Q21** | What is a homogeneous database migration? |
|:---|:---|
| **A** | Same engine: Oracle on-prem → Oracle on RDS.<br>DMS only. No schema conversion needed. |

| **Q22** | What is a heterogeneous database migration? |
|:---|:---|
| **A** | Different engines: Oracle → Aurora PostgreSQL.<br>Use AWS Schema Conversion Tool (SCT) first, then DMS. |

| **Q23** | Which service assists with schema conversion? |
|:---|:---|
| **A** | AWS Schema Conversion Tool (SCT) — converts schema and SQL code<br>between database engines. Free desktop application. |

| **Q24** | Company wants max read performance for RDS MySQL? |
|:---|:---|
| **A** | Add Read Replicas — distribute read queries across multiple replicas.<br>App: reads to replica endpoints, writes to primary endpoint only. |

| **Q25** | What happens during RDS Multi-AZ failover? |
|:---|:---|
| **A** | AWS automatically switches DNS endpoint to the standby (~1-2 min).<br>Zero data loss (synchronous replication). App must handle reconnect. |

| **Q26** | Which DB natively replicates across multiple AWS regions? |
|:---|:---|
| **A** | DynamoDB Global Tables — multi-region, multi-active replication.<br>Write anywhere, replicated to all regions in <1 second. |

| **Q27** | Aurora storage auto-scaling increment? |
|:---|:---|
| **A** | 10GB — grows automatically in 10GB increments up to 128TB. No downtime. |

| **Q28** | Gaming leaderboard with millions of concurrent users? |
|:---|:---|
| **A** | DynamoDB with DAX — serverless, any scale, microsecond latency. |

| **Q29** | ElastiCache engine with persistence and pub/sub? |
|:---|:---|
| **A** | Redis — more feature-rich. Sorted sets (perfect for leaderboards),<br>persistence, pub/sub, replication, transactions. |

| **Q30** | ElastiCache for simple high-throughput caching? |
|:---|:---|
| **A** | Memcached — simpler, multi-threaded, no persistence. Pure caching. |

| **Q31** | Run SQL queries on S3 data without loading into a database? |
|:---|:---|
| **A** | YES — Amazon Athena. Serverless. $5/TB scanned. Query S3 directly. |

| **Q32** | Company needs SQL queries on S3 data lake? |
|:---|:---|
| **A** | Amazon Athena — define table in Glue Catalog, query S3 with SQL.<br>Use Parquet format: columnar = scan less data = cheaper + faster. |

| **Q33** | Difference between RDS and database on EC2? |
|:---|:---|
| **A** | RDS managed: AWS handles OS, DB patching, backups, HA, scaling.<br>EC2 DB: YOU handle everything. More control, much more work.<br>Use EC2 when: unsupported engine, need OS access, special config. |

| **Q34** | Which scenario requires database on EC2 rather than RDS? |
|:---|:---|
| **A** | Unsupported engine (IBM DB2, Sybase), OS-level access needed,<br>Oracle RAC clustering, specific legacy version not in RDS. |

| **Q35** | What is Aurora Global Database? |
|:---|:---|
| **A** | Single Aurora database spanning multiple regions. Sub-second replication.<br>RPO < 1 second, RTO < 1 minute. Up to 5 secondary regions. |

| **Q36** | How many Aurora Read Replicas can you have? |
|:---|:---|
| **A** | Up to 15 read replicas. NO replication lag (shared distributed storage).<br>Standard RDS: up to 5 replicas (with lag). |

| **Q37** | Which DB for content management storing JSON documents? |
|:---|:---|
| **A** | Amazon DocumentDB — MongoDB-compatible. JSON documents stored naturally.<br>No complex JOINs needed for nested document data. |

| **Q38** | Financial company needs unalterable transaction history? |
|:---|:---|
| **A** | Amazon QLDB — immutable ledger, cryptographic hash chain.<br>Prove records were NEVER altered since creation. |

| **Q39** | What makes Redshift different from RDS for analytics? |
|:---|:---|
| **A** | Redshift: COLUMNAR storage — only reads columns needed for query.<br>RDS: ROW storage — must read entire row even if only 2 columns needed.<br>For analytics: columnar = 10-100x faster and cheaper. |

| **Q40** | Cache most frequently run RDS queries? |
|:---|:---|
| **A** | Amazon ElastiCache — cache query results, reduce DB load.<br>TTL = Time to Live (how long to keep data in cache before refreshing). |

| **Q41** | Primary key structure in DynamoDB? |
|:---|:---|
| **A** | Partition key (required) + optional sort key = composite primary key.<br>GSI = Global Secondary Index (query on non-key attributes).<br>LSI = Local Secondary Index (alternative sort key). |

| **Q42** | E-commerce site needing fast scalable product catalog? |
|:---|:---|
| **A** | DynamoDB — flexible schema (different attributes per product),<br>single-digit ms latency, auto-scales for Black Friday traffic. |

| **Q43** | DynamoDB consistency types? |
|:---|:---|
| **A** | Eventually consistent reads (default, cheaper).<br>Strongly consistent reads (request option, 2x cost, no lag).<br>Use strong consistency: financial balances, inventory counts. |

| **Q44** | RDS feature for compliance by maintaining automated backups? |
|:---|:---|
| **A** | Automated backups — daily snapshot + transaction logs every 5 min.<br>PITR = Point-In-Time Recovery — restore to any 5-minute window.<br>Retention: 1-35 days (you configure). |

| **Q45** | RDS automated backup retention period? |
|:---|:---|
| **A** | 1 to 35 days. Default varies by engine.<br>Manual snapshots: kept UNTIL YOU DELETE THEM (no expiry). |

| **Q46** | SQL queries on S3 data without servers? |
|:---|:---|
| **A** | Amazon Athena — serverless, no cluster to manage, pay per TB scanned. |

| **Q47** | Social network needing to find connections between users? |
|:---|:---|
| **A** | Graph database — Amazon Neptune. Nodes=people, Edges=connections.<br>100x faster than relational JOINs for connected data at scale. |

| **Q48** | What is Amazon Redshift Serverless? |
|:---|:---|
| **A** | Redshift that auto-provisions and scales capacity.<br>Pay per RPU-second. Good for sporadic analytics workloads.<br>RPU = Redshift Processing Unit. |

| **Q49** | Purpose of RDS parameter group? |
|:---|:---|
| **A** | Container for DB engine configuration values.<br>Like my.cnf for MySQL or postgresql.conf. Managed by AWS in RDS.<br>Static parameters: require reboot. Dynamic: applied immediately. |

| **Q50** | Which is correct about DynamoDB? A) Must manage servers  B) Supports SQL natively C) Single-digit ms latency  D) Key-value only |
|:---|:---|
| **A** | C — Single-digit millisecond performance at ANY scale.<br>A is wrong: serverless. B: uses its own API (PartiQL for SQL-like).<br>D: key-value AND document, with GSI for rich queries. |

DAY 5 COMPLETE
*Tomorrow: Day 6 — Networking & Content Delivery*

## Day 6 — NETWORKING & CONTENT DELIVERY

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 6)

| Acronym | Definition |
|---|---|
| `VPC` | Virtual Private Cloud (your private network in AWS) |
| `IGW` | Internet Gateway (connects VPC to internet) |
| `NAT` | Network Address Translation (private → internet outbound) |
| `NACL` | Network Access Control List (subnet-level firewall) |
| `SG` | Security Group (instance-level firewall) |
| `CIDR` | Classless Inter-Domain Routing (IP range notation e.g. 10.0.0.0/16) |
| `DNS` | Domain Name System (translates domain names to IP addresses) |
| `BGP` | Border Gateway Protocol (internet routing protocol) |
| `ENI` | Elastic Network Interface (virtual NIC) |
| `TLS` | Transport Layer Security (encryption protocol) |
| `HTTPS` | HTTP Secure (HTTP + TLS encryption) |
| `WAF` | Web Application Firewall |
| `DDoS` | Distributed Denial of Service |
| `TGW` | Transit Gateway (hub for connecting multiple VPCs) |
| `DX` | Direct Connect (dedicated private fiber to AWS) |
| `CGW` | Customer Gateway (your on-premises VPN device) |
| `VGW` | Virtual Private Gateway (AWS side of VPN) |
| `XSS` | Cross-Site Scripting (web attack type) |

STUDY NOTES — HOURS 1 & 2: NETWORKING AND CONTENT DELIVERY
VPC KEY RULES:
Public subnet: has route to Internet Gateway (0.0.0.0/0 → IGW)
Private subnet: no direct internet route
Security Groups: INSTANCE level, STATEFUL, ALLOW only, all rules evaluated
NACLs: SUBNET level, STATELESS, ALLOW + DENY, rules evaluated by number order
VPC Peering: NOT transitive (A↔B + B↔C ≠ A↔C)
Transit Gateway: IS transitive, hub-and-spoke for many VPCs
Direct Connect: private fiber, consistent, expensive, weeks to set up
Site-to-Site VPN: encrypted over internet, quick/cheap, variable performance

ROUTE 53 ROUTING POLICIES:
Simple: one resource. Weighted: split by %. Latency: lowest latency region.
Failover: active-passive DR. Geolocation: user's physical location.
Multivalue: up to 8 healthy records.

CONTENT DELIVERY:
CloudFront: CDN, caches at 400+ edge locations, HTTP/HTTPS only
Global Accelerator: routes over AWS private network, TCP/UDP, static IPs
API Gateway: create/manage APIs, works with Lambda for serverless APIs

### Questions & Answers — Day 6

| **Q1** | What is a VPC? |
|:---|:---|
| **A** | Virtual Private Cloud — your logically isolated private network in AWS.<br>You define IP range (CIDR), subnets, routes, gateways, security rules.<br>Like your T. Rowe network today but in the cloud.<br>CIDR: 10.0.0.0/16 = first 16 bits fixed = 65,536 possible IPs. |

| **Q2** | Difference between public and private subnet? |
|:---|:---|
| **A** | Public: has route to Internet Gateway (0.0.0.0/0 → IGW).<br>Internet can reach resources. Use for: web servers, load balancers.<br>Private: no direct internet route. Internet cannot reach resources.<br>Use for: databases, application servers. |

| **Q3** | What is an Internet Gateway? |
|:---|:---|
| **A** | VPC component allowing resources to communicate with internet.<br>Bidirectional. Horizontally scaled, redundant, HA. FREE to attach.<br>ONE IGW per VPC. Performs NAT for public IPs. |

| **Q4** | What is a NAT Gateway? |
|:---|:---|
| **A** | Allows private subnet instances to initiate OUTBOUND internet connections.<br>Internet CANNOT initiate connection back in (one-way only).<br>Managed service. Must be placed in PUBLIC subnet.<br>Use for: EC2 patching, external API calls from private instances. |

| **Q5** | Where must a NAT Gateway be placed? |
|:---|:---|
| **A** | In a PUBLIC subnet. It needs internet access (via IGW) itself to forward traffic.<br>NAT in private subnet = broken. Place one in EACH AZ for HA. |

| **Q6** | What is a Security Group? |
|:---|:---|
| **A** | Virtual firewall at INSTANCE level. Stateful. ALLOW rules only.<br>All rules evaluated simultaneously (no order). Default: deny all inbound.<br>Applied to: EC2, RDS, ELB, Lambda (in VPC), ElastiCache. |

| **Q7** | What does "stateful" mean for Security Groups? |
|:---|:---|
| **A** | Return traffic automatically allowed. If inbound port 443 allowed,<br>response traffic outbound is automatically permitted.<br>Don't need outbound rule for the response. Remembers connections. |

| **Q8** | What is a Network ACL? |
|:---|:---|
| **A** | Firewall at SUBNET level. Stateless. ALLOW + DENY rules.<br>Rules evaluated by number order (lowest first, first match wins).<br>Applies to ALL resources in the subnet automatically. |

| **Q9** | What does "stateless" mean for NACLs? |
|:---|:---|
| **A** | Must explicitly allow BOTH inbound AND outbound traffic.<br>Response traffic NOT automatically allowed. Must add outbound rules<br>for ephemeral ports (1024-65535) to allow responses back out. |

| **Q10** | Can NACLs have Deny rules? |
|:---|:---|
| **A** | YES — unlike Security Groups, NACLs support explicit Deny rules.<br>Use to: block specific IP address from accessing your VPC. |

| **Q11** | Security Groups operate at which level? |
|:---|:---|
| **A** | Instance level — EC2, RDS, Lambda (in VPC), ELB, ElastiCache, etc. |

| **Q12** | NACLs operate at which level? |
|:---|:---|
| **A** | Subnet level — applies to ALL resources within the subnet.<br>One NACL per subnet. One NACL can cover multiple subnets. |

| **Q13** | Company wants to block a specific IP from accessing VPC? |
|:---|:---|
| **A** | Network ACL — add explicit DENY rule for that IP.<br>Security Groups cannot do Deny rules, only NACLs can. |

| **Q14** | What is VPC Peering? |
|:---|:---|
| **A** | Direct networking connection between two VPCs for private communication.<br>Works across accounts and regions. No overlapping IP ranges allowed.<br>NOT transitive: A↔B + B↔C does NOT give A↔C access. |

| **Q15** | Is VPC Peering transitive? |
|:---|:---|
| **A** | NO. Each pair needs a direct peering connection.<br>10 VPCs = 45 peering connections needed = complex mesh. Use TGW instead. |

| **Q16** | What problem does Transit Gateway solve? |
|:---|:---|
| **A** |  |

```
Hub-and-spoke model connecting all VPCs and on-premises networks.
Transitive routing: A → TGW → C without direct A↔C peering.
50 VPCs + DX/VPN = just 51 TGW attachments instead of 1,225 peerings.
```

| **Q17** | Difference between VPN Gateway and Direct Connect? |
|:---|:---|
| **A** |  |

```
VPN: encrypted over PUBLIC internet. Hours to set up. Cheap. Variable performance.
Direct Connect: PRIVATE fiber. Weeks to set up. Expensive. Consistent low latency.
EXAM: "consistent performance" → DX. "quick/cheap" → VPN.
```

| **Q18** | What is Amazon CloudFront? |
|:---|:---|
| **A** | CDN (Content Delivery Network) — caches content at 400+ edge locations.<br>Also: DDoS protection (Shield), HTTPS/TLS termination, geo-restriction.<br>Reduces latency globally. HTTP/HTTPS only. |

| **Q19** | What is Amazon Route 53? |
|:---|:---|
| **A** | Managed DNS service. Also: domain registration, health checks, traffic routing.<br>Name: DNS runs on port 53.<br>DNS = translates domain names (example.com) to IP addresses. |

| **Q20** | Which Route 53 policy splits 10% traffic to new app version? |
|:---|:---|
| **A** | Weighted routing — assign weights (10% new, 90% existing).<br>Use for: A/B testing, blue/green deployments, canary releases. |

| **Q21** | Which Route 53 policy routes to lowest latency region? |
|:---|:---|
| **A** | Latency-based routing — routes to region with lowest measured latency.<br>Based on actual network latency, not geographic distance. |

| **Q22** | Which Route 53 policy routes by user's physical location? |
|:---|:---|
| **A** | Geolocation routing — routes based on user's geographic location.<br>Use for: data compliance, content localization, country restrictions. |

| **Q23** | Difference between CloudFront and Global Accelerator? |
|:---|:---|
| **A** |  |

```
CloudFront: CACHES content at edge. HTTP/HTTPS only. CDN.
Global Accelerator: ROUTES traffic over AWS private network. TCP/UDP.
                    No caching. Provides 2 static anycast IPs.
EXAM: "cache images globally" → CF. "2 static IPs whitelist" → GA.
```

| **Q24** | What is Amazon API Gateway? |
|:---|:---|
| **A** | Create, publish, manage, and secure APIs at any scale.<br>Works with Lambda for serverless APIs. Handles: auth, throttling, caching.<br>JWT = JSON Web Token (secure authentication token). |

| **Q25** | Company in US wants low latency for Asian users? |
|:---|:---|
| **A** | Amazon CloudFront — caches content at edge locations near Asian users.<br>Tokyo, Singapore, Sydney, Mumbai, Seoul, Hong Kong — all have edge locations. |

| **Q26** | What does Route 53 Failover routing do? |
|:---|:---|
| **A** | Routes to primary when healthy. Automatically switches to secondary when<br>primary fails health checks. Active-passive disaster recovery. |

| **Q27** | Which is NOT a valid Route 53 routing policy? A) Simple  B) Weighted  C) Geolocation  D) Alphabetical |
|:---|:---|
| **A** | D. Valid: Simple, Weighted, Latency, Failover, Geolocation,<br>Geoproximity, Multivalue, IP-based. |

| **Q28** | What is an Elastic IP address? |
|:---|:---|
| **A** | Static public IPv4 address. Persists even when EC2 stops.<br>Reassign to new instance instantly. FREE when associated with running EC2.<br>CHARGED ($0.005/hr) when not associated or instance stopped. |

| **Q29** | Two main firewall options and their levels? |
|:---|:---|
| **A** | Security Groups (instance level, stateful, allow only) +<br>Network ACLs (subnet level, stateless, allow AND deny).<br>Two layers of defense in VPC architecture. |

| **Q30** | Developer wants to connect on-premises to AWS securely and quickly? |
|:---|:---|
| **A** | Site-to-Site VPN using VPN Gateway — hours to set up, encrypted.<br>CGW = Customer Gateway (your VPN device).<br>VGW = Virtual Private Gateway (AWS side). |

| **Q31** | Financial company needs consistent low-latency connectivity to AWS? |
|:---|:---|
| **A** | AWS Direct Connect — dedicated private fiber, consistent performance.<br>1 Gbps, 10 Gbps, 100 Gbps options. Through colocation providers (Equinix). |

| **Q32** | What is the default VPC? |
|:---|:---|
| **A** | Auto-created in each region on new account. Pre-configured with<br>IGW, public subnets (one per AZ), main route table (internet access).<br>CIDR: 172.31.0.0/16. Less secure for production — use custom VPCs. |

| **Q33** | Which service provides automatic DDoS protection for CloudFront? |
|:---|:---|
| **A** | AWS Shield Standard — free, automatic, all customers, Layers 3 & 4.<br>Shield Advanced: $3,000+/month, Layer 7, 24/7 DRT team, cost protection.<br>DRT = DDoS Response Team. |

| **Q34** | Restrict S3 bucket to only your VPC? |
|:---|:---|
| **A** | VPC Endpoint (Gateway Endpoint for S3) — private access, no internet.<br>Traffic stays on AWS network. FREE gateway endpoint. |

| **Q35** | What is a VPC Endpoint? |
|:---|:---|
| **A** | Private connection between VPC and AWS services. No internet, NAT, or DX needed.<br>Gateway Endpoint: S3 and DynamoDB only. FREE. Added to route table.<br>Interface Endpoint: 100s of AWS services. Creates ENI with private IP. Charged. |

| **Q36** | Which VPC Endpoint type works like an ENI? |
|:---|:---|
| **A** | Interface Endpoint — creates ENI in your subnet with private IP.<br>ENI = Elastic Network Interface (virtual network card).<br>Traffic to AWS service goes to private IP instead of public endpoint. |

| **Q37** | Which VPC Endpoint type for S3 and DynamoDB? |
|:---|:---|
| **A** | Gateway Endpoint — free, added to route table, S3 and DynamoDB ONLY. |

| **Q38** | How many route tables can a subnet be associated with? |
|:---|:---|
| **A** | ONE at a time. Each subnet has exactly one route table.<br>One route table can cover MANY subnets. |

| **Q39** | What wins in a route table (most specific or least)? |
|:---|:---|
| **A** | Most specific (longest prefix) wins.<br>/32 > /24 > /16 > /0. Example: traffic to 10.0.1.50 → /32 wins over /0. |

| **Q40** | Company needs global app with two static IPs for whitelisting? |
|:---|:---|
| **A** | AWS Global Accelerator — provides 2 static anycast IPs that never change.<br>Anycast = same IP announced from multiple locations. Traffic → nearest. |

| **Q41** | Difference between Route 53 Simple and Multivalue routing? |
|:---|:---|
| **A** | Simple: returns ONE record (no health checks).<br>Multivalue: returns up to 8 HEALTHY records (requires health checks).<br>Multivalue is NOT a full load balancer replacement — use ELB for that. |

| **Q42** | What component connects EC2 to the network? |
|:---|:---|
| **A** | ENI — Elastic Network Interface (virtual NIC).<br>Each instance has at least one ENI with private IP.<br>Can attach multiple ENIs to one EC2 (multiple network interfaces).<br>NIC = Network Interface Card (physical equivalent). |

| **Q43** | What is VPC Flow Logs? |
|:---|:---|
| **A** | Captures IP traffic metadata (source/dest IPs, ports, protocol, allow/reject).<br>Does NOT capture actual packet content.<br>Destinations: CloudWatch Logs, S3 bucket, Kinesis Firehose. |

| **Q44** | Which service filters malicious web traffic? |
|:---|:---|
| **A** | AWS WAF (Web Application Firewall) — protects at Layer 7.<br>Blocks: SQL injection, XSS, rate limiting.<br>Works with: CloudFront, ALB, API Gateway.<br>XSS = Cross-Site Scripting. SQL injection = attacker injects SQL code. |

| **Q45** | Route 53 monitors endpoint health. What feature? |
|:---|:---|
| **A** | Route 53 Health Checks — monitors endpoints and removes unhealthy<br>ones from DNS responses. Checks every 10 or 30 seconds. |

| **Q46** | What does CloudFront's "origin" refer to? |
|:---|:---|
| **A** |  |

```
The source of original content — S3 bucket, EC2, ALB, or any HTTP server.
Multiple origins per distribution with path-based routing.
/images/* → S3, /api/* → ALB, /* → default.
```

| **Q47** | Accelerate file uploads from worldwide users to S3? |
|:---|:---|
| **A** |  |

```
S3 Transfer Acceleration — uses CloudFront edge locations.
Upload to mybucket.s3-accelerate.amazonaws.com.
Users in Brazil upload → nearest edge → AWS backbone → S3 in US.
```

| **Q48** | Manage routing between 50 VPCs across multiple accounts? |
|:---|:---|
| **A** | AWS Transit Gateway — hub-and-spoke, 50 attachments vs 1,225 peerings.<br>Control which VPCs talk to each other via TGW route tables. |

| **Q49** | Key difference between Security Group rules and NACL evaluation? |
|:---|:---|
| **A** | Security Groups: ALL rules evaluated simultaneously, then decision made.<br>NACLs: rules evaluated in NUMBER ORDER, first match STOPS evaluation. |

| **Q50** | Technical difference between CloudFront and Global Accelerator? |
|:---|:---|
| **A** | CloudFront: CACHES content at edge. HTTP/HTTPS. CDN.<br>          Best for static content, website performance.<br>Global Accelerator: ROUTES traffic over AWS private network. ANY TCP/UDP.<br>                   No caching. Best for gaming, IoT, non-HTTP, static IPs. |

DAY 6 COMPLETE
*Tomorrow: Day 7 — Security Services*

## Day 7 — SECURITY SERVICES

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 7)

| Acronym | Definition |
|---|---|
| `KMS` | Key Management Service (encryption key management) |
| `CMK` | Customer Master Key (encryption key in KMS) |
| `HSM` | Hardware Security Module (dedicated crypto hardware) |
| `PII` | Personally Identifiable Information (name, SSN, DOB, etc.) |
| `PHI` | Protected Health Information (medical records) |
| `ACM` | AWS Certificate Manager (free SSL/TLS certs) |
| `CSR` | Certificate Signing Request |
| `CA` | Certificate Authority (issues digital certificates) |
| `SOC` | Service Organization Control (audit reports) |
| `PCI DSS` | Payment Card Industry Data Security Standard |
| `HIPAA` | Health Insurance Portability and Accountability Act |
| `GDPR` | General Data Protection Regulation (EU) |
| `BAA` | Business Associate Agreement (HIPAA contract) |
| `NDA` | Non-Disclosure Agreement |
| `CVE` | Common Vulnerabilities and Exposures (database of known vulns) |
| `RCE` | Remote Code Execution (critical vulnerability type) |
| `SSRF` | Server-Side Request Forgery (web attack type) |

STUDY NOTES — HOURS 1 & 2: SECURITY SERVICES
KNOW THESE DISTINCTIONS (most tested):
CloudTrail:    WHO did WHAT API call (audit log)
CloudWatch:    HOW is infrastructure PERFORMING (metrics/alarms)
Config:        WHAT did resources look like over TIME (compliance)
GuardDuty:     THREATS detected via ML (anomaly detection)
Inspector:     VULNERABILITIES in EC2/containers (CVE scanning)
Macie:         SENSITIVE DATA discovered in S3 (PII/credentials)
Security Hub:  CENTRAL DASHBOARD aggregating all findings

KEY FACTS:
KMS: manage encryption keys. $1/month per CMK. Auto-rotate annually.
CloudTrail: enabled by default (90 days in console). Create trail for S3 long-term.
GuardDuty: no agents needed. Analyzes CloudTrail, VPC Flow Logs, DNS logs.
Inspector: vulnerability scanning for EC2 instances and container images.
Macie: S3 sensitive data discovery. Finds SSNs, credit cards, AWS keys.
Secrets Manager: auto-rotate secrets. $0.40/secret/month. RDS native rotation.
Parameter Store: free tier for config values and secrets. No auto-rotation.
Shield Standard: FREE, automatic, all customers, Layers 3/4 DDoS protection.
Shield Advanced: $3,000+/month, 24/7 DRT, Layer 7, cost protection.
WAF: Layer 7 firewall, SQL injection/XSS protection, rate limiting.
ACM: FREE SSL/TLS certs for AWS services (CloudFront, ALB, API GW). Auto-renews.
Cognito: user auth for apps. User Pools = authentication. Identity Pools = AWS creds.
Artifact: download compliance reports (SOC, PCI DSS, ISO) — FREE.
Trusted Advisor: recommendations across 5 categories (Cost, Perf, Security, FT, Limits).
STS: Security Token Service — issues temporary credentials for roles.

### Questions & Answers — Day 7

| **Q1** | What does AWS KMS do? |
|:---|:---|
| **A** | Creates and manages encryption keys (CMKs) used to encrypt data.<br>Keys stored securely in HSM hardware. Access controlled by IAM.<br>Every use logged in CloudTrail. Auto-rotation annually.<br>HSM = Hardware Security Module (physical hardware for crypto keys). |

| **Q2** | What does CloudTrail record? |
|:---|:---|
| **A** | Every API call in your AWS account — every action (console click,<br>CLI command, SDK call). Records: WHO, WHAT, WHEN, WHERE (IP address). |

| **Q3** | Is CloudTrail enabled by default? |
|:---|:---|
| **A** | YES — 90-day event history free in console.<br>For long-term: create Trail to deliver logs to S3 bucket.<br>Management events: control plane (creating/deleting resources).<br>Data events: S3 reads/writes (extra cost). |

| **Q4** | Difference between CloudTrail and CloudWatch? |
|:---|:---|
| **A** | CloudTrail: "WHO did WHAT?" — API audit log.<br>CloudWatch: "HOW is it performing?" — metrics (CPU, latency, errors).<br>EXAM: "audit log" = CloudTrail. "CPU alarm" = CloudWatch. |

| **Q5** | Difference between CloudTrail and AWS Config? |
|:---|:---|
| **A** | CloudTrail: WHO made API calls (activity).<br>Config: WHAT resources looked like before/after (configuration history + compliance).<br>Use both: Config = WHAT changed. CloudTrail = WHO changed it. |

| **Q6** | Who changed a security group last Tuesday? |
|:---|:---|
| **A** | AWS CloudTrail — records all API calls including SG modifications.<br>Filter by: EventName=AuthorizeSecurityGroupIngress, date range. |

| **Q7** | Verify EC2 instances always used encrypted EBS volumes? |
|:---|:---|
| **A** | AWS Config — tracks configuration history and runs compliance rules.<br>Rule: ec2-ebs-encryption-by-default. |

| **Q8** | What does Amazon GuardDuty do? |
|:---|:---|
| **A** | Intelligent threat detection using ML, anomaly detection, and threat intel.<br>Detects: compromised credentials, cryptomining, port scanning, data exfiltration.<br>Analyzes: CloudTrail, VPC Flow Logs, DNS logs. No agents needed. |

| **Q9** | Does GuardDuty require agents on EC2? |
|:---|:---|
| **A** |  |

```
NO. Fully managed. Reads logs that already exist.
Enable → click "Enable" → monitoring starts. No software to install.
```

| **Q10** | What does Amazon Inspector do? |
|:---|:---|
| **A** | Automated vulnerability assessment for EC2 and container images.<br>Finds: unpatched CVEs, network exposure (open ports), software vulns.<br>CVE = Common Vulnerabilities and Exposures (public database of security flaws).<br>RCE = Remote Code Execution (attacker runs code on your server). |

| **Q11** | What does Amazon Macie do? |
|:---|:---|
| **A** | ML to discover and protect sensitive data (PII, credentials) in S3.<br>Finds: SSNs, credit card numbers, AWS access keys, medical records.<br>PII = Personally Identifiable Information. |

| **Q12** | What is AWS Security Hub? |
|:---|:---|
| **A** | Central security dashboard aggregating findings from multiple services.<br>Combines: GuardDuty, Inspector, Macie, Config, IAM Analyzer, third-party.<br>CSPM compliance checks. Multi-account support.<br>CSPM = Cloud Security Posture Management. |

| **Q13** | Difference between Shield Standard and Advanced? |
|:---|:---|
| **A** | Standard: FREE, automatic, ALL customers, Layers 3 and 4.<br>Advanced: $3,000+/month, Layer 7 app DDoS, 24/7 DRT team, cost protection.<br>SYN flood = DDoS attack type (send many SYN packets without completing handshake). |

| **Q14** | What does AWS WAF protect against? |
|:---|:---|
| **A** | SQL injection, XSS, rate limiting, bot attacks at Layer 7.<br>Works with: CloudFront, ALB, API Gateway.<br>AWS Managed Rules: pre-built for common threats. Custom rules: you write. |

| **Q15** | Which services can AWS WAF protect? |
|:---|:---|
| **A** | CloudFront (edge), Application Load Balancer (regional), API Gateway. |

| **Q16** | What is AWS Secrets Manager? |
|:---|:---|
| **A** | Store, rotate, and manage secrets (DB passwords, API keys, tokens).<br>AUTO-ROTATION built in for RDS, Redshift, DocumentDB.<br>$0.40/secret/month. No credentials hardcoded in code. |

| **Q17** | Benefit of Secrets Manager over storing credentials in code? |
|:---|:---|
| **A** | Never hardcoded. Auto-rotation without code changes.<br>Full audit trail. Access via IAM. Encrypted at rest (KMS). |

| **Q18** | Difference between Secrets Manager and Parameter Store? |
|:---|:---|
| **A** | Secrets Manager: built for secrets, auto-rotation, $0.40/secret/month.<br>Parameter Store: config + secrets, FREE standard tier, no auto-rotation.<br>Use SM: DB passwords with rotation needed.<br>Use PS: app config values, feature flags, connection strings. |

| **Q19** | What does ACM provide? |
|:---|:---|
| **A** | Free SSL/TLS certificates for AWS services with automatic renewal.<br>Never pay for cert, never worry about expiry.<br>Works with: CloudFront, ALB, API Gateway.<br>SSL/TLS = protocol for encrypting data in transit (HTTPS). |

| **Q20** | What is Amazon Cognito? |
|:---|:---|
| **A** | User authentication for web/mobile apps.<br>User Pools: authentication (sign-up, sign-in, MFA, social login).<br>           Returns JWT tokens (not AWS credentials).<br>Identity Pools: authorization (exchange JWT for temporary AWS credentials).<br>OAuth = Open Authorization standard for social login. |

| **Q21** | What is AWS Artifact? |
|:---|:---|
| **A** | Portal providing access to AWS compliance reports and certifications.<br>Download: SOC 1/2/3, PCI DSS, ISO 27001, FedRAMP, HIPAA BAA.<br>FREE. No waiting. Download in minutes for auditors. |

| **Q22** | Company needs compliance reports proving AWS is PCI compliant? |
|:---|:---|
| **A** | AWS Artifact — download PCI DSS Attestation of Compliance directly.<br>PCI DSS = Payment Card Industry Data Security Standard. |

| **Q23** | What does Trusted Advisor check? |
|:---|:---|
| **A** | Five categories:<br>1. Cost Optimization (oversized instances)<br>2. Performance (IOPS limits)<br>3. Security (public S3 buckets, open ports)<br>4. Fault Tolerance (no Multi-AZ on RDS)<br>5. Service Limits/Quotas (approaching limits) |

| **Q24** | Which Trusted Advisor checks are free? |
|:---|:---|
| **A** | 7 core checks including S3 bucket permissions, SG open ports,<br>root MFA, IAM use, service limits.<br>Full checks require Business or Enterprise support plan. |

| **Q25** | Which support plan gives access to ALL Trusted Advisor checks? |
|:---|:---|
| **A** | Business ($100+/month), Enterprise On-Ramp ($5,500+), or Enterprise ($15,000+). |

| **Q26** | Startup left S3 bucket publicly accessible. Which alerts them? |
|:---|:---|
| **A** | Trusted Advisor (security check) and AWS Config (rule).<br>Also: S3 Block Public Access (account-level prevention setting). |

| **Q27** | How does GuardDuty detect threats? |
|:---|:---|
| **A** | ML behavior baseline + anomaly detection + threat intelligence feeds.<br>Learns: "admin always logs in from New York at 9 AM"<br>Detects: "admin login from Russia at 3 AM" → HIGH severity alert. |

| **Q28** | Which service monitors CPU and alerts when it exceeds 80%? |
|:---|:---|
| **A** | Amazon CloudWatch — create metric alarm on CPUUtilization.<br>Alarm states: OK, ALARM, INSUFFICIENT_DATA.<br>Memory metrics require CloudWatch Agent (not available by default). |

| **Q29** | What is a CloudWatch Alarm? |
|:---|:---|
| **A** | Notification triggered when metric crosses a threshold.<br>Actions: SNS notification, Auto Scaling, EC2 action.<br>SNS = Simple Notification Service (sends to email, SMS, etc.). |

| **Q30** | What is Amazon EventBridge? |
|:---|:---|
| **A** |  |

```
Serverless event bus connecting AWS services with automation.
Event (EC2 stopped, S3 upload) → Rule → Target (Lambda, SNS, SSM).
```

| **Q31** | Ensure all S3 buckets are encrypted. Which service? |
|:---|:---|
| **A** | AWS Config with rule: s3-bucket-server-side-encryption-enabled.<br>Auto-remediation: detects non-compliant → automatically enables encryption. |

| **Q32** | Single view of security across all AWS accounts? |
|:---|:---|
| **A** | AWS Security Hub — aggregate all security findings into one dashboard.<br>Security account as admin → all member accounts feed findings in. |

| **Q33** | What logs does GuardDuty analyze? |
|:---|:---|
| **A** | CloudTrail event logs + VPC Flow Logs + Route 53 DNS query logs.<br>No additional setup needed — these logs already exist. |

| **Q34** | Difference between CloudWatch and CloudTrail for EC2? |
|:---|:---|
| **A** | CloudWatch: CPU, memory, network, disk performance (HOW running).<br>CloudTrail: who started/stopped/modified instances (ACTIONS taken). |

| **Q35** | What is AWS Systems Manager? |
|:---|:---|
| **A** | Manage EC2 infrastructure at scale.<br>Session Manager: browser-based shell, no SSH keys or open port 22.<br>Run Command: execute scripts on 1000s of instances at once.<br>Patch Manager: automate OS patching with maintenance windows. |

| **Q36** | Which CloudWatch metric requires agent (NOT available by default)? |
|:---|:---|
| **A** | Memory utilization — AWS cannot see inside guest OS without agent.<br>Default metrics: CPU, Network, Disk I/O.<br>Memory/disk utilization: require CloudWatch Agent installed on EC2. |

| **Q37** | Purpose of KMS key rotation? |
|:---|:---|
| **A** | Auto-rotates key material annually. Key ID stays same.<br>Old data still decryptable (KMS keeps old versions).<br>Limits exposure window if key is ever compromised. |

| **Q38** | Company wants to auto-rotate RDS passwords every 30 days? |
|:---|:---|
| **A** | AWS Secrets Manager — built-in RDS rotation, configurable schedule.<br>Updates password in RDS and in Secrets Manager. App unchanged. |

| **Q39** | Difference between AWS managed keys and customer managed keys? |
|:---|:---|
| **A** | AWS managed: auto-created by service, FREE, cannot customize, no audit.<br>Customer managed: you create, $1/month, customize policy, full CloudTrail audit. |

| **Q40** | Which service detects IAM credentials used from unusual location? |
|:---|:---|
| **A** | Amazon GuardDuty — ML detects anomalous credential usage.<br>Login from Russia when user always logs in from New York → HIGH severity. |

| **Q41** | What does Macie specifically look for in S3? |
|:---|:---|
| **A** | PII (SSN, passport, driver's license), financial data (credit cards, bank accounts),<br>credentials (AWS access keys, private keys, HTTP auth), medical records (PHI). |

| **Q42** | Compliance frameworks accessible via AWS Artifact? |
|:---|:---|
| **A** | SOC 1/2/3, PCI DSS, ISO 27001/27017/27018/9001, FedRAMP, GDPR, ITAR, HIPAA BAA. |

| **Q43** | Developer hardcoded RDS password in code. Recommended fix? |
|:---|:---|
| **A** | 1. Rotate password immediately (it may be compromised via Git).<br>2. Store in Secrets Manager.<br>3. Update app to call Secrets Manager API at runtime.<br>4. Enable auto-rotation every 90 days. |

| **Q44** | What is an AWS Config Rule? |
|:---|:---|
| **A** | Evaluates whether resources comply with your configuration policies.<br>AWS managed: 300+ pre-built rules.<br>Custom: Lambda function with your compliance logic. |

| **Q45** | Full history of changes to EC2 security group over past year? |
|:---|:---|
| **A** | AWS Config — configuration timeline showing before/after for every change.<br>CloudTrail tells WHO changed it. Config tells WHAT changed. |

| **Q46** | What is Amazon Detective? |
|:---|:---|
| **A** | Security investigation tool. Visualizes findings from GuardDuty.<br>Shows: IP relationships, API call patterns, connections between events.<br>Reduces investigation from hours to minutes. |

| **Q47** | Difference between Cognito User Pool and Identity Pool? |
|:---|:---|
| **A** | User Pool: authentication (who are you?) → returns JWT tokens.<br>Identity Pool: authorization (here are your AWS permissions) → temp AWS creds. |

| **Q48** | What is VPC Flow Logs? |
|:---|:---|
| **A** | Captures network traffic metadata. Does NOT capture packet content.<br>Records: source IP, dest IP, ports, protocol, bytes, ACCEPT/REJECT.<br>Send to: CloudWatch Logs, S3, Kinesis Firehose. |

| **Q49** | What is the AWS Security Token Service (STS)? |
|:---|:---|
| **A** | Issues temporary, limited-privilege credentials for IAM roles.<br>Temp credentials: Access Key ID + Secret Key + Session Token + Expiration.<br>Used by: EC2 instance roles, cross-account access, federation. |

| **Q50** | Company considering AWS migration needs compliance certs. Where? |
|:---|:---|
| **A** |  |

```
AWS Artifact — immediate access to all AWS compliance documentation.
Log in → download → give to auditor. 5 minutes total. FREE.
```

DAY 7 COMPLETE
*Tomorrow: Day 8 — Monitoring, Management & Pricing*

## Day 8 — MONITORING, MANAGEMENT & PRICING

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 8)

| Acronym | Definition |
|---|---|
| `IaC` | Infrastructure as Code |
| `CDK` | Cloud Development Kit (define infra in Python/Java/TypeScript) |
| `TCO` | Total Cost of Ownership |
| `TAM` | Technical Account Manager |
| `CUR` | Cost and Usage Report (most detailed billing data) |
| `OU` | Organizational Unit |
| `SCP` | Service Control Policy |
| `CapEx` | Capital Expenditure (upfront purchase) |
| `OpEx` | Operational Expenditure (ongoing costs) |
| `SSM` | Systems Manager |
| `WAF` | Well-Architected Framework |

STUDY NOTES — HOURS 1 & 2: MANAGEMENT & PRICING
MANAGEMENT SERVICES:
CloudFormation: IaC — JSON/YAML templates. Create/update/delete resource stacks.
CDK: Define infra in Python/Java/TypeScript that generates CloudFormation.
Systems Manager: Session Manager (no SSH), Run Command (mass scripts), Patch Manager.
Organizations: Multi-account management, consolidated billing, SCPs.
Control Tower: Landing zone = pre-configured secure multi-account environment.
Service Catalog: Approved self-service IT catalog for teams.

PRICING FUNDAMENTALS:
Pay as you go — no upfront, pay only what you use.
Save when you reserve — 1-3 year commit = up to 72% off.
Pay less as you use more — volume discounts (S3 tiers).
Data IN to AWS: ALWAYS FREE
Data OUT from AWS: CHARGED (~$0.09/GB to internet)

COST TOOLS:
Cost Explorer: visualize and analyze spending. RI recommendations. FREE.
AWS Budgets: set alerts when approaching limits. Actions to restrict usage.
CUR: most granular (hourly line items). Delivered to S3. Query with Athena.
Pricing Calculator: estimate costs BEFORE deploying. calculator.aws. FREE.
Compute Optimizer: right-sizing recommendations for EC2, EBS, Lambda.

SUPPORT PLANS:
Basic:             FREE — 7 Trusted Advisor checks, no engineer contact
Developer:         $29/month — email, business hours, 12-hr response (impaired)
Business:          $100+/month — 24/7 phone+chat+email, 1-hr (prod down), ALL TA checks
Enterprise On-Ramp:$5,500+/month — TAM pool, 30-min (critical)
Enterprise:        $15,000+/month — DEDICATED TAM, 15-min (critical)

WELL-ARCHITECTED 6 PILLARS (memory trick "OSRPCS"):
Operational Excellence, Security, Reliability, Performance Efficiency,
Cost Optimization, Sustainability

### Questions & Answers — Day 8

| **Q1** | What is AWS CloudFormation? |
|:---|:---|
| **A** | Infrastructure as Code — define AWS resources in JSON or YAML templates.<br>Deploy as a "stack" — create, update, delete all resources together.<br>Same template + deploy 10 times = same result every time.<br>IaC = Infrastructure as Code (treat infra like software — versioned, repeatable). |

| **Q2** | What is a CloudFormation Stack? |
|:---|:---|
| **A** |  |

```
Collection of AWS resources created, updated, deleted as a unit.
Template → Stack. Delete stack → all resources deleted automatically.
Prevents orphaned resources (forgotten EC2s, security groups, etc.).
```

| **Q3** | Benefit of CloudFormation over manually creating resources? |
|:---|:---|
| **A** | Repeatability, consistency, version control, disaster recovery (redeploy template).<br>Config drift = gradual deviation from intended configuration over time.<br>CloudFormation Drift Detection finds resources changed outside CloudFormation. |

| **Q4** | Three fundamental AWS pricing principles? |
|:---|:---|
| **A** | 1. Pay as you go (no upfront, variable costs).<br>2. Save when you reserve (1-3 year commits = 72% off).<br>3. Pay less as you use more (volume discounts). |

| **Q5** | Is data transfer INTO AWS charged? |
|:---|:---|
| **A** | NO — data transfer IN to AWS is ALWAYS FREE.<br>Upload to S3, send to EC2, any inbound = FREE. |

| **Q6** | Is data transfer OUT of AWS charged? |
|:---|:---|
| **A** |  |

```
YES — outbound to internet ~$0.09/GB.
S3 → CloudFront: FREE. CloudFront → users: cheaper than S3 direct.
Cross-region: ~$0.02/GB. Same region/AZ via private IP: FREE.
```

| **Q7** | What is the AWS Free Tier? |
|:---|:---|
| **A** | Always Free (permanent): Lambda 1M req/month, DynamoDB 25GB, etc.<br>12-month Free: EC2 t2.micro 750 hrs, S3 5GB, RDS 750 hrs.<br>Short Trials: Redshift 2 months, Lightsail 3 months. |

| **Q8** | How many Lambda requests in always-free tier? |
|:---|:---|
| **A** | 1 million requests/month FOREVER + 400,000 GB-seconds compute/month.<br>Most small apps run on Lambda completely free permanently. |

| **Q9** | What is AWS Cost Explorer? |
|:---|:---|
| **A** | Visualize and analyze historical spending. RI recommendations. Forecasting.<br>View by service, tag, region, account. FREE to use.<br>Direction: looking BACKWARD (and forecasting forward). |

| **Q10** | What is AWS Budgets? |
|:---|:---|
| **A** | Set spending/usage thresholds and receive alerts.<br>Budget Actions: automatically apply IAM or SCP policies when exceeded.<br>Direction: looking FORWARD (prevent overspend proactively). |

| **Q11** | Which tool provides most granular billing data? |
|:---|:---|
| **A** | AWS Cost and Usage Report (CUR) — hourly line-item detail.<br>Delivered to S3. Query with Athena. Used for chargebacks/showbacks.<br>Blended vs unblended cost. RI discounts applied per line item. |

| **Q12** | Which tool estimates costs BEFORE deploying? |
|:---|:---|
| **A** |  |

```
AWS Pricing Calculator at calculator.aws. No AWS account needed. FREE.
Build estimate: add services → see monthly cost → share URL.
```

| **Q13** | Which support plan has a dedicated TAM? |
|:---|:---|
| **A** | Enterprise Support ($15,000+/month) — dedicated TAM assigned to your account.<br>Enterprise On-Ramp: pool of shared TAMs (not dedicated). |

| **Q14** | Which plan for 24/7 phone+chat with 1-hour prod-down response? |
|:---|:---|
| **A** | Business Support ($100+/month).<br>Response times: General guidance 24hr, System impaired 12hr,<br>Prod impaired 4hr, Prod DOWN 1 HOUR. |

| **Q15** | Startup needs AWS support but only $29/month budget? |
|:---|:---|
| **A** | Developer Support — email support during business hours.<br>NOT for production workloads (12-hour business-hours response only). |

| **Q16** | What is AWS Organizations? |
|:---|:---|
| **A** | Central management of multiple AWS accounts.<br>Consolidated billing (one invoice, volume discounts, RI sharing).<br>Service Control Policies (SCPs) for account-level guardrails. |

| **Q17** | What is a Service Control Policy (SCP)? |
|:---|:---|
| **A** | Policy at organizational level setting MAXIMUM permission limits.<br>SCPs can only RESTRICT, never GRANT permissions.<br>Example: DENY all services except in us-east-1 and us-west-2. |

| **Q18** | Can an SCP grant permissions to a user? |
|:---|:---|
| **A** | NO. SCPs only restrict. Actual permissions still need IAM policies.<br>Effective permissions = SCP (ceiling) AND IAM policies (grant).<br>Must satisfy BOTH to get access. |

| **Q19** | Benefit of consolidated billing in Organizations? |
|:---|:---|
| **A** | One bill for all accounts. Volume discounts combined across accounts.<br>RI sharing: unused RI in Account A auto-applies to Account B.<br>Save money by pooling usage for better discount tiers. |

| **Q20** | What is AWS Control Tower? |
|:---|:---|
| **A** | Sets up and governs a secure multi-account environment.<br>Landing Zone = pre-configured accounts (Management, Log Archive, Security).<br>Guardrails = SCPs + Config rules (Mandatory, Recommended, Elective). |

| **Q21** | Difference between CloudFormation and CDK? |
|:---|:---|
| **A** | CloudFormation: templates in JSON or YAML (declarative).<br>CDK: define infra in Python/Java/TypeScript → generates CloudFormation.<br>CDK benefits: loops, functions, type checking, IDE autocomplete. |

| **Q22** | What is Systems Manager Session Manager? |
|:---|:---|
| **A** | Browser-based shell access to EC2 with NO SSH keys, NO port 22, NO bastion.<br>All sessions logged in CloudTrail. Works for private instances via SSM agent. |

| **Q23** | What is Systems Manager Run Command? |
|:---|:---|
| **A** |  |

```
Execute scripts/commands on many EC2 instances simultaneously.
"Patch 500 web servers NOW" → one Run Command → done in minutes.
Results per server. Rate control (e.g., 50 servers at a time).
```

| **Q24** | What is Systems Manager Patch Manager? |
|:---|:---|
| **A** | Automate OS patching. Define patch baseline. Schedule maintenance windows.<br>Auto-patches during window. Reports compliance status per instance. |

| **Q25** | What is AWS Service Catalog? |
|:---|:---|
| **A** | Create approved IT service catalog. Teams self-serve compliant resources.<br>Admin creates product (approved EC2 with correct tags/encryption).<br>Developer selects from catalog → compliance automatic. |

| **Q26** | Which tool for understanding and forecasting your AWS bill? |
|:---|:---|
| **A** | AWS Cost Explorer — charts of historical spending + cost forecast. |

| **Q27** | Company wants alert when monthly AWS bill exceeds $1,000? |
|:---|:---|
| **A** | AWS Budgets — set $1,000 cost budget with alert at 80% and 100%. |

| **Q28** | Difference between AWS Budgets and Cost Explorer? |
|:---|:---|
| **A** | Budgets: proactive alerts and actions (FORWARD looking, prevent overspend).<br>Cost Explorer: analytical charts and history (BACKWARD looking, understand spend). |

| **Q29** | Which EC2 type in 12-month free tier? |
|:---|:---|
| **A** | t2.micro (or t3.micro). 750 hours/month.<br>730 hours in a month — 1 instance running 24/7 = within free tier.<br>2 instances running = 1,460 hours, charged for extra 710. |

| **Q30** | What happens to free tier limits after 12 months? |
|:---|:---|
| **A** | 12-month offers expire — standard rates apply.<br>Always-free (Lambda, DynamoDB) continue forever.<br>Best practice: set $1 Budget alert — fires when free tier expires. |

| **Q31** | Which plan for 15-minute critical response? |
|:---|:---|
| **A** | Enterprise Support ($15,000+/month) — 15-minute response for business-critical down.<br>Enterprise On-Ramp: 30 minutes. Business: 1 hour. |

| **Q32** | What is a CloudFormation ChangeSet? |
|:---|:---|
| **A** |  |

```
Preview of changes BEFORE executing update. Shows: + Add, ~ Modify, - Delete.
Prevents accidental deletions (like production database).
Review ChangeSet → fix issues → execute safely.
```

| **Q33** | What is CloudFormation Drift Detection? |
|:---|:---|
| **A** | Detects when actual configuration differs from CloudFormation expected state.<br>"Who manually changed that security group in the console?"<br>Drift = difference between actual state and IaC template. |

| **Q34** | Maximum response time for Business Support production system down? |
|:---|:---|
| **A** | 1 HOUR for production system completely inaccessible.<br>Response time = when engineer contacts you (not fix time). |

| **Q35** | Developer plan customer has critical production outage response time? |
|:---|:---|
| **A** | Developer plan only supports email during business hours.<br>Saturday afternoon outage → response may come Monday. Very bad for production.<br>Developer plan = development only (not for production). |

| **Q36** | What is AWS Compute Optimizer? |
|:---|:---|
| **A** | Analyzes CloudWatch metrics → recommends right-sized resources.<br>"This m5.4xlarge runs at 2% CPU — downsize to m5.xlarge, save $280/month."<br>Analyzes: EC2 instances, EBS volumes, Lambda functions. |

| **Q37** | Which provides recommendations across Cost, Performance, Security, FT, Limits? |
|:---|:---|
| **A** | AWS Trusted Advisor. |

| **Q38** | Difference between Trusted Advisor and Cost Explorer? |
|:---|:---|
| **A** | Trusted Advisor: "Here is what you should DO" (actionable recommendations).<br>Cost Explorer: "Here is how you SPENT money" (analytical visibility). |

| **Q39** | Which CloudFormation resource type for nested stack? |
|:---|:---|
| **A** | AWS::CloudFormation::Stack — modular template composition.<br>Benefits: reuse templates, teams own their templates, easier to manage large stacks. |

| **Q40** | What is the AWS Well-Architected Framework? |
|:---|:---|
| **A** | Best practices across 6 pillars.<br>Memory: "Only Stupid Rabbits Play Cost-free Sustainability"<br>Operational Excellence, Security, Reliability, Performance, Cost, Sustainability. |

| **Q41** | 6th pillar of Well-Architected Framework added in 2021? |
|:---|:---|
| **A** | Sustainability — minimize environmental impact.<br>Right-size resources, use managed services, maximize utilization.<br>AWS: 100% renewable energy (achieved 2023), water positive 2030, net zero 2040. |

| **Q42** | Give partner access without creating IAM users? |
|:---|:---|
| **A** |  |

```
IAM Roles with cross-account trust policy.
Partner assumes role → gets temporary credentials → accesses specific resources.
Role can be revoked instantly. No permanent credentials shared.
```

| **Q43** | Custom reports on spending by department, project, and time? |
|:---|:---|
| **A** | AWS Cost and Usage Report (CUR) + Amazon Athena.<br>CUR delivers to S3 → Athena SQL queries for custom analysis. |

| **Q44** | What are AWS Cost Allocation Tags? |
|:---|:---|
| **A** | Key-value pairs on resources that appear in billing reports.<br>Example: Project=WebApp, Environment=Prod, Team=Backend, Owner=alice.<br>Must activate tags in billing console for them to appear in reports. |

| **Q45** | What is the AWS TCO Calculator? |
|:---|:---|
| **A** | Compare total cost of on-premises vs AWS cloud.<br>On-premises hidden costs: power, cooling, space, staff, hardware refresh.<br>TCO = Total Cost of Ownership (ALL costs over time). |

| **Q46** | How do Reserved Instances work with consolidated billing? |
|:---|:---|
| **A** | RI discounts shared across all accounts in Organizations.<br>Unused RI in Account A auto-applies to Account B's matching instance.<br>Can disable RI sharing per account if needed. |

| **Q47** | What is Amazon Managed Grafana? |
|:---|:---|
| **A** | Managed Grafana for visualizing CloudWatch, Prometheus, X-Ray data.<br>Build operational dashboards. AWS manages server, you manage dashboards.<br>Prometheus = open-source monitoring time-series database. |

| **Q48** | Which monitors costs and can automatically restrict usage when exceeded? |
|:---|:---|
| **A** | AWS Budgets Actions — applies IAM policies or SCPs when budget exceeded.<br>Example: deny ec2:RunInstances for dev group when budget hit 90%. |

| **Q49** | AWS Free Tier for S3? |
|:---|:---|
| **A** | 5GB Standard storage + 20,000 GET requests + 2,000 PUT requests per month.<br>Valid for 12 months from account creation. |

| **Q50** | Minimum plan for 24/7 phone and chat support? |
|:---|:---|
| **A** | Business Support ($100+/month). EXAM ANSWER: always "Business Support."<br>Developer = email business hours only. Basic = no engineer contact. |

DAY 8 COMPLETE
*Tomorrow: Day 9 — Cloud Migration & Architecture*

## Day 9 — CLOUD MIGRATION & ARCHITECTURE

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 9)

| Acronym | Definition |
|---|---|
| `CAF` | Cloud Adoption Framework (6 perspectives for cloud adoption) |
| `MGN` | Application Migration Service (lift-and-shift tool) |
| `FIFO` | First In First Out (queue ordering guarantee) |
| `DLQ` | Dead Letter Queue (for failed message processing) |
| `MQTT` | Message Queuing Telemetry Transport (IoT protocol) |
| `CCoE` | Cloud Center of Excellence |
| `PIR` | Post-Incident Review (also called post-mortem) |
| `ROI` | Return on Investment |
| `ITIL` | IT Infrastructure Library (IT service mgmt framework) |
| `KPI` | Key Performance Indicator |
| `ITSM` | IT Service Management |

STUDY NOTES — HOURS 1 & 2: MIGRATION & MESSAGING
6 R'S OF MIGRATION:
Rehost:     Lift and shift — move to EC2 as-is. Fastest. Use MGN.
Replatform: Minor optimization — MySQL on EC2 → MySQL on RDS. App code unchanged.
Repurchase: Switch to SaaS — on-prem CRM → Salesforce. Vendor manages everything.
Refactor:   Re-architect as cloud-native microservices/serverless. Most work, best ROI.
Retire:     Shut off apps no longer needed (10-20% of portfolio typically).
Retain:     Keep on-premises — not ready, compliance, too complex.

CAF 6 PERSPECTIVES: (memory: "Business People Go Play Soccer Online")
Business:   WHY move to cloud? Business case, KPIs, ROI.
People:     WHO needs training? HR, change management, skills development.
Governance: HOW to manage risk? Portfolio management, compliance.
Platform:   WHAT to build? Architecture, infrastructure, DevOps.
Security:   HOW to stay secure? Identity, detection, incident response.
Operations: HOW to run it? Monitoring, incident management, ITIL.

WELL-ARCHITECTED 6 PILLARS:
Operational Excellence: run, monitor, improve operations
Security: protect data, systems, assets
Reliability: recover from failures, scale dynamically
Performance Efficiency: use resources efficiently
Cost Optimization: avoid unnecessary costs
Sustainability: minimize environmental impact

MESSAGING SERVICES:
SNS: pub/sub. One message → many subscribers simultaneously. Push model.
SQS: queue. Messages stored until consumer pulls them. Buffer/decouple.
Kinesis: real-time streaming. High volume. Multiple consumers.
Step Functions: orchestrate workflows with visual state machines.

### Questions & Answers — Day 9

| **Q1** | What are the 6 R's of migration? |
|:---|:---|
| **A** | Rehost, Replatform, Repurchase, Refactor, Retire, Retain.<br>Memory: "Real People Really Refuse Refactoring Regularly" |

| **Q2** | Which migration strategy is "lift and shift"? |
|:---|:---|
| **A** | Rehost — move to EC2 exactly as-is. No code or architecture changes.<br>Tool: AWS Application Migration Service (MGN). Continuous replication.<br>Fastest to execute. Lowest effort. Least cloud benefit long-term. |

| **Q3** | Moving MySQL from EC2 to RDS with minimal changes. Which R? |
|:---|:---|
| **A** |  |

```
Replatform — move to managed service with minor optimization.
App code: unchanged. Operations: better (AWS manages patching/backups).
Other examples: Tomcat on EC2 → Elastic Beanstalk, Redis on EC2 → ElastiCache.
```

| **Q4** | Which R requires most effort but provides most cloud benefit? |
|:---|:---|
| **A** | Refactor (re-architect) — rebuild as cloud-native.<br>Monolith → microservices, Lambda, containers, event-driven.<br>Highest effort, highest ROI long-term. 50-70% cost savings possible. |

| **Q5** | Which R means shutting off applications no longer needed? |
|:---|:---|
| **A** | Retire — discover unused/redundant apps and decommission them.<br>Typical: 10-20% of enterprise applications can be retired at migration time.<br>Reduces: migration scope, ongoing costs, security attack surface. |

| **Q6** | Which R means keeping apps on-premises for now? |
|:---|:---|
| **A** | Retain — not ready, recently purchased hardware, compliance requirement,<br>mainframe with no cloud equivalent, too complex to migrate now.<br>Revisit retained apps periodically as cloud options evolve. |

| **Q7** | What are the 6 perspectives of the AWS CAF? |
|:---|:---|
| **A** | Business, People, Governance, Platform, Security, Operations.<br>Memory trick: "Business People Go Play Soccer Online" |

| **Q8** | Which CAF perspective focuses on HR and change management? |
|:---|:---|
| **A** | People perspective — culture change, skills development (certs!),<br>organizational change management, leadership alignment. |

| **Q9** | What is AWS Migration Hub? |
|:---|:---|
| **A** | Central dashboard tracking migration status across all tools and accounts.<br>Integrates: MGN, DMS, Snowball, App Discovery, partner tools.<br>One view: discovered, in-progress, completed, failed server counts. |

| **Q10** | What is AWS Application Migration Service (MGN)? |
|:---|:---|
| **A** |  |

```
Continuous block-level replication from source servers to AWS.
Steps: Install agent → Continuous replication → Test launch → Cutover.
Downtime: minutes (only during final cutover). Zero data loss.
Replaced: old AWS Server Migration Service (SMS — deprecated).
```

| **Q11** | What is AWS DataSync? |
|:---|:---|
| **A** |  |

```
Automated data transfer between on-premises storage and AWS.
Use for: bulk/scheduled batch transfers. One-time migration.
Supports: on-prem NFS/SMB to S3/EFS/FSx. Also S3→S3, EFS→EFS.
Speed: up to 10 Gbps.
```

| **Q12** | Which service handles SFTP-based file transfers to S3 or EFS? |
|:---|:---|
| **A** | AWS Transfer Family — managed SFTP, FTPS, FTP endpoints.<br>Partners upload via SFTP to your managed endpoint → files go to S3.<br>AWS manages: server, HA, keys. You manage: users, bucket policy. |

| **Q13** | Well-Architected pillar focused on recovering from failures? |
|:---|:---|
| **A** | Reliability — recover automatically from failures, scale to meet demand.<br>Design patterns: Multi-AZ, Auto Scaling, tested backups, chaos engineering. |

| **Q14** | Well-Architected pillar focused on using right resources at right size? |
|:---|:---|
| **A** | Performance Efficiency — use resources efficiently.<br>Principles: democratize tech, go global in minutes, use serverless, experiment. |

| **Q15** | Well-Architected pillar focused on minimizing environmental impact? |
|:---|:---|
| **A** | Sustainability — added 2021. Right-size, maximize utilization, use managed services.<br>AWS: 100% renewable energy (2023), water positive 2030, net zero 2040. |

| **Q16** | What is Amazon SNS? |
|:---|:---|
| **A** | Simple Notification Service — pub/sub messaging.<br>Publish to TOPIC → ALL subscribers receive simultaneously.<br>Protocols: email, SMS, HTTP, SQS, Lambda.<br>Fan-out: one message → multiple SQS queues simultaneously. |

| **Q17** | What does SNS stand for? |
|:---|:---|
| **A** | Simple Notification Service.<br>S = Simple (easy to use). N = Notification (push alerts). S = Service. |

| **Q18** | What is Amazon SQS? |
|:---|:---|
| **A** |  |

```
Simple Queue Service — decoupling applications with message queues.
Producer → Queue → Consumer POLLS for messages.
Messages stored safely if consumer is down (up to 14 days).
```

| **Q19** | Maximum retention period for SQS messages? |
|:---|:---|
| **A** | 14 days. Default is 4 days. Minimum 1 minute.<br>After max retention: message deleted automatically regardless. |

| **Q20** | Difference between SNS and SQS? |
|:---|:---|
| **A** | SNS: push to MANY subscribers simultaneously (fan-out). Message delivered once.<br>SQS: STORED in queue, ONE consumer per message, persists until processed.<br>Combined pattern: SNS → multiple SQS queues (fan-out + durability). |

| **Q21** | What is Amazon Kinesis? |
|:---|:---|
| **A** | Real-time streaming data collection and processing.<br>High-volume streams from many sources simultaneously.<br>Multiple consumers can read same stream.<br>Kinesis Data Streams: raw stream, you manage consumers.<br>Kinesis Data Firehose: managed delivery to S3/Redshift (near real-time). |

| **Q22** | Which service for processing real-time clickstream data? |
|:---|:---|
| **A** | Amazon Kinesis — designed for high-volume real-time streaming.<br>Detect fraud in seconds vs batch processing next day. |

| **Q23** | What is AWS Step Functions? |
|:---|:---|
| **A** | Serverless workflow orchestration — coordinate Lambda and AWS services<br>in visual state machine workflows.<br>Features: retry logic, error handling, parallel branches, human approval.<br>Standard: up to 1 year. Express: high-volume up to 5 minutes. |

| **Q24** | What is Amazon Lightsail? |
|:---|:---|
| **A** | Simple VPS platform with fixed monthly pricing.<br>Pre-configured for WordPress, LAMP, Node.js, etc. Starting at $3.50/month.<br>For: beginners, small businesses, simple web apps, portfolio sites. |

| **Q25** | Who is Lightsail designed for? |
|:---|:---|
| **A** | Users wanting simplicity without deep cloud knowledge.<br>Small businesses, freelancers, startup MVPs.<br>NOT for: complex architectures, auto-scaling enterprise apps. |

| **Q26** | Well-Architected pillar about cost waste and undifferentiated work? |
|:---|:---|
| **A** | Cost Optimization — avoid unnecessary costs, use managed services.<br>"Undifferentiated heavy lifting" = work that doesn't make your product unique. |

| **Q27** | Which R for replacing on-premises HR software with Workday SaaS? |
|:---|:---|
| **A** |  |

```
Repurchase — moving from self-managed app to commercial SaaS.
Other examples: on-prem CRM → Salesforce, on-prem email → Google Workspace.
ITSM = IT Service Management (ServiceNow, Jira are common tools).
```

| **Q28** | What is the Well-Architected Tool? |
|:---|:---|
| **A** |  |

```
Free tool reviewing your architecture against 6 pillars.
Answer ~65 questions → get findings (High/Medium risk) → improvement plan.
WAR = Well-Architected Review (formal review with AWS Solution Architect).
```

| **Q29** | Relationship between Trusted Advisor and Well-Architected? |
|:---|:---|
| **A** | Well-Architected: theoretical best practices, manual review, done occasionally.<br>Trusted Advisor: automated checks against YOUR actual environment, daily.<br>TA implements WA principles as automated real-time checks. |

| **Q30** | Critical app taking 2 years to re-architect. What to do now? |
|:---|:---|
| **A** |  |

```
Retain (keep on-premises) OR Rehost to EC2 now while planning Refactor.
Common pattern: Rehost → stabilize → Replatform/Refactor over time.
```

| **Q31** | Which CAF perspective covers risk management? |
|:---|:---|
| **A** | Governance perspective — portfolio management, risk, compliance,<br>program management, benefits realization, financial management. |

| **Q32** | Which service fans out one message to multiple SQS queues? |
|:---|:---|
| **A** | Amazon SNS — publish to topic, multiple SQS queues subscribe.<br>Each queue processes independently. One failure doesn't affect others. |

| **Q33** | Reliability pillar approach to designing for failure? |
|:---|:---|
| **A** | "Everything fails all the time" — Werner Vogels, AWS CTO.<br>No single points of failure. Automate recovery. Test failure scenarios.<br>Chaos engineering = intentionally causing failures to test recovery. |

| **Q34** | Which R has highest ROI long-term but most effort? |
|:---|:---|
| **A** | Refactor — cloud-native re-architecture.<br>50-70% cost savings possible. Elasticity, pay-per-use, faster delivery. |

| **Q35** | What is AWS Application Discovery Service? |
|:---|:---|
| **A** |  |

```
Discover on-premises servers before migration. Map dependencies.
Agentless (VMware vCenter) or Agent-based (physical/other VMs).
WebServer → AppServer → Database → must migrate all 3 together!
```

| **Q36** | Difference between DataSync and Storage Gateway? |
|:---|:---|
| **A** | DataSync: MIGRATION/TRANSFER — move data to AWS (one-time or scheduled batch).<br>Storage Gateway: ONGOING HYBRID — permanent connection, apps use S3 as local storage. |

| **Q37** | SQS queue type guaranteeing exactly-once processing and order? |
|:---|:---|
| **A** | FIFO (First-In-First-Out) queue.<br>Standard: at-least-once (may duplicate), unlimited throughput.<br>FIFO: exactly-once, strict order, up to 3,000 msg/sec.<br>Use FIFO: financial transactions, order processing, anything order-sensitive. |

| **Q38** | Standard SQS queue's delivery guarantee? |
|:---|:---|
| **A** | At-least-once delivery — messages may be delivered more than once.<br>Apps must be idempotent (same result whether processed once or twice).<br>Idempotent = same result when done multiple times as when done once. |

| **Q39** | What is Amazon EventBridge? |
|:---|:---|
| **A** |  |

```
Serverless event bus routing AWS events to targets automatically.
Event (EC2 stops) → Rule (matches) → Target (Lambda, SNS, SSM automation).
Formerly CloudWatch Events. Used for event-driven automation.
```

| **Q40** | Well-Architected pillar covering CI/CD and monitoring? |
|:---|:---|
| **A** | Operational Excellence — run, monitor, and improve operations.<br>Principles: IaC, frequent small reversible changes, post-incident reviews.<br>PIR = Post-Incident Review (blameless, improve runbooks after incidents). |

| **Q41** | Company found 40% of servers unused. Which R? |
|:---|:---|
| **A** | Retire — decommission unused servers before migration.<br>Saves: migration effort, licensing costs, hardware refresh, security risk. |

| **Q42** | Replatforming to RDS instead of MySQL on EC2 provides? |
|:---|:---|
| **A** | Managed service benefits: automatic patching, backups, Multi-AZ HA.<br>No application code changes. Same MySQL engine. 9 hours/month freed per DB. |

| **Q43** | What is the CAF Operations perspective? |
|:---|:---|
| **A** | Ensuring cloud services are delivered per agreed business SLAs.<br>Monitoring, incident management, DR testing, cloud operations model.<br>CCoE = Cloud Center of Excellence (team that sets cloud standards). |

| **Q44** | What does the CAF Platform perspective cover? |
|:---|:---|
| **A** | Building cloud platform architecture, landing zones, network topology.<br>Application architecture: microservices, containers, serverless patterns.<br>Your VMware/SAN/storage expertise directly relevant here. |

| **Q45** | Which migration tool provides continuous replication for lift-and-shift? |
|:---|:---|
| **A** |  |

```
AWS Application Migration Service (MGN) — continuous block-level replication.
Install agent → replicate → test → cutover (minutes of downtime).
```

| **Q46** | What is an SNS topic? |
|:---|:---|
| **A** | Logical communication channel. Publishers send to topic.<br>Subscribers receive from topic. Like a TV channel — one broadcast, many viewers.<br>Standard topics: high throughput, unordered. FIFO topics: ordered, exactly-once. |

| **Q47** | Maximum message size in SQS? |
|:---|:---|
| **A** | 256 KB. For larger payloads: store in S3, put S3 reference in SQS message.<br>AWS Extended Client Library handles this pattern automatically. |

| **Q48** | Service for serverless workflows coordinating Lambda and AWS services? |
|:---|:---|
| **A** | AWS Step Functions — visual workflow builder.<br>Standard (up to 1 year, complex orchestration) or<br>Express (up to 5 min, high volume event processing). |

| **Q49** | What is the CAF Business perspective? |
|:---|:---|
| **A** | Align cloud investment with business goals.<br>Business case: TCO analysis, expected savings.<br>Success metrics: cost per transaction, time-to-market, availability %. |

| **Q50** | Most appropriate R for legacy mainframe with no cloud equivalent? |
|:---|:---|
| **A** | Retain — keep on-premises until viable migration path exists or app retired.<br>Mainframe migration: can take years. Plan, document, gradual replacement.<br>Strangler fig pattern = gradually replace old system piece by piece. |

DAY 9 COMPLETE
*Tomorrow: Day 10 — Additional Services & Full Review*

## Day 10 — ADDITIONAL SERVICES & FULL REVIEW

*Study: 3 hours  |  Questions: 50*

#### Acronym Reference (DAY 10)

| Acronym | Definition |
|---|---|
| `ML` | Machine Learning |
| `AI` | Artificial Intelligence |
| `NLP` | Natural Language Processing |
| `OCR` | Optical Character Recognition |
| `TTS` | Text-to-Speech |
| `STT` | Speech-to-Text |
| `BI` | Business Intelligence |
| `IDE` | Integrated Development Environment |
| `HDFS` | Hadoop Distributed File System |
| `CI` | Continuous Integration |
| `CD` | Continuous Delivery/Deployment |

ADDITIONAL SERVICES QUICK REFERENCE:
Rekognition:    Computer vision — image/video analysis, face detection
Transcribe:     STT — speech to text (call center transcription, subtitles)
Polly:          TTS — text to speech (IVR, accessibility, notifications)
Translate:      Language translation (75+ languages)
Comprehend:     NLP — sentiment analysis, entity detection, key phrases
Lex:            Chatbots (same tech as Alexa). Understand voice/text intent.
SageMaker:      End-to-end ML platform — build, train, deploy models
Textract:       OCR+ — extract structured text/tables/forms from documents
Kendra:         ML-powered intelligent enterprise search
Personalize:    Real-time personalized recommendations (like Amazon.com)
Forecast:       Time-series ML forecasting (demand, staffing, energy)
Fraud Detector: ML-based fraud detection and prevention

Athena:         Serverless SQL on S3 ($5/TB scanned)
EMR:            Managed Hadoop/Spark for big data processing
Glue:           Serverless ETL service
QuickSight:     BI dashboards and visualizations (native AWS)
Lake Formation: Set up and secure data lakes in days not months

CodeCommit:  Managed Git repositories
CodeBuild:   Build and test code (CI) — compiles, runs tests, creates artifacts
CodeDeploy:  Deploy to EC2, Lambda, on-premises (CD)
CodePipeline:Orchestrate full CI/CD pipeline
X-Ray:       Distributed tracing — find performance bottlenecks in microservices
Cloud9:      Cloud-based browser IDE — no local install

WorkSpaces:  Managed virtual desktop (DaaS) — full Windows/Linux desktop
AppStream:   Stream specific applications via browser — no install needed
SES:         Simple Email Service — transactional and bulk email
Connect:     Cloud contact center

### Questions & Answers — Day 10

| **Q1** | Which AWS AI service converts speech to text? |
|:---|:---|
| **A** | Amazon Transcribe — STT. Takes audio, returns text transcript.<br>Use for: call center analytics, meeting notes, video subtitles.<br>Features: speaker identification, PII redaction from transcripts. |

| **Q2** | Which AWS AI service converts text to speech? |
|:---|:---|
| **A** | Amazon Polly — TTS. 60+ voices, 29 languages. Neural TTS = natural sound.<br>Use for: accessibility, e-learning narration, IVR systems, notifications.<br>IVR = Interactive Voice Response (phone menu systems). |

| **Q3** | Which analyzes images and videos for objects, faces, and scenes? |
|:---|:---|
| **A** | Amazon Rekognition — computer vision service.<br>Detects: objects, scenes, faces, celebrities, text in images, unsafe content.<br>Videos: track people across frames, detect activities. |

| **Q4** | Which service powers chatbots (same tech as Alexa)? |
|:---|:---|
| **A** | Amazon Lex — Natural Language Understanding.<br>User speaks/types → Lex identifies intent and extracts slots (parameters).<br>Integrates with: Lambda, Amazon Connect, Slack, Facebook Messenger. |

| **Q5** | Service for building, training, and deploying ML models? |
|:---|:---|
| **A** |  |

```
Amazon SageMaker — complete ML lifecycle platform.
Data Wrangler (prepare) → Studio (build) → Training (train) → Endpoints (deploy).
Pay only for compute when training runs.
```

| **Q6** | Service extracting structured data from scanned documents? |
|:---|:---|
| **A** | Amazon Textract — OCR+ extracts key-value pairs, tables, forms.<br>Regular OCR: just raw text. Textract: structured JSON output.<br>Use for: invoice processing, tax form extraction, contract analysis. |

| **Q7** | Add product recommendations to e-commerce site? |
|:---|:---|
| **A** |  |

```
Amazon Personalize — real-time personalized recommendations.
Same ML as Amazon.com. Feed historical data → train model → query API.
No ML expertise needed.
```

| **Q8** | Service for serverless SQL queries on S3? |
|:---|:---|
| **A** | Amazon Athena — serverless, $5/TB scanned, standard SQL.<br>Glue Data Catalog = metadata store (schema definitions for S3 data).<br>Parquet format: columnar = scan less data = cheaper + faster. |

| **Q9** | What is AWS Glue? |
|:---|:---|
| **A** |  |

```
Serverless ETL service — extract, transform, load data for analytics.
Connects: S3, RDS, DynamoDB → transforms → delivers to Redshift, S3.
Runs on managed Spark. Glue Crawlers: auto-discover schema.
```

| **Q10** | What is Amazon QuickSight? |
|:---|:---|
| **A** | AWS BI (Business Intelligence) service. Interactive dashboards.<br>Reads directly from S3, Athena, Redshift, RDS. Serverless. Pay per session.<br>ML-powered anomaly detection built-in. |

| **Q11** | What is Amazon EMR? |
|:---|:---|
| **A** | Elastic MapReduce — managed Hadoop/Spark clusters for big data.<br>AWS manages: cluster setup, config, scaling. You manage: your code.<br>Use Spot Instances for task nodes = 90% savings on big data processing. |

| **Q12** | What is AWS CodePipeline? |
|:---|:---|
| **A** |  |

```
Orchestrates complete CI/CD pipeline: source → build → test → deploy.
Integrates: CodeCommit (source), CodeBuild (build), CodeDeploy (deploy).
All automated — developer pushes code → production deployment.
```

| **Q13** | Difference between CodeBuild and CodeDeploy? |
|:---|:---|
| **A** | CodeBuild: BUILD + TEST code (CI). Input: source code. Output: artifact.<br>CodeDeploy: DEPLOY artifact (CD). Input: artifact. Output: running app. |

| **Q14** | What is AWS X-Ray? |
|:---|:---|
| **A** |  |

```
Distributed tracing — trace requests through all microservices.
Shows which service is slow/erroring.
Service Map: API GW (15ms) → Lambda (45ms) → RDS (890ms) ← PROBLEM!
```

| **Q15** | What is AWS WorkSpaces? |
|:---|:---|
| **A** | Managed virtual desktop service (DaaS).<br>Full Windows/Linux desktop in the cloud. Access from any device via browser.<br>Use for: remote work, contractors, regulated environments, call centers. |

| **Q16** | What is Amazon SES? |
|:---|:---|
| **A** | Simple Email Service — managed email at scale.<br>Transactional: "Your order shipped" (triggered by app).<br>Bulk/marketing: newsletters to 500K subscribers.<br>Cost: $0.10/1,000 emails. |

| **Q17** | Service for ML-powered intelligent enterprise search? |
|:---|:---|
| **A** |  |

```
Amazon Kendra — understands natural language questions.
"How many vacation days in first year?" → reads HR docs → returns direct answer.
Not just keyword matching — understands context and intent.
```

| **Q18** | What is AWS Lake Formation? |
|:---|:---|
| **A** | Set up and secure data lakes in days instead of months.<br>Automates: S3 setup, Glue crawlers, data catalog, access permissions.<br>Column-level security = restrict access to specific columns (hide SSNs). |

| **Q19** | What is Amazon AppStream 2.0? |
|:---|:---|
| **A** | Stream specific applications via browser. No local install needed.<br>Different from WorkSpaces (full desktop) — AppStream = specific apps only.<br>Use for: expensive licensed software (AutoCAD), shared across users. |

| **Q20** | Which service for ML-based fraud detection? |
|:---|:---|
| **A** | Amazon Fraud Detector — ML models trained on fraud patterns.<br>Analyzes: account age, location, device, time, amount → fraud score.<br>Return: fraud score + outcome (approve/review/block). |

| **Q21** | REVIEW: Key difference between CloudWatch and CloudTrail? |
|:---|:---|
| **A** |  |

```
CloudWatch: "How is infrastructure PERFORMING?" (metrics, CPU, latency).
CloudTrail: "WHO did WHAT to my infrastructure?" (API audit log).
EXAM: "audit log" → CloudTrail. "CPU alarm" → CloudWatch.
```

| **Q22** | REVIEW: Security Group vs NACL? |
|:---|:---|
| **A** |  |

```
Security Group: INSTANCE level, STATEFUL, ALLOW only.
NACL: SUBNET level, STATELESS, ALLOW + DENY.
"Block specific IP" → NACL. "Open port 443 on EC2" → Security Group.
```

| **Q23** | REVIEW: RDS Multi-AZ vs Read Replicas? |
|:---|:---|
| **A** |  |

```
Multi-AZ: SYNCHRONOUS, HIGH AVAILABILITY, automatic failover, cannot read standby.
Read Replica: ASYNCHRONOUS, PERFORMANCE, read scaling, any region.
"Disaster recovery" → Multi-AZ. "Scale reads" → Read Replica.
```

| **Q24** | REVIEW: When to use Spot Instances? |
|:---|:---|
| **A** | For fault-tolerant, interruptible workloads: batch jobs, big data, CI/CD, rendering.<br>NEVER for: production databases, real-time apps (cannot be interrupted). |

| **Q25** | REVIEW: Difference between SNS and SQS? |
|:---|:---|
| **A** |  |

```
SNS: push to MANY simultaneously, fan-out, message lost if subscriber down.
SQS: STORED queue, one consumer per message, persists up to 14 days.
"Send to multiple recipients" → SNS. "Decouple applications" → SQS.
```

| **Q26** | REVIEW: Direct Connect vs VPN? |
|:---|:---|
| **A** |  |

```
Direct Connect: PRIVATE fiber, CONSISTENT performance, weeks, expensive.
VPN: ENCRYPTED internet, VARIABLE performance, hours, cheap.
"Consistent performance" → DX. "Quick/cheap setup" → VPN.
```

| **Q27** | REVIEW: GuardDuty vs Inspector vs Macie? |
|:---|:---|
| **A** | GuardDuty: THREATS in account (ML, anomaly detection, threat intel).<br>Inspector: VULNERABILITIES in EC2/containers (CVE scanning).<br>Macie: SENSITIVE DATA in S3 (PII, credentials, financial data). |

| **Q28** | REVIEW: CloudFront vs Global Accelerator? |
|:---|:---|
| **A** |  |

```
CloudFront: CACHES content at edge, HTTP/HTTPS only, CDN.
Global Accelerator: ROUTES over AWS private network, TCP/UDP, static IPs.
"Cache images globally" → CF. "Two static IPs for whitelist" → GA.
```

| **Q29** | REVIEW: Secrets Manager vs Parameter Store? |
|:---|:---|
| **A** |  |

```
Secrets Manager: secrets + auto-rotation, $0.40/secret/month.
Parameter Store: config + secrets, FREE standard tier, no auto-rotation.
"DB passwords with auto-rotation" → SM. "Config values" → PS.
```

| **Q30** | REVIEW: S3 vs EBS vs EFS vs Instance Store? |
|:---|:---|
| **A** |  |

```
S3: object/unlimited. EBS: block/single-instance/persistent.
EFS: file/multi-instance/persistent. Instance Store: temporary/fastest.
"Multiple EC2 share files" → EFS. "Database volume" → EBS.
```

| **Q31** | Translate app into 50 languages? |
|:---|:---|
| **A** | Amazon Translate — neural machine translation, 75+ languages.<br>Use for: real-time chat translation, content localization, document translation. |

| **Q32** | Running Apache Spark jobs on large datasets? |
|:---|:---|
| **A** | Amazon EMR — managed Hadoop/Spark. Submit Spark job, AWS runs it.<br>Core nodes process data. Task nodes (Spot Instances) for cost savings. |

| **Q33** | Build complete CI/CD pipeline using only AWS services? |
|:---|:---|
| **A** |  |

```
CodeCommit (source) → CodeBuild (build/test) → CodeDeploy (deploy).
CodePipeline orchestrates the entire flow end-to-end.
```

| **Q34** | What is Amazon Cloud9? |
|:---|:---|
| **A** | Cloud-based browser IDE. Full code editor, terminal, pre-installed AWS CLI.<br>Runs on EC2. Access from any device — iPad, library computer, client site.<br>Collaborative editing (pair programming). |

| **Q35** | Service providing NLP for sentiment and entity extraction? |
|:---|:---|
| **A** | Amazon Comprehend — NLP for text analysis.<br>Sentiment: positive/negative/neutral/mixed.<br>Entities: PERSON, ORGANIZATION, LOCATION, DATE.<br>Key phrases, language detection, topic modeling. |

| **Q36** | Difference between Kinesis Data Streams and Firehose? |
|:---|:---|
| **A** | Data Streams: real-time (ms), you write consumers, multiple readers, replay.<br>Firehose: near real-time (60s buffer), managed delivery, one destination, simpler.<br>Use Streams: need replay, multiple consumers, custom processing.<br>Use Firehose: just deliver to S3/Redshift/OpenSearch easily. |

| **Q37** | Which service sends push notifications to mobile devices? |
|:---|:---|
| **A** | Amazon SNS — supports APNs (Apple) and FCM (Android/Google).<br>APNs = Apple Push Notification service. FCM = Firebase Cloud Messaging. |

| **Q38** | REVIEW: Which pillar covers encryption, least privilege, MFA? |
|:---|:---|
| **A** | Security pillar — protect data, systems, and assets.<br>Implement strong identity, enable traceability, apply security at all layers. |

| **Q39** | REVIEW: Which pillar covers Multi-AZ, Auto Scaling, backups? |
|:---|:---|
| **A** | Reliability pillar — recover from failures, scale dynamically.<br>Design for failure. Automate recovery. Test recovery procedures. |

| **Q40** | REVIEW: What does Replatform mean? |
|:---|:---|
| **A** |  |

```
"Lift, tinker, and shift" — minor optimization, no re-architecture.
App code unchanged. Architecture mostly same. Operations improved.
Examples: EC2 MySQL → RDS MySQL. Tomcat EC2 → Elastic Beanstalk.
```

| **Q41** | Hadoop on-premises. AWS equivalent? |
|:---|:---|
| **A** | Amazon EMR (Elastic MapReduce) — managed Hadoop/Spark on AWS.<br>You submit jobs. AWS manages cluster, scaling, OS.<br>Store data in S3 (not HDFS). Use Spot for 90% savings. |

| **Q42** | What is Amazon Forecast? |
|:---|:---|
| **A** |  |

```
ML time-series forecasting. Demand, staffing, energy predictions.
Feed historical data → Forecast trains model → return predictions with confidence.
Same technology Amazon uses for supply chain forecasting.
```

| **Q43** | Which developer tool finds performance bottlenecks in microservices? |
|:---|:---|
| **A** | AWS X-Ray — distributed tracing. Service Map shows latency per service.<br>Each request traced through ALL services it touches. |

| **Q44** | REVIEW: Three AWS pricing fundamentals? |
|:---|:---|
| **A** | 1. Pay as you go (variable, no upfront).<br>2. Save when you reserve (1-3 year commit = 72% off).<br>3. Pay less as you use more (volume discounts — S3 tiers). |

| **Q45** | REVIEW: Is data transfer into AWS free? |
|:---|:---|
| **A** | YES — data transfer IN to AWS is ALWAYS FREE.<br>Data OUT costs money (~$0.09/GB to internet).<br>EXAM SHORTCUT: Data IN = Free. Data OUT = Costs. |

| **Q46** | REVIEW: What is AWS CAF? |
|:---|:---|
| **A** | Cloud Adoption Framework. 6 perspectives:<br>Business, People, Governance, Platform, Security, Operations.<br>Memory: "Business People Go Play Soccer Online" |

| **Q47** | REVIEW: Which S3 class is cheapest with 12-hour retrieval? |
|:---|:---|
| **A** |  |

```
S3 Glacier Deep Archive — $0.00099/GB/month. 12-hour retrieval. 180-day min.
Storage class order (cheapest last):
Standard → Intelligent → Standard-IA → One Zone-IA → Glacier Instant
→ Glacier Flexible → Glacier Deep Archive.
```

| **Q48** | REVIEW: What does a NAT Gateway allow? |
|:---|:---|
| **A** | Private subnet instances initiate OUTBOUND internet connections.<br>Internet CANNOT initiate inbound connections to private instances.<br>Must be in PUBLIC subnet. One per AZ for HA. |

| **Q49** | REVIEW: Which support plan includes a dedicated TAM? |
|:---|:---|
| **A** | Enterprise Support ($15,000+/month) — dedicated TAM.<br>Enterprise On-Ramp: pool of shared TAMs. Business: no TAM. |

| **Q50** | REVIEW: What is the principle of least privilege? |
|:---|:---|
| **A** | Grant only minimum permissions needed for the job.<br>Start: zero permissions. Add: only what's needed. Review: remove unused.<br>If compromised with least privilege: minimal blast radius. |

DAY 10 COMPLETE — ALL CONTENT COVERED

## Day 11 — FULL PRACTICE EXAM #1

USE: https://tutorialsdojo.com/courses/
aws-certified-cloud-practitioner-practice-exams

EXAM SIMULATION INSTRUCTIONS:
No notes, no references, no searching
Set a 90-minute timer
Read every question TWICE before answering
Flag uncertain questions, return at end
Record score per domain when done

TARGET SCORE: 75%+ (passing = 700/1000 on real exam)

4 EXAM DOMAINS AND WEIGHTINGS:
Domain 1: Cloud Concepts         24%
Domain 2: Security & Compliance  30%
Domain 3: Cloud Technology       34%
Domain 4: Billing & Pricing      12%

AFTER EXAM — REVIEW EVERY WRONG ANSWER:
For each wrong answer, write:
1. Why you got it wrong
2. What the correct answer is and WHY
3. The topic to review

DAY 11 STUDY NOTES (review while waiting for exam link):

GLOBAL vs REGIONAL SERVICES (commonly tested):
GLOBAL (create once, works everywhere):
IAM, Route 53, CloudFront, WAF, Shield
REGIONAL (deploy per region):
EC2, S3, RDS, VPC, Lambda, DynamoDB, EFS, ELB

KEY NUMBERS TO MEMORIZE:
Lambda max timeout: 15 minutes
Lambda free tier: 1 million requests/month
SQS max retention: 14 days
EBS: one instance at a time (standard)
Aurora read replicas: up to 15
RDS read replicas: up to 5
S3 Glacier Deep Archive minimum: 180 days
S3 Standard-IA minimum: 30 days
RDS backup retention: 1-35 days
Free tier EC2: 750 hours/month (t2/t3.micro)
Business Support: $100+/month minimum
Enterprise Support: $15,000+/month (dedicated TAM)
Reserved Instance max savings: 72% (3-year all-upfront)
Spot Instance max savings: 90%

SERVICES TO KNOW BY PURPOSE:
Threat detection (ML): GuardDuty
Vulnerability scanning: Inspector
Sensitive data in S3: Macie
Compliance reports: Artifact
Encryption keys: KMS
API audit log: CloudTrail
Performance metrics: CloudWatch
Resource config history: Config
Central security view: Security Hub
Secrets with auto-rotation: Secrets Manager
Free config values: Parameter Store
Free SSL/TLS certs: ACM
User authentication for apps: Cognito
Serverless recommendations: Trusted Advisor
Cost visualization: Cost Explorer
Cost alerts: AWS Budgets
Most granular billing: CUR (Cost and Usage Report)
Pre-deploy cost estimate: Pricing Calculator

## Day 12 — WEAK AREA DRILL + PRACTICE EXAM #2

HOUR 1: Review weakest domains from Day 11 exam.
Score < 70% on Cloud Concepts → Re-read Days 1 notes
Score < 70% on Security → Re-read Days 2 and 7 notes
Score < 70% on Technology → Re-read Days 3-9 notes
Score < 70% on Billing → Re-read Day 8 notes

ADDITIONAL REVIEW — SERVICES THAT ARE EASILY CONFUSED:

COMPUTE CONFUSION:
EC2 vs Lambda vs Fargate vs Beanstalk vs Lightsail
- EC2: full VM control, you patch OS
- Lambda: serverless functions, event-triggered, max 15 min
- Fargate: serverless containers, no EC2 management
- Beanstalk: PaaS, upload code, AWS manages everything
- Lightsail: simple VPS, fixed price, beginners

DATABASE CONFUSION:
RDS vs DynamoDB vs Redshift vs ElastiCache vs Aurora
- RDS: relational, managed, OLTP
- DynamoDB: NoSQL, serverless, ms latency at any scale
- Redshift: data warehouse, OLAP, columnar, analytics
- ElastiCache: in-memory cache, sub-ms, Redis or Memcached
- Aurora: cloud-native relational, 5x faster, MySQL/PostgreSQL

STORAGE CONFUSION:
S3 vs EBS vs EFS vs Instance Store vs Storage Gateway
- S3: object, unlimited, internet access, no direct EC2 mount
- EBS: block, one EC2 at a time, same AZ, persistent
- EFS: file NFS, many EC2 simultaneously, multi-AZ, Linux
- Instance Store: temporary, fastest, lost on stop/terminate
- Storage Gateway: hybrid, connects on-prem apps to S3/Glacier

SECURITY CONFUSION:
GuardDuty vs Inspector vs Macie vs Config vs Security Hub
- GuardDuty: threats (anomaly detection, ML)
- Inspector: vulnerabilities (CVE scanning)
- Macie: sensitive data (PII in S3)
- Config: resource compliance (configuration history)
- Security Hub: aggregate all findings into one dashboard

HOURS 2-3: Full Practice Exam #2
TARGET: 80%+
If 80%+: You are ready to schedule the exam.
If below 80%: Identify remaining gaps, drill Day 13.

## Day 13 — FINAL PRACTICE EXAM + GAP CLOSE

HOUR 1: Service Cheat Sheet Review

COMPUTE:
EC2, Lambda, Fargate, ECS, EKS, Beanstalk, Lightsail, Batch, Outposts

STORAGE:
S3 (7 classes), EBS (gp3/io2/st1/sc1), EFS, Instance Store,
Storage Gateway (File/Volume/Tape), Snow Family, DataSync, FSx

DATABASE:
RDS, Aurora, DynamoDB (+ DAX), ElastiCache (Redis/Memcached),
Redshift, DocumentDB, Neptune, QLDB, Timestream, DMS, Athena

NETWORK:
VPC, Subnets, IGW, NAT Gateway, Route Tables, Security Groups,
NACLs, VPC Peering, Transit Gateway, VPN, Direct Connect,
CloudFront, Route 53, Global Accelerator, API Gateway

SECURITY:
IAM, KMS, CloudTrail, CloudWatch, Config, GuardDuty, Inspector,
Macie, Security Hub, Shield (Standard/Advanced), WAF, Secrets Manager,
Parameter Store, ACM, Cognito, Artifact, Trusted Advisor, STS

MANAGEMENT:
CloudFormation, CDK, SSM, Organizations, Control Tower,
Cost Explorer, Budgets, CUR, Pricing Calculator, Compute Optimizer

MESSAGING:
SNS, SQS (Standard/FIFO), Kinesis (Streams/Firehose), Step Functions, EventBridge

ML/AI:
Rekognition, Transcribe, Polly, Translate, Comprehend, Lex,
SageMaker, Textract, Kendra, Personalize, Forecast, Fraud Detector

ANALYTICS:
Athena, EMR, Glue, QuickSight, Kinesis Analytics, Lake Formation

DEV TOOLS:
CodeCommit, CodeBuild, CodeDeploy, CodePipeline, X-Ray, Cloud9

HOURS 2-3: Full Practice Exam #3
TARGET: 82%+
82%+: Ready. Exam is tomorrow. Stop studying.
78-81%: Take the exam. You are in range.
Below 78%: Postpone exam 3-4 days. Drill specific gaps.

## Day 14 — EXAM DAY

MORNING ROUTINE (30 minutes MAX):
Read this cheat sheet only.
NO new topics. NO practice questions.
Light breakfast. Water. You prepared for 14 days.

FINAL CHEAT SHEET — MEMORIZE BEFORE WALKING IN

6 CLOUD ADVANTAGES:
1. Trade CapEx for OpEx
2. Benefit from economies of scale
3. Stop guessing capacity
4. Increase speed and agility
5. Stop spending on data centers
6. Go global in minutes

3 CLOUD MODELS: IaaS, PaaS, SaaS
3 DEPLOYMENT MODELS: Public, Private, Hybrid

6 R'S OF MIGRATION:
Rehost (lift/shift), Replatform (minor tweak), Repurchase (SaaS),
Refactor (cloud-native), Retire (shut down), Retain (keep on-prem)

6 CAF PERSPECTIVES:
Business, People, Governance, Platform, Security, Operations
Memory: "Business People Go Play Soccer Online"

6 WELL-ARCHITECTED PILLARS:
Operational Excellence, Security, Reliability,
Performance Efficiency, Cost Optimization, Sustainability
Memory: "Only Stupid Rabbits Play Cost-free Sustainability"

GLOBAL SERVICES (create once = works everywhere):
IAM, Route 53, CloudFront, WAF

SECURITY GROUP vs NACL:
SG  = INSTANCE / STATEFUL  / ALLOW ONLY
NACL = SUBNET   / STATELESS / ALLOW + DENY

MULTI-AZ vs READ REPLICA:
Multi-AZ    = High Availability (failover, synchronous)
Read Replica = Performance (read scaling, asynchronous)

PURCHASING OPTIONS:
On-Demand = flexible, no commit, most expensive/hr
Reserved  = 1-3 year commit, up to 72% savings
Spot      = interruptible batch, up to 90% savings
Dedicated = BYOL, physical isolation

SNS vs SQS:
SNS = push to MANY simultaneously (pub/sub, fan-out)
SQS = store for ONE consumer to pull (queue, decouple)

DIRECT CONNECT vs VPN:
DX  = private fiber, consistent, expensive, weeks
VPN = encrypted internet, variable, cheap, hours

CLOUDFRONT vs GLOBAL ACCELERATOR:
CloudFront       = CDN, caches at edge, HTTP/HTTPS
Global Accel     = routes over AWS network, TCP/UDP, static IPs

S3 CLASSES CHEAPEST TO MOST EXPENSIVE (retrieve fee → storage cost):
Glacier Deep Archive < Glacier Flexible < Glacier Instant
< One Zone-IA < Standard-IA < Intelligent-Tiering < Standard

SUPPORT PLANS:
Basic              = FREE (7 TA checks, no engineer)
Developer          = $29/month (email, business hours)
Business           = $100+/month (24/7 phone/chat, 1-hr prod down)
Enterprise On-Ramp = $5,500+/month (TAM pool, 30-min critical)
Enterprise         = $15,000+/month (DEDICATED TAM, 15-min critical)

DATA TRANSFER:
IN to AWS  = ALWAYS FREE
OUT to internet = CHARGED (~$0.09/GB)

AWS SECURITY SERVICES:
CloudTrail = WHO did WHAT (API audit log)
CloudWatch = HOW is it performing (metrics)
Config = WHAT did resources look like (compliance history)
GuardDuty = THREATS (ML anomaly detection)
Inspector = VULNERABILITIES (CVE scanning)
Macie = SENSITIVE DATA in S3 (PII finder)

EXAM STRATEGY — THE FINAL CHECKLIST

Time: 90 minutes / 65 questions = ~83 seconds per question

1. Read EVERY question TWICE before selecting
2. Eliminate obviously wrong answers first (usually 2 of 4)
3. Look for qualifier words: MOST cost-effective, MINIMUM effort,
BEST practice, WHICH is NOT, etc.
4. Flag uncertain questions — come back at end
5. NEVER leave a question blank (no penalty for wrong)
6. When 2 options seem right: pick the MORE specific/managed AWS answer
7. Trust your 14 days of preparation

COMMON EXAM PATTERNS AND ANSWERS:
"Most cost-effective stable workload"  → Reserved Instance
"Most cost-effective batch/flexible"  → Spot Instance
"Highly available web application"    → Multi-AZ + ALB + ASG
"Managed service / no server mgmt"    → RDS, Lambda, Fargate, DynamoDB
"Who patches EC2 OS?"                 → Customer (you)
"Who patches RDS database engine?"    → AWS
"Block specific IP from VPC"          → NACL (not Security Group)
"Dedicated TAM"                       → Enterprise Support
"24/7 phone support minimum"          → Business Support
"Single view of security findings"    → Security Hub
"Audit trail of API calls"            → CloudTrail
"Compliance documents"                → AWS Artifact
"Cost breakdown by team/project"      → Cost Allocation Tags
"Pre-deployment cost estimate"        → Pricing Calculator
"Recommend resource right-sizing"     → Compute Optimizer or Trusted Advisor
"Fan-out to multiple endpoints"       → SNS
"Decouple application components"     → SQS
"Real-time streaming data"            → Kinesis
"Serverless function triggered by S3" → Lambda
"Cross-region disaster recovery"      → Multi-region + Route 53 Failover

MASTER ACRONYM GLOSSARY — ALL DAYS

ACM    = AWS Certificate Manager
AD     = Active Directory
AES    = Advanced Encryption Standard
AI     = Artificial Intelligence
ALB    = Application Load Balancer
AMI    = Amazon Machine Image
ARN    = Amazon Resource Name
ASG    = Auto Scaling Group
AZ     = Availability Zone
BAA    = Business Associate Agreement
BI     = Business Intelligence
BYOL   = Bring Your Own License
CA     = Certificate Authority
CAF    = Cloud Adoption Framework
CapEx  = Capital Expenditure
CCoE   = Cloud Center of Excellence
CDK    = Cloud Development Kit
CDN    = Content Delivery Network
CDC    = Change Data Capture
CI/CD  = Continuous Integration / Continuous Delivery
CIDR   = Classless Inter-Domain Routing
CMK    = Customer Master Key
CRR    = Cross-Region Replication
CUR    = Cost and Usage Report
CVE    = Common Vulnerabilities and Exposures
DAX    = DynamoDB Accelerator
DC     = Data Center
DDoS   = Distributed Denial of Service
DLQ    = Dead Letter Queue
DMS    = Database Migration Service
DNS    = Domain Name System
DR     = Disaster Recovery
DRT    = DDoS Response Team
DX     = Direct Connect
EBS    = Elastic Block Store
EC2    = Elastic Compute Cloud
ECS    = Elastic Container Service
EFA    = Elastic Fabric Adapter
EFS    = Elastic File System
EKS    = Elastic Kubernetes Service
ELB    = Elastic Load Balancer
EMR    = Elastic MapReduce
ENI    = Elastic Network Interface
ETL    = Extract Transform Load
FCM    = Firebase Cloud Messaging
FIFO   = First In First Out
GDPR   = General Data Protection Regulation
GLB    = Gateway Load Balancer
GPU    = Graphics Processing Unit
GSI    = Global Secondary Index
HA     = High Availability
HDFS   = Hadoop Distributed File System
HIPAA  = Health Insurance Portability and Accountability Act
HPC    = High Performance Computing
HSM    = Hardware Security Module
HTTP   = HyperText Transfer Protocol
HTTPS  = HTTP Secure
IaaS   = Infrastructure as a Service
IAM    = Identity and Access Management
IaC    = Infrastructure as Code
IDE    = Integrated Development Environment
IGW    = Internet Gateway
IOPS   = Input/Output Operations Per Second
IoT    = Internet of Things
IP     = Internet Protocol
ITSM   = IT Service Management
IVR    = Interactive Voice Response
JSON   = JavaScript Object Notation
K8s    = Kubernetes
KMS    = Key Management Service
KPI    = Key Performance Indicator
LSI    = Local Secondary Index
LTO    = Linear Tape-Open
MGN    = Application Migration Service
MFA    = Multi-Factor Authentication
ML     = Machine Learning
MQTT   = Message Queuing Telemetry Transport
NACL   = Network Access Control List
NAS    = Network Attached Storage
NAT    = Network Address Translation
NDA    = Non-Disclosure Agreement
NFS    = Network File System
NIC    = Network Interface Card
NLB    = Network Load Balancer
NLP    = Natural Language Processing
NVMe   = Non-Volatile Memory Express
OCR    = Optical Character Recognition
OLAP   = Online Analytical Processing
OLTP   = Online Transaction Processing
OpEx   = Operational Expenditure
OU     = Organizational Unit
PaaS   = Platform as a Service
PB     = Petabyte
PCI DSS= Payment Card Industry Data Security Standard
PHI    = Protected Health Information
PII    = Personally Identifiable Information
PITR   = Point-In-Time Recovery
PKI    = Public Key Infrastructure
PaaS   = Platform as a Service
RCE    = Remote Code Execution
RCU    = Read Capacity Unit
RDS    = Relational Database Service
RI     = Reserved Instance
RPO    = Recovery Point Objective
RTO    = Recovery Time Objective
S3     = Simple Storage Service
SaaS   = Software as a Service
SAML   = Security Assertion Markup Language
SCT    = Schema Conversion Tool
SCP    = Service Control Policy
SES    = Simple Email Service
SG     = Security Group
SMB    = Server Message Block
SNS    = Simple Notification Service
SQS    = Simple Queue Service
SQL    = Structured Query Language
SRR    = Same-Region Replication
SSE    = Server-Side Encryption
SSM    = Systems Manager
SSO    = Single Sign-On
SSRF   = Server-Side Request Forgery
STT    = Speech-to-Text
STS    = Security Token Service
TAM    = Technical Account Manager
TCO    = Total Cost of Ownership
TGW    = Transit Gateway
TLS    = Transport Layer Security
TOTP   = Time-based One-Time Password
TTS    = Text-to-Speech
TLS    = Transport Layer Security
UDP    = User Datagram Protocol
vCPU   = Virtual CPU
VM     = Virtual Machine
VGW    = Virtual Private Gateway
VPC    = Virtual Private Cloud
VPN    = Virtual Private Network
VTL    = Virtual Tape Library
WAF    = Web Application Firewall
WCU    = Write Capacity Unit
WORM   = Write Once Read Many
XSS    = Cross-Site Scripting

YOU ARE READY. GO PASS YOUR CLF-C02 EXAM.
Schedule at: https://www.aws.training/certification

14 days. 700 questions. 42 hours. You did the work.
Trust your preparation. Read each question twice. Go.

Christos Anastasiadis | AWS CCP CLF-C02 Study Plan
Generated: May 2026

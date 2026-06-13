---
tags:
  - aws
  - certifications
---
# AWS Cloud Practitioner CLF-C02 — 14-Day Study Plan


<div class="kb-summary">
**3 hrs/day · 50 Q&A per day · May 2026** AWS CLOUD PRACTITIONER CLF-C02 14-DAY STUDY PLAN  |  3 HRS/DAY  |  50 Q&A PER DAY Christos Anastasiadis  |  May 2026
</div>

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

### Acronym Reference (DAY 1)

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
- Private cloud  — Resources on your own data center
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
- Run AWS services on-premises


### Questions & Answers — Day 1

??? question "Q1. What is the definition of cloud computing?"

    On-demand delivery of IT (Information Technology) resources
    over the internet with pay-as-you-go pricing.

    NEW ACRONYM: IT = Information Technology
    Everything digital: servers, storage, networking, databases.

    ```text
    TRADITIONAL IT                    CLOUD (AWS)
    ┌────────────────────────────────────────── ┐               ┌ ──────────────────────────────────────────┐
    │  Buy servers     │               │  Request online  │
    │  Wait weeks      │     vs        │  Ready in mins   │
    │  Pay upfront     │               │  Pay per use     │
    │  Guess capacity  │               │  Scale anytime   │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q2. Which cloud advantage eliminates the need to guess how much infrastructure capacity you need?"

    Stop guessing capacity. AWS scales automatically
    using Auto Scaling.

    NEW ACRONYM: Auto Scaling = AWS service that automatically
    adds or removes servers based on real-time demand.

    ```text
    TRADITIONAL (guessing)            CLOUD (auto-match)
    ┌────────────────────────────────────────── ┐              ┌ ───────────────────────────────────────────┐
    │ Buy too much?    │              │  Auto Scaling    │
    │  wasted capacity │   vs         │  scales UP/DOWN  │
    │ Buy too little?  │              │  Always matches  │
    │  crashes!        │              │  actual demand   │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q3. What does "trade fixed expense for variable expense" mean?"

    Instead of investing upfront (CapEx), you pay only for
    what you consume (OpEx).

    CapEx = Capital Expenditure: Big upfront purchase
            Example: buying 500 servers for $2M
    OpEx  = Operational Expenditure: Ongoing costs
            Example: paying $50K/month AWS bill

    ```text
    CAPEX (Traditional)               OPEX (Cloud)
    ┌─────────────────────────────────────────── ┐             ┌ ───────────────────────────────────────────┐
    │ Jan: $2,000,000    │             │ Jan:  $45,000      │
    │ (buy servers)      │    vs       │ Feb:  $48,000      │
    │ Feb-Dec: maintain  │             │ (matches usage)    │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q4. Which cloud model gives the most control over infrastructure?"

    IaaS (Infrastructure as a Service) — you manage OS and above.

    ```text
    RESPONSIBILITY STACK
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │           IaaS        PaaS        SaaS       │
    │        ┌────────┐  ┌────────┐  ┌────────┐   │
    │  YOU → │  App   │  │  App   │  │        │   │
    │  YOU → │  Data  │  │  Data  │  │  AWS   │   │
    │  YOU → │  OS    │  │        │  │manages │   │
    │  AWS → │  Virt  │  │  AWS   │  │  ALL   │   │
    │  AWS → │  HW/DC │  │manages │  │        │   │
    │        └────────┘  └────────┘  └────────┘   │
    │  Control: HIGH         MID          LOW      │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q5. EC2 is an example of which cloud model?"

    IaaS — you manage the OS, AWS manages physical infra.

    NEW ACRONYM: EC2 = Elastic Compute Cloud
    Elastic = can grow/shrink. Compute = CPU+RAM. Cloud = hosted on AWS.
    = Virtual servers you rent on AWS. Like a VM on your VMware cluster
      except AWS owns the physical hardware.

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  EC2 (Elastic Compute Cloud)     │
    │  YOU manage: OS, apps, data, SGs │
    │  AWS manages: hardware, hypervisor│
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q6. Elastic Beanstalk is an example of which model?"

    PaaS — you deploy code, AWS manages everything else.

    NEW ACRONYM: PaaS = Platform as a Service
    AWS provides complete platform. You bring the code.

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  Elastic Beanstalk (PaaS)            │
    │  YOU → Upload your code              │
    │  AWS → Provisions EC2, OS, LB, ASG   │
    │  App is running! (you did nothing)   │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q7. Which cloud model requires managing the least infrastructure?"

    SaaS — provider manages everything, you just use it.

    NEW ACRONYM: SaaS = Software as a Service
    Like a streaming service for software. Just log in and use it.
    Examples: Gmail, Salesforce, ServiceNow, Jira

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  SaaS: Open browser → Log in → Use  │
    │  Provider manages: code, DB, servers │
    │  You manage: NOTHING                 │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q8. A company wants to keep sensitive data on-premises while using AWS for other workloads. Which deployment model?"

    Hybrid cloud — mix of on-premises and cloud.

    ```text
    YOUR DATA CENTER          AWS CLOUD
    ┌──────────────────────────────────────────── ┐          ┌ ─────────────────────────────────────────────┐
    │  Sensitive   │◄────────►│  Web servers │
    │  financial   │  VPN /   │  Dev/test    │
    │  records     │  Direct  │  Analytics   │
    │  (on-prem)   │  Connect │  Backups     │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    Classic hybrid cloud pattern.
    ```

??? question "Q9. Which deployment model uses only AWS with no on-premises?"

    Public cloud (all-in cloud).

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  INTERNET → AWS Region             │
    │  EC2, S3, RDS, Lambda — 100% cloud │
    │  No servers you own anywhere       │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q10. What is an AWS Region?"

    A geographical area with 2+ AZs, isolated from other regions.

    NEW ACRONYM: AZ = Availability Zone
    Physically separate data center(s) within a Region with
    independent power, cooling, and networking.

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  30+ Regions worldwide               │
    │  Examples: us-east-1 (N. Virginia)   │
    │            eu-west-1 (Ireland)       │
    │  Data stays IN region unless you     │
    │  explicitly move it                  │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q11. How many AZs does each AWS Region have at minimum?"

    At least two. Most have three or more.

    ```text
    AWS REGION (e.g. us-east-1)
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌─────────┐  ┌─────────┐  ┌─────┐  │
    │  │   AZ-1  │  │   AZ-2  │  │AZ-3 │  │
    │  │(min req)│  │(min req)│  │     │  │
    │  └─────────┘  └─────────┘  └─────┘  │
    │       └────────────┴────────────┘    │
    │         High-bandwidth private fiber  │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q12. What is an Availability Zone?"

    One or more discrete data centers with redundant power,
    networking, and connectivity within a region.

    ```text
    AVAILABILITY ZONE
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌──────────┐  ┌──────────┐      │
    │  │  Data    │  │  Data    │      │
    │  │ Center A │  │ Center B │      │
    │  └──────────┘  └──────────┘      │
    │  Independent power and cooling    │
    │  Connected to other AZs via       │
    │  private high-bandwidth fiber     │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    Like a separate building in your DC campus
    with its own power feed.
    ```

??? question "Q13. Why deploy applications across multiple AZs?"

    High availability — if one AZ fails, app continues in others.

    NEW ACRONYM: HA = High Availability
    Like your dual-fabric SAN — if Fabric A fails, Fabric B runs.

    ```text
    SINGLE AZ (bad)          MULTI-AZ (good)
    ┌──────────────────────────────────────────── ┐          ┌ ─────────────────────────────────────────────┐
    │     AZ-1    │          │  AZ-1    │  AZ-2    │
    │  ┌────────┐ │          │ ┌──────┐ │ ┌──────┐ │
    │  │  App   │ │          │ │ App  │ │ │ App  │ │
    │  └────────┘ │          │ └──────┘ │ └──────┘ │
    │  AZ fails   │          │ AZ fails │ Still UP!│
    │  OUTAGE!    │          │          │    ✓     │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q14. What are Edge Locations used for?"

    Caching content via CloudFront CDN to reduce latency.

    NEW ACRONYM: CDN = Content Delivery Network
    Network of servers worldwide caching content close to users.
    CloudFront = AWS's CDN service.

    ```text
    WITHOUT EDGE: [User: Tokyo] →→→→→ [Origin: us-east-1] ~150ms
    WITH EDGE:    [User: Tokyo] → [Edge: Tokyo] ~5ms (cached)
    ```

??? question "Q15. Which has more locations — Regions or Edge Locations?"

    Edge Locations (400+) vs Regions (30+).

    ```text
    Regions:         ██  30+
    AZs:             █████  90+
    Edge Locations:  ████████████████  400+
    Rule: Edge > AZs > Regions
    ```

??? question "Q16. What is an AWS Local Zone?"

    An extension of an AWS Region placed closer to large
    population centers for single-digit millisecond latency.

    NEW ACRONYM: ms = milliseconds (1/1000 of a second)

    ```text
    REGION (N. Virginia) ──extends──► [LA Local Zone]
    User in LA: ~20ms to VA vs ~1ms to Local Zone
    ```

??? question "Q17. What is AWS Wavelength?"

    AWS infrastructure embedded in 5G telecom networks for
    ultra-low latency mobile applications.

    NEW ACRONYMS: 5G = Fifth Generation mobile network
                  IoT = Internet of Things

    ```text
    STANDARD: [Mobile] → [5G Tower] → [Internet] → [AWS] ~15ms
    WAVELENGTH:[Mobile] → [5G Tower + AWS compute] ~1-2ms
    ```

??? question "Q18. What is AWS Outposts?"

    AWS-managed hardware installed in YOUR data center to run
    AWS services on-premises.

    ```text
    YOUR DATA CENTER
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  AWS Outposts Rack:              │
    │  EC2 | EBS | RDS | ECS           │
    │  AWS hardware in YOUR building   │
    │  Connects to AWS via Direct Connect│
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    Extend on-prem to AWS.
    ```

??? question "Q19. Which AWS service runs AWS infrastructure in your own DC?"

    AWS Outposts.

??? question "Q20. A company needs data to stay in a specific country. What should they consider?"

    Select an AWS Region in that country. AWS never moves
    data out of a region without your explicit action.

    NEW ACRONYM: GDPR = General Data Protection Regulation
    EU law requiring personal data of EU citizens stays in EU.

??? question "Q21. Which is NOT a cloud advantage? A) Go global in minutes  B) Eliminate all security concerns C) Stop guessing capacity  D) Trade fixed for variable"

    B — Cloud does NOT eliminate security concerns.
    Security is a SHARED responsibility.

    THE REAL 6 ADVANTAGES:
    1. Trade CapEx for OpEx
    2. Economies of scale
    3. Stop guessing capacity
    4. Speed and agility
    5. Stop spending on data centers
    6. Go global in minutes

??? question "Q22. What does "go global in minutes" mean?"

    Deploy in multiple AWS Regions worldwide quickly.

    WITHOUT CLOUD: Find DC, sign lease, order hardware → 6 months
    WITH AWS: Open console, select region, deploy → 10 minutes

??? question "Q23. Which deployment model is most like traditional IT?"

    Private cloud — your own hardware, your own DC.
    Your own hardware, fully under your control.

??? question "Q24. How are AZs connected within a region?"

    High-bandwidth, low-latency PRIVATE fiber — NOT internet.
    Similar to your dual-fabric SAN ISLs between buildings.

??? question "Q25. A startup wants global launch with minimal upfront cost. Which cloud advantage?"

    Trade fixed expense (CapEx) for variable expense (OpEx).
    Pay $0 upfront. Pay only when users arrive.

??? question "Q26. What factor is NOT used when choosing a Region? A) Compliance  B) Proximity  C) Services  D) Logo color"

    D. Real factors: Compliance first, then proximity,
    available services, then cost.

??? question "Q27. Which is correct about AWS Regions? A) All same services  B) Connected by public internet C) Each region isolated  D) One region only allowed"

    C — Regions are geographically isolated.
    If us-east-1 fails, eu-west-1 is NOT affected.

??? question "Q28. What is the primary purpose of multiple AZs?"

    Fault tolerance and HA — apps survive individual AZ failures.

    ELB = Elastic Load Balancer (routes traffic to healthy AZs)
    SYNC = Synchronous replication (data written to both at once)

??? question "Q29. Which component reduces content delivery latency globally?"

    Edge Locations used by CloudFront CDN.

??? question "Q30. A healthcare company must ensure EU patient data stays in EU."

    AWS Regions — data stays in the region you choose.
    Deploy in eu-west-1 or eu-central-1.

??? question "Q31. What best describes economies of scale?"

    AWS aggregates usage from millions of customers → lower costs
    → passes savings to customers through lower prices.

??? question "Q32. What type of expense is a monthly AWS bill?"

    OpEx (Operational Expenditure) — variable, pay-as-you-go.

??? question "Q33. What type of expense is buying physical servers?"

    CapEx (Capital Expenditure) — large upfront investment.
    Goes on balance sheet, depreciated over years.

??? question "Q34. A company runs on-premises infrastructure alongside an AWS pilot. Which model?"

    Hybrid cloud.

??? question "Q35. How many edge locations does AWS have approximately?"

    400+ edge locations worldwide.

??? question "Q36. Which is a characteristic of ALL cloud models? A) No security mgmt  B) On-demand self-service C) Requires on-prem  D) Fixed monthly pricing"

    B — On-demand self-service (NIST characteristic).

    NIST = National Institute of Standards and Technology
    5 cloud characteristics: On-demand self-service, broad network
    access, resource pooling, rapid elasticity, measured service.

??? question "Q37. What makes Wavelength different from AZs?"

    Wavelength is embedded in 5G telecom networks (~1-2ms).
    AZs are standalone data center facilities (~10-20ms).

??? question "Q38. Which for single-digit ms latency near a specific city?"

    AWS Local Zone if available near that city.

??? question "Q39. Which about AWS global infrastructure is TRUE? A) One region only  B) Edge = region locations C) AZs are physically separate  D) Same services everywhere"

    C — AZs are physically separate with independent
    power and networking.

??? question "Q40. What is the main benefit of "increase speed and agility"?"

    Access new resources in minutes. New EC2 in 60 seconds
    vs 6-8 weeks for physical server procurement.

    SSH = Secure Shell (how you remotely access Linux servers)

??? question "Q41. In IaaS, what does the customer manage?"

    OS, middleware, runtime, data, and applications.

    IaaS boundary: Customer owns OS and above.
    AWS owns: virtualization, hardware, data center.

??? question "Q42. In PaaS, what does AWS manage?"

    Everything except customer data and applications.
    OS, middleware, runtime, hardware — all AWS.

??? question "Q43. Gmail is an example of which model?"

    SaaS — Google manages everything.

??? question "Q44. What does Outposts allow that standard Regions do not?"

    Run AWS services on your own on-premises hardware
    inside your building.

??? question "Q45. Which advantage for expanding to new countries?"

    Go global in minutes — deploy in new regions in minutes
    vs months of physical DC build-out.

??? question "Q46. How does AWS achieve massive economies of scale?"

    Aggregating usage from hundreds of thousands of customers,
    achieving lower costs and passing savings to customers.
    AWS has dropped prices 100+ times since 2006.

??? question "Q47. Minimum AZs required for a Region to exist?"

    Two. Most regions have three. us-east-1 has six.

??? question "Q48. Which is SaaS? A) EC2  B) RDS  C) Salesforce CRM  D) Elastic Beanstalk"

    C — Salesforce. Log in via browser, use it.
    TRICK: RDS is PaaS (you still manage schema and data).
    CRM = Customer Relationship Management software.

??? question "Q49. Moving 500 servers to AWS changes from which expense to which?"

    From CapEx (owning servers) to OpEx (paying for usage).

??? question "Q50. Correct order of AWS infrastructure from largest to smallest?"

    ```text
    Region → Availability Zone → Data Center.
    (Edge locations exist separately for CloudFront CDN only.)
    ```

DAY 1 COMPLETE
*Tomorrow: Day 2 — Shared Responsibility Model & IAM*

## Day 2 — SHARED RESPONSIBILITY MODEL & IAM

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 2)

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

??? question "Q1. What is the AWS Shared Responsibility Model?"

    AWS = Security OF the cloud (physical infra, hardware, hypervisor).
    Customer = Security IN the cloud (data, IAM, OS, apps, network config).

    ```text
    CUSTOMER: Your data, IAM, OS patching, app code, security groups
    ═══════════════════════════════════ THE LINE
    AWS: Physical facilities, hardware, hypervisor, global network
    ```

??? question "Q2. Who patches the OS on an EC2 instance?"

    The CUSTOMER. On EC2 you manage the guest OS including patching.

    Guest OS = OS running INSIDE your VM (Windows/Linux you installed).
    Host OS = AWS hypervisor layer (Nitro/Xen — AWS manages this).

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  EC2 Instance                            │
    │  GUEST OS (Windows/Linux) ← YOU patch   │
    │  ─────────────────────────────────────   │
    │  HYPERVISOR (Nitro)       ← AWS patches  │
    │  PHYSICAL SERVER          ← AWS manages  │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q3. Who patches the database engine on RDS?"

    AWS. RDS is a managed service — AWS handles OS and DB patching.

    RDS vs EC2 DATABASE:
    RDS: AWS patches OS + DB engine. YOU manage data, schema, access.
    EC2: YOU patch everything. More control, more work.

??? question "Q4. Who is responsible for physical security of AWS data centers?"

    AWS. Always AWS. You never visit or touch AWS hardware.
    AWS uses: armed guards, biometrics, cameras, unmarked buildings.

??? question "Q5. Customer stores sensitive data in S3. Who encrypts it?"

    The CUSTOMER. AWS provides encryption OPTIONS (SSE-S3, SSE-KMS, SSE-C)
    but YOU must enable and configure encryption.

    SSE = Server-Side Encryption
    KMS = Key Management Service (manages encryption keys)
    Encryption = Converting readable data to scrambled form.

??? question "Q6. Who configures security group rules on EC2?"

    The CUSTOMER. Network configuration is always customer responsibility.

??? question "Q7. What does "security OF the cloud" mean?"

    AWS responsibility — physical facilities, hardware, hypervisor,
    global infrastructure, managed service underlying infrastructure.

??? question "Q8. What does "security IN the cloud" mean?"

    Customer responsibility — data, IAM, OS patching, app code,
    security groups, NACLs, VPC config, encryption choices.

??? question "Q9. For Lambda, what is the customer responsible for?"

    Function code and IAM roles/permissions.
    AWS manages all infrastructure, OS, runtime, scaling.

    Lambda = AWS serverless compute. You upload code, AWS runs it.
    Serverless = no servers for YOU to manage.

??? question "Q10. Which is ALWAYS AWS's responsibility? A) Encrypting customer data  B) Managing IAM passwords C) Physical decommissioning of storage hardware D) Patching guest OS on EC2"

    C — Physical decommissioning. AWS wipes/destroys old disks.
    DoD = Department of Defense (military-grade data wiping standard).

??? question "Q11. What is the AWS root user?"

    The identity created when account first opens.
    Complete unrestricted access to everything. Cannot be deleted.

    Like "sa" in SQL Server or "root" in Linux — don't use daily.

??? question "Q12. Best practice for AWS root user?"

    Enable MFA immediately. Create IAM admin user for daily work.
    Only use root for tasks that specifically require it.

??? question "Q13. Which tasks require root user?"

    Change account settings/email, close account, change support plan,
    restore deleted IAM admin, enable MFA delete on S3.
    Everything else: use IAM users or roles.

??? question "Q14. What does IAM stand for?"

    Identity and Access Management.
    Identity = WHO are you?  Access Management = WHAT can you do?
    FREE service. GLOBAL (not region-specific).

??? question "Q15. Is IAM regional or global?"

    GLOBAL. IAM users, groups, roles, policies work across all regions.

    GLOBAL services: IAM, Route 53, CloudFront, WAF
    REGIONAL services: EC2, S3, RDS, VPC, Lambda

??? question "Q16. What permissions does a new IAM user have by default?"

    NONE. Zero permissions. Must be explicitly granted.
    Principle of least privilege: start with nothing, add only what's needed.

??? question "Q17. What is the principle of least privilege?"

    Grant users only the minimum permissions needed for their job.
    If credentials are stolen: minimal damage possible.

??? question "Q18. What is an IAM Group?"

    ```sql
    Collection of IAM users. Attach policies to groups, not individuals.
    New person joins → add to group → instantly gets all permissions.
    Person leaves → remove from group → instantly loses permissions.
    ```

??? question "Q19. Can an IAM group contain other IAM groups?"

    NO. Groups contain only users, never other groups.
    A user CAN belong to multiple groups simultaneously.

??? question "Q20. What is an IAM Role?"

    Temporary identity not tied to a specific person.
    Assumed by: EC2 instances, Lambda functions, cross-account access.
    Best practice: use roles for EC2 apps instead of access keys.

    USER = permanent identity for a specific person.
    ROLE = like a hat anyone can put on temporarily.

??? question "Q21. When to use IAM Role vs access keys for EC2?"

    ALWAYS use IAM Role. Never store access keys on EC2.
    Roles: no credentials stored, auto-rotate, easy to update.
    Access keys on EC2: security risk if instance compromised.

??? question "Q22. What is an IAM Policy?"

    JSON document defining permissions — Allow or Deny specific
    actions on specific resources.

    Example: {"Effect":"Allow","Action":"s3:GetObject","Resource":"*"}
    ARN = Amazon Resource Name (unique identifier for every AWS resource)

??? question "Q23. Three types of IAM policies?"

    AWS managed (created by AWS), customer managed (created by you),
    inline (embedded directly in a user/role, not reusable).

??? question "Q24. What is MFA?"

    Multi-Factor Authentication.
    Multi = more than one. Factor = proof of identity.
    = Password (something you know) + Device (something you have).
    Even if password stolen, attacker needs your physical device.

??? question "Q25. Which MFA type uses a smartphone app?"

    Virtual MFA device — Google Authenticator or Authy generates
    TOTP = Time-based One-Time Password (6-digit code, changes every 30s).

??? question "Q26. Developer needs to make API calls from laptop. What credentials?"

    Access keys — Access Key ID (like username) +
    Secret Access Key (like password, shown ONCE at creation).

    CLI = Command Line Interface  SDK = Software Development Kit
    API = Application Programming Interface

??? question "Q27. Best practice for access keys?"

    Never share. Never put in code. Never commit to Git.
    Use IAM roles instead when possible. Rotate every 90 days.
    Git = version control system (code repository).

??? question "Q28. All developers need S3 read access. Most efficient approach?"

    Create Developers IAM group, attach S3 read policy to group,
    add all developers to group. One policy update affects all.

??? question "Q29. Which is TRUE about IAM? A) $0.01/user/month  B) Regional service C) New users have no permissions  D) Use root daily"

    C — new IAM users have ZERO permissions by default.

??? question "Q30. EC2 app needs to read from DynamoDB. Correct approach?"

    Create IAM Role with DynamoDB read permissions, attach to EC2.
    DynamoDB = AWS's managed NoSQL database (serverless, ms performance).
    NoSQL = Not only SQL (flexible schema, key-value store).

??? question "Q31. Difference between authentication and authorization?"

    Authentication = verifying WHO you are (login/identity).
    Authorization = determining WHAT you can do (permissions).

??? question "Q32. Which is correct about IAM policies? A) Deny always overrides Allow  B) Allow overrides Deny C) They cancel each other  D) Users have Allow by default"

    A — DENY ALWAYS OVERRIDES ANY ALLOW. The golden IAM rule.

??? question "Q33. User in two groups: one allows S3, one denies S3. Can user access?"

    NO. Explicit Deny always wins. S3 access denied.

??? question "Q34. What is federated identity in IAM?"

    External identity providers (like Active Directory, Google) can
    assume IAM roles via SAML. No separate IAM users needed per person.
    SSO = Single Sign-On (log in once, access multiple systems).
    AD = Active Directory (Microsoft's user directory).

??? question "Q35. Which service provides SSO across multiple AWS accounts?"

    AWS IAM Identity Center (formerly AWS SSO).

??? question "Q36. Lost MFA device for root account?"

    Contact AWS Support to recover access. Can take DAYS.
    This is why storing root credentials safely is critical.

??? question "Q37. IMMEDIATELY after creating a new AWS account? A) Create 10 IAM users  B) Enable MFA on root C) Delete root  D) Create S3 buckets"

    B — Enable MFA on root IMMEDIATELY.

??? question "Q38. What is an access key composed of?"

    Access Key ID (starts with AKIA, 20 chars, like username) +
    Secret Access Key (40 chars random, like password, shown ONCE).
    If secret key lost: create new key pair, cannot retrieve old one.

??? question "Q39. Can you retrieve a Secret Access Key after creation?"

    NO. Only viewable once at creation. If lost, create new key pair.

??? question "Q40. Best IAM entity to grant third party temporary access?"

    IAM Role with cross-account trust policy.
    STS = Security Token Service (issues temporary credentials).
    They assume the role, get temp creds that expire automatically.

??? question "Q41. What is AWS Organizations?"

    Manage multiple AWS accounts centrally with consolidated billing,
    volume discounts, and Service Control Policies (SCPs).
    OU = Organizational Unit (folder for grouping accounts).

??? question "Q42. What are Service Control Policies (SCPs)?"

    IAM policies at organizational level setting MAXIMUM permission
    limits for accounts. SCPs can only RESTRICT, never GRANT permissions.

??? question "Q43. Who manages the hypervisor in EC2?"

    AWS. The virtualization layer is always AWS's responsibility.
    AWS uses Nitro hypervisor (like VMware ESXi but AWS's own).

??? question "Q44. IAM feature that enforces strong passwords?"

    IAM Password Policy — set minimum length, complexity, expiry,
    rotation period, password history (prevent reuse).

??? question "Q45. Which is customer's responsibility for RDS? A) Patching DB engine  B) Managing EC2 instance C) Configuring security group rules  D) Physical security"

    C — Customer configures security groups and network access for RDS.

??? question "Q46. Type of policy to grant EC2 permission to write to S3?"

    IAM Role with S3 write policy, attached to EC2 as instance profile.
    Instance Profile = container that passes IAM Role to EC2.

??? question "Q47. Can you attach multiple IAM policies to one user?"

    YES. All policies combined. Any DENY = final answer DENY.

??? question "Q48. Difference between IAM user and IAM role?"

    User = permanent identity for a specific person.
    Role = temporary identity assumed by services or users.

??? question "Q49. Which service logs all API calls in your AWS account?"

    AWS CloudTrail — WHO made what API call, when, from where.
    CloudTrail answers: WHO, WHAT, WHEN, WHERE for every action.

??? question "Q50. Who is responsible for enabling CloudTrail?"

    The CUSTOMER. AWS provides the service but YOU must enable it.
    AWS never monitors your account FOR you — you set it up.

DAY 2 COMPLETE
*Tomorrow: Day 3 — Core Compute Services*

## Day 3 — CORE COMPUTE SERVICES

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 3)

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

??? question "Q1. What is Amazon EC2?"

    Elastic Compute Cloud — virtual servers in the cloud.
    Like a VM on your VMware cluster but AWS owns the hardware.
    YOU manage: OS, apps, data, security groups.
    AWS manages: physical servers, hypervisor, network hardware.

??? question "Q2. EC2 family for in-memory databases like SAP HANA?"

    Memory Optimized (R5, X1 family).
    SAP HANA = SAP's enterprise database that keeps data in RAM.
    RAM is 1,000x faster than SSD — memory-optimized maximizes this.

??? question "Q3. EC2 family for machine learning with GPUs?"

    Accelerated Computing (P3, G4 family).
    GPU = Graphics Processing Unit: thousands of small cores for
    parallel math — perfect for ML/AI matrix operations.

??? question "Q4. Which EC2 option has no upfront commitment and highest hourly cost?"

    On-Demand Instances. Maximum flexibility, maximum per-hour price.
    Best for: testing, unknown workloads, short-term experiments.

??? question "Q5. Which EC2 option offers up to 90% discount but can be interrupted?"

    ```text
    Spot Instances. AWS needs capacity back → 2-min warning → terminated.
    GOOD: batch jobs, big data, CI/CD, rendering (can restart).
    BAD: production databases, real-time apps (cannot interrupt).
    ```

??? question "Q6. When would you NOT use Spot Instances?"

    Critical workloads that cannot be interrupted: databases, real-time
    apps. If Spot is terminated at 11 PM → production DOWN.

??? question "Q7. Best option for steady-state workload running 24/7 for 3 years?"

    Reserved Instances — 3-year commitment = up to 72% savings.
    3yr m5.xlarge: $5,046 On-Demand vs ~$1,413 Reserved = 72% off.

??? question "Q8. Difference between Standard and Convertible Reserved Instances?"

    Standard RI: biggest discount (72%), cannot change instance type.
    Convertible RI: smaller discount (~66%), CAN change instance family.

??? question "Q9. Company needs dedicated physical servers for software licensing."

    Dedicated Hosts. BYOL = Bring Your Own License.
    You see exact socket/core count for Oracle/Windows licensing.

??? question "Q10. Difference between Dedicated Hosts and Dedicated Instances?"

    Dedicated Host: you control and see the physical server.
    Dedicated Instance: dedicated hardware but AWS manages the host.

??? question "Q11. What is Auto Scaling?"

    Automatically adjusts EC2 instance count based on demand.
    Scale out (add instances) when demand rises.
    Scale in (remove instances) when demand drops.

    ```text
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  ASG: Min=2, Max=10, Desired=2           │
    │  CPU > 70%: launch more instances        │
    │  CPU < 30%: terminate some instances     │
    │  Always right-sized, never over-paying   │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

??? question "Q12. Difference between scaling out and scaling up?"

    Scale OUT (horizontal): add more instances. No downtime. Preferred.
    Scale UP (vertical): increase size of existing instance. Requires restart.

??? question "Q13. Which ELB operates at Layer 7 and supports HTTP/HTTPS routing?"

    ```bash
    Application Load Balancer (ALB).
    Layer 7 = Application layer. Can route by URL path, hostname, headers.
    Example: /api/* → Server Group A, /web/* → Server Group B
    ```

??? question "Q14. Which ELB for ultra-low latency TCP/UDP traffic?"

    Network Load Balancer (NLB).
    Layer 4 = Transport layer. Handles millions of requests/second.
    Use for: gaming (UDP), financial trading (TCP), IoT.

??? question "Q15. What is AWS Lambda?"

    Serverless compute — run code without managing servers.
    Event-driven: triggers from S3, API Gateway, SQS, CloudWatch, etc.
    Pay ONLY when code runs. Free tier: 1M requests/month forever.

??? question "Q16. Maximum execution time for a Lambda function?"

    15 minutes (900 seconds). If > 15 min needed: use EC2 or ECS.

??? question "Q17. How are you charged for Lambda?"

    Number of requests + duration of execution.
    Pay $0 when not running. 3 AM with no requests = $0 cost.

??? question "Q18. What is Elastic Beanstalk?"

    PaaS — deploy your application, AWS handles everything else.
    Upload code → Beanstalk creates EC2, ELB, ASG, security groups.
    Supported: Java, .NET, PHP, Python, Ruby, Go, Node.js, Docker.

??? question "Q19. Compute service for Docker containers without managing servers?"

    AWS Fargate — serverless containers. No EC2 instances to manage.
    Docker = platform for building/running containers.
    Container = lightweight VM-like unit packaging app and dependencies.

??? question "Q20. Difference between ECS and EKS?"

    ECS = AWS's own container orchestration (simpler, AWS-native).
    EKS = Managed Kubernetes on AWS (for teams already using K8s).
    K8s = Kubernetes (industry standard container orchestration).

??? question "Q21. Startup wants to deploy web app without managing any servers?"

    Lambda (backend functions) + Elastic Beanstalk (full app deployment).
    Fargate also valid for containerized apps.
    REST API = Representational State Transfer API (web standard).

??? question "Q22. Which option commits to $/hr across EC2, Lambda, and Fargate?"

    Savings Plans — more flexible than Reserved Instances.
    Compute Savings Plans: apply across EC2, Lambda, Fargate.
    EC2 Instance Savings Plans: specific family/region, higher discount.

??? question "Q23. Batch processing jobs that can be interrupted. Best option?"

    Spot Instances — up to 90% savings, batch jobs can restart.

??? question "Q24. What happens to Spot Instance when AWS needs capacity back?"

    2-minute warning, then terminated. Unsaved data = LOST.
    Save checkpoints to S3 regularly for restartable jobs.

??? question "Q25. Which load balancer for third-party virtual firewall appliances?"

    Gateway Load Balancer (GWLB/GLB).
    Intercepts all traffic, routes through Palo Alto/Fortinet, returns.

??? question "Q26. Two services that handle traffic spikes automatically?"

    Auto Scaling (adjusts instance count) +
    Elastic Load Balancing (distributes traffic to healthy instances).

??? question "Q27. Best EC2 family for a web server with balanced requirements?"

    General Purpose (T3, M5 family).
    Memory trick: M5 = "Medium/balanced", C5 = "CPU", R5 = "RAM".

??? question "Q28. What is an EC2 instance profile?"

    Container that passes an IAM Role to an EC2 instance so it can
    make AWS API calls. App retrieves temp credentials automatically
    from http://169.254.169.254 (instance metadata service).

??? question "Q29. Company wants Java web app deployed without managing EC2?"

    AWS Elastic Beanstalk — supports Java (WAR files) and manages
    all underlying infrastructure automatically.
    JDK = Java Development Kit. WAR = Web Application Archive.

??? question "Q30. How does serverless differ from traditional compute?"

    Serverless: don't provision, manage, or pay for idle servers.
    Pay only when code actually runs. Lambda, Fargate, DynamoDB, S3.

??? question "Q31. Which is correct about Reserved Instances? A) Change types freely  B) 1 or 3 year commitment C) More expensive than On-Demand  D) One region only"

    B — RI requires 1 or 3 year commitment.

??? question "Q32. HPC simulations. Which EC2 family?"

    Compute Optimized (C5/C5n for CPU) or Accelerated (P3/P4 for GPU).
    HPC = High Performance Computing (scientific simulations).
    EFA = Elastic Fabric Adapter (low-latency HPC networking).

??? question "Q33. Relationship between ECS and Fargate?"

    Fargate is a LAUNCH TYPE for ECS (and EKS) that removes need
    to manage underlying EC2 infrastructure for containers.

??? question "Q34. Which service automatically replaces unhealthy EC2 instances?"

    Auto Scaling — health checks detect failure, terminate, replace.
    Self-healing infrastructure with no human intervention needed.

??? question "Q35. Media company processes video in 6-hour nightly batch jobs?"

    Spot Instances — batch jobs can tolerate interruption, 90% savings.

??? question "Q36. Benefit of multiple AZs with Application Load Balancer?"

    High availability — if one AZ fails, ELB routes to healthy AZs.
    ALB automatically discovers new instances added by Auto Scaling.

??? question "Q37. Best option for a 3-day experiment?"

    On-Demand — no commitment, pay hourly, stop when done.

??? question "Q38. Which is a valid Lambda trigger? A) S3 object upload  B) DynamoDB change  C) EC2 launch D) All of the above"

    D — Lambda can be triggered by hundreds of AWS events.

??? question "Q39. What type of scaling does a load balancer support?"

    Horizontal scaling (scale out) — distributing traffic across
    multiple instances instead of one large server.

??? question "Q40. Migrate VMware workloads to AWS. Which service?"

    VMware Cloud on AWS — same vCenter, NSX, vSAN tools in AWS.
    vMotion/HCX for live VM migration with no application changes.
    HCX = Hybrid Cloud Extension (VMware migration tool).

??? question "Q41. What does EC2 stand for?"

    Elastic Compute Cloud.
    Elastic = scales on demand. Compute = CPU+RAM. Cloud = AWS hosted.

??? question "Q42. Which is NOT a valid EC2 purchasing option? A) On-Demand  B) Spot  C) Perpetual License  D) Savings Plans"

    C — Perpetual License is not an EC2 pricing model.

??? question "Q43. How much can Reserved Instances save vs On-Demand?"

    Up to 72% with 3-year all-upfront commitment.

??? question "Q44. How much can Spot Instances save?"

    Up to 90% vs On-Demand pricing.

??? question "Q45. Compute Savings Plans vs EC2 Instance Savings Plans?"

    Compute SP: applies to EC2+Lambda+Fargate, any region (66% off).
    EC2 Instance SP: specific instance family in specific region (72% off).

??? question "Q46. Which service for a serverless REST API backend?"

    AWS Lambda with API Gateway — standard serverless API pattern.

??? question "Q47. Company wants to never over-provision compute. Which feature?"

    Auto Scaling — automatically adjusts capacity to match actual demand.
    Never paying for idle capacity. Never running short either.

??? question "Q48. What makes Fargate different from containers on EC2?"

    With Fargate you don't manage underlying EC2 instances at all.
    Just define container CPU/memory requirements, AWS handles the rest.

??? question "Q49. Which model for new app with completely unknown usage pattern?"

    On-Demand — no commitment. Observe actual usage for 3 months,
    then buy Reserved Instances or Savings Plans based on real data.

??? question "Q50. Financial company needs EC2 physically isolated from other customers?"

    Dedicated Hosts or Dedicated Instances — hardware not shared with
    other AWS customer accounts.
    Tenancy = who shares physical hardware.

DAY 3 COMPLETE
*Tomorrow: Day 4 — Storage Services*

## Day 4 — STORAGE SERVICES

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 4)

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

??? question "Q1. What type of storage is Amazon S3?"

    Object storage. Files stored as objects with key, data, and metadata.
    Unlimited storage. Objects up to 5 TB each. Globally unique bucket names.
    99.999999999% (11 nines) durability — stored across 3+ AZs automatically.

??? question "Q2. Maximum size of a single S3 object?"

    5 TB. Files > 5 GB must use Multipart Upload (uploads in parallel chunks).

??? question "Q3. S3 durability?"

    99.999999999% (11 nines). Store 10 billion objects, expect to lose 1/year.
    Automatically stores across minimum 3 AZs within the region.

??? question "Q4. Most cost-effective for data rarely accessed with 12-hour retrieval?"

    S3 Glacier Deep Archive. $0.00099/GB/month. 180-day minimum retention.

??? question "Q5. Which S3 class for unknown or changing access patterns?"

    S3 Intelligent-Tiering — auto-moves objects between tiers.
    Small monthly monitoring fee. Access object → moves back to frequent tier.

??? question "Q6. Minimum storage duration for S3 Glacier Deep Archive?"

    180 days. Delete before 180 days = still charged for 180.

??? question "Q7. Which S3 class stores data in ONLY ONE Availability Zone?"

    S3 One Zone-IA. Cheaper but data permanently LOST if that AZ fails.
    Use only for recreatable data (thumbnails, processed outputs).

??? question "Q8. What is an S3 bucket?"

    Container for storing objects. Names must be GLOBALLY UNIQUE across all AWS.
    URL: https://[bucket-name].s3.amazonaws.com/[key]

??? question "Q9. How to automatically move S3 objects between classes over time?"

    ```sql
    S3 Lifecycle Rules — define policies to transition or expire objects.
    Example: Standard → Standard-IA (day 30) → Glacier (day 90) → Delete (day 365)
    ```

??? question "Q10. Store compliance archives for 7 years, rarely accessed?"

    S3 Glacier Deep Archive. Most cost-effective. 12-hour retrieval fine for audit.

??? question "Q11. What is Amazon EBS?"

    Elastic Block Store — persistent block storage volumes for EC2.
    Like a virtual hard drive. Network-attached (not physically attached).
    Persists when EC2 stops. Must be in same AZ as EC2 instance.

??? question "Q12. How many EC2 instances can an EBS volume attach to?"

    ONE (standard volumes). io2 Multi-Attach allows up to 16 in same AZ.
    Like a SAN LUN — one host maps to one LUN (normally).

??? question "Q13. What happens to EBS data when EC2 terminates?"

    Root EBS volume: deleted by default.
    Additional volumes: persist by default.
    STOPPED (not terminated): all EBS data intact.

??? question "Q14. What is an EBS Snapshot?"

    Point-in-time backup stored in S3. Incremental (only changed blocks).
    Use to: restore in same AZ, create in different AZ, copy cross-region.

??? question "Q15. Difference between EBS and Instance Store?"

    EBS: persistent — survives stop/terminate (network-attached).
    Instance Store: temporary — LOST when stopped/terminated/fails.
    Instance Store: physically attached NVMe, much faster than EBS.

??? question "Q16. Which storage is fastest and physically attached?"

    Instance Store — directly attached NVMe SSD.
    NVMe = Non-Volatile Memory Express (fastest SSD interface).
    Speed order: Instance Store > EBS gp3 > EFS > S3

??? question "Q17. What is Amazon EFS?"

    Elastic File System — managed NFS that multiple EC2 instances can
    mount SIMULTANEOUSLY. Auto-scales. Linux only.
    For Windows shared files: use FSx for Windows File Server.

??? question "Q18. How does EFS differ from EBS?"

    EFS: shared across MULTIPLE instances and AZs. Auto-scales. NFS.
    EBS: attached to SINGLE instance. Manual sizing. Block storage.
    Use EFS: shared content management, web farm (100 servers same files).
    Use EBS: database volumes, OS boot drives.

??? question "Q19. Shared filesystem for 100 Linux EC2 instances simultaneously?"

    Amazon EFS — designed for shared access across many instances.

??? question "Q20. What is AWS Storage Gateway?"

    ```text
    Hybrid cloud storage — connects on-premises environments to AWS.
    Apps see local interface; data actually stored in S3/Glacier.
    Types: File Gateway (NFS/SMB→S3), Volume (iSCSI→S3), Tape (VTL→Glacier)
    ```

??? question "Q21. Which Storage Gateway type presents NFS/SMB interface to S3?"

    File Gateway — apps write to NFS/SMB share, data goes to S3.

??? question "Q22. Which Storage Gateway type presents iSCSI block storage?"

    Volume Gateway. iSCSI = Internet Small Computer Systems Interface
    (block storage over IP/TCP — like SAN but over Ethernet).

??? question "Q23. Which Storage Gateway type replaces tape libraries?"

    Tape Gateway — VTL (Virtual Tape Library) backed by S3/Glacier.
    Same backup software (NetBackup/TSM) unchanged. No physical tapes.

??? question "Q24. When to use Snowball Edge instead of internet transfer?"

    When data is too large (>10TB generally) or bandwidth is insufficient.
    1 PB over 100 Mbps internet = ~3 years. Snowball = weeks.

??? question "Q25. Capacity of AWS Snowmobile?"

    100 petabytes — 45-foot semi-truck. Armed guards, GPS, encrypted.
    AWS drives the truck to your DC. Plug in fiber, transfer data.

??? question "Q26. Best FSx for Windows SMB file shares?"

    Amazon FSx for Windows File Server — fully managed, AD integration,
    DFS namespaces, SMB protocol. AD = Active Directory.

??? question "Q27. Which FSx is relevant to NetApp ONTAP users?"

    Amazon FSx for NetApp ONTAP — same SVM, NFS/CIFS/iSCSI, SnapMirror.
    Migrate NetApp workloads to AWS with no application changes.

??? question "Q28. Which S3 feature protects against accidental deletion?"

    S3 Versioning — keeps multiple versions. Delete adds a delete marker
    (versions still exist). Remove marker = file restored.

??? question "Q29. Replicate S3 data to another region for DR?"

    S3 Cross-Region Replication (CRR). Requires versioning on both buckets.
    SRR = Same-Region Replication (for log aggregation, test sync).

??? question "Q30. What is an S3 presigned URL?"

    Time-limited URL granting temporary access to private S3 object.
    No AWS credentials needed. Configurable expiry (seconds to days).

??? question "Q31. Best EBS type for high-performance databases needing high IOPS?"

    io2 (Provisioned IOPS SSD) — up to 256,000 IOPS. For SAP HANA, Oracle, SQL Server.

??? question "Q32. Best EBS type for general purpose at lowest cost?"

    gp3 (General Purpose SSD) — 3,000 baseline IOPS, $0.08/GB.
    Replaced gp2 as default. IOPS independent of volume size.

??? question "Q33. Can EBS volumes be in a different AZ than EC2?"

    NO. Must be in same AZ. To move: take snapshot, create volume
    from snapshot in target AZ.

??? question "Q34. How to move EBS volume to a different AZ?"

    Snapshot the volume → create new volume from snapshot in target AZ
    → attach to EC2 in that AZ. Cannot directly "move" a volume.

??? question "Q35. Which S3 encryption uses AWS-managed keys requiring no customer work?"

    SSE-S3 — AWS manages keys entirely. AES-256. Free. No audit trail.

??? question "Q36. Which S3 encryption lets you use KMS for key control?"

    SSE-KMS — you control key policies, can audit all key usage via CloudTrail.
    Better for compliance requiring separation of duties.

??? question "Q37. S3 Standard-IA minimum storage duration?"

    30 days. Delete before 30 days = still charged for 30.

??? question "Q38. S3 Glacier Instant Retrieval minimum storage duration?"

    90 days. Millisecond retrieval (vs minutes-hours for Flexible).

??? question "Q39. Host a static website (HTML/CSS/JS) with no servers?"

    Amazon S3 static website hosting. Extremely cheap. No EC2 needed.
    Add CloudFront for HTTPS and custom domain.

??? question "Q40. Difference between S3 Standard and S3 Standard-IA?"

    Standard: $0.023/GB, no retrieval fee, for frequent daily access.
    Standard-IA: $0.0125/GB + retrieval fee, for monthly/occasional access.

??? question "Q41. Snow Family for migrating 50TB with no internet access?"

    Snowball Edge — up to 80TB usable, works offline.

??? question "Q42. Which storage auto-grows and shrinks based on usage?"

    Amazon EFS — no pre-provisioning. Start at 0 GB. Pay per GB used.

??? question "Q43. Can S3 bucket names be reused after deletion?"

    YES — name becomes globally available again. Security risk: old URLs
    could serve attacker's content if they register the name.

??? question "Q44. What is S3 Object Lock?"

    Prevents deletion/overwriting for set time — WORM compliance.
    Governance Mode: privileged users can override.
    Compliance Mode: NOBODY can delete (not even root!) during retention.
    WORM = Write Once Read Many. Use for SEC, FINRA, HIPAA compliance.

??? question "Q45. Extend on-premises NAS to AWS while maintaining local access?"

    AWS Storage Gateway File Gateway — local NFS/SMB interface backed by S3.
    NAS = Network Attached Storage (Isilon/PowerScale, NetApp, etc.)

??? question "Q46. What happens to Instance Store data if host fails?"

    Data is PERMANENTLY LOST. Instance Store has zero durability guarantees.
    Good for: temporary cache, scratch space, swap files.

??? question "Q47. Company has 2PB to migrate. Internet would take years?"

    AWS Snowmobile — 100PB semi-truck.
    2PB over Snowmobile: ~27 minutes of data transfer. Plus shipping weeks.

??? question "Q48. Best S3 class for frequently accessed data with highest performance?"

    S3 Standard. 99.99% availability, no retrieval fee, no minimum duration.

??? question "Q49. What is S3 Transfer Acceleration?"

    Uses CloudFront edge locations to speed up S3 uploads worldwide.
    Upload to mybucket.s3-accelerate.amazonaws.com instead of s3.amazonaws.com.

??? question "Q50. DR scenario with RTO of 12 hours, data accessed less than once/year?"

    S3 Glacier Deep Archive — 12-hour retrieval matches 12-hour RTO.
    Cheapest option. 180-day minimum retention.
    RTO = Recovery Time Objective (max acceptable downtime).
    RPO = Recovery Point Objective (max acceptable data loss).

DAY 4 COMPLETE
*Tomorrow: Day 5 — Databases*

## Day 5 — DATABASES

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 5)

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

??? question "Q1. What does RDS manage for you vs running DB on EC2?"

    RDS manages: OS patching, DB engine patching, backups, scaling, hardware.
    You manage: data, schema, queries, access, security groups.
    EC2 DB: YOU manage everything above plus OS and DB patching.

??? question "Q2. Which database engines does RDS support?"

    MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Amazon Aurora.

??? question "Q3. Difference between RDS Multi-AZ and Read Replicas?"

    ```sql
    Multi-AZ: SYNCHRONOUS replication → HIGH AVAILABILITY → automatic failover.
    Read Replica: ASYNCHRONOUS replication → PERFORMANCE → read scaling only.
    Multi-AZ standby: CANNOT be read from (failover only).
    Read Replica: CAN be read from. Can be in different region.
    EXAM TRAP: Read Replicas ≠ failover. Only Multi-AZ = failover.
    ```

??? question "Q4. Can you use Read Replica for automatic failover?"

    NO. Read Replicas are for read scaling only. Multi-AZ handles failover.
    Failover time for Multi-AZ: ~1-2 minutes (DNS updates automatically).

??? question "Q5. What is Amazon Aurora?"

    AWS cloud-native relational DB. MySQL + PostgreSQL compatible.
    5x faster than MySQL, 3x faster than PostgreSQL.
    6 copies across 3 AZs. Storage auto-grows in 10GB increments to 128TB.

??? question "Q6. How much faster is Aurora vs MySQL?"

    Up to 5x faster than standard MySQL.

??? question "Q7. What is Aurora Serverless?"

    Aurora that auto-starts, scales capacity, and pauses based on demand.
    Paused = $0 cost. Good for: dev/test, variable/unpredictable load.
    ACU = Aurora Capacity Unit (unit of compute for Serverless).

??? question "Q8. What is DynamoDB?"

    Fully managed NoSQL key-value + document database.
    Serverless. Single-digit millisecond performance at ANY scale.
    From 1 item to 10 petabytes — same ms latency.

??? question "Q9. What type of database is DynamoDB?"

    NoSQL — key-value and document store.
    NoSQL = Not only SQL. Flexible schema. No rigid table structure.

??? question "Q10. Which DB service requires no server management and scales automatically?"

    DynamoDB — fully serverless NoSQL. Also Aurora Serverless.

??? question "Q11. What is DynamoDB DAX?"

    DynamoDB Accelerator — in-memory cache for DynamoDB.
    Microsecond response times (vs ms for DynamoDB).
    Cache HIT: serve from DAX, no DynamoDB charge.
    Cache MISS: fetch from DynamoDB, cache it, serve.

??? question "Q12. DAX vs ElastiCache — when to use each?"

    DAX: ONLY for DynamoDB caching. Same API as DynamoDB.
    ElastiCache: for RDS, MySQL, or any other general caching needs.

??? question "Q13. What is Amazon ElastiCache?"

    Managed in-memory caching (Redis or Memcached).
    Sub-millisecond latency. Reduces database load for repeated queries.

??? question "Q14. What is Amazon Redshift?"

    Data warehouse for analytics. OLAP workloads. Columnar storage.
    Petabyte-scale. Use for BI and complex analytical queries.
    NOT for transactional workloads (use RDS/DynamoDB for OLTP).

??? question "Q15. Difference between OLTP and OLAP?"

    OLTP: many small fast transactions (INSERT/UPDATE). Use RDS/DynamoDB.
         Example: ATM, e-commerce orders, trading transactions.
    OLAP: complex queries on large historical datasets. Use Redshift.
         Example: revenue by region, risk analysis, regulatory reporting.

??? question "Q16. Which database for MongoDB workloads?"

    Amazon DocumentDB — MongoDB-compatible managed document database.

??? question "Q17. What is Amazon Neptune?"

    Graph database. Data stored as nodes and edges.
    Use for: social networks, fraud detection, knowledge graphs.
    Graph queries are 100x faster than relational JOINs at scale.

??? question "Q18. Which DB for immutable cryptographically verifiable transactions?"

    ```text
    Amazon QLDB — Quantum Ledger Database.
    Hash chain: change old record → hash chain breaks → tampering detected.
    Use for: banking ledgers, supply chain, insurance, financial compliance.
    ```

??? question "Q19. IoT sensors sending data every second. Which DB?"

    Amazon Timestream — purpose-built time-series database.
    Auto-tiering: recent data hot, older data cold. Built-in time functions.

??? question "Q20. What is AWS DMS?"

    Database Migration Service — migrate DBs to AWS with minimal downtime.
    Full Load (copy existing) + CDC (capture ongoing changes) = near-zero downtime.
    CDC = Change Data Capture.

??? question "Q21. What is a homogeneous database migration?"

    Same engine: Oracle on-prem → Oracle on RDS.
    DMS only. No schema conversion needed.

??? question "Q22. What is a heterogeneous database migration?"

    Different engines: Oracle → Aurora PostgreSQL.
    Use AWS Schema Conversion Tool (SCT) first, then DMS.

??? question "Q23. Which service assists with schema conversion?"

    AWS Schema Conversion Tool (SCT) — converts schema and SQL code
    between database engines. Free desktop application.

??? question "Q24. Company wants max read performance for RDS MySQL?"

    Add Read Replicas — distribute read queries across multiple replicas.
    App: reads to replica endpoints, writes to primary endpoint only.

??? question "Q25. What happens during RDS Multi-AZ failover?"

    AWS automatically switches DNS endpoint to the standby (~1-2 min).
    Zero data loss (synchronous replication). App must handle reconnect.

??? question "Q26. Which DB natively replicates across multiple AWS regions?"

    DynamoDB Global Tables — multi-region, multi-active replication.
    Write anywhere, replicated to all regions in <1 second.

??? question "Q27. Aurora storage auto-scaling increment?"

    10GB — grows automatically in 10GB increments up to 128TB. No downtime.

??? question "Q28. Gaming leaderboard with millions of concurrent users?"

    DynamoDB with DAX — serverless, any scale, microsecond latency.

??? question "Q29. ElastiCache engine with persistence and pub/sub?"

    Redis — more feature-rich. Sorted sets (perfect for leaderboards),
    persistence, pub/sub, replication, transactions.

??? question "Q30. ElastiCache for simple high-throughput caching?"

    Memcached — simpler, multi-threaded, no persistence. Pure caching.

??? question "Q31. Run SQL queries on S3 data without loading into a database?"

    YES — Amazon Athena. Serverless. $5/TB scanned. Query S3 directly.

??? question "Q32. Company needs SQL queries on S3 data lake?"

    Amazon Athena — define table in Glue Catalog, query S3 with SQL.
    Use Parquet format: columnar = scan less data = cheaper + faster.

??? question "Q33. Difference between RDS and database on EC2?"

    RDS managed: AWS handles OS, DB patching, backups, HA, scaling.
    EC2 DB: YOU handle everything. More control, much more work.
    Use EC2 when: unsupported engine, need OS access, special config.

??? question "Q34. Which scenario requires database on EC2 rather than RDS?"

    Unsupported engine (IBM DB2, Sybase), OS-level access needed,
    Oracle RAC clustering, specific legacy version not in RDS.

??? question "Q35. What is Aurora Global Database?"

    Single Aurora database spanning multiple regions. Sub-second replication.
    RPO < 1 second, RTO < 1 minute. Up to 5 secondary regions.

??? question "Q36. How many Aurora Read Replicas can you have?"

    Up to 15 read replicas. NO replication lag (shared distributed storage).
    Standard RDS: up to 5 replicas (with lag).

??? question "Q37. Which DB for content management storing JSON documents?"

    Amazon DocumentDB — MongoDB-compatible. JSON documents stored naturally.
    No complex JOINs needed for nested document data.

??? question "Q38. Financial company needs unalterable transaction history?"

    Amazon QLDB — immutable ledger, cryptographic hash chain.
    Prove records were NEVER altered since creation.

??? question "Q39. What makes Redshift different from RDS for analytics?"

    Redshift: COLUMNAR storage — only reads columns needed for query.
    RDS: ROW storage — must read entire row even if only 2 columns needed.
    For analytics: columnar = 10-100x faster and cheaper.

??? question "Q40. Cache most frequently run RDS queries?"

    Amazon ElastiCache — cache query results, reduce DB load.
    TTL = Time to Live (how long to keep data in cache before refreshing).

??? question "Q41. Primary key structure in DynamoDB?"

    Partition key (required) + optional sort key = composite primary key.
    GSI = Global Secondary Index (query on non-key attributes).
    LSI = Local Secondary Index (alternative sort key).

??? question "Q42. E-commerce site needing fast scalable product catalog?"

    DynamoDB — flexible schema (different attributes per product),
    single-digit ms latency, auto-scales for Black Friday traffic.

??? question "Q43. DynamoDB consistency types?"

    Eventually consistent reads (default, cheaper).
    Strongly consistent reads (request option, 2x cost, no lag).
    Use strong consistency: financial balances, inventory counts.

??? question "Q44. RDS feature for compliance by maintaining automated backups?"

    Automated backups — daily snapshot + transaction logs every 5 min.
    PITR = Point-In-Time Recovery — restore to any 5-minute window.
    Retention: 1-35 days (you configure).

??? question "Q45. RDS automated backup retention period?"

    1 to 35 days. Default varies by engine.
    Manual snapshots: kept UNTIL YOU DELETE THEM (no expiry).

??? question "Q46. SQL queries on S3 data without servers?"

    Amazon Athena — serverless, no cluster to manage, pay per TB scanned.

??? question "Q47. Social network needing to find connections between users?"

    Graph database — Amazon Neptune. Nodes=people, Edges=connections.
    100x faster than relational JOINs for connected data at scale.

??? question "Q48. What is Amazon Redshift Serverless?"

    Redshift that auto-provisions and scales capacity.
    Pay per RPU-second. Good for sporadic analytics workloads.
    RPU = Redshift Processing Unit.

??? question "Q49. Purpose of RDS parameter group?"

    Container for DB engine configuration values.
    Like my.cnf for MySQL or postgresql.conf. Managed by AWS in RDS.
    Static parameters: require reboot. Dynamic: applied immediately.

??? question "Q50. Which is correct about DynamoDB? A) Must manage servers  B) Supports SQL natively C) Single-digit ms latency  D) Key-value only"

    C — Single-digit millisecond performance at ANY scale.
    A is wrong: serverless. B: uses its own API (PartiQL for SQL-like).
    D: key-value AND document, with GSI for rich queries.

DAY 5 COMPLETE
*Tomorrow: Day 6 — Networking & Content Delivery*

## Day 6 — NETWORKING & CONTENT DELIVERY

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 6)

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

??? question "Q1. What is a VPC?"

    Virtual Private Cloud — your logically isolated private network in AWS.
    You define IP range (CIDR), subnets, routes, gateways, security rules.
    Your own isolated network in the cloud.
    CIDR: 10.0.0.0/16 = first 16 bits fixed = 65,536 possible IPs.

??? question "Q2. Difference between public and private subnet?"

    Public: has route to Internet Gateway (0.0.0.0/0 → IGW).
    Internet can reach resources. Use for: web servers, load balancers.
    Private: no direct internet route. Internet cannot reach resources.
    Use for: databases, application servers.

??? question "Q3. What is an Internet Gateway?"

    VPC component allowing resources to communicate with internet.
    Bidirectional. Horizontally scaled, redundant, HA. FREE to attach.
    ONE IGW per VPC. Performs NAT for public IPs.

??? question "Q4. What is a NAT Gateway?"

    Allows private subnet instances to initiate OUTBOUND internet connections.
    Internet CANNOT initiate connection back in (one-way only).
    Managed service. Must be placed in PUBLIC subnet.
    Use for: EC2 patching, external API calls from private instances.

??? question "Q5. Where must a NAT Gateway be placed?"

    In a PUBLIC subnet. It needs internet access (via IGW) itself to forward traffic.
    NAT in private subnet = broken. Place one in EACH AZ for HA.

??? question "Q6. What is a Security Group?"

    Virtual firewall at INSTANCE level. Stateful. ALLOW rules only.
    All rules evaluated simultaneously (no order). Default: deny all inbound.
    Applied to: EC2, RDS, ELB, Lambda (in VPC), ElastiCache.

??? question "Q7. What does "stateful" mean for Security Groups?"

    Return traffic automatically allowed. If inbound port 443 allowed,
    response traffic outbound is automatically permitted.
    Don't need outbound rule for the response. Remembers connections.

??? question "Q8. What is a Network ACL?"

    Firewall at SUBNET level. Stateless. ALLOW + DENY rules.
    Rules evaluated by number order (lowest first, first match wins).
    Applies to ALL resources in the subnet automatically.

??? question "Q9. What does "stateless" mean for NACLs?"

    Must explicitly allow BOTH inbound AND outbound traffic.
    Response traffic NOT automatically allowed. Must add outbound rules
    for ephemeral ports (1024-65535) to allow responses back out.

??? question "Q10. Can NACLs have Deny rules?"

    YES — unlike Security Groups, NACLs support explicit Deny rules.
    Use to: block specific IP address from accessing your VPC.

??? question "Q11. Security Groups operate at which level?"

    Instance level — EC2, RDS, Lambda (in VPC), ELB, ElastiCache, etc.

??? question "Q12. NACLs operate at which level?"

    Subnet level — applies to ALL resources within the subnet.
    One NACL per subnet. One NACL can cover multiple subnets.

??? question "Q13. Company wants to block a specific IP from accessing VPC?"

    Network ACL — add explicit DENY rule for that IP.
    Security Groups cannot do Deny rules, only NACLs can.

??? question "Q14. What is VPC Peering?"

    Direct networking connection between two VPCs for private communication.
    Works across accounts and regions. No overlapping IP ranges allowed.
    NOT transitive: A↔B + B↔C does NOT give A↔C access.

??? question "Q15. Is VPC Peering transitive?"

    NO. Each pair needs a direct peering connection.
    10 VPCs = 45 peering connections needed = complex mesh. Use TGW instead.

??? question "Q16. What problem does Transit Gateway solve?"

    ```text
    Hub-and-spoke model connecting all VPCs and on-premises networks.
    Transitive routing: A → TGW → C without direct A↔C peering.
    50 VPCs + DX/VPN = just 51 TGW attachments instead of 1,225 peerings.
    ```

??? question "Q17. Difference between VPN Gateway and Direct Connect?"

    ```text
    VPN: encrypted over PUBLIC internet. Hours to set up. Cheap. Variable performance.
    Direct Connect: PRIVATE fiber. Weeks to set up. Expensive. Consistent low latency.
    EXAM: "consistent performance" → DX. "quick/cheap" → VPN.
    ```

??? question "Q18. What is Amazon CloudFront?"

    CDN (Content Delivery Network) — caches content at 400+ edge locations.
    Also: DDoS protection (Shield), HTTPS/TLS termination, geo-restriction.
    Reduces latency globally. HTTP/HTTPS only.

??? question "Q19. What is Amazon Route 53?"

    Managed DNS service. Also: domain registration, health checks, traffic routing.
    Name: DNS runs on port 53.
    DNS = translates domain names (example.com) to IP addresses.

??? question "Q20. Which Route 53 policy splits 10% traffic to new app version?"

    Weighted routing — assign weights (10% new, 90% existing).
    Use for: A/B testing, blue/green deployments, canary releases.

??? question "Q21. Which Route 53 policy routes to lowest latency region?"

    Latency-based routing — routes to region with lowest measured latency.
    Based on actual network latency, not geographic distance.

??? question "Q22. Which Route 53 policy routes by user's physical location?"

    Geolocation routing — routes based on user's geographic location.
    Use for: data compliance, content localization, country restrictions.

??? question "Q23. Difference between CloudFront and Global Accelerator?"

    ```text
    CloudFront: CACHES content at edge. HTTP/HTTPS only. CDN.
    Global Accelerator: ROUTES traffic over AWS private network. TCP/UDP.
                        No caching. Provides 2 static anycast IPs.
    EXAM: "cache images globally" → CF. "2 static IPs whitelist" → GA.
    ```

??? question "Q24. What is Amazon API Gateway?"

    Create, publish, manage, and secure APIs at any scale.
    Works with Lambda for serverless APIs. Handles: auth, throttling, caching.
    JWT = JSON Web Token (secure authentication token).

??? question "Q25. Company in US wants low latency for Asian users?"

    Amazon CloudFront — caches content at edge locations near Asian users.
    Tokyo, Singapore, Sydney, Mumbai, Seoul, Hong Kong — all have edge locations.

??? question "Q26. What does Route 53 Failover routing do?"

    Routes to primary when healthy. Automatically switches to secondary when
    primary fails health checks. Active-passive disaster recovery.

??? question "Q27. Which is NOT a valid Route 53 routing policy? A) Simple  B) Weighted  C) Geolocation  D) Alphabetical"

    D. Valid: Simple, Weighted, Latency, Failover, Geolocation,
    Geoproximity, Multivalue, IP-based.

??? question "Q28. What is an Elastic IP address?"

    Static public IPv4 address. Persists even when EC2 stops.
    Reassign to new instance instantly. FREE when associated with running EC2.
    CHARGED ($0.005/hr) when not associated or instance stopped.

??? question "Q29. Two main firewall options and their levels?"

    Security Groups (instance level, stateful, allow only) +
    Network ACLs (subnet level, stateless, allow AND deny).
    Two layers of defense in VPC architecture.

??? question "Q30. Developer wants to connect on-premises to AWS securely and quickly?"

    Site-to-Site VPN using VPN Gateway — hours to set up, encrypted.
    CGW = Customer Gateway (your VPN device).
    VGW = Virtual Private Gateway (AWS side).

??? question "Q31. Financial company needs consistent low-latency connectivity to AWS?"

    AWS Direct Connect — dedicated private fiber, consistent performance.
    1 Gbps, 10 Gbps, 100 Gbps options. Through colocation providers (Equinix).

??? question "Q32. What is the default VPC?"

    Auto-created in each region on new account. Pre-configured with
    IGW, public subnets (one per AZ), main route table (internet access).
    CIDR: 172.31.0.0/16. Less secure for production — use custom VPCs.

??? question "Q33. Which service provides automatic DDoS protection for CloudFront?"

    AWS Shield Standard — free, automatic, all customers, Layers 3 & 4.
    Shield Advanced: $3,000+/month, Layer 7, 24/7 DRT team, cost protection.
    DRT = DDoS Response Team.

??? question "Q34. Restrict S3 bucket to only your VPC?"

    VPC Endpoint (Gateway Endpoint for S3) — private access, no internet.
    Traffic stays on AWS network. FREE gateway endpoint.

??? question "Q35. What is a VPC Endpoint?"

    Private connection between VPC and AWS services. No internet, NAT, or DX needed.
    Gateway Endpoint: S3 and DynamoDB only. FREE. Added to route table.
    Interface Endpoint: 100s of AWS services. Creates ENI with private IP. Charged.

??? question "Q36. Which VPC Endpoint type works like an ENI?"

    Interface Endpoint — creates ENI in your subnet with private IP.
    ENI = Elastic Network Interface (virtual network card).
    Traffic to AWS service goes to private IP instead of public endpoint.

??? question "Q37. Which VPC Endpoint type for S3 and DynamoDB?"

    Gateway Endpoint — free, added to route table, S3 and DynamoDB ONLY.

??? question "Q38. How many route tables can a subnet be associated with?"

    ONE at a time. Each subnet has exactly one route table.
    One route table can cover MANY subnets.

??? question "Q39. What wins in a route table (most specific or least)?"

    Most specific (longest prefix) wins.
    /32 > /24 > /16 > /0. Example: traffic to 10.0.1.50 → /32 wins over /0.

??? question "Q40. Company needs global app with two static IPs for whitelisting?"

    AWS Global Accelerator — provides 2 static anycast IPs that never change.
    Anycast = same IP announced from multiple locations. Traffic → nearest.

??? question "Q41. Difference between Route 53 Simple and Multivalue routing?"

    Simple: returns ONE record (no health checks).
    Multivalue: returns up to 8 HEALTHY records (requires health checks).
    Multivalue is NOT a full load balancer replacement — use ELB for that.

??? question "Q42. What component connects EC2 to the network?"

    ENI — Elastic Network Interface (virtual NIC).
    Each instance has at least one ENI with private IP.
    Can attach multiple ENIs to one EC2 (multiple network interfaces).
    NIC = Network Interface Card (physical equivalent).

??? question "Q43. What is VPC Flow Logs?"

    Captures IP traffic metadata (source/dest IPs, ports, protocol, allow/reject).
    Does NOT capture actual packet content.
    Destinations: CloudWatch Logs, S3 bucket, Kinesis Firehose.

??? question "Q44. Which service filters malicious web traffic?"

    AWS WAF (Web Application Firewall) — protects at Layer 7.
    Blocks: SQL injection, XSS, rate limiting.
    Works with: CloudFront, ALB, API Gateway.
    XSS = Cross-Site Scripting. SQL injection = attacker injects SQL code.

??? question "Q45. Route 53 monitors endpoint health. What feature?"

    Route 53 Health Checks — monitors endpoints and removes unhealthy
    ones from DNS responses. Checks every 10 or 30 seconds.

??? question "Q46. What does CloudFront's "origin" refer to?"

    ```text
    The source of original content — S3 bucket, EC2, ALB, or any HTTP server.
    Multiple origins per distribution with path-based routing.
    /images/* → S3, /api/* → ALB, /* → default.
    ```

??? question "Q47. Accelerate file uploads from worldwide users to S3?"

    ```text
    S3 Transfer Acceleration — uses CloudFront edge locations.
    Upload to mybucket.s3-accelerate.amazonaws.com.
    Users in Brazil upload → nearest edge → AWS backbone → S3 in US.
    ```

??? question "Q48. Manage routing between 50 VPCs across multiple accounts?"

    AWS Transit Gateway — hub-and-spoke, 50 attachments vs 1,225 peerings.
    Control which VPCs talk to each other via TGW route tables.

??? question "Q49. Key difference between Security Group rules and NACL evaluation?"

    Security Groups: ALL rules evaluated simultaneously, then decision made.
    NACLs: rules evaluated in NUMBER ORDER, first match STOPS evaluation.

??? question "Q50. Technical difference between CloudFront and Global Accelerator?"

    CloudFront: CACHES content at edge. HTTP/HTTPS. CDN.
              Best for static content, website performance.
    Global Accelerator: ROUTES traffic over AWS private network. ANY TCP/UDP.
                       No caching. Best for gaming, IoT, non-HTTP, static IPs.

DAY 6 COMPLETE
*Tomorrow: Day 7 — Security Services*

## Day 7 — SECURITY SERVICES

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 7)

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

??? question "Q1. What does AWS KMS do?"

    Creates and manages encryption keys (CMKs) used to encrypt data.
    Keys stored securely in HSM hardware. Access controlled by IAM.
    Every use logged in CloudTrail. Auto-rotation annually.
    HSM = Hardware Security Module (physical hardware for crypto keys).

??? question "Q2. What does CloudTrail record?"

    Every API call in your AWS account — every action (console click,
    CLI command, SDK call). Records: WHO, WHAT, WHEN, WHERE (IP address).

??? question "Q3. Is CloudTrail enabled by default?"

    YES — 90-day event history free in console.
    For long-term: create Trail to deliver logs to S3 bucket.
    Management events: control plane (creating/deleting resources).
    Data events: S3 reads/writes (extra cost).

??? question "Q4. Difference between CloudTrail and CloudWatch?"

    CloudTrail: "WHO did WHAT?" — API audit log.
    CloudWatch: "HOW is it performing?" — metrics (CPU, latency, errors).
    EXAM: "audit log" = CloudTrail. "CPU alarm" = CloudWatch.

??? question "Q5. Difference between CloudTrail and AWS Config?"

    CloudTrail: WHO made API calls (activity).
    Config: WHAT resources looked like before/after (configuration history + compliance).
    Use both: Config = WHAT changed. CloudTrail = WHO changed it.

??? question "Q6. Who changed a security group last Tuesday?"

    AWS CloudTrail — records all API calls including SG modifications.
    Filter by: EventName=AuthorizeSecurityGroupIngress, date range.

??? question "Q7. Verify EC2 instances always used encrypted EBS volumes?"

    AWS Config — tracks configuration history and runs compliance rules.
    Rule: ec2-ebs-encryption-by-default.

??? question "Q8. What does Amazon GuardDuty do?"

    Intelligent threat detection using ML, anomaly detection, and threat intel.
    Detects: compromised credentials, cryptomining, port scanning, data exfiltration.
    Analyzes: CloudTrail, VPC Flow Logs, DNS logs. No agents needed.

??? question "Q9. Does GuardDuty require agents on EC2?"

    ```text
    NO. Fully managed. Reads logs that already exist.
    Enable → click "Enable" → monitoring starts. No software to install.
    ```

??? question "Q10. What does Amazon Inspector do?"

    Automated vulnerability assessment for EC2 and container images.
    Finds: unpatched CVEs, network exposure (open ports), software vulns.
    CVE = Common Vulnerabilities and Exposures (public database of security flaws).
    RCE = Remote Code Execution (attacker runs code on your server).

??? question "Q11. What does Amazon Macie do?"

    ML to discover and protect sensitive data (PII, credentials) in S3.
    Finds: SSNs, credit card numbers, AWS access keys, medical records.
    PII = Personally Identifiable Information.

??? question "Q12. What is AWS Security Hub?"

    Central security dashboard aggregating findings from multiple services.
    Combines: GuardDuty, Inspector, Macie, Config, IAM Analyzer, third-party.
    CSPM compliance checks. Multi-account support.
    CSPM = Cloud Security Posture Management.

??? question "Q13. Difference between Shield Standard and Advanced?"

    Standard: FREE, automatic, ALL customers, Layers 3 and 4.
    Advanced: $3,000+/month, Layer 7 app DDoS, 24/7 DRT team, cost protection.
    SYN flood = DDoS attack type (send many SYN packets without completing handshake).

??? question "Q14. What does AWS WAF protect against?"

    SQL injection, XSS, rate limiting, bot attacks at Layer 7.
    Works with: CloudFront, ALB, API Gateway.
    AWS Managed Rules: pre-built for common threats. Custom rules: you write.

??? question "Q15. Which services can AWS WAF protect?"

    CloudFront (edge), Application Load Balancer (regional), API Gateway.

??? question "Q16. What is AWS Secrets Manager?"

    Store, rotate, and manage secrets (DB passwords, API keys, tokens).
    AUTO-ROTATION built in for RDS, Redshift, DocumentDB.
    $0.40/secret/month. No credentials hardcoded in code.

??? question "Q17. Benefit of Secrets Manager over storing credentials in code?"

    Never hardcoded. Auto-rotation without code changes.
    Full audit trail. Access via IAM. Encrypted at rest (KMS).

??? question "Q18. Difference between Secrets Manager and Parameter Store?"

    Secrets Manager: built for secrets, auto-rotation, $0.40/secret/month.
    Parameter Store: config + secrets, FREE standard tier, no auto-rotation.
    Use SM: DB passwords with rotation needed.
    Use PS: app config values, feature flags, connection strings.

??? question "Q19. What does ACM provide?"

    Free SSL/TLS certificates for AWS services with automatic renewal.
    Never pay for cert, never worry about expiry.
    Works with: CloudFront, ALB, API Gateway.
    SSL/TLS = protocol for encrypting data in transit (HTTPS).

??? question "Q20. What is Amazon Cognito?"

    User authentication for web/mobile apps.
    User Pools: authentication (sign-up, sign-in, MFA, social login).
               Returns JWT tokens (not AWS credentials).
    Identity Pools: authorization (exchange JWT for temporary AWS credentials).
    OAuth = Open Authorization standard for social login.

??? question "Q21. What is AWS Artifact?"

    Portal providing access to AWS compliance reports and certifications.
    Download: SOC 1/2/3, PCI DSS, ISO 27001, FedRAMP, HIPAA BAA.
    FREE. No waiting. Download in minutes for auditors.

??? question "Q22. Company needs compliance reports proving AWS is PCI compliant?"

    AWS Artifact — download PCI DSS Attestation of Compliance directly.
    PCI DSS = Payment Card Industry Data Security Standard.

??? question "Q23. What does Trusted Advisor check?"

    Five categories:
    1. Cost Optimization (oversized instances)
    2. Performance (IOPS limits)
    3. Security (public S3 buckets, open ports)
    4. Fault Tolerance (no Multi-AZ on RDS)
    5. Service Limits/Quotas (approaching limits)

??? question "Q24. Which Trusted Advisor checks are free?"

    7 core checks including S3 bucket permissions, SG open ports,
    root MFA, IAM use, service limits.
    Full checks require Business or Enterprise support plan.

??? question "Q25. Which support plan gives access to ALL Trusted Advisor checks?"

    Business ($100+/month), Enterprise On-Ramp ($5,500+), or Enterprise ($15,000+).

??? question "Q26. Startup left S3 bucket publicly accessible. Which alerts them?"

    Trusted Advisor (security check) and AWS Config (rule).
    Also: S3 Block Public Access (account-level prevention setting).

??? question "Q27. How does GuardDuty detect threats?"

    ML behavior baseline + anomaly detection + threat intelligence feeds.
    Learns: "admin always logs in from New York at 9 AM"
    Detects: "admin login from Russia at 3 AM" → HIGH severity alert.

??? question "Q28. Which service monitors CPU and alerts when it exceeds 80%?"

    Amazon CloudWatch — create metric alarm on CPUUtilization.
    Alarm states: OK, ALARM, INSUFFICIENT_DATA.
    Memory metrics require CloudWatch Agent (not available by default).

??? question "Q29. What is a CloudWatch Alarm?"

    Notification triggered when metric crosses a threshold.
    Actions: SNS notification, Auto Scaling, EC2 action.
    SNS = Simple Notification Service (sends to email, SMS, etc.).

??? question "Q30. What is Amazon EventBridge?"

    ```text
    Serverless event bus connecting AWS services with automation.
    Event (EC2 stopped, S3 upload) → Rule → Target (Lambda, SNS, SSM).
    ```

??? question "Q31. Ensure all S3 buckets are encrypted. Which service?"

    AWS Config with rule: s3-bucket-server-side-encryption-enabled.
    Auto-remediation: detects non-compliant → automatically enables encryption.

??? question "Q32. Single view of security across all AWS accounts?"

    AWS Security Hub — aggregate all security findings into one dashboard.
    Security account as admin → all member accounts feed findings in.

??? question "Q33. What logs does GuardDuty analyze?"

    CloudTrail event logs + VPC Flow Logs + Route 53 DNS query logs.
    No additional setup needed — these logs already exist.

??? question "Q34. Difference between CloudWatch and CloudTrail for EC2?"

    CloudWatch: CPU, memory, network, disk performance (HOW running).
    CloudTrail: who started/stopped/modified instances (ACTIONS taken).

??? question "Q35. What is AWS Systems Manager?"

    Manage EC2 infrastructure at scale.
    Session Manager: browser-based shell, no SSH keys or open port 22.
    Run Command: execute scripts on 1000s of instances at once.
    Patch Manager: automate OS patching with maintenance windows.

??? question "Q36. Which CloudWatch metric requires agent (NOT available by default)?"

    Memory utilization — AWS cannot see inside guest OS without agent.
    Default metrics: CPU, Network, Disk I/O.
    Memory/disk utilization: require CloudWatch Agent installed on EC2.

??? question "Q37. Purpose of KMS key rotation?"

    Auto-rotates key material annually. Key ID stays same.
    Old data still decryptable (KMS keeps old versions).
    Limits exposure window if key is ever compromised.

??? question "Q38. Company wants to auto-rotate RDS passwords every 30 days?"

    AWS Secrets Manager — built-in RDS rotation, configurable schedule.
    Updates password in RDS and in Secrets Manager. App unchanged.

??? question "Q39. Difference between AWS managed keys and customer managed keys?"

    AWS managed: auto-created by service, FREE, cannot customize, no audit.
    Customer managed: you create, $1/month, customize policy, full CloudTrail audit.

??? question "Q40. Which service detects IAM credentials used from unusual location?"

    Amazon GuardDuty — ML detects anomalous credential usage.
    Login from Russia when user always logs in from New York → HIGH severity.

??? question "Q41. What does Macie specifically look for in S3?"

    PII (SSN, passport, driver's license), financial data (credit cards, bank accounts),
    credentials (AWS access keys, private keys, HTTP auth), medical records (PHI).

??? question "Q42. Compliance frameworks accessible via AWS Artifact?"

    SOC 1/2/3, PCI DSS, ISO 27001/27017/27018/9001, FedRAMP, GDPR, ITAR, HIPAA BAA.

??? question "Q43. Developer hardcoded RDS password in code. Recommended fix?"

    1. Rotate password immediately (it may be compromised via Git).
    2. Store in Secrets Manager.
    3. Update app to call Secrets Manager API at runtime.
    4. Enable auto-rotation every 90 days.

??? question "Q44. What is an AWS Config Rule?"

    Evaluates whether resources comply with your configuration policies.
    AWS managed: 300+ pre-built rules.
    Custom: Lambda function with your compliance logic.

??? question "Q45. Full history of changes to EC2 security group over past year?"

    AWS Config — configuration timeline showing before/after for every change.
    CloudTrail tells WHO changed it. Config tells WHAT changed.

??? question "Q46. What is Amazon Detective?"

    Security investigation tool. Visualizes findings from GuardDuty.
    Shows: IP relationships, API call patterns, connections between events.
    Reduces investigation from hours to minutes.

??? question "Q47. Difference between Cognito User Pool and Identity Pool?"

    User Pool: authentication (who are you?) → returns JWT tokens.
    Identity Pool: authorization (here are your AWS permissions) → temp AWS creds.

??? question "Q48. What is VPC Flow Logs?"

    Captures network traffic metadata. Does NOT capture packet content.
    Records: source IP, dest IP, ports, protocol, bytes, ACCEPT/REJECT.
    Send to: CloudWatch Logs, S3, Kinesis Firehose.

??? question "Q49. What is the AWS Security Token Service (STS)?"

    Issues temporary, limited-privilege credentials for IAM roles.
    Temp credentials: Access Key ID + Secret Key + Session Token + Expiration.
    Used by: EC2 instance roles, cross-account access, federation.

??? question "Q50. Company considering AWS migration needs compliance certs. Where?"

    ```text
    AWS Artifact — immediate access to all AWS compliance documentation.
    Log in → download → give to auditor. 5 minutes total. FREE.
    ```

DAY 7 COMPLETE
*Tomorrow: Day 8 — Monitoring, Management & Pricing*

## Day 8 — MONITORING, MANAGEMENT & PRICING

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 8)

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

??? question "Q1. What is AWS CloudFormation?"

    Infrastructure as Code — define AWS resources in JSON or YAML templates.
    Deploy as a "stack" — create, update, delete all resources together.
    Same template + deploy 10 times = same result every time.
    IaC = Infrastructure as Code (treat infra like software — versioned, repeatable).

??? question "Q2. What is a CloudFormation Stack?"

    ```sql
    Collection of AWS resources created, updated, deleted as a unit.
    Template → Stack. Delete stack → all resources deleted automatically.
    Prevents orphaned resources (forgotten EC2s, security groups, etc.).
    ```

??? question "Q3. Benefit of CloudFormation over manually creating resources?"

    Repeatability, consistency, version control, disaster recovery (redeploy template).
    Config drift = gradual deviation from intended configuration over time.
    CloudFormation Drift Detection finds resources changed outside CloudFormation.

??? question "Q4. Three fundamental AWS pricing principles?"

    1. Pay as you go (no upfront, variable costs).
    2. Save when you reserve (1-3 year commits = 72% off).
    3. Pay less as you use more (volume discounts).

??? question "Q5. Is data transfer INTO AWS charged?"

    NO — data transfer IN to AWS is ALWAYS FREE.
    Upload to S3, send to EC2, any inbound = FREE.

??? question "Q6. Is data transfer OUT of AWS charged?"

    ```text
    YES — outbound to internet ~$0.09/GB.
    S3 → CloudFront: FREE. CloudFront → users: cheaper than S3 direct.
    Cross-region: ~$0.02/GB. Same region/AZ via private IP: FREE.
    ```

??? question "Q7. What is the AWS Free Tier?"

    Always Free (permanent): Lambda 1M req/month, DynamoDB 25GB, etc.
    12-month Free: EC2 t2.micro 750 hrs, S3 5GB, RDS 750 hrs.
    Short Trials: Redshift 2 months, Lightsail 3 months.

??? question "Q8. How many Lambda requests in always-free tier?"

    1 million requests/month FOREVER + 400,000 GB-seconds compute/month.
    Most small apps run on Lambda completely free permanently.

??? question "Q9. What is AWS Cost Explorer?"

    Visualize and analyze historical spending. RI recommendations. Forecasting.
    View by service, tag, region, account. FREE to use.
    Direction: looking BACKWARD (and forecasting forward).

??? question "Q10. What is AWS Budgets?"

    Set spending/usage thresholds and receive alerts.
    Budget Actions: automatically apply IAM or SCP policies when exceeded.
    Direction: looking FORWARD (prevent overspend proactively).

??? question "Q11. Which tool provides most granular billing data?"

    AWS Cost and Usage Report (CUR) — hourly line-item detail.
    Delivered to S3. Query with Athena. Used for chargebacks/showbacks.
    Blended vs unblended cost. RI discounts applied per line item.

??? question "Q12. Which tool estimates costs BEFORE deploying?"

    ```text
    AWS Pricing Calculator at calculator.aws. No AWS account needed. FREE.
    Build estimate: add services → see monthly cost → share URL.
    ```

??? question "Q13. Which support plan has a dedicated TAM?"

    Enterprise Support ($15,000+/month) — dedicated TAM assigned to your account.
    Enterprise On-Ramp: pool of shared TAMs (not dedicated).

??? question "Q14. Which plan for 24/7 phone+chat with 1-hour prod-down response?"

    Business Support ($100+/month).
    Response times: General guidance 24hr, System impaired 12hr,
    Prod impaired 4hr, Prod DOWN 1 HOUR.

??? question "Q15. Startup needs AWS support but only $29/month budget?"

    Developer Support — email support during business hours.
    NOT for production workloads (12-hour business-hours response only).

??? question "Q16. What is AWS Organizations?"

    Central management of multiple AWS accounts.
    Consolidated billing (one invoice, volume discounts, RI sharing).
    Service Control Policies (SCPs) for account-level guardrails.

??? question "Q17. What is a Service Control Policy (SCP)?"

    Policy at organizational level setting MAXIMUM permission limits.
    SCPs can only RESTRICT, never GRANT permissions.
    Example: DENY all services except in us-east-1 and us-west-2.

??? question "Q18. Can an SCP grant permissions to a user?"

    NO. SCPs only restrict. Actual permissions still need IAM policies.
    Effective permissions = SCP (ceiling) AND IAM policies (grant).
    Must satisfy BOTH to get access.

??? question "Q19. Benefit of consolidated billing in Organizations?"

    One bill for all accounts. Volume discounts combined across accounts.
    RI sharing: unused RI in Account A auto-applies to Account B.
    Save money by pooling usage for better discount tiers.

??? question "Q20. What is AWS Control Tower?"

    Sets up and governs a secure multi-account environment.
    Landing Zone = pre-configured accounts (Management, Log Archive, Security).
    Guardrails = SCPs + Config rules (Mandatory, Recommended, Elective).

??? question "Q21. Difference between CloudFormation and CDK?"

    CloudFormation: templates in JSON or YAML (declarative).
    CDK: define infra in Python/Java/TypeScript → generates CloudFormation.
    CDK benefits: loops, functions, type checking, IDE autocomplete.

??? question "Q22. What is Systems Manager Session Manager?"

    Browser-based shell access to EC2 with NO SSH keys, NO port 22, NO bastion.
    All sessions logged in CloudTrail. Works for private instances via SSM agent.

??? question "Q23. What is Systems Manager Run Command?"

    ```text
    Execute scripts/commands on many EC2 instances simultaneously.
    "Patch 500 web servers NOW" → one Run Command → done in minutes.
    Results per server. Rate control (e.g., 50 servers at a time).
    ```

??? question "Q24. What is Systems Manager Patch Manager?"

    Automate OS patching. Define patch baseline. Schedule maintenance windows.
    Auto-patches during window. Reports compliance status per instance.

??? question "Q25. What is AWS Service Catalog?"

    Create approved IT service catalog. Teams self-serve compliant resources.
    Admin creates product (approved EC2 with correct tags/encryption).
    Developer selects from catalog → compliance automatic.

??? question "Q26. Which tool for understanding and forecasting your AWS bill?"

    AWS Cost Explorer — charts of historical spending + cost forecast.

??? question "Q27. Company wants alert when monthly AWS bill exceeds $1,000?"

    AWS Budgets — set $1,000 cost budget with alert at 80% and 100%.

??? question "Q28. Difference between AWS Budgets and Cost Explorer?"

    Budgets: proactive alerts and actions (FORWARD looking, prevent overspend).
    Cost Explorer: analytical charts and history (BACKWARD looking, understand spend).

??? question "Q29. Which EC2 type in 12-month free tier?"

    t2.micro (or t3.micro). 750 hours/month.
    730 hours in a month — 1 instance running 24/7 = within free tier.
    2 instances running = 1,460 hours, charged for extra 710.

??? question "Q30. What happens to free tier limits after 12 months?"

    12-month offers expire — standard rates apply.
    Always-free (Lambda, DynamoDB) continue forever.
    Best practice: set $1 Budget alert — fires when free tier expires.

??? question "Q31. Which plan for 15-minute critical response?"

    Enterprise Support ($15,000+/month) — 15-minute response for business-critical down.
    Enterprise On-Ramp: 30 minutes. Business: 1 hour.

??? question "Q32. What is a CloudFormation ChangeSet?"

    ```sql
    Preview of changes BEFORE executing update. Shows: + Add, ~ Modify, - Delete.
    Prevents accidental deletions (like production database).
    Review ChangeSet → fix issues → execute safely.
    ```

??? question "Q33. What is CloudFormation Drift Detection?"

    Detects when actual configuration differs from CloudFormation expected state.
    "Who manually changed that security group in the console?"
    Drift = difference between actual state and IaC template.

??? question "Q34. Maximum response time for Business Support production system down?"

    1 HOUR for production system completely inaccessible.
    Response time = when engineer contacts you (not fix time).

??? question "Q35. Developer plan customer has critical production outage response time?"

    Developer plan only supports email during business hours.
    Saturday afternoon outage → response may come Monday. Very bad for production.
    Developer plan = development only (not for production).

??? question "Q36. What is AWS Compute Optimizer?"

    Analyzes CloudWatch metrics → recommends right-sized resources.
    "This m5.4xlarge runs at 2% CPU — downsize to m5.xlarge, save $280/month."
    Analyzes: EC2 instances, EBS volumes, Lambda functions.

??? question "Q37. Which provides recommendations across Cost, Performance, Security, FT, Limits?"

    AWS Trusted Advisor.

??? question "Q38. Difference between Trusted Advisor and Cost Explorer?"

    Trusted Advisor: "Here is what you should DO" (actionable recommendations).
    Cost Explorer: "Here is how you SPENT money" (analytical visibility).

??? question "Q39. Which CloudFormation resource type for nested stack?"

    AWS::CloudFormation::Stack — modular template composition.
    Benefits: reuse templates, teams own their templates, easier to manage large stacks.

??? question "Q40. What is the AWS Well-Architected Framework?"

    Best practices across 6 pillars.
    Memory: "Only Stupid Rabbits Play Cost-free Sustainability"
    Operational Excellence, Security, Reliability, Performance, Cost, Sustainability.

??? question "Q41. 6th pillar of Well-Architected Framework added in 2021?"

    Sustainability — minimize environmental impact.
    Right-size resources, use managed services, maximize utilization.
    AWS: 100% renewable energy (achieved 2023), water positive 2030, net zero 2040.

??? question "Q42. Give partner access without creating IAM users?"

    ```text
    IAM Roles with cross-account trust policy.
    Partner assumes role → gets temporary credentials → accesses specific resources.
    Role can be revoked instantly. No permanent credentials shared.
    ```

??? question "Q43. Custom reports on spending by department, project, and time?"

    AWS Cost and Usage Report (CUR) + Amazon Athena.
    CUR delivers to S3 → Athena SQL queries for custom analysis.

??? question "Q44. What are AWS Cost Allocation Tags?"

    Key-value pairs on resources that appear in billing reports.
    Example: Project=WebApp, Environment=Prod, Team=Backend, Owner=alice.
    Must activate tags in billing console for them to appear in reports.

??? question "Q45. What is the AWS TCO Calculator?"

    Compare total cost of on-premises vs AWS cloud.
    On-premises hidden costs: power, cooling, space, staff, hardware refresh.
    TCO = Total Cost of Ownership (ALL costs over time).

??? question "Q46. How do Reserved Instances work with consolidated billing?"

    RI discounts shared across all accounts in Organizations.
    Unused RI in Account A auto-applies to Account B's matching instance.
    Can disable RI sharing per account if needed.

??? question "Q47. What is Amazon Managed Grafana?"

    Managed Grafana for visualizing CloudWatch, Prometheus, X-Ray data.
    Build operational dashboards. AWS manages server, you manage dashboards.
    Prometheus = open-source monitoring time-series database.

??? question "Q48. Which monitors costs and can automatically restrict usage when exceeded?"

    AWS Budgets Actions — applies IAM policies or SCPs when budget exceeded.
    Example: deny ec2:RunInstances for dev group when budget hit 90%.

??? question "Q49. AWS Free Tier for S3?"

    5GB Standard storage + 20,000 GET requests + 2,000 PUT requests per month.
    Valid for 12 months from account creation.

??? question "Q50. Minimum plan for 24/7 phone and chat support?"

    Business Support ($100+/month). EXAM ANSWER: always "Business Support."
    Developer = email business hours only. Basic = no engineer contact.

DAY 8 COMPLETE
*Tomorrow: Day 9 — Cloud Migration & Architecture*

## Day 9 — CLOUD MIGRATION & ARCHITECTURE

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 9)

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

??? question "Q1. What are the 6 R's of migration?"

    Rehost, Replatform, Repurchase, Refactor, Retire, Retain.
    Memory: "Real People Really Refuse Refactoring Regularly"

??? question "Q2. Which migration strategy is "lift and shift"?"

    Rehost — move to EC2 exactly as-is. No code or architecture changes.
    Tool: AWS Application Migration Service (MGN). Continuous replication.
    Fastest to execute. Lowest effort. Least cloud benefit long-term.

??? question "Q3. Moving MySQL from EC2 to RDS with minimal changes. Which R?"

    ```bash
    Replatform — move to managed service with minor optimization.
    App code: unchanged. Operations: better (AWS manages patching/backups).
    Other examples: Tomcat on EC2 → Elastic Beanstalk, Redis on EC2 → ElastiCache.
    ```

??? question "Q4. Which R requires most effort but provides most cloud benefit?"

    Refactor (re-architect) — rebuild as cloud-native.
    Monolith → microservices, Lambda, containers, event-driven.
    Highest effort, highest ROI long-term. 50-70% cost savings possible.

??? question "Q5. Which R means shutting off applications no longer needed?"

    Retire — discover unused/redundant apps and decommission them.
    Typical: 10-20% of enterprise applications can be retired at migration time.
    Reduces: migration scope, ongoing costs, security attack surface.

??? question "Q6. Which R means keeping apps on-premises for now?"

    Retain — not ready, recently purchased hardware, compliance requirement,
    mainframe with no cloud equivalent, too complex to migrate now.
    Revisit retained apps periodically as cloud options evolve.

??? question "Q7. What are the 6 perspectives of the AWS CAF?"

    Business, People, Governance, Platform, Security, Operations.
    Memory trick: "Business People Go Play Soccer Online"

??? question "Q8. Which CAF perspective focuses on HR and change management?"

    People perspective — culture change, skills development (certs!),
    organizational change management, leadership alignment.

??? question "Q9. What is AWS Migration Hub?"

    Central dashboard tracking migration status across all tools and accounts.
    Integrates: MGN, DMS, Snowball, App Discovery, partner tools.
    One view: discovered, in-progress, completed, failed server counts.

??? question "Q10. What is AWS Application Migration Service (MGN)?"

    ```sql
    Continuous block-level replication from source servers to AWS.
    Steps: Install agent → Continuous replication → Test launch → Cutover.
    Downtime: minutes (only during final cutover). Zero data loss.
    Replaced: old AWS Server Migration Service (SMS — deprecated).
    ```

??? question "Q11. What is AWS DataSync?"

    ```text
    Automated data transfer between on-premises storage and AWS.
    Use for: bulk/scheduled batch transfers. One-time migration.
    Supports: on-prem NFS/SMB to S3/EFS/FSx. Also S3→S3, EFS→EFS.
    Speed: up to 10 Gbps.
    ```

??? question "Q12. Which service handles SFTP-based file transfers to S3 or EFS?"

    AWS Transfer Family — managed SFTP, FTPS, FTP endpoints.
    Partners upload via SFTP to your managed endpoint → files go to S3.
    AWS manages: server, HA, keys. You manage: users, bucket policy.

??? question "Q13. Well-Architected pillar focused on recovering from failures?"

    Reliability — recover automatically from failures, scale to meet demand.
    Design patterns: Multi-AZ, Auto Scaling, tested backups, chaos engineering.

??? question "Q14. Well-Architected pillar focused on using right resources at right size?"

    Performance Efficiency — use resources efficiently.
    Principles: democratize tech, go global in minutes, use serverless, experiment.

??? question "Q15. Well-Architected pillar focused on minimizing environmental impact?"

    Sustainability — added 2021. Right-size, maximize utilization, use managed services.
    AWS: 100% renewable energy (2023), water positive 2030, net zero 2040.

??? question "Q16. What is Amazon SNS?"

    Simple Notification Service — pub/sub messaging.
    Publish to TOPIC → ALL subscribers receive simultaneously.
    Protocols: email, SMS, HTTP, SQS, Lambda.
    Fan-out: one message → multiple SQS queues simultaneously.

??? question "Q17. What does SNS stand for?"

    Simple Notification Service.
    S = Simple (easy to use). N = Notification (push alerts). S = Service.

??? question "Q18. What is Amazon SQS?"

    ```text
    Simple Queue Service — decoupling applications with message queues.
    Producer → Queue → Consumer POLLS for messages.
    Messages stored safely if consumer is down (up to 14 days).
    ```

??? question "Q19. Maximum retention period for SQS messages?"

    14 days. Default is 4 days. Minimum 1 minute.
    After max retention: message deleted automatically regardless.

??? question "Q20. Difference between SNS and SQS?"

    SNS: push to MANY subscribers simultaneously (fan-out). Message delivered once.
    SQS: STORED in queue, ONE consumer per message, persists until processed.
    Combined pattern: SNS → multiple SQS queues (fan-out + durability).

??? question "Q21. What is Amazon Kinesis?"

    Real-time streaming data collection and processing.
    High-volume streams from many sources simultaneously.
    Multiple consumers can read same stream.
    Kinesis Data Streams: raw stream, you manage consumers.
    Kinesis Data Firehose: managed delivery to S3/Redshift (near real-time).

??? question "Q22. Which service for processing real-time clickstream data?"

    Amazon Kinesis — designed for high-volume real-time streaming.
    Detect fraud in seconds vs batch processing next day.

??? question "Q23. What is AWS Step Functions?"

    Serverless workflow orchestration — coordinate Lambda and AWS services
    in visual state machine workflows.
    Features: retry logic, error handling, parallel branches, human approval.
    Standard: up to 1 year. Express: high-volume up to 5 minutes.

??? question "Q24. What is Amazon Lightsail?"

    Simple VPS platform with fixed monthly pricing.
    Pre-configured for WordPress, LAMP, Node.js, etc. Starting at $3.50/month.
    For: beginners, small businesses, simple web apps, portfolio sites.

??? question "Q25. Who is Lightsail designed for?"

    Users wanting simplicity without deep cloud knowledge.
    Small businesses, freelancers, startup MVPs.
    NOT for: complex architectures, auto-scaling enterprise apps.

??? question "Q26. Well-Architected pillar about cost waste and undifferentiated work?"

    Cost Optimization — avoid unnecessary costs, use managed services.
    "Undifferentiated heavy lifting" = work that doesn't make your product unique.

??? question "Q27. Which R for replacing on-premises HR software with Workday SaaS?"

    ```sql
    Repurchase — moving from self-managed app to commercial SaaS.
    Other examples: on-prem CRM → Salesforce, on-prem email → Google Workspace.
    ITSM = IT Service Management (ServiceNow, Jira are common tools).
    ```

??? question "Q28. What is the Well-Architected Tool?"

    ```text
    Free tool reviewing your architecture against 6 pillars.
    Answer ~65 questions → get findings (High/Medium risk) → improvement plan.
    WAR = Well-Architected Review (formal review with AWS Solution Architect).
    ```

??? question "Q29. Relationship between Trusted Advisor and Well-Architected?"

    Well-Architected: theoretical best practices, manual review, done occasionally.
    Trusted Advisor: automated checks against YOUR actual environment, daily.
    TA implements WA principles as automated real-time checks.

??? question "Q30. Critical app taking 2 years to re-architect. What to do now?"

    ```text
    Retain (keep on-premises) OR Rehost to EC2 now while planning Refactor.
    Common pattern: Rehost → stabilize → Replatform/Refactor over time.
    ```

??? question "Q31. Which CAF perspective covers risk management?"

    Governance perspective — portfolio management, risk, compliance,
    program management, benefits realization, financial management.

??? question "Q32. Which service fans out one message to multiple SQS queues?"

    Amazon SNS — publish to topic, multiple SQS queues subscribe.
    Each queue processes independently. One failure doesn't affect others.

??? question "Q33. Reliability pillar approach to designing for failure?"

    "Everything fails all the time" — Werner Vogels, AWS CTO.
    No single points of failure. Automate recovery. Test failure scenarios.
    Chaos engineering = intentionally causing failures to test recovery.

??? question "Q34. Which R has highest ROI long-term but most effort?"

    Refactor — cloud-native re-architecture.
    50-70% cost savings possible. Elasticity, pay-per-use, faster delivery.

??? question "Q35. What is AWS Application Discovery Service?"

    ```text
    Discover on-premises servers before migration. Map dependencies.
    Agentless (VMware vCenter) or Agent-based (physical/other VMs).
    WebServer → AppServer → Database → must migrate all 3 together!
    ```

??? question "Q36. Difference between DataSync and Storage Gateway?"

    DataSync: MIGRATION/TRANSFER — move data to AWS (one-time or scheduled batch).
    Storage Gateway: ONGOING HYBRID — permanent connection, apps use S3 as local storage.

??? question "Q37. SQS queue type guaranteeing exactly-once processing and order?"

    FIFO (First-In-First-Out) queue.
    Standard: at-least-once (may duplicate), unlimited throughput.
    FIFO: exactly-once, strict order, up to 3,000 msg/sec.
    Use FIFO: financial transactions, order processing, anything order-sensitive.

??? question "Q38. Standard SQS queue's delivery guarantee?"

    At-least-once delivery — messages may be delivered more than once.
    Apps must be idempotent (same result whether processed once or twice).
    Idempotent = same result when done multiple times as when done once.

??? question "Q39. What is Amazon EventBridge?"

    ```text
    Serverless event bus routing AWS events to targets automatically.
    Event (EC2 stops) → Rule (matches) → Target (Lambda, SNS, SSM automation).
    Formerly CloudWatch Events. Used for event-driven automation.
    ```

??? question "Q40. Well-Architected pillar covering CI/CD and monitoring?"

    Operational Excellence — run, monitor, and improve operations.
    Principles: IaC, frequent small reversible changes, post-incident reviews.
    PIR = Post-Incident Review (blameless, improve runbooks after incidents).

??? question "Q41. Company found 40% of servers unused. Which R?"

    Retire — decommission unused servers before migration.
    Saves: migration effort, licensing costs, hardware refresh, security risk.

??? question "Q42. Replatforming to RDS instead of MySQL on EC2 provides?"

    Managed service benefits: automatic patching, backups, Multi-AZ HA.
    No application code changes. Same MySQL engine. 9 hours/month freed per DB.

??? question "Q43. What is the CAF Operations perspective?"

    Ensuring cloud services are delivered per agreed business SLAs.
    Monitoring, incident management, DR testing, cloud operations model.
    CCoE = Cloud Center of Excellence (team that sets cloud standards).

??? question "Q44. What does the CAF Platform perspective cover?"

    Building cloud platform architecture, landing zones, network topology.
    Application architecture: microservices, containers, serverless patterns.
    Your VMware/SAN/storage expertise directly relevant here.

??? question "Q45. Which migration tool provides continuous replication for lift-and-shift?"

    ```text
    AWS Application Migration Service (MGN) — continuous block-level replication.
    Install agent → replicate → test → cutover (minutes of downtime).
    ```

??? question "Q46. What is an SNS topic?"

    Logical communication channel. Publishers send to topic.
    Subscribers receive from topic. Like a TV channel — one broadcast, many viewers.
    Standard topics: high throughput, unordered. FIFO topics: ordered, exactly-once.

??? question "Q47. Maximum message size in SQS?"

    256 KB. For larger payloads: store in S3, put S3 reference in SQS message.
    AWS Extended Client Library handles this pattern automatically.

??? question "Q48. Service for serverless workflows coordinating Lambda and AWS services?"

    AWS Step Functions — visual workflow builder.
    Standard (up to 1 year, complex orchestration) or
    Express (up to 5 min, high volume event processing).

??? question "Q49. What is the CAF Business perspective?"

    Align cloud investment with business goals.
    Business case: TCO analysis, expected savings.
    Success metrics: cost per transaction, time-to-market, availability %.

??? question "Q50. Most appropriate R for legacy mainframe with no cloud equivalent?"

    Retain — keep on-premises until viable migration path exists or app retired.
    Mainframe migration: can take years. Plan, document, gradual replacement.
    Strangler fig pattern = gradually replace old system piece by piece.

DAY 9 COMPLETE
*Tomorrow: Day 10 — Additional Services & Full Review*

## Day 10 — ADDITIONAL SERVICES & FULL REVIEW

*Study: 3 hours  |  Questions: 50*

### Acronym Reference (DAY 10)

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

??? question "Q1. Which AWS AI service converts speech to text?"

    Amazon Transcribe — STT. Takes audio, returns text transcript.
    Use for: call center analytics, meeting notes, video subtitles.
    Features: speaker identification, PII redaction from transcripts.

??? question "Q2. Which AWS AI service converts text to speech?"

    Amazon Polly — TTS. 60+ voices, 29 languages. Neural TTS = natural sound.
    Use for: accessibility, e-learning narration, IVR systems, notifications.
    IVR = Interactive Voice Response (phone menu systems).

??? question "Q3. Which analyzes images and videos for objects, faces, and scenes?"

    Amazon Rekognition — computer vision service.
    Detects: objects, scenes, faces, celebrities, text in images, unsafe content.
    Videos: track people across frames, detect activities.

??? question "Q4. Which service powers chatbots (same tech as Alexa)?"

    Amazon Lex — Natural Language Understanding.
    User speaks/types → Lex identifies intent and extracts slots (parameters).
    Integrates with: Lambda, Amazon Connect, Slack, Facebook Messenger.

??? question "Q5. Service for building, training, and deploying ML models?"

    ```text
    Amazon SageMaker — complete ML lifecycle platform.
    Data Wrangler (prepare) → Studio (build) → Training (train) → Endpoints (deploy).
    Pay only for compute when training runs.
    ```

??? question "Q6. Service extracting structured data from scanned documents?"

    Amazon Textract — OCR+ extracts key-value pairs, tables, forms.
    Regular OCR: just raw text. Textract: structured JSON output.
    Use for: invoice processing, tax form extraction, contract analysis.

??? question "Q7. Add product recommendations to e-commerce site?"

    ```text
    Amazon Personalize — real-time personalized recommendations.
    Same ML as Amazon.com. Feed historical data → train model → query API.
    No ML expertise needed.
    ```

??? question "Q8. Service for serverless SQL queries on S3?"

    Amazon Athena — serverless, $5/TB scanned, standard SQL.
    Glue Data Catalog = metadata store (schema definitions for S3 data).
    Parquet format: columnar = scan less data = cheaper + faster.

??? question "Q9. What is AWS Glue?"

    ```text
    Serverless ETL service — extract, transform, load data for analytics.
    Connects: S3, RDS, DynamoDB → transforms → delivers to Redshift, S3.
    Runs on managed Spark. Glue Crawlers: auto-discover schema.
    ```

??? question "Q10. What is Amazon QuickSight?"

    AWS BI (Business Intelligence) service. Interactive dashboards.
    Reads directly from S3, Athena, Redshift, RDS. Serverless. Pay per session.
    ML-powered anomaly detection built-in.

??? question "Q11. What is Amazon EMR?"

    Elastic MapReduce — managed Hadoop/Spark clusters for big data.
    AWS manages: cluster setup, config, scaling. You manage: your code.
    Use Spot Instances for task nodes = 90% savings on big data processing.

??? question "Q12. What is AWS CodePipeline?"

    ```text
    Orchestrates complete CI/CD pipeline: source → build → test → deploy.
    Integrates: CodeCommit (source), CodeBuild (build), CodeDeploy (deploy).
    All automated — developer pushes code → production deployment.
    ```

??? question "Q13. Difference between CodeBuild and CodeDeploy?"

    CodeBuild: BUILD + TEST code (CI). Input: source code. Output: artifact.
    CodeDeploy: DEPLOY artifact (CD). Input: artifact. Output: running app.

??? question "Q14. What is AWS X-Ray?"

    ```bash
    Distributed tracing — trace requests through all microservices.
    Shows which service is slow/erroring.
    Service Map: API GW (15ms) → Lambda (45ms) → RDS (890ms) ← PROBLEM!
    ```

??? question "Q15. What is AWS WorkSpaces?"

    Managed virtual desktop service (DaaS).
    Full Windows/Linux desktop in the cloud. Access from any device via browser.
    Use for: remote work, contractors, regulated environments, call centers.

??? question "Q16. What is Amazon SES?"

    Simple Email Service — managed email at scale.
    Transactional: "Your order shipped" (triggered by app).
    Bulk/marketing: newsletters to 500K subscribers.
    Cost: $0.10/1,000 emails.

??? question "Q17. Service for ML-powered intelligent enterprise search?"

    ```text
    Amazon Kendra — understands natural language questions.
    "How many vacation days in first year?" → reads HR docs → returns direct answer.
    Not just keyword matching — understands context and intent.
    ```

??? question "Q18. What is AWS Lake Formation?"

    Set up and secure data lakes in days instead of months.
    Automates: S3 setup, Glue crawlers, data catalog, access permissions.
    Column-level security = restrict access to specific columns (hide SSNs).

??? question "Q19. What is Amazon AppStream 2.0?"

    Stream specific applications via browser. No local install needed.
    Different from WorkSpaces (full desktop) — AppStream = specific apps only.
    Use for: expensive licensed software (AutoCAD), shared across users.

??? question "Q20. Which service for ML-based fraud detection?"

    Amazon Fraud Detector — ML models trained on fraud patterns.
    Analyzes: account age, location, device, time, amount → fraud score.
    Return: fraud score + outcome (approve/review/block).

??? question "Q21. REVIEW: Key difference between CloudWatch and CloudTrail?"

    ```text
    CloudWatch: "How is infrastructure PERFORMING?" (metrics, CPU, latency).
    CloudTrail: "WHO did WHAT to my infrastructure?" (API audit log).
    EXAM: "audit log" → CloudTrail. "CPU alarm" → CloudWatch.
    ```

??? question "Q22. REVIEW: Security Group vs NACL?"

    ```text
    Security Group: INSTANCE level, STATEFUL, ALLOW only.
    NACL: SUBNET level, STATELESS, ALLOW + DENY.
    "Block specific IP" → NACL. "Open port 443 on EC2" → Security Group.
    ```

??? question "Q23. REVIEW: RDS Multi-AZ vs Read Replicas?"

    ```text
    Multi-AZ: SYNCHRONOUS, HIGH AVAILABILITY, automatic failover, cannot read standby.
    Read Replica: ASYNCHRONOUS, PERFORMANCE, read scaling, any region.
    "Disaster recovery" → Multi-AZ. "Scale reads" → Read Replica.
    ```

??? question "Q24. REVIEW: When to use Spot Instances?"

    For fault-tolerant, interruptible workloads: batch jobs, big data, CI/CD, rendering.
    NEVER for: production databases, real-time apps (cannot be interrupted).

??? question "Q25. REVIEW: Difference between SNS and SQS?"

    ```text
    SNS: push to MANY simultaneously, fan-out, message lost if subscriber down.
    SQS: STORED queue, one consumer per message, persists up to 14 days.
    "Send to multiple recipients" → SNS. "Decouple applications" → SQS.
    ```

??? question "Q26. REVIEW: Direct Connect vs VPN?"

    ```text
    Direct Connect: PRIVATE fiber, CONSISTENT performance, weeks, expensive.
    VPN: ENCRYPTED internet, VARIABLE performance, hours, cheap.
    "Consistent performance" → DX. "Quick/cheap setup" → VPN.
    ```

??? question "Q27. REVIEW: GuardDuty vs Inspector vs Macie?"

    GuardDuty: THREATS in account (ML, anomaly detection, threat intel).
    Inspector: VULNERABILITIES in EC2/containers (CVE scanning).
    Macie: SENSITIVE DATA in S3 (PII, credentials, financial data).

??? question "Q28. REVIEW: CloudFront vs Global Accelerator?"

    ```text
    CloudFront: CACHES content at edge, HTTP/HTTPS only, CDN.
    Global Accelerator: ROUTES over AWS private network, TCP/UDP, static IPs.
    "Cache images globally" → CF. "Two static IPs for whitelist" → GA.
    ```

??? question "Q29. REVIEW: Secrets Manager vs Parameter Store?"

    ```text
    Secrets Manager: secrets + auto-rotation, $0.40/secret/month.
    Parameter Store: config + secrets, FREE standard tier, no auto-rotation.
    "DB passwords with auto-rotation" → SM. "Config values" → PS.
    ```

??? question "Q30. REVIEW: S3 vs EBS vs EFS vs Instance Store?"

    ```text
    S3: object/unlimited. EBS: block/single-instance/persistent.
    EFS: file/multi-instance/persistent. Instance Store: temporary/fastest.
    "Multiple EC2 share files" → EFS. "Database volume" → EBS.
    ```

??? question "Q31. Translate app into 50 languages?"

    Amazon Translate — neural machine translation, 75+ languages.
    Use for: real-time chat translation, content localization, document translation.

??? question "Q32. Running Apache Spark jobs on large datasets?"

    Amazon EMR — managed Hadoop/Spark. Submit Spark job, AWS runs it.
    Core nodes process data. Task nodes (Spot Instances) for cost savings.

??? question "Q33. Build complete CI/CD pipeline using only AWS services?"

    ```text
    CodeCommit (source) → CodeBuild (build/test) → CodeDeploy (deploy).
    CodePipeline orchestrates the entire flow end-to-end.
    ```

??? question "Q34. What is Amazon Cloud9?"

    Cloud-based browser IDE. Full code editor, terminal, pre-installed AWS CLI.
    Runs on EC2. Access from any device — iPad, library computer, client site.
    Collaborative editing (pair programming).

??? question "Q35. Service providing NLP for sentiment and entity extraction?"

    Amazon Comprehend — NLP for text analysis.
    Sentiment: positive/negative/neutral/mixed.
    Entities: PERSON, ORGANIZATION, LOCATION, DATE.
    Key phrases, language detection, topic modeling.

??? question "Q36. Difference between Kinesis Data Streams and Firehose?"

    Data Streams: real-time (ms), you write consumers, multiple readers, replay.
    Firehose: near real-time (60s buffer), managed delivery, one destination, simpler.
    Use Streams: need replay, multiple consumers, custom processing.
    Use Firehose: just deliver to S3/Redshift/OpenSearch easily.

??? question "Q37. Which service sends push notifications to mobile devices?"

    Amazon SNS — supports APNs (Apple) and FCM (Android/Google).
    APNs = Apple Push Notification service. FCM = Firebase Cloud Messaging.

??? question "Q38. REVIEW: Which pillar covers encryption, least privilege, MFA?"

    Security pillar — protect data, systems, and assets.
    Implement strong identity, enable traceability, apply security at all layers.

??? question "Q39. REVIEW: Which pillar covers Multi-AZ, Auto Scaling, backups?"

    Reliability pillar — recover from failures, scale dynamically.
    Design for failure. Automate recovery. Test recovery procedures.

??? question "Q40. REVIEW: What does Replatform mean?"

    ```text
    "Lift, tinker, and shift" — minor optimization, no re-architecture.
    App code unchanged. Architecture mostly same. Operations improved.
    Examples: EC2 MySQL → RDS MySQL. Tomcat EC2 → Elastic Beanstalk.
    ```

??? question "Q41. Hadoop on-premises. AWS equivalent?"

    Amazon EMR (Elastic MapReduce) — managed Hadoop/Spark on AWS.
    You submit jobs. AWS manages cluster, scaling, OS.
    Store data in S3 (not HDFS). Use Spot for 90% savings.

??? question "Q42. What is Amazon Forecast?"

    ```python
    ML time-series forecasting. Demand, staffing, energy predictions.
    Feed historical data → Forecast trains model → return predictions with confidence.
    Same technology Amazon uses for supply chain forecasting.
    ```

??? question "Q43. Which developer tool finds performance bottlenecks in microservices?"

    AWS X-Ray — distributed tracing. Service Map shows latency per service.
    Each request traced through ALL services it touches.

??? question "Q44. REVIEW: Three AWS pricing fundamentals?"

    1. Pay as you go (variable, no upfront).
    2. Save when you reserve (1-3 year commit = 72% off).
    3. Pay less as you use more (volume discounts — S3 tiers).

??? question "Q45. REVIEW: Is data transfer into AWS free?"

    YES — data transfer IN to AWS is ALWAYS FREE.
    Data OUT costs money (~$0.09/GB to internet).
    EXAM SHORTCUT: Data IN = Free. Data OUT = Costs.

??? question "Q46. REVIEW: What is AWS CAF?"

    Cloud Adoption Framework. 6 perspectives:
    Business, People, Governance, Platform, Security, Operations.
    Memory: "Business People Go Play Soccer Online"

??? question "Q47. REVIEW: Which S3 class is cheapest with 12-hour retrieval?"

    ```python
    S3 Glacier Deep Archive — $0.00099/GB/month. 12-hour retrieval. 180-day min.
    Storage class order (cheapest last):
    Standard → Intelligent → Standard-IA → One Zone-IA → Glacier Instant
    → Glacier Flexible → Glacier Deep Archive.
    ```

??? question "Q48. REVIEW: What does a NAT Gateway allow?"

    Private subnet instances initiate OUTBOUND internet connections.
    Internet CANNOT initiate inbound connections to private instances.
    Must be in PUBLIC subnet. One per AZ for HA.

??? question "Q49. REVIEW: Which support plan includes a dedicated TAM?"

    Enterprise Support ($15,000+/month) — dedicated TAM.
    Enterprise On-Ramp: pool of shared TAMs. Business: no TAM.

??? question "Q50. REVIEW: What is the principle of least privilege?"

    Grant only minimum permissions needed for the job.
    Start: zero permissions. Add: only what's needed. Review: remove unused.
    If compromised with least privilege: minimal blast radius.

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

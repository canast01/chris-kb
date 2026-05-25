# Dell ECS — Security


```text
┌───────────────────────────────────────── Dell ECS — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     ECS security: multitenancy isolation, IAM, encryption, bucket policies, and compliance    │   │
│   │    IAM: namespace-level users, IAM roles, S3 bucket policies, ACLs, resource-based policies   │   │
│   │       Encryption: SSE-S3 and SSE-C (customer-managed keys) for object encryption at rest      │   │
│   │       Network: TLS 1.2+ for all data and management; VLANs separate data from management      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Client auth → IAM/policy check → namespace isolation → encrypted write → audit logged              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Identity & Access      │  │        Data Security        │  │          Compliance         │   │
│   │          IAM users          │  │        SSE-S3 encrypt       │  │          Audit log          │   │
│   │       S3 bucket policy      │  │          SSE-C key          │  │         WORM / lock         │   │
│   │             ACLs            │  │           TLS 1.2+          │  │        Retention lock       │   │
│   │      Namespace isolate      │  │       VLAN separation       │  │         WORM bucket         │   │
│   │           LDAP/AD           │  │      Data-at-rest enc.      │  │         SOC 2 ready         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Namespaces are fully isolated; tenants cannot access other namespace buckets or objects            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │     Standard     │       Scope       │      Config      │      Owner       │   │
│   │    IAM policy    │  AWS IAM compat  │     Per bucket    │   JSON policy    │     App team     │   │
│   │      SSE-S3      │     AES-256      │    All objects    │  Bucket default  │   Storage eng.   │   │
│   │     TLS 1.2+     │   PCI DSS 4.0    │   All endpoints   │    TLS config    │    Infra team    │   │
│   │   WORM bucket    │    SEC 17a-4     │    Bucket level   │  Immutable flag  │   Legal + ops    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS data VLAN and management VLAN separate; TLS on both; nodes not internet-facing       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    IAM            = Identity and Access Management; ECS supports S3-compatible IAM policies           │
│    Bucket policy  = JSON policy attached to S3 bucket defining who can read, write, or list           │
│    ACL            = Access Control List; per-object or per-bucket access; simpler than policies       │
│    SSE-S3         = Server-Side Encryption with S3-managed keys; AES-256; transparent to client       │
│    SSE-C          = Server-Side Encryption with Customer-provided key; client sends key per request   │
│    Namespace isolate = ECS tenant boundary; buckets and users in one NS cannot see another NS         │
│    WORM bucket    = Bucket with object lock enabled; objects cannot be deleted before retention date  │
│    Retention lock = Object-level retention; object immutable until specified expiry timestamp         │
│    LDAP/AD        = ECS can authenticate management users via LDAP or Active Directory                │
│    SOC 2 ready    = ECS audit logging and WORM features support SOC 2 compliance requirements         │
│    VLAN separation = Data VLAN for S3 traffic; management VLAN for ECS Portal and SSH access          │
│    SEC 17a-4      = US regulation requiring WORM storage for financial records; ECS qualifies         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────────── Dell ECS — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     ECS security: multitenancy isolation, IAM, encryption, bucket policies, and compliance    │   │
│   │    IAM: namespace-level users, IAM roles, S3 bucket policies, ACLs, resource-based policies   │   │
│   │       Encryption: SSE-S3 and SSE-C (customer-managed keys) for object encryption at rest      │   │
│   │       Network: TLS 1.2+ for all data and management; VLANs separate data from management      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Client auth → IAM/policy check → namespace isolation → encrypted write → audit logged              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Identity & Access      │  │        Data Security        │  │          Compliance         │   │
│   │          IAM users          │  │        SSE-S3 encrypt       │  │          Audit log          │   │
│   │       S3 bucket policy      │  │          SSE-C key          │  │         WORM / lock         │   │
│   │             ACLs            │  │           TLS 1.2+          │  │        Retention lock       │   │
│   │      Namespace isolate      │  │       VLAN separation       │  │         WORM bucket         │   │
│   │           LDAP/AD           │  │      Data-at-rest enc.      │  │         SOC 2 ready         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Namespaces are fully isolated; tenants cannot access other namespace buckets or objects            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │     Standard     │       Scope       │      Config      │      Owner       │   │
│   │    IAM policy    │  AWS IAM compat  │     Per bucket    │   JSON policy    │     App team     │   │
│   │      SSE-S3      │     AES-256      │    All objects    │  Bucket default  │   Storage eng.   │   │
│   │     TLS 1.2+     │   PCI DSS 4.0    │   All endpoints   │    TLS config    │    Infra team    │   │
│   │   WORM bucket    │    SEC 17a-4     │    Bucket level   │  Immutable flag  │   Legal + ops    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS data VLAN and management VLAN separate; TLS on both; nodes not internet-facing       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    IAM            = Identity and Access Management; ECS supports S3-compatible IAM policies           │
│    Bucket policy  = JSON policy attached to S3 bucket defining who can read, write, or list           │
│    ACL            = Access Control List; per-object or per-bucket access; simpler than policies       │
│    SSE-S3         = Server-Side Encryption with S3-managed keys; AES-256; transparent to client       │
│    SSE-C          = Server-Side Encryption with Customer-provided key; client sends key per request   │
│    Namespace isolate = ECS tenant boundary; buckets and users in one NS cannot see another NS         │
│    WORM bucket    = Bucket with object lock enabled; objects cannot be deleted before retention date  │
│    Retention lock = Object-level retention; object immutable until specified expiry timestamp         │
│    LDAP/AD        = ECS can authenticate management users via LDAP or Active Directory                │
│    SOC 2 ready    = ECS audit logging and WORM features support SOC 2 compliance requirements         │
│    VLAN separation = Data VLAN for S3 traffic; management VLAN for ECS Portal and SSH access          │
│    SEC 17a-4      = US regulation requiring WORM storage for financial records; ECS qualifies         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────────── Dell ECS — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     ECS security: multitenancy isolation, IAM, encryption, bucket policies, and compliance    │   │
│   │    IAM: namespace-level users, IAM roles, S3 bucket policies, ACLs, resource-based policies   │   │
│   │       Encryption: SSE-S3 and SSE-C (customer-managed keys) for object encryption at rest      │   │
│   │       Network: TLS 1.2+ for all data and management; VLANs separate data from management      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Client auth → IAM/policy check → namespace isolation → encrypted write → audit logged              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Identity & Access      │  │        Data Security        │  │          Compliance         │   │
│   │          IAM users          │  │        SSE-S3 encrypt       │  │          Audit log          │   │
│   │       S3 bucket policy      │  │          SSE-C key          │  │         WORM / lock         │   │
│   │             ACLs            │  │           TLS 1.2+          │  │        Retention lock       │   │
│   │      Namespace isolate      │  │       VLAN separation       │  │         WORM bucket         │   │
│   │           LDAP/AD           │  │      Data-at-rest enc.      │  │         SOC 2 ready         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Namespaces are fully isolated; tenants cannot access other namespace buckets or objects            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │     Standard     │       Scope       │      Config      │      Owner       │   │
│   │    IAM policy    │  AWS IAM compat  │     Per bucket    │   JSON policy    │     App team     │   │
│   │      SSE-S3      │     AES-256      │    All objects    │  Bucket default  │   Storage eng.   │   │
│   │     TLS 1.2+     │   PCI DSS 4.0    │   All endpoints   │    TLS config    │    Infra team    │   │
│   │   WORM bucket    │    SEC 17a-4     │    Bucket level   │  Immutable flag  │   Legal + ops    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS data VLAN and management VLAN separate; TLS on both; nodes not internet-facing       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    IAM            = Identity and Access Management; ECS supports S3-compatible IAM policies           │
│    Bucket policy  = JSON policy attached to S3 bucket defining who can read, write, or list           │
│    ACL            = Access Control List; per-object or per-bucket access; simpler than policies       │
│    SSE-S3         = Server-Side Encryption with S3-managed keys; AES-256; transparent to client       │
│    SSE-C          = Server-Side Encryption with Customer-provided key; client sends key per request   │
│    Namespace isolate = ECS tenant boundary; buckets and users in one NS cannot see another NS         │
│    WORM bucket    = Bucket with object lock enabled; objects cannot be deleted before retention date  │
│    Retention lock = Object-level retention; object immutable until specified expiry timestamp         │
│    LDAP/AD        = ECS can authenticate management users via LDAP or Active Directory                │
│    SOC 2 ready    = ECS audit logging and WORM features support SOC 2 compliance requirements         │
│    VLAN separation = Data VLAN for S3 traffic; management VLAN for ECS Portal and SSH access          │
│    SEC 17a-4      = US regulation requiring WORM storage for financial records; ECS qualifies         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>

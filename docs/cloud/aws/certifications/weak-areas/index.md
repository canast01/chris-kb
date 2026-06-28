---
tags:
  - aws
  - certifications
---
# AWS Weak Areas

<div class="kb-summary">
AWS Weak Areas reference covering VPC Peering vs PrivateLink vs Transit Gateway, S3 Storage Classes, IAM Policy Evaluation, RDS Multi-AZ vs Read Replicas, Security Group vs NACL and 1 more sections.
</div>

## VPC Peering vs PrivateLink vs Transit Gateway

| Feature | VPC Peering | PrivateLink | Transit Gateway |
|---|---|---|---|
| Traffic path | Direct VPC-to-VPC | Private endpoint in your VPC | Centralized hub routing |
| Transitivity | Non-transitive | N/A (endpoint-based) | Transitive |
| CIDR overlap | Not allowed | Allowed | Not allowed |
| Use case | Small-scale VPC connectivity | Expose service privately at scale | Hub-and-spoke, many VPCs |
| Cross-account | Yes | Yes | Yes |
| Cost | Data transfer charges | Per endpoint + data transfer | Per attachment + data |

Exam pattern: "Company wants 100 VPCs to communicate without managing individual peering connections" → Transit Gateway. "Service provider wants to expose service to customers without VPC peering" → PrivateLink.

## S3 Storage Classes

| Class | Min Storage | Min Object Size | Retrieval Time | Use Case |
|---|---|---|---|---|
| Standard | None | None | Immediate | Frequent access |
| Intelligent-Tiering | None | None (< 128KB stays in Frequent) | Immediate | Unknown/changing access patterns |
| Standard-IA | 30 days | 128KB | Immediate | Infrequent, millisecond access needed |
| One Zone-IA | 30 days | 128KB | Immediate | Infrequent, single AZ acceptable |
| Glacier Instant | 90 days | 128KB | Milliseconds | Archive with instant retrieval |
| Glacier Flexible | 90 days | 40KB | Minutes to hours | Archive, flexible retrieval |
| Glacier Deep Archive | 180 days | 40KB | 12 hours | Long-term, rarely accessed |

Exam gotchas:
- S3 Lifecycle policies can transition objects between classes automatically
- Objects < 128KB in Intelligent-Tiering are always billed at Frequent Access tier rate
- Glacier Flexible has three retrieval options: Expedited (1–5 min), Standard (3–5 hr), Bulk (5–12 hr)

## IAM Policy Evaluation

Policy evaluation order (most to least restrictive):
1. Explicit Deny (in any applicable policy)
2. Service Control Policy (SCP) — if in AWS Organizations
3. Permission Boundary — if attached to identity
4. Identity-based policy
5. Resource-based policy (may allow cross-account without identity policy)

Key rules:
- An explicit Deny ALWAYS wins
- Without an explicit Allow, access is implicitly denied
- SCPs do not grant permissions; they restrict maximum permissions

## RDS Multi-AZ vs Read Replicas

| Feature | Multi-AZ | Read Replica |
|---|---|---|
| Purpose | High availability / failover | Read scaling / reporting |
| Replication | Synchronous | Asynchronous |
| Readable | No (standby is passive) | Yes |
| Failover | Automatic (60–120 sec) | Manual promotion |
| Cross-region | Yes (with Multi-AZ option) | Yes |
| Aurora difference | Automatic 6 copies across 3 AZs | Up to 15 replicas; low replica lag |

## Security Group vs NACL

| Feature | Security Group | NACL |
|---|---|---|
| Applies to | ENI / instance | Subnet |
| Stateful | Yes (return traffic automatic) | No (must explicitly allow both directions) |
| Rules | Allow only | Allow and Deny |
| Rule processing | All rules evaluated | Rules evaluated in order (lowest number wins) |
| Default behavior | Deny all inbound; allow all outbound | Allow all (default NACL) |

## Study Checklist

- [ ] Draw a Transit Gateway vs Peering vs PrivateLink decision diagram from memory
- [ ] Recite S3 storage class minimum durations and retrieval times for each class
- [ ] Walk through 3 IAM policy evaluation scenarios including cross-account
- [ ] Explain why Multi-AZ standby is not a read replica
- [ ] Describe two scenarios where NACL Deny rules are needed (SGs cannot deny)
- [ ] Practice 10 weak-area questions until consistently correct

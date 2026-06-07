# S3


<div class="kb-summary">
S3 reference.
</div>

```text
┌──────────────────────────────────────────── AWS CLI — S3 ─────────────────────────────────────────────┐
│                                                                                                       │
│  S3 CLI commands for bucket management, object operations, sync, and policy config.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            High-Level S3 Commands            │  │              Object Operations              │   │
│   │           s3 cp: copy file/folder            │  │          s3api get-object: download         │   │
│   │              s3 mv: move/rename              │  │           s3api put-object: upload          │   │
│   │           s3 rm: delete object(s)            │  │             s3api delete-object             │   │
│   │          s3 ls: list bucket/prefix           │  │            s3api list-objects-v2            │   │
│   │          s3 sync: delta sync folder          │  │         s3api head-object: metadata         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  s3 commands wrap multipart upload; s3api gives direct REST API access                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Bucket Management               │  │             Security and Policy             │   │
│   │             s3api create-bucket              │  │           s3api put-bucket-policy           │   │
│   │             s3api delete-bucket              │  │        s3api put-public-access-block        │   │
│   │         s3api put-bucket-versioning          │  │         s3api put-bucket-encryption         │   │
│   │   s3api put-bucket-lifecycle-configuration   │  │           s3api put-bucket-logging          │   │
│   │         s3api put-bucket-replication         │  │     s3api put-object-lock-configuration     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  S3 storage nodes (11 nines durability) · KMS · CloudTrail · CloudFront (CDN)                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  s3 sync         = Transfers only new or changed objects; --delete removes extras                     │
│  Multipart upload= S3 splits large files into parts; automatic via aws s3 cp                          │
│  s3api           = Low-level REST API wrapper; all S3 operations directly                             │
│  Versioning      = Keeps all object versions; protects against accidental delete                      │
│  Object lock     = WORM: prevents object deletion during retention period                             │
│  Lifecycle rule  = Transitions objects to cheaper tiers or expires them                               │
│  Replication     = Cross-region or cross-account object copy for DR/compliance                        │
│  put-public-access-block= Blocks all public ACLs and bucket policies; account level                   │
│  head-object     = Returns metadata without downloading the object body                               │
│  Bucket policy   = Resource-based IAM policy controlling access to bucket                             │
│  Server-side encryption= SSE-S3 (managed) or SSE-KMS (CMK) encrypts stored objects                    │
│  list-objects-v2 = Paginated listing of objects in bucket with prefix filter                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

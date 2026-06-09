# S3


<div class="kb-summary">
AWS CLI S3 command reference: high-level s3 commands (cp, mv, sync, ls, rm) and low-level s3api operations for bucket management, object handling, versioning, encryption, lifecycle rules, and access policy configuration.
</div>

```text
┌─────────────────────────────────── AWS CLI — S3 Command Reference ────────────────────────────────────┐
│                                                                                                       │
│   Two CLI interfaces: s3 (high-level, multipart auto) and s3api (direct REST, fine-grained control)   │
│   Use s3 for day-to-day copy/sync; use s3api when you need exact control over request headers         │
│   All S3 operations require correct IAM permissions on the calling identity                           │
│                                                                                                       │
│   High-level s3 commands                                                                              │
│   aws s3 cp src dst         copy file or folder; --recursive for directories                          │
│   aws s3 mv src dst         move or rename; removes source after copy                                 │
│   aws s3 rm s3://bucket/key delete object; --recursive deletes prefix                                 │
│   aws s3 ls s3://bucket/    list bucket contents or prefixes                                          │
│   aws s3 sync src dst       delta sync; --delete removes objects not in source                        │
│   aws s3 mb s3://bucket     make a new bucket                                                         │
│                                                                                                       │
│   s3api object operations                                                                             │
│   put-object                upload a single object with full metadata control                         │
│   get-object                download an object; supports Range for partial reads                      │
│   delete-object             delete a specific version or current object                               │
│   head-object               returns metadata without downloading the object body                      │
│   list-objects-v2           paginated listing with --prefix and --max-items filter                    │
│   copy-object               server-side copy; used for storage class transitions                      │
│                                                                                                       │
│   Bucket management                                                                                   │
│   create-bucket             creates bucket; --create-bucket-configuration sets region                 │
│   delete-bucket             bucket must be empty before deletion                                      │
│   put-bucket-versioning     enables versioning; keeps all object versions on overwrite/delete         │
│   put-bucket-lifecycle-configuration  transitions objects to cheaper tiers or expires them            │
│   put-bucket-replication    cross-region or cross-account copy for DR or compliance                   │
│                                                                                                       │
│   Security and policy                                                                                 │
│   put-bucket-policy         resource-based IAM policy controlling access to the bucket                │
│   put-public-access-block   blocks all public ACLs and bucket policies; set at account level          │
│   put-bucket-encryption     enforces SSE-S3 (managed) or SSE-KMS (CMK) for stored objects             │
│   put-bucket-logging        enables server access logging to a target bucket                          │
│   put-object-lock-configuration  WORM retention; prevents object deletion during retention period     │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   S3 storage nodes: 11 nines durability across multiple AZs                                           │
│   Supporting services: KMS (encryption), CloudTrail (API logging), CloudFront (CDN delivery)          │
│                                                                                                       │
│   Key terms:                                                                                          │
│   s3api          = low-level REST API wrapper; exposes all S3 operations directly                     │
│   Multipart upload = S3 splits large files into parts; automatic via aws s3 cp                        │
│   Versioning     = keeps all object versions; protects against accidental delete                      │
│   Object lock    = WORM: prevents object deletion during retention period                             │
│   Lifecycle rule = transitions objects to cheaper tiers (Glacier) or expires them                     │
│   Replication    = CRR/SRR: cross-region or same-region copy for DR or compliance                     │
│   head-object    = returns metadata without downloading the object body                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

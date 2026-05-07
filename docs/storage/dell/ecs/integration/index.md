# ECS Integration
## S3 Client Integration

ECS exposes a native S3-compatible API on HTTPS port 443 (or 9021 for plain HTTP in lab environments). Any S3-compatible client can connect using path-style or virtual-hosted-style addressing.

**Connection parameters:**
- Endpoint: `https://<ecs-load-balancer-or-node>` (port 443)
- Access key: object user access key from ECS Portal → Namespace → IAM Users
- Secret key: associated secret from key creation
- Region: ECS does not enforce AWS regions; set to any value (e.g., `us-east-1`) in the client config

**AWS CLI configuration:**

```bash
aws configure set aws_access_key_id <ecs_access_key>
aws configure set aws_secret_access_key <ecs_secret_key>
aws configure set default.region us-east-1

# Use --endpoint-url and --no-verify-ssl (if using self-signed cert)
aws s3 ls --endpoint-url https://<ecs-endpoint> --no-verify-ssl

# Upload a file
aws s3 cp localfile.tar.gz s3://<bucket>/ \
  --endpoint-url https://<ecs-endpoint>
```

ECS supports S3 multipart upload, S3 Object Lock (WORM), presigned URLs, bucket versioning, and lifecycle policies. Virtual-hosted-style (`<bucket>.<ecs-endpoint>`) requires DNS configuration; path-style (`<ecs-endpoint>/<bucket>`) works without DNS changes.

## Veeam Object Repository

ECS is a certified S3-compatible target for Veeam Backup & Replication object repositories (Scale-out Backup Repository offload and Capacity Tier).

**Integration steps:**
1. Create a dedicated ECS namespace and bucket for Veeam (`veeam-prod-offload`)
2. Create a dedicated object user with read/write access to the bucket
3. In Veeam: Add Object Storage Repository → S3 Compatible → enter ECS endpoint, port, bucket name, and credentials
4. Optionally enable Veeam Immutability (requires ECS Object Lock enabled on the bucket at creation)

**Key ECS settings for Veeam:**
- Bucket versioning: not required for Veeam (Veeam manages its own metadata)
- Object Lock: enable only if Veeam immutable backups are required; set the retention period on the bucket
- Quota: set a hard quota on the bucket to prevent Veeam from consuming unbounded cluster capacity

## HDFS Integration

ECS supports HDFS-compatible access through the ECS HDFS connector, enabling Hadoop ecosystem tools (Spark, Hive, MapReduce) to read and write directly to ECS buckets.

- Install the ECS HDFS connector JAR on Hadoop cluster nodes
- Configure `core-site.xml` to point to `ecss://` or `ecshdfs://` scheme with the ECS endpoint
- Authentication uses Kerberos or simple auth depending on the ECS namespace HDFS auth setting
- ECS presents HDFS namespace paths mapped to buckets; directory emulation is handled by the connector

## Metadata Search Integration

ECS supports custom object metadata tagging and a Metadata Search API (based on Elasticsearch) that allows querying objects by custom key-value tags across a namespace.

```bash
# Search for objects with a custom metadata tag (requires metadata search enabled on namespace)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/object/namespaces/<namespace>/buckets/<bucket>/query?query=<key>%3D<value>" \
  | python3 -m json.tool
```

Enable metadata search per namespace in ECS Portal → Namespace → Edit. Metadata search requires additional indexer capacity; plan ECS node sizing accordingly.

## External Authentication (LDAP/AD)

ECS can delegate IAM user authentication to an external LDAP or Active Directory service for namespace-level access. Configure under ECS Portal → Namespace → Edit → Authentication Domain. Object users with S3 keys always authenticate locally; LDAP integration applies to management console users.

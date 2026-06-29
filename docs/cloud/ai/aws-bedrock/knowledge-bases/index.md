---
tags:
  - aws
  - ai
---
# Bedrock Knowledge Bases

<div class="kb-summary">
Bedrock Knowledge Bases provide retrieval-augmented generation (RAG) by connecting foundation models to your data stored in S3. Documents are chunked, embedded, and stored in a vector store for semantic search at inference time.

*Applies to: AWS Bedrock*
</div>

```d2
direction: down

s3_data_sources: "S3 Data Sources" {shape: rectangle}
embeddings_and_chunking: "Embeddings and Chunking" {shape: rectangle}
retrieval_configuration: "Retrieval Configuration" {shape: rectangle}
syncing_data_sources: "Syncing Data Sources" {shape: rectangle}
associating_with_an_agent: "Associating with an Agent" {shape: rectangle}
troubleshooting: "Troubleshooting" {shape: rectangle}

s3_data_sources -> embeddings_and_chunking: uses
embeddings_and_chunking -> retrieval_configuration: uses
retrieval_configuration -> syncing_data_sources: uses
syncing_data_sources -> associating_with_an_agent: uses
associating_with_an_agent -> troubleshooting: uses
```

## S3 Data Sources

Data sources point to S3 prefixes. Supported formats include PDF, DOCX, TXT, HTML, CSV, and Markdown.

```bash
# Create a knowledge base (requires an existing vector store, e.g. OpenSearch Serverless)
aws bedrock-agent create-knowledge-base \
  --name "product-docs-kb" \
  --role-arn "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForKnowledgeBase" \
  --knowledge-base-configuration '{
    "type": "VECTOR",
    "vectorKnowledgeBaseConfiguration": {
      "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
    }
  }' \
  --storage-configuration '{
    "type": "OPENSEARCH_SERVERLESS",
    "opensearchServerlessConfiguration": {
      "collectionArn": "arn:aws:aoss:us-east-1:123456789012:collection/abc123",
      "vectorIndexName": "product-docs-index",
      "fieldMapping": {"vectorField":"embedding","textField":"text","metadataField":"metadata"}
    }
  }'

# Add an S3 data source
aws bedrock-agent create-data-source \
  --knowledge-base-id "KB123456" \
  --name "product-docs-s3" \
  --data-source-configuration '{
    "type": "S3",
    "s3Configuration": {"bucketArn":"arn:aws:s3:::my-product-docs"}
  }'
```


```text title="Expected output"
{
    "knowledgeBase": {
        "id": "KB123456",
        "name": "product-docs-kb",
        "status": "CREATING",
        "roleArn": "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForKnowledgeBase",
        "knowledgeBaseConfiguration": {
            "type": "VECTOR",
            "vectorKnowledgeBaseConfiguration": {
                "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
            }
        },
        "storageConfiguration": {
            "type": "OPENSEARCH_SERVERLESS",
            "opensearchServerlessConfiguration": {
                "collectionArn": "arn:aws:aoss:us-east-1:123456789012:collection/abc123",
                "vectorIndexName": "product-docs-index"
            }
        },
        "createdAt": "2024-01-15T14:32:18.456Z",
        "updatedAt": "2024-01-15T14:32:18.456Z"
    }
}
{
    "dataSource": {
        "id": "DS789012",
        "name": "product-docs-s3",
        "status": "AVAILABLE",
        "knowledgeBaseId": "KB123456",
        "dataSourceConfiguration": {
            "type": "S3",
            "s3Configuration": {
                "bucketArn": "arn:aws:s3:::my-product-docs"
            }
        },
        "createdAt": "2024-01-15T14:32:45.123Z",
        "updatedAt": "2024-01-15T14:32:45.123Z"
    }
}
```

!!! warning "Common errors"
    **`An error occurred (ValidationException) when calling the CreateKnowledgeBase operation: Invalid IAM role ARN format or role does not have required trust relationship with Bedrock`** — Verify the role ARN is correct and the role's trust policy includes `bedrock.amazonaws.com` as a principal.
    **`An error occurred (ResourceNotFoundException) when calling the CreateDataSource operation: Knowledge base KB123456 not found`** — Wait for the knowledge base creation to complete (status changes from CREATING to ACTIVE) before creating data sources.
    **`An error occurred (ValidationException) when calling the CreateKnowledgeBase operation: Collection arn:aws:aoss:us-east-1:123456789012:collection/abc123 does not exist or is not accessible`** — Ensure the OpenSearch Serverless collection exists in the same region and the Bedrock execution role has `aoss:APIAccessAll` permissions.
## Embeddings and Chunking

Bedrock supports several embedding models. Chunking strategy affects retrieval quality significantly.

| Embedding Model | Dimensions | Max Input Tokens | Best For |
|---|---|---|---|
| amazon.titan-embed-text-v1 | 1536 | 8192 | General English text |
| amazon.titan-embed-text-v2:0 | 1024 | 8192 | Multilingual, updated knowledge |
| cohere.embed-english-v3 | 1024 | 512 | High-accuracy English retrieval |
| cohere.embed-multilingual-v3 | 1024 | 512 | Non-English documents |

Chunking options: `FIXED_SIZE` (default 300 tokens, 20% overlap), `HIERARCHICAL`, `SEMANTIC`, or `NONE` (one chunk per file).

## Retrieval Configuration

Control how many chunks are retrieved and whether a reranking model is applied.

```python
import boto3

bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

response = bedrock_runtime.retrieve(
    knowledgeBaseId="KB123456",
    retrievalQuery={"text": "What is the return policy for electronics?"},
    retrievalConfiguration={
        "vectorSearchConfiguration": {
            "numberOfResults": 5,
            "overrideSearchType": "HYBRID"   # SEMANTIC | HYBRID
        }
    }
)

for result in response["retrievalResults"]:
    print(result["score"], result["content"]["text"][:200])
```

## Syncing Data Sources

After uploading new documents to S3, trigger an ingestion job to re-embed and index content.

```bash
# Start a sync job
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id "KB123456" \
  --data-source-id "DS789" \
  --region us-east-1

# Poll until complete
aws bedrock-agent get-ingestion-job \
  --knowledge-base-id "KB123456" \
  --data-source-id "DS789" \
  --ingestion-job-id "JOB_ID" \
  --query 'ingestionJob.status'
```


```text title="Expected output"
{
    "ingestionJobId": "job-a1b2c3d4e5f6g7h8",
    "knowledgeBaseId": "KB123456",
    "dataSourceId": "DS789",
    "ingestionJobStatus": "STARTING"
}
"STARTING"
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the StartIngestionJob operation: Knowledge base KB123456 not found`** — Verify the knowledge base ID exists in your account and region using `aws bedrock-agent list-knowledge-bases --region us-east-1`.
    **`An error occurred (ValidationException) when calling the GetIngestionJob operation: Invalid ingestion job ID format`** — Replace `JOB_ID` with the actual job ID returned from the start command (e.g., `job-a1b2c3d4e5f6g7h8`).
    **`An error occurred (AccessDeniedException) when calling the StartIngestionJob operation: User is not authorized to perform: bedrock-agent:StartIngestionJob`** — Add the `bedrock:StartIngestionJob` and `bedrock:GetIngestionJob` permissions to your IAM user or role policy.
Ingestion jobs process documents in parallel. Large buckets (10k+ files) can take 30+ minutes. Check `statistics.numberOfDocumentsFailed` in the job response for partial failures.

## Associating with an Agent

```bash
aws bedrock-agent associate-agent-knowledge-base \
  --agent-id "AGENTID123" \
  --agent-version "DRAFT" \
  --knowledge-base-id "KB123456" \
  --description "Product documentation for support queries" \
  --knowledge-base-state "ENABLED"
```


```text title="Expected output"
{
    "agentKnowledgeBaseId": "AGKB-a7f2c9e1d4b6",
    "agentId": "AGENTID123",
    "agentVersion": "DRAFT",
    "knowledgeBaseId": "KB123456",
    "description": "Product documentation for support queries",
    "knowledgeBaseState": "ENABLED",
    "createdAt": "2024-01-15T14:32:18.456Z",
    "updatedAt": "2024-01-15T14:32:18.456Z"
}
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the AssociateAgentKnowledgeBase operation: Could not find agent with id AGENTID123`** — Verify the agent ID exists in your AWS account and region using `aws bedrock-agent list-agents`.
    **`An error occurred (ValidationException) when calling the AssociateAgentKnowledgeBase operation: Knowledge base KB123456 does not exist`** — Confirm the knowledge base ID is correct and exists in the same region using `aws bedrock list-knowledge-bases`.
    **`An error occurred (ConflictException) when calling the AssociateAgentKnowledgeBase operation: Knowledge base is already associated with this agent`** — Remove the existing association first using `aws bedrock-agent disassociate-agent-knowledge-base` before re-associating.
## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Zero results returned | Documents not synced | Check ingestion job status and failures |
| Poor relevance | Wrong chunking strategy | Switch to SEMANTIC chunking for prose |
| Embedding throttling | Too many concurrent sync jobs | Reduce parallelism or request quota increase |
| `ValidationException` on retrieve | Incorrect index field mapping | Verify vectorField/textField names in storage config |

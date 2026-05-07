# Bedrock Knowledge Bases

Bedrock Knowledge Bases provide retrieval-augmented generation (RAG) by connecting foundation models to your data stored in S3. Documents are chunked, embedded, and stored in a vector store for semantic search at inference time.

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

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Zero results returned | Documents not synced | Check ingestion job status and failures |
| Poor relevance | Wrong chunking strategy | Switch to SEMANTIC chunking for prose |
| Embedding throttling | Too many concurrent sync jobs | Reduce parallelism or request quota increase |
| `ValidationException` on retrieve | Incorrect index field mapping | Verify vectorField/textField names in storage config |

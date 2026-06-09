# Cloud AI

<div class="kb-summary">
Cloud-hosted AI and LLM API services — AWS Bedrock, Azure OpenAI, and the OpenAI API. Covers model access, authentication, private networking, cost management, and security for enterprise AI integration.
</div>

```text
┌──────────────────────────────────── Cloud AI Services — Overview ─────────────────────────────────────┐
│                                                                                                       │
│   Three cloud AI platforms: AWS Bedrock, Azure OpenAI, and the public OpenAI API                      │
│   Key decisions: data residency, private networking, RBAC, cost controls, and model availability      │
│   All require IAM/identity configuration before model access; none allow anonymous requests           │
│                                                                                                       │
│   AWS Bedrock                                                                                         │
│   Fully managed; access foundation models (Claude, Llama, Titan) via AWS SDK and API                  │
│   Authentication: IAM roles and policies; supports VPC endpoints for private networking               │
│   Key controls: model access request per-region, guardrails for content filtering, CloudTrail logs    │
│                                                                                                       │
│   Azure OpenAI                                                                                        │
│   Azure-hosted GPT-4, embeddings, and DALL-E; private endpoint support for VNET isolation             │
│   Authentication: Azure AD RBAC; supports managed identities for service-to-service auth              │
│   Key controls: content filtering tiers, quota per deployment, diagnostic logging to Log Analytics    │
│                                                                                                       │
│   OpenAI API                                                                                          │
│   Public API; requires API key management and rate-limit awareness for production use                 │
│   Authentication: bearer token (API key); org-level and project-level key scoping available           │
│   Key controls: usage tiers, rate limits per model, spend limits, usage dashboard                     │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Foundation model = large pre-trained model (Claude, GPT-4, Llama) accessed via API                  │
│   Guardrail       = Bedrock feature that filters model inputs and outputs against defined policies    │
│   VPC endpoint    = private AWS network path to Bedrock; traffic does not traverse the public internet│
│   Managed identity = Azure credential attached to a service; no stored secrets                        │
│   Rate limit      = per-model request and token quota; exceeded = 429 responses                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="aws-bedrock/">
  <strong>AWS Bedrock</strong>
  <span>Fully managed service for deploying foundation models (Claude, Llama, Titan) via AWS APIs.</span>
</a>

<a class="kb-card" href="azure-openai/">
  <strong>Azure OpenAI</strong>
  <span>Azure-hosted OpenAI models (GPT-4, embeddings, DALL-E) with private networking and RBAC.</span>
</a>

<a class="kb-card" href="openai/">
  <strong>OpenAI API</strong>
  <span>OpenAI API usage, model selection, prompt patterns, rate limits, and security considerations.</span>
</a>

<a class="kb-card" href="certifications/">
  <strong>Certifications</strong>
  <span>AI and ML certification study notes — exam tracking, practice notes, and review plans.</span>
</a>
</div>

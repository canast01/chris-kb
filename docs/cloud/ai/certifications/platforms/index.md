---
tags:
  - certifications
---
# AI Platforms


<div class="kb-summary">
AI Platforms reference covering AWS Bedrock, Azure OpenAI Service, Google Vertex AI, Hugging Face, Platform Comparison Table and 1 more sections.
</div>
```text
┌───────────────────────────────────── Certifications Ai Platforms ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Ai: Certifications Ai Platforms platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Certifications Ai Platforms management console                  │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Certifications Ai Platforms infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Ai                 = Certifications Ai Platforms platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## AWS Bedrock

Amazon Bedrock is a fully managed service providing access to foundation models via API without managing infrastructure.

| Feature | Detail |
|---|---|
| Model access | Anthropic Claude, Meta Llama, Mistral, Amazon Titan, Cohere, AI21 |
| Fine-tuning | Supported for select models (Titan, Cohere) via continued pre-training |
| Agents | Bedrock Agents orchestrates multi-step tasks with tool use |
| Knowledge bases | Managed RAG: S3 → chunking → OpenSearch/Aurora vector store |
| Guardrails | Content filtering, PII redaction, grounding checks |
| Pricing model | Pay-per-token (on-demand) or Provisioned Throughput |

Exam gotchas:
- Bedrock does NOT require GPU instance management — serverless API
- Provisioned Throughput guarantees a model unit (MU) of throughput for a fixed hourly cost
- Bedrock Knowledge Bases handles the full RAG pipeline; you only supply an S3 data source
- Bedrock Guardrails: topic denial, content filters, PII redaction, grounding, word filters

## Azure OpenAI Service

| Feature | Detail |
|---|---|
| Model access | GPT-4o, GPT-4, GPT-3.5-turbo, DALL-E, Whisper, text-embedding models |
| Deployment types | Standard (shared capacity), Provisioned (dedicated PTUs) |
| Fine-tuning | GPT-3.5-turbo and GPT-4 supported |
| Integration | Azure AI Studio, Azure Machine Learning, Azure Cognitive Search |
| Compliance | Data does not leave your Azure region; SOC2, HIPAA eligible |
| Content filtering | Configurable severity levels per harm category |

Key exam point: Azure OpenAI is NOT the same as OpenAI.com — data residency, private networking, and compliance boundaries differ.

## Google Vertex AI

| Feature | Detail |
|---|---|
| Model access | Gemini 1.5 Pro/Flash, PaLM 2, Imagen, Codey, Chirp |
| Model Garden | Curated catalogue of first-party and OSS models (Llama, Mistral) |
| Grounding | Connect model responses to Google Search or a custom data store |
| Agents | Vertex AI Agent Builder (formerly Dialogflow CX + Gen App Builder) |
| Fine-tuning | Supervised tuning + RLHF available for Gemini models |
| MLOps | Vertex AI Pipelines, Experiments, Feature Store, Model Registry |

## Hugging Face

| Feature | Detail |
|---|---|
| Model Hub | 500K+ public models; search by task, language, framework |
| Transformers library | Unified API for BERT, GPT, T5, LLaMA, etc. |
| Inference Endpoints | Managed hosting for any Hub model |
| Spaces | Demo apps (Gradio/Streamlit) with free or upgraded compute |
| Datasets Hub | Standard datasets for benchmarking and fine-tuning |
| PEFT library | LoRA, QLoRA, prompt tuning — efficient fine-tuning methods |

## Platform Comparison Table

| Dimension | AWS Bedrock | Azure OpenAI | Vertex AI | Hugging Face |
|---|---|---|---|---|
| Model variety | High (multi-vendor) | OpenAI-focused | Google-focused | Very high (OSS) |
| Managed RAG | Yes (Knowledge Bases) | Yes (AI Search integration) | Yes (Grounding) | No (DIY) |
| Private networking | VPC endpoint | Private endpoint | VPC Service Controls | Dedicated endpoints |
| Fine-tuning | Limited models | GPT-3.5/4 | Gemini | Any model |
| OSS model support | Via SageMaker JumpStart | Limited | Model Garden | Native |

## Study Checklist

- [ ] Name three foundation model providers available on AWS Bedrock
- [ ] Explain the difference between on-demand and provisioned throughput on Bedrock
- [ ] Describe how Azure OpenAI differs from OpenAI.com for data handling and compliance
- [ ] Know what Vertex AI Model Garden provides and how grounding works
- [ ] Explain when to use Hugging Face Inference Endpoints vs Spaces
- [ ] Compare managed RAG offerings across all four platforms
- [ ] Understand Bedrock Guardrails categories (topic, content, PII, grounding, word)

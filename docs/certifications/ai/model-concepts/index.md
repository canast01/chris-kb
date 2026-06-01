# AI Model Concepts


<div class="kb-summary">
AI Model Concepts reference covering Transformers and Attention Mechanisms, Embeddings, Tokens and Tokenization, Fine-Tuning vs. RAG vs. Prompting, Generation Parameters and 1 more sections.
</div>
```
┌────────────────────────────────── Certifications Ai Model Concepts ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Ai: Certifications Ai Model Concepts platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Certifications Ai Model Concepts management console                │   │
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
│    Physical: Certifications Ai Model Concepts infrastructure · management network · monitoring        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Ai                 = Certifications Ai Model Concepts platform overview and core concepts          │
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


## Transformers and Attention Mechanisms

The Transformer architecture underpins virtually all modern LLMs. Key components tested on AI certification exams:

| Component | Role | Exam Focus |
|---|---|---|
| Self-attention | Relates every token to every other token | Quadratic complexity O(n²) |
| Multi-head attention | Parallel attention across different subspaces | Head count is a hyperparameter |
| Positional encoding | Injects sequence order (no recurrence) | Sinusoidal or learned |
| Feed-forward layer | Per-token transformation after attention | Applied identically at each position |
| Layer normalization | Stabilizes training, applied pre or post | Pre-LN preferred in modern models |

Attention formula: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`

- `d_k` is the key dimension; dividing prevents vanishing gradients in softmax
- Encoder-only models (BERT): bidirectional attention, good for classification
- Decoder-only models (GPT): causal/autoregressive, good for generation
- Encoder-decoder (T5, BART): seq2seq tasks, translation, summarization

## Embeddings

Embeddings map discrete tokens or documents to continuous vector spaces.

| Type | Dimensionality (typical) | Use Case |
|---|---|---|
| Word embeddings (Word2Vec, GloVe) | 100–300 | Legacy NLP tasks |
| Contextual embeddings (BERT) | 768–1024 | Semantic search, classification |
| Sentence/document embeddings | 384–1536 | RAG retrieval, clustering |
| Multimodal embeddings (CLIP) | 512–1024 | Image-text alignment |

Key exam points:
- Cosine similarity is the standard distance metric for comparing embeddings
- Embedding dimension affects both quality and storage/compute cost
- OpenAI `text-embedding-3-small` supports Matryoshka (variable dimension output)

## Tokens and Tokenization

- Tokenization converts raw text to integer IDs via Byte Pair Encoding (BPE) or SentencePiece
- ~1 token = approximately 0.75 English words (rough rule for exam questions)
- Context window = maximum token count for prompt + completion combined
- Tokens, not characters or words, determine pricing and context limits

| Model Family | Approximate Context Window |
|---|---|
| GPT-3.5-turbo | 4K / 16K variants |
| GPT-4o | 128K |
| Claude 3 / 3.5 | 200K |
| Gemini 1.5 Pro | 1M |

## Fine-Tuning vs. RAG vs. Prompting

| Approach | When to Use | Cost | Latency | Knowledge Freshness |
|---|---|---|---|---|
| Zero/few-shot prompting | Quick experiments, well-defined tasks | Low | Low | Real-time via prompt |
| RAG | Dynamic, large, frequently updated knowledge | Medium | Medium | High (retrieval at inference) |
| Fine-tuning | Task-specific style/format, domain vocabulary | High (training) | Low (inference) | Static at training time |
| Full pre-training | New domain from scratch | Very high | Low | Static |

RAG pipeline stages: document ingestion → chunking → embedding → vector store indexing → query embedding → ANN retrieval → context injection → generation.

## Generation Parameters

| Parameter | Range | Effect |
|---|---|---|
| Temperature | 0–2 | Higher = more random output |
| Top-p (nucleus sampling) | 0–1 | Limits to top-p probability mass |
| Top-k | Integer | Limits to top-k tokens at each step |
| Max tokens | Integer | Hard cap on output length |
| Frequency penalty | 0–2 | Reduces repetition of frequent tokens |

## Study Checklist

- [ ] Explain self-attention vs cross-attention
- [ ] Describe encoder-only, decoder-only, and encoder-decoder architectures with examples
- [ ] Calculate approximate token count for a given text passage
- [ ] Compare RAG vs fine-tuning trade-offs for three distinct scenarios
- [ ] Define cosine similarity and when it is preferred over dot product
- [ ] Explain positional encoding and why it is necessary
- [ ] Describe temperature and top-p sampling and their interaction
- [ ] Know context window sizes for GPT-4o, Claude 3.5, and Gemini 1.5 Pro

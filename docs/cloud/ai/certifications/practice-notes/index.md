---
tags:
  - certifications
---
# AI Practice Notes

<div class="kb-summary">
AI Practice Notes reference covering Question Pattern Recognition, Common Wrong Answers to Avoid, Exam Domain Breakdown — AWS Certified AI Practitioner (AIF-C01), Key Terminology Distinctions, Scoring and Exam Strategy and 2 more sections.
</div>

```d2
direction: down

question_pattern_recognition: "Question Pattern Recognition" {shape: rectangle}
common_wrong_answers_to_avoid: "Common Wrong Answers to Avoid" {shape: rectangle}
exam_domain_breakdown_aws_certified_: "Exam Domain Breakdown — AWS Certified AI Practitioner (AIF-C" {shape: rectangle}
key_terminology_distinctions: "Key Terminology Distinctions" {shape: rectangle}
scoring_and_exam_strategy: "Scoring and Exam Strategy" {shape: rectangle}
service_boundary_quick_reference: "Service Boundary Quick Reference" {shape: rectangle}

question_pattern_recognition -> common_wrong_answers_to_avoid: uses
common_wrong_answers_to_avoid -> exam_domain_breakdown_aws_certified_: uses
exam_domain_breakdown_aws_certified_ -> key_terminology_distinctions: uses
key_terminology_distinctions -> scoring_and_exam_strategy: uses
scoring_and_exam_strategy -> service_boundary_quick_reference: uses
```

## Question Pattern Recognition

Most AI certification exams use scenario-based questions. Common patterns:

| Pattern Type | What to Look For | Typical Wrong Answers |
|---|---|---|
| "Best approach for X" | Constraints in the scenario (cost, latency, freshness) | Ignoring stated constraints |
| "Which service provides Y" | Managed vs self-managed distinction | Confusing SageMaker with Bedrock |
| "Most cost-effective" | On-demand vs provisioned, batch inference | Always picking provisioned |
| "Responsible AI" | Bias, fairness, transparency, explainability | Treating it as only a security question |
| "Fine-tune vs RAG" | Knowledge update frequency, data volume | Defaulting to fine-tuning for freshness |

## Common Wrong Answers to Avoid

- **Fine-tuning for freshness**: Fine-tuning is NOT the right answer when knowledge must be updated frequently — use RAG instead.
- **Temperature = creativity**: Temperature controls randomness/diversity. High temperature → more random, not necessarily more creative.
- **Larger model = better**: For specific narrow tasks a smaller fine-tuned model often outperforms a large general model at lower cost.
- **Embedding = output**: Embeddings are intermediate representations, not final model outputs.
- **RAG eliminates hallucination**: RAG reduces hallucination by grounding responses but does NOT eliminate it.
- **Tokens = words**: 1 token ≈ 0.75 words in English; code and non-English text tokenize differently.

## Exam Domain Breakdown — AWS Certified AI Practitioner (AIF-C01)

| Domain | Weight |
|---|---|
| Domain 1: Fundamentals of AI and ML | 20% |
| Domain 2: Fundamentals of Generative AI | 24% |
| Domain 3: Applications of Foundation Models | 28% |
| Domain 4: Guidelines for Responsible AI | 14% |
| Domain 5: Security, Compliance, and Governance | 14% |

Passing score: 700/1000. Exam length: 85 questions, 90 minutes.

## Key Terminology Distinctions

| Term A | Term B | Key Difference |
|---|---|---|
| Training | Inference | Training updates weights; inference uses fixed weights |
| Supervised | Unsupervised | Supervised needs labels; unsupervised finds structure |
| Pre-training | Fine-tuning | Pre-training from scratch on large corpus; fine-tuning adapts |
| RLHF | SFT | RLHF uses human preference ranking; SFT uses demonstration data |
| Prompt engineering | Fine-tuning | Prompt engineering modifies input only; fine-tuning modifies weights |
| Hard prompt | Soft prompt | Hard: human-readable text; soft: learned continuous embeddings |
| Hallucination | Bias | Hallucination: factual errors; bias: systematic skewed outputs |

## Scoring and Exam Strategy

- Questions scored 100–1000; raw score is scaled — passing is typically 700
- Unscored pilot questions (~15) are mixed in; you cannot identify them
- Flag and return strategy: do not get stuck; spend ~60 seconds per question on first pass
- For "most"/"best" questions: eliminate obviously wrong answers first, then choose the option that most directly addresses all stated constraints
- Responsible AI questions: map to fairness, explainability, privacy, robustness, governance, transparency pillars

## Service Boundary Quick Reference

| Scenario | Correct Service | Common Mistake |
|---|---|---|
| Call a Claude model via API without GPU management | AWS Bedrock | SageMaker |
| Train a custom ML model on your own data | SageMaker | Bedrock |
| Add guardrails to a Bedrock model call | Bedrock Guardrails | Lambda |
| Managed RAG from S3 | Bedrock Knowledge Bases | Kendra alone |
| NLP on structured data (sentiment, entities) | Amazon Comprehend | Bedrock |

## Study Checklist

- [ ] Complete at least 2 full practice exams (65+ questions each)
- [ ] Review all incorrect answers and identify the wrong-answer trap used
- [ ] Memorize domain weights and topic coverage percentages
- [ ] Practice distinguishing RAG vs fine-tuning scenarios
- [ ] Know Bedrock, SageMaker, and Comprehend service boundaries
- [ ] Review AWS Responsible AI documentation and pillar definitions
- [ ] Time yourself: target 60–75 seconds per question average

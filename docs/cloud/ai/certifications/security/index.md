---
tags:
  - certifications
  - security
---
# AI Security and Responsible AI


<div class="kb-summary">
AI Security and Responsible AI reference covering Responsible AI Pillars, AI Safety Concepts, Data Privacy in the ML Lifecycle, Bias Types and Mitigations, AI Governance Frameworks and 1 more sections.
</div>
```text
┌──────────────────────────────── Certifications Ai Security — Security ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Ai security: access control, authentication, encryption, and hardening guide         │   │
│   │          Principle of least privilege applied to all admin roles and service accounts         │   │
│   │          Encryption at rest and in transit enforced; key rotation on defined schedule         │   │
│   │            Annual security review and audit; logs forwarded to SIEM for correlation           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Define roles → enforce MFA → enable encryption → harden → audit                                    │
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
│    Physical: Certifications Ai Security infrastructure · management network · monitoring              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Ai                 = Certifications Ai Security platform overview and core concepts                │
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


## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Responsible AI Pillars

| Pillar | Definition | Example Control |
|---|---|---|
| Fairness | Model outputs do not discriminate based on protected attributes | Bias audits, balanced training data |
| Explainability | Decisions can be understood and interpreted | SHAP values, LIME, attention visualization |
| Privacy | Personal data is protected throughout the ML lifecycle | Differential privacy, data anonymization |
| Robustness | Model performs reliably under adversarial or out-of-distribution input | Adversarial testing, input validation |
| Governance | Processes and controls manage AI risk at organizational level | Model cards, audit trails, approval gates |
| Transparency | Stakeholders understand AI capabilities, limitations, and data usage | Disclosure policies, model documentation |

## AI Safety Concepts

| Threat | Description | Mitigation |
|---|---|---|
| Prompt injection | Malicious input overrides system instructions | Input sanitization, guardrails, system prompt hardening |
| Jailbreaking | Bypassing safety filters via creative prompting | RLHF, Constitutional AI, output filtering |
| Hallucination | Model generates plausible but false information | RAG grounding, citation requirements, human review |
| Data poisoning | Training data manipulated to influence model behavior | Data provenance, anomaly detection in training sets |
| Model extraction | Adversary reconstructs model via repeated queries | Rate limiting, output perturbation |
| Membership inference | Adversary determines if a sample was in training data | Differential privacy, output confidence masking |

## Data Privacy in the ML Lifecycle

- **Data collection**: Consent, minimization, purpose limitation (GDPR principles)
- **Training**: PII should be removed or anonymized before training
- **Inference**: Prompts may contain PII — use PII detection/redaction (e.g., Bedrock Guardrails)
- **Output**: Models may regurgitate PII from training data — requires monitoring
- **Retention**: Define retention policies for prompts, completions, and model artifacts

Key AWS services for AI data privacy:
- Amazon Macie: PII detection in S3
- Bedrock Guardrails: PII redaction at inference time
- AWS PrivateLink: Keep API calls off the public internet

## Bias Types and Mitigations

| Bias Type | Cause | Mitigation |
|---|---|---|
| Historical bias | Training data reflects past discrimination | Re-weighting, curated balanced datasets |
| Representation bias | Underrepresentation of a group in training data | Oversampling, synthetic data augmentation |
| Measurement bias | Proxy metrics poorly represent the target variable | Feature selection review, ground truth audits |
| Aggregation bias | Model ignores sub-group differences | Stratified evaluation, per-group metrics |

## AI Governance Frameworks

| Framework | Owner | Focus |
|---|---|---|
| NIST AI RMF 1.0 | NIST (US) | Govern, map, measure, manage risk |
| EU AI Act | European Union | Risk-based regulation by AI application type |
| ISO/IEC 42001 | ISO | AI management system standard |
| AWS Responsible AI | Amazon | Fairness, explainability, privacy, robustness, governance, transparency |

High-risk AI categories under EU AI Act: biometric identification, critical infrastructure, educational access, employment, essential services, law enforcement, border control, justice.

## Study Checklist

- [ ] Memorize the 6 AWS Responsible AI pillars with one sentence definition each
- [ ] Explain prompt injection and three mitigations
- [ ] Distinguish hallucination from bias
- [ ] Know which AWS services address PII in AI workloads
- [ ] Describe differential privacy at a conceptual level
- [ ] Map the NIST AI RMF four functions (Govern, Map, Measure, Manage)
- [ ] Know EU AI Act risk categories for exam scenario questions

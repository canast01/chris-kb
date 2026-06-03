# Data Classification


<div class="kb-summary">
Data classification defines how sensitive information must be labelled, handled, stored, and shared.
</div>

## Classification Levels

| Level | Description | Examples | Controls |
|---|---|---|---|
| Public | Approved for public distribution | Marketing materials, public docs | No restrictions |
| Internal | Internal use only — not for public | Internal policies, project plans | Employee access only |
| Confidential | Sensitive business or personal data | Financial data, HR records, customer data | Need-to-know; encrypted at rest |
| Restricted | Highest sensitivity; regulatory or legal implications | PII, PHI, PCI card data, credentials, legal privilege | Strict access; encrypted; audit-logged |

## Labelling Requirements

| Level | Email | Documents | Storage |
|---|---|---|---|
| Public | Optional | Optional | No special requirement |
| Internal | Header/footer label | Classification tag | Standard access control |
| Confidential | Label + encryption for external recipients | MIP/Purview sensitivity label | Encrypted volume or folder |
| Restricted | Encrypted send only | MIP Protect; watermark | Dedicated encrypted store; DLP policy |

## Microsoft Purview / MIP Labels

```powershell
Install-Module ExchangeOnlineManagement
Connect-IPPSSession

# List sensitivity labels
Get-Label | Select-Object DisplayName, Priority, IsDefault, Guid

# Check label policy assignments
Get-LabelPolicy | Select-Object Name, Labels, Users, Workloads
```text
┌──────────────────────────────── Data Protection — Data Classification ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Classification defines how sensitive information must be labelled, handled, and stored    │   │
│   │       Four tiers: Public → Internal → Confidential → Restricted; each has handling rules      │   │
│   │            Apply the highest classification that any data element in a set warrants           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │    Classification Levels    │  │    Labelling Requirements   │  │      Handling Controls      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │            Public           │  │        Optional label       │  │       No restrictions       │   │
│   │           Internal          │  │     Header/footer label     │  │     Employee access only    │   │
│   │         Confidential        │  │      MIP label required     │  │    Need-to-know; encrypt    │   │
│   │      Restricted/PII/PHI     │  │     Purview sensitivity     │  │     Strict; audit logged    │   │
│   │      Examples per level     │  │    Email + docs + storage   │  │       Encrypted volume      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │      Level       │     Examples     │      Storage      │      Email       │      Access      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Public      │    Marketing     │   No requirement  │     No label     │      Anyone      │   │
│   │     Internal     │ Policies, plans  │    Standard ACL   │    Label only    │    Employees     │   │
│   │   Confidential   │   Finance, HR    │   Encrypted vol   │   +encrypt ext   │   Need-to-know   │   │
│   │    Restricted    │  PII, PCI, PHI   │     HSM-backed    │   +DLP policy    │  Strict + audit  │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Sensitivity label  = Tag applied to document/email; drives DLP and encryption policies             │
│    MIP / Purview      = Microsoft tools for applying and enforcing sensitivity labels                 │
│    Need-to-know       = Access granted only when required by job function; not role alone             │
│    Data owner         = Business-unit leader accountable for a dataset and its classification         │
│    DLP policy         = Enforces labelling rules; blocks transfer of classified data outside perimeter│
│    Reclassification   = Formal review to raise or lower a classification based on changed context     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Classification Workflow

1. **Identify** — what type of data? Who created it? What system stores it?
2. **Classify** — apply the correct level based on content and context
3. **Label** — apply MIP/Purview label or physical label to storage/document
4. **Apply controls** — access restrictions, encryption, DLP rules per level
5. **Review** — revisit classification when data changes hands or usage changes

## DLP Policy Alignment

| Classification | DLP Action |
|---|---|
| Restricted — PCI | Block external email of card numbers; alert security |
| Restricted — PII | Encrypt external email; log access |
| Confidential | Warn on external sharing; allow with justification |
| Internal | Allow internally; block public share links |

## Responsibilities

| Role | Responsibility |
|---|---|
| Data Owner | Classify data; approve access requests |
| Data Custodian (IT) | Implement controls; maintain storage; enforce labels |
| Data User | Handle data per classification; report misclassification |
| Security / DLP team | Define policy; monitor violations; audit |

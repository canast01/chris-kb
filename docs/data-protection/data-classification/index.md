```powershell
Install-Module ExchangeOnlineManagement
Connect-IPPSSession

# List sensitivity labels
Get-Label | Select-Object DisplayName, Priority, IsDefault, Guid

# Check label policy assignments
Get-LabelPolicy | Select-Object Name, Labels, Users, Workloads
```

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

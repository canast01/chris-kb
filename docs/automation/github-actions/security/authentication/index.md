---
tags:
  - github-actions
  - security
---
# GitHub Actions — Authentication

```yaml
# Default token usage
jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Call GitHub API
        run: |
          curl -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
               https://api.github.com/repos/${{ github.repository }}
```

```bash
# Create a fine-grained PAT at:
# GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens

# Store as a repository secret, then reference in workflows
- name: Cross-repo checkout
  uses: actions/checkout@v4
  with:
    repository: myorg/other-repo
    token: ${{ secrets.PAT_TOKEN }}
```
```mermaid
flowchart LR
    githubToken["GITHUB_TOKEN\nAuto-generated per run\nScoped to repo"]
    oidc["OIDC JWT\nShort-lived token\nno stored secrets"]
    pat["Fine-grained PAT\nStored as repo secret\nDays to years"]
    classicPat["Classic PAT\nBroad scope\nAvoid — legacy"]

    githubToken -->|"best for: default API\npackages write"| ghApi["GitHub API\nGHCR / Releases"]
    oidc -->|"best for: cloud deploy"| cloudProv["AWS / GCP / Azure"]
    pat -->|"best for: cross-repo\noperations"| otherRepo["Other repos\nadmin ops"]
    classicPat -.->|"avoid"| legacy["Legacy only"]
```

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "GitHub Actions" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

@enduml
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [GitHub Actions — Access Control](../access-control/)
- [GitHub Actions — Hardening](../hardening/)
- [GitHub Actions — Encryption](../encryption/)

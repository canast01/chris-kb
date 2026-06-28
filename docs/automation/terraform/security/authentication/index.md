---
tags:
  - security
  - terraform
---
# Terraform — Authentication


<div class="kb-summary">
Authentication reference covering Provider Credential Flow — CI/CD, CI/CD Credential Injection, Credential Management Reference.

*Applies to: Terraform 1.x*
</div>
![Terraform — Authentication](../../../../assets/automation-terraform-security-authentication-index.svg)


```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "Authentication" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

note over SVC
  Provider Credential Flow  CI/CD
  CI/CD Credential Injection
  Credential Management Reference
end note

@enduml
```

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Provider Credential Flow — CI/CD

```mermaid
graph LR
    ciPipeline["CI/CD Pipeline\n(GitHub Actions / GitLab)"]
    ciSecrets["CI/CD Secrets\n(repository secrets)"]
    oidcToken["OIDC Token\n(short-lived)"]
    iamRole["Cloud IAM Role\n(assume via OIDC)"]
    envVars["Environment Variables\n(AWS_ / ARM_ / GOOGLE_)"]
    tfProvider["Terraform Provider\n(aws / azurerm / google)"]
    cloudAPI["Cloud API\n(EC2 / ARM / GCP)"]

    ciPipeline --> ciSecrets
    ciPipeline --> oidcToken
    oidcToken -->|Preferred: keyless| iamRole
    ciSecrets -->|Fallback: static keys| envVars
    iamRole --> envVars
    envVars --> tfProvider
    tfProvider --> cloudAPI
```


### Google Cloud

```bash
# Application Default Credentials
gcloud auth application-default login

# Or via service account key (CI/CD)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## CI/CD Credential Injection

Credentials should be stored as CI/CD secrets and injected at runtime — never committed to source control.

```yaml
# GitHub Actions example — inject AWS credentials as secrets
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: eu-west-1
```

## Credential Management Reference

| Provider | Recommended method | CI/CD approach |
|---|---|---|
| AWS | IAM role (EC2/ECS) or OIDC | GitHub OIDC → IAM role (no static keys) |
| Azure | Managed Identity | Service principal via env vars |
| GCP | Workload Identity | Service account via OIDC |
| HashiCorp Vault | Vault agent | Vault token via CI secret |

---

## See also

- [Terraform — Access Control](../access-control/)
- [Terraform — Hardening](../hardening/)
- [Terraform — Encryption](../encryption/)

# GitHub Actions — Integrations


<div class="kb-summary">
> Part of the [GitHub Actions Architecture](../index.md) reference.
</div>

## Cloud Providers

### AWS — OIDC (Keyless)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-prod
      aws-region: eu-west-1

  - name: Deploy to ECS
    run: aws ecs update-service --cluster prod --service app --force-new-deployment
```
┌──────────────────────────────────── GitHub Actions — Integrations ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  GitHub Actions integrates with cloud providers, registries, ITSM, Slack, and security tools  │   │
│   │        Cloud auth via OIDC: AWS, Azure, GCP — no stored access keys; federated identity       │   │
│   │        Container registries: GHCR, ECR, ACR, Docker Hub — login action then docker push       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Cloud            │  │         DevOps Tools        │  │        Notifications        │   │
│   │   AWS (OIDC → AssumeRole)   │  │     Terraform plan/apply    │  │        Slack webhook        │   │
│   │   Azure (OIDC → federated)  │  │     Ansible AWX trigger     │  │      GitHub PR comment      │   │
│   │   GCP (Workload Identity)   │  │     Docker build + push     │  │       Email on failure      │   │
│   │     kubectl + kubeconfig    │  │    Security scan (Trivy)    │  │       PagerDuty alert       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ OIDC / Workload Identity = cloud-side trust policy allows GitHub Actions JWT to assume a role │   │
│   │     repository_dispatch      = external system triggers workflow via GitHub API POST event    │   │
│   │ Deployment API           = GitHub Deployments track which SHA is deployed to which environment│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────── GitHub Actions — Integrations ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  GitHub Actions integrates with cloud providers, registries, ITSM, Slack, and security tools  │   │
│   │        Cloud auth via OIDC: AWS, Azure, GCP — no stored access keys; federated identity       │   │
│   │        Container registries: GHCR, ECR, ACR, Docker Hub — login action then docker push       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Cloud            │  │         DevOps Tools        │  │        Notifications        │   │
│   │   AWS (OIDC → AssumeRole)   │  │     Terraform plan/apply    │  │        Slack webhook        │   │
│   │   Azure (OIDC → federated)  │  │     Ansible AWX trigger     │  │      GitHub PR comment      │   │
│   │   GCP (Workload Identity)   │  │     Docker build + push     │  │       Email on failure      │   │
│   │     kubectl + kubeconfig    │  │    Security scan (Trivy)    │  │       PagerDuty alert       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ OIDC / Workload Identity = cloud-side trust policy allows GitHub Actions JWT to assume a role │   │
│   │     repository_dispatch      = external system triggers workflow via GitHub API POST event    │   │
│   │ Deployment API           = GitHub Deployments track which SHA is deployed to which environment│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Kubernetes

```yaml
# Deploy via kubectl
- uses: azure/setup-kubectl@v4
  with:
    version: v1.30.0

- name: Deploy
  run: |
    kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}
    kubectl rollout status deployment/app --timeout=300s

# Helm
- uses: azure/setup-helm@v4
  with:
    version: v3.15.0

- name: Helm upgrade
  run: |
    helm upgrade --install myapp ./charts/myapp \
      --set image.tag=${{ github.sha }} \
      --wait --timeout 5m
```

## Slack Notifications

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: "C0123ALERTS"
    slack-message: |
      *Deployment failed* :red_circle:
      Repo: ${{ github.repository }}
      Branch: ${{ github.ref_name }}
      Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

## HashiCorp Vault

```yaml
- uses: hashicorp/vault-action@v3
  with:
    url: https://vault.example.com
    method: jwt
    jwtGithubAudience: https://vault.example.com
    role: github-actions
    secrets: |
      secret/data/prod/db password | DB_PASSWORD;
      secret/data/prod/api token | API_TOKEN

- name: Use secrets
  run: ./deploy.sh
  env:
    DB_PASSWORD: ${{ steps.vault.outputs.DB_PASSWORD }}
    API_TOKEN: ${{ steps.vault.outputs.API_TOKEN }}
```

## Ansible

```yaml
- name: Run Ansible playbook
  uses: dawidd6/action-ansible-playbook@v2
  with:
    playbook: site.yml
    directory: ./ansible
    key: ${{ secrets.ANSIBLE_SSH_KEY }}
    inventory: |
      [webservers]
      web01.example.com
      web02.example.com
    options: |
      --extra-vars "version=${{ github.sha }}"
      --vault-password-file /tmp/vault_pass
```

## Terraform

```yaml
- uses: hashicorp/setup-terraform@v3
  with:
    terraform_version: 1.9.0

- name: Terraform Plan
  run: |
    terraform init
    terraform plan -out=plan.tfplan
  env:
    TF_VAR_image_tag: ${{ github.sha }}
    ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}

- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: terraform apply plan.tfplan
```

## Jira / GitHub Issue Integration

```yaml
# Create Jira ticket on failure
- name: Create Jira issue on failure
  if: failure()
  uses: atlassian/gajira-create@v3
  with:
    project: OPS
    issuetype: Bug
    summary: "CI failure — ${{ github.repository }} ${{ github.run_id }}"
    description: "Workflow failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
  env:
    JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
    JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
    JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
```

## Integration Summary

| Platform | Action | Auth Method |
|---|---|---|
| AWS | `aws-actions/configure-aws-credentials` | OIDC (keyless) |
| Azure | `azure/login` | OIDC (keyless) |
| GCP | `google-github-actions/auth` | Workload Identity Federation |
| Docker Hub | `docker/login-action` | Username + Access Token |
| GHCR | `docker/login-action` | `GITHUB_TOKEN` |
| HashiCorp Vault | `hashicorp/vault-action` | JWT / AppRole |
| Slack | `slackapi/slack-github-action` | Bot Token |
| Terraform | `hashicorp/setup-terraform` | Cloud OIDC |
| Ansible | `dawidd6/action-ansible-playbook` | SSH key secret |
| Jira | `atlassian/gajira-*` | API Token |

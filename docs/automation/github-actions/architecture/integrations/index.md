# GitHub Actions — Integrations

> Part of the [GitHub Actions Architecture](../index.md) reference.

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

### GCP — Workload Identity Federation

```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/123/locations/global/workloadIdentityPools/github/providers/github
    service_account: deploy@myproject.iam.gserviceaccount.com

- uses: google-github-actions/setup-gcloud@v2
- run: gcloud run deploy myapp --image gcr.io/myproject/myapp:${{ github.sha }}
```

## Container Registries

```yaml
# Docker Hub
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

# GitHub Container Registry (GHCR) — no secrets needed with GITHUB_TOKEN
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

# Build and push
- uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
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

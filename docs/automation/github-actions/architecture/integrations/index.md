---
tags:
  - architecture
  - github-actions
---
# GitHub Actions — Integrations

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

---

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [Github Actions — Design Standards](../design-standards/)

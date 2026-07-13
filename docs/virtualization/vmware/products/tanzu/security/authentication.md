---
tags:
  - security
  - tanzu
  - vmware
description: "Authentication reference covering Supervisor Authentication (vSphere with Tanzu), TKG Workload Cluster Authentication (Pinniped + Dex), Harbor..."
---
# Tanzu — Authentication

<div class="kb-summary">
Authentication reference covering Supervisor Authentication (vSphere with Tanzu), TKG Workload Cluster Authentication (Pinniped + Dex), Harbor Authentication, Service Account Tokens (Kubernetes), Pull Secret Management and 3 more sections.

*Applies to: Tanzu 3.x*
</div>
![Tanzu — Authentication](../../../../../assets/virtualization-vmware-tanzu-security-authentication.svg)

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Supervisor Authentication (vSphere with Tanzu)

Users authenticate to the Supervisor cluster using vCenter SSO credentials:

```bash
kubectl vsphere login \
  --server https://supervisor.example.local \
  --username user@corp.local \
  --insecure-skip-tls-verify
# Prompts for password
# Creates OIDC kubeconfig entry with short-lived token
```


```text title="Expected output"
Password:
Logged in successfully.

You have access to the following contexts:
   supervisor.example.local

The current context is now "supervisor.example.local".

To switch contexts, run: kubectl config use-context <context-name>

Current context: supervisor.example.local
Cluster: supervisor.example.local
User: user@corp.local
```

!!! warning "Common errors"
    **`error: x509: certificate signed by unknown authority`** — Remove the `--insecure-skip-tls-verify` flag and ensure the supervisor cluster's CA certificate is trusted on your system, or add the CA to your system's certificate store.
    **`error: the server has asked for the client to provide credentials, but none were provided`** — Verify your username format matches your vSphere SSO domain (typically `user@domain.local`) and that your password is correct.
    **`error: unable to connect to the server: dial tcp: lookup supervisor.example.local: no such host`** — Confirm the supervisor cluster hostname is resolvable and correct, and verify network connectivity to the vSphere environment.
The token expires after a configured TTL — users must re-login. Use `--insecure-skip-tls-verify` only during initial setup; trust the CA cert properly in production.

---

## TKG Workload Cluster Authentication (Pinniped + Dex)

TKG uses Pinniped as the Kubernetes authentication proxy, which federates OIDC/LDAP identity:

```bash
# Login to a TKG workload cluster (triggers OIDC flow through Pinniped)
kubectl vsphere login \
  --server https://supervisor.example.local \
  --username user@corp.local \
  --tanzu-kubernetes-cluster-name my-cluster \
  --tanzu-kubernetes-cluster-namespace my-namespace
```


```text title="Expected output"
Logging in to the vSphere Supervisor Cluster...
Waiting for OIDC provider to be ready...
Opening browser for authentication at: https://pinniped.supervisor.example.local/auth?client_id=tanzu-cli&redirect_uri=http://localhost:12345/callback
Authentication successful. Token received.
Connecting to Tanzu Kubernetes cluster 'my-cluster' in namespace 'my-namespace'...
Updating kubeconfig at /home/user/.kube/config
Added context 'my-cluster' to kubeconfig
Current context set to 'my-cluster'
You have access to the cluster. Try 'kubectl get nodes' to verify connectivity.
```

!!! warning "Common errors"
    **`error: the server has asked for the client to provide credentials`** — Ensure your vSphere SSO credentials are correct and your user account has permissions to access the Supervisor Cluster.
    **`error: unable to reach the Supervisor Cluster at https://supervisor.example.local`** — Verify the Supervisor Cluster hostname/IP is reachable and correct, and that your network allows HTTPS traffic to port 443.
    **`error: Tanzu Kubernetes cluster 'my-cluster' not found in namespace 'my-namespace'`** — Confirm the cluster name and namespace exist by running `kubectl get tanzukubernetesclusters -n my-namespace` on the Supervisor Cluster.
Configure Pinniped's upstream identity provider (LDAP example):

```yaml
# On the management cluster:
apiVersion: idp.supervisor.pinniped.dev/v1alpha1
kind: LDAPIdentityProvider
metadata:
  name: corp-ldap
  namespace: pinniped-supervisor
spec:
  host: ldaps://dc01.example.local:636
  tls:
    certificateAuthorityData: <base64-encoded-CA-cert>
  bind:
    secretName: ldap-bind-secret
  userSearch:
    base: DC=corp,DC=local
    filter: '(&(objectClass=user)(sAMAccountName={}))'
    attributes:
      username: sAMAccountName
      uid: objectGUID
  groupSearch:
    base: OU=Groups,DC=corp,DC=local
    filter: '(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={}))'
    attributes:
      groupName: sAMAccountName
```

---

## Harbor Authentication

```bash
# Harbor local admin
docker login harbor.example.local -u admin -p <password>

# Harbor with LDAP: configure in Harbor UI
# Administration → Configuration → Authentication
#   Auth Mode: LDAP
#   LDAP URL: ldap://dc01.example.local:389
#   LDAP Search DN: CN=svc-harbor,OU=ServiceAccounts,DC=corp,DC=local
#   LDAP Base DN: DC=corp,DC=local
#   LDAP Filter: objectClass=person
#   LDAP UID: sAMAccountName
```


```text title="Expected output"
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Login Succeeded
```

!!! warning "Common errors"
    **`Error response from daemon: Get "https://harbor.example.local/v2/": dial tcp: lookup harbor.example.local on 127.0.0.11:53: no such host`** — Verify Harbor hostname resolves in DNS or add an entry to `/etc/hosts` pointing to the Harbor registry IP.
    **`Error response from daemon: Get "https://harbor.example.local/v2/": x509: certificate signed by unknown authority`** — Add Harbor's self-signed certificate to your Docker daemon's trusted CA store or configure insecure registries in `/etc/docker/daemon.json`.
    **`LDAP Error: Connection refused`** — Confirm the LDAP server is reachable on port 389 from the Harbor pod and that the firewall allows outbound LDAP traffic.
---

## Service Account Tokens (Kubernetes)

```bash
# Create a service account and get its token (for CI/CD pipelines)
kubectl create serviceaccount ci-runner -n production

# Create token (v1.24+ — tokens are no longer auto-created)
kubectl create token ci-runner -n production --duration=8760h

# Create a rolebinding for the service account
kubectl create rolebinding ci-runner-edit \
  --clusterrole=edit \
  --serviceaccount=production:ci-runner \
  --namespace=production
```


```text title="Expected output"
serviceaccount/ci-runner created
eyJhbGciOiJIUzI1NiIsImtpZCI6IjZkNDI3YzhhLWY0ZTItNDc5Yi04YzU4LWEyMzQ1Njc4OWFiYyJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJwcm9kdWN0aW9uIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImNpLXJ1bm5lciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjI4ZjQ5YzAxLTkzZTItNDJhZi1iYjQ3LWI1YzM0ZjU2N2QyYSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpwcm9kdWN0aW9uOmNpLXJ1bm5lciJ9.xK8vN2pQrL9mW4jZ6tYhB3cDeFgHsJ5uI7oP1aX8nM9vQ2rS4wT5yU6zV7aB8cD9eF0gH1iJ2kL3mN4oP5qR6sT7uV8wX9yZ0aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV1wX2yZ3aB4cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0iJ1kL2mN3oP4qR5sT6uV7wX8yZ9aB0cD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4yZ5aB6cD7eF8gH9iJ0kL1mN2oP3qR4sT5uV6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV
```
---

## Pull Secret Management

```bash
# Create a Docker registry pull secret for Harbor
kubectl create secret docker-registry harbor-pull-secret \
  --docker-server=harbor.example.local \
  --docker-username=robot$ci-runner \
  --docker-password=<robot-account-secret> \
  --namespace=production

# Attach pull secret to default ServiceAccount in namespace
kubectl patch serviceaccount default -n production \
  -p '{"imagePullSecrets": [{"name": "harbor-pull-secret"}]}'

# Create robot account in Harbor (for pull-only CI use):
# Harbor UI → [Project] → Robot Accounts → Add Robot Account
#   Name: ci-runner
#   Permissions: pull
```


```text title="Expected output"
secret/harbor-pull-secret created
serviceaccount/default patched
```

!!! warning "Common errors"
    **`error: failed to create secret: secrets "harbor-pull-secret" already exists`** — Delete the existing secret with `kubectl delete secret harbor-pull-secret -n production` before recreating it.
    **`error: the server doesn't have a resource type "serviceaccount"`** — Verify you are connected to the correct Kubernetes cluster with `kubectl cluster-info` and that the production namespace exists.
    **`error: unable to parse '{"imagePullSecrets": [{"name": "harbor-pull-secret"}]}'`** — Ensure the JSON is properly escaped; use single quotes around the entire patch argument and double-check bracket/brace matching.
---

## OIDC for Harbor

```text
Harbor UI → Administration → Configuration → Authentication
  Auth Mode: OIDC
  OIDC Provider Name: Workspace ONE
  OIDC Endpoint: https://vidm.example.local/SAAS/auth/oauthtoken
  OIDC Client ID: harbor-oidc-client
  OIDC Client Secret: <client-secret>
  Group Claim Name: groups
  OIDC Scope: openid,profile,email,groups
  Verify Certificate: Yes
  Auto-onboard: Yes (create Harbor user on first OIDC login)
```

---

## Admin Kubeconfig Security

```bash
# Admin kubeconfig (tanzu cluster kubeconfig get --admin) embeds long-lived certs
# Store admin kubeconfigs in secrets manager — not on developer workstations
# Use non-admin OIDC login for day-to-day operations

# Restrict who can get admin kubeconfig:
# Only cluster-admins should run: tanzu cluster kubeconfig get --admin
# Others use OIDC login: tanzu cluster kubeconfig get (no --admin flag)
```
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

## See also

- [Tanzu — Access Control](../access-control/)
- [Tanzu — Hardening](../hardening/)

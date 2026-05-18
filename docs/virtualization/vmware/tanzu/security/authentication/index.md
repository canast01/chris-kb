# Tanzu — Authentication

```
┌──────────────── Tanzu Authentication Flow ─────────────────────────────────────┐
│                                                                                 │
│  User / CI/CD pipeline                                                          │
│      │  kubectl vsphere login --server https://supervisor.corp.local            │
│      ▼                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Pinniped Supervisor (management cluster)                                │  │
│  │  LDAPIdentityProvider ──► AD/LDAP ──► sAMAccountName / group search     │   │
│  └────────────────────────────────────┬─────────────────────────────────────┘  │
│                                        │ OIDC token exchange                    │
│  ┌────────────────────────────────────▼──────────────────────────────────────┐ │
│  │  Pinniped Concierge (per workload cluster)                                │ │
│  │  JWT token ──► kubeconfig ──► kubectl context                            │  │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  Token TTL: short-lived (re-login when expired)                                 │
│  Admin kubeconfig (--admin flag): long-lived cert ── store in secrets manager  │
│                                                                                 │
│  Harbor: LDAP / OIDC (vIDM) │ robot accounts for CI pull secrets               │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Supervisor Authentication (vSphere with Tanzu)

Users authenticate to the Supervisor cluster using vCenter SSO credentials:

```bash
kubectl vsphere login \
  --server https://supervisor.corp.local \
  --username user@corp.local \
  --insecure-skip-tls-verify
# Prompts for password
# Creates OIDC kubeconfig entry with short-lived token
```

The token expires after a configured TTL — users must re-login. Use `--insecure-skip-tls-verify` only during initial setup; trust the CA cert properly in production.

---

## TKG Workload Cluster Authentication (Pinniped + Dex)

TKG uses Pinniped as the Kubernetes authentication proxy, which federates OIDC/LDAP identity:

```bash
# Login to a TKG workload cluster (triggers OIDC flow through Pinniped)
kubectl vsphere login \
  --server https://supervisor.corp.local \
  --username user@corp.local \
  --tanzu-kubernetes-cluster-name my-cluster \
  --tanzu-kubernetes-cluster-namespace my-namespace
```

Configure Pinniped's upstream identity provider (LDAP example):

```yaml
# On the management cluster:
apiVersion: idp.supervisor.pinniped.dev/v1alpha1
kind: LDAPIdentityProvider
metadata:
  name: corp-ldap
  namespace: pinniped-supervisor
spec:
  host: ldaps://dc01.corp.local:636
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
docker login harbor.corp.local -u admin -p <password>

# Harbor with LDAP: configure in Harbor UI
# Administration → Configuration → Authentication
#   Auth Mode: LDAP
#   LDAP URL: ldap://dc01.corp.local:389
#   LDAP Search DN: CN=svc-harbor,OU=ServiceAccounts,DC=corp,DC=local
#   LDAP Base DN: DC=corp,DC=local
#   LDAP Filter: objectClass=person
#   LDAP UID: sAMAccountName
```

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

---

## Pull Secret Management

```bash
# Create a Docker registry pull secret for Harbor
kubectl create secret docker-registry harbor-pull-secret \
  --docker-server=harbor.corp.local \
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

---

## OIDC for Harbor

```
Harbor UI → Administration → Configuration → Authentication
  Auth Mode: OIDC
  OIDC Provider Name: Workspace ONE
  OIDC Endpoint: https://vidm.corp.local/SAAS/auth/oauthtoken
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

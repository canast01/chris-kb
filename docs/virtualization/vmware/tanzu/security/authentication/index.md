# Tanzu — Authentication


<div class="kb-summary">
Authentication reference covering Supervisor Authentication (vSphere with Tanzu), TKG Workload Cluster Authentication (Pinniped + Dex), Harbor Authentication, Service Account Tokens (Kubernetes), Pull Secret Management and 3 more sections.
</div>
```text
┌──────────────────────────── Virtualization Vmware Tanzu — Authentication ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Vmware authentication: local accounts, LDAP/AD, RADIUS, and SAML SSO options         │   │
│   │        MFA: time-based OTP or hardware token required for all privileged admin accounts       │   │
│   │         Service accounts: dedicated accounts for automation; API tokens/keys preferred        │   │
│   │       Session: idle timeout enforced; concurrent session limits for admin role accounts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Login → authenticate LDAP/SAML/local → MFA → authorise role → session                              │
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
│   │      Method      │     Use case     │  Config location  │       MFA        │     Priority     │   │
│   │     LDAP/AD      │  Staff accounts  │   Auth settings   │     Required     │     Primary      │   │
│   │     SAML SSO     │    Federated     │    SSO settings   │   IdP-enforced   │    Preferred     │   │
│   │      Local       │   Break-glass    │    Local users    │     Required     │  Emergency only  │   │
│   │    API token     │    Automation    │  Service account  │   N/A (token)    │    Automation    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Tanzu infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Tanzu platform overview and core concepts               │
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

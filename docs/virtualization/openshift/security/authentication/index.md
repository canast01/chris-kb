# OpenShift — Authentication

<div class="kb-summary">
OpenShift OAuth server, identity providers (LDAP, HTPasswd, OIDC/GitHub), token management, and disabling the default kubeadmin account after production setup.
</div>

```text
┌──────────────────────────────────── OpenShift Authentication Flow ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   oc login / browser → OAuth server (openshift-authentication namespace)                      │   │
│   │   OAuth server delegates to configured IdentityProvider (LDAP, HTPasswd, OIDC)               │    │
│   │   On success: OAuth token issued; used as Bearer token for API calls                          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    User → oc login → OAuth server → LDAP bind → success → token → kube-apiserver (Bearer token)       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      HTPasswd (local)       │  │     LDAP / Active Directory  │  │     OpenID Connect          │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  File-based user store      │  │  Binds against AD/LDAP        │  │  Okta, Azure AD, Keycloak  │  │
│   │  For break-glass / lab      │  │  Group sync via oc adm        │  │  PKCE flow supported        │ │
│   │  Store as OCP Secret        │  │  Bind DN required for search  │  │  claims mapped to identity │  │
│   │  No MFA support             │  │  TLS recommended              │  │  MFA via IdP               │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OAuth server  = Built-in OCP OAuth2 server in openshift-authentication namespace                   │
│    IdentityProvider= Configuration mapping login method → user identity in OCP                        │
│    kubeadmin    = Default bootstrap admin; delete after configuring production identity provider      │
│    Bearer token  = OAuth access token passed as Authorization: Bearer header to API                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## HTPasswd Identity Provider

```bash
# Create htpasswd file
htpasswd -c -B htpasswd.file alice
htpasswd -B htpasswd.file bob

# Create OCP Secret from htpasswd file
oc create secret generic htpass-secret \
  --from-file=htpasswd=htpasswd.file \
  -n openshift-config

# Configure OAuth CR
oc apply -f - <<EOF
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: htpasswd
    type: HTPasswd
    htpasswd:
      fileData:
        name: htpass-secret
EOF

# Add/remove users from htpasswd file later
oc get secret htpass-secret -n openshift-config -o jsonpath='{.data.htpasswd}' | base64 -d > htpasswd.file
htpasswd -B htpasswd.file carol
oc create secret generic htpass-secret \
  --from-file=htpasswd=htpasswd.file \
  -n openshift-config --dry-run=client -o yaml | oc replace -f -
```

## LDAP Identity Provider

```bash
# Create bind password secret
oc create secret generic ldap-bind-password \
  --from-literal=bindPassword='<password>' \
  -n openshift-config

# Create CA cert configmap (if using LDAPS)
oc create configmap ldap-ca \
  --from-file=ca.crt=ldap-ca.crt \
  -n openshift-config

# Configure LDAP OAuth
oc apply -f - <<EOF
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: ldap
    type: LDAP
    ldap:
      url: "ldaps://ad.example.com/CN=Users,DC=example,DC=com?sAMAccountName"
      bindDN: "CN=svc-ocp,OU=ServiceAccounts,DC=example,DC=com"
      bindPassword:
        name: ldap-bind-password
      insecure: false
      ca:
        name: ldap-ca
      attributes:
        id: ["dn"]
        email: ["mail"]
        name: ["cn"]
        preferredUsername: ["sAMAccountName"]
EOF
```

## OpenID Connect (OIDC)

```bash
# Create client secret
oc create secret generic oidc-client-secret \
  --from-literal=clientSecret='<oidc-client-secret>' \
  -n openshift-config

oc apply -f - <<EOF
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: okta
    type: OpenID
    openID:
      clientID: "0oa1b2c3d4e5"
      clientSecret:
        name: oidc-client-secret
      issuer: "https://dev-12345.okta.com"
      claims:
        preferredUsername: ["email"]
        name: ["name"]
        email: ["email"]
        groups: ["groups"]
EOF
```

## Post-Setup: Disable kubeadmin

```bash
# Only after: at least one admin user confirmed working via LDAP/OIDC/HTPasswd
# Verify you can log in as cluster-admin via new IDP
oc login -u alice -p password

# Grant cluster-admin to the new admin
oc adm policy add-cluster-role-to-user cluster-admin alice

# Confirm alice can perform admin operations
oc get nodes
oc get co

# Remove kubeadmin secret (irreversible without full etcd restore)
oc delete secret kubeadmin -n kube-system
```

## Token Management

```bash
# View current token
oc whoami --show-token

# Create long-lived service account token (for automation)
oc create token myapp-sa -n my-project --duration=8760h   # 1 year

# List active OAuth tokens (admin)
oc get oauthaccesstokens

# Revoke a specific token
oc delete oauthaccesstoken <token-name>

# Token TTL (default 24h access, 30d refresh)
oc get oauth cluster -o yaml | grep -A5 tokenConfig
```

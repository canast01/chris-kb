---
tags:
  - security
description: "OpenShift OAuth server, identity providers (LDAP, HTPasswd, OIDC/GitHub), token management, certificate auth, session revocation, and disabling the..."
---
# OpenShift — Authentication

<div class="kb-summary">
OpenShift OAuth server, identity providers (LDAP, HTPasswd, OIDC/GitHub), token management, certificate auth, session revocation, and disabling the default kubeadmin account after production setup.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

A: "User / oc login" {shape: rectangle}
B: "OAuth Server\nopenshift-authentication" {shape: rectangle}
C: "C" {shape: rectangle}
D: "htpasswd file\nin Secret" {shape: rectangle}
E: "LDAP Bind\nDN lookup" {shape: rectangle}
F: "External IdP\nOkta / Azure AD" {shape: rectangle}
G: "Identity verified" {shape: rectangle}
H: "OAuth token issued\n24h default TTL" {shape: rectangle}
I: "oc login stores token\nin ~/.kube/config" {shape: rectangle}
J: "API requests\nAuthorization: Bearer token" {shape: rectangle}

A -> B
C -> D
C -> E
C -> F
D -> G
E -> G
F -> G
G -> H
H -> I
I -> J
```

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "OpenShift" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

note over SVC
  HTPasswd Identity Provider
  LDAP Identity Provider
  OpenID Connect (OIDC)
end note

@enduml
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## HTPasswd Identity Provider

```bash
# Create htpasswd file with bcrypt hashing (-B flag)
htpasswd -c -B htpasswd.file alice
htpasswd -B htpasswd.file bob

# Create OCP Secret from htpasswd file
oc create secret generic htpass-secret \
  --from-file=htpasswd=htpasswd.file \
  -n openshift-config

# Configure OAuth CR to use HTPasswd provider
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
```


```text title="Expected output"
New password: 
Re-type new password: 
Adding password for user bob
secret/htpass-secret created
oauth.config.openshift.io/cluster configured
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `htpasswd: cannot open file htpasswd.file for read` | Remove the `-c` flag from the second htpasswd command, as `-c` creates a new file and overwrites existing entries. |
    | `error: unable to recognize "STDIN": no matches for kind "OAuth" in version "config.openshift.io/v1"` | Verify the OpenShift cluster version supports the OAuth API; use `oc api-resources | grep oauth` to confirm availability. |
### HTPasswd Update Procedure

Adding or removing users requires updating the Secret in-place — the OAuth server watches for changes.

```bash
# 1. Extract current htpasswd file from the Secret
oc get secret htpass-secret -n openshift-config \
  -o jsonpath='{.data.htpasswd}' | base64 -d > /tmp/users.htpasswd

# 2. Add a new user
htpasswd -bB /tmp/users.htpasswd newuser MyP@ssw0rd

# 3. Delete an existing user
htpasswd -D /tmp/users.htpasswd olduser

# 4. Update the Secret (OAuth pods reload automatically)
oc set data secret/htpass-secret \
  --from-file=htpasswd=/tmp/users.htpasswd \
  -n openshift-config

# 5. Confirm OAuth pods restarted
oc rollout status deployment/oauth-openshift -n openshift-authentication
```


```text title="Expected output"
system:admin:$2y$05$8Kz7p9mQ2xL1vN4rT6sJ8eH3jK0wP5qR2yM9nL7vB4cD1eF6gH5Oi
olduser:$2y$05$9Lm2k8pQ3xN0vM5sU7tK9fI4jL1xQ6rS3zN0oM8wC5dE2fG7hI6Pj
Adding password for user newuser
Deleting user olduser
secret/htpass-secret data updated
deployment "oauth-openshift" successfully rolled out
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `htpasswd: cannot open file /tmp/users.htpasswd for read` | Ensure the base64 decode step completed successfully and the file exists before running htpasswd commands. |
    | `error: the server doesn't have a resource type "secret"` | Verify you are connected to the correct cluster with `oc cluster-info` and that the htpass-secret exists in openshift-config namespace. |
    | `error: deployment.apps "oauth-openshift" not found` | Check that the OAuth deployment exists with `oc get deployment -n openshift-authentication` and wait for the pods to stabilize after the secret update. |
## LDAP Identity Provider

```bash
# Create bind password secret
oc create secret generic ldap-bind-password \
  --from-literal=bindPassword='<password>' \
  -n openshift-config

# Create CA cert configmap (required for LDAPS)
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


```text title="Expected output"
secret/ldap-bind-password created
configmap/ldap-ca created
oauth.config.openshift.io/cluster configured
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to read ca.crt: no such file or directory` | Ensure the ldap-ca.crt file exists in your current working directory before running the configmap creation command. |
    | `error: unable to authenticate to LDAP server at ldaps://ad.example.com: x509: certificate signed by unknown authority` | Verify the CA certificate in ldap-ca.crt matches the LDAP server's certificate chain, or set `insecure: true` temporarily for testing only. |
    | `error: the server doesn't have a resource type "oauth" in group "config.openshift.io"` | Confirm you are connected to an OpenShift 4.x cluster with sufficient permissions (cluster-admin role required) to modify OAuth configuration. |
## OpenID Connect (OIDC)

OIDC providers (Okta, Azure AD, Keycloak, Dex) issue JWTs verified by the OAuth server. MFA is handled entirely by the external IdP.

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


```text title="Expected output"
secret/oidc-client-secret created
oauth.config.openshift.io/cluster configured
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: failed to create secret: secrets "oidc-client-secret" already exists` | Delete the existing secret with `oc delete secret oidc-client-secret -n openshift-config` before recreating it, or use `oc patch` to update it instead. |
    | `error: unable to recognize "": no matches for kind "OAuth" in version "config.openshift.io/v1"` | Verify the OpenShift cluster version supports this OAuth API by running `oc api-resources | grep oauth` and check cluster compatibility documentation. |
    | `The OAuth server is not available` | Wait 2-3 minutes for the OAuth operator to reconcile the configuration, then verify with `oc get oauth cluster -o yaml` to check the status conditions. |
### OIDC Token Refresh Behavior

OCP issues its own OAuth tokens (not the OIDC JWT). The OAuth token defaults to 24 h TTL. The OIDC session at the external IdP is separate — on token expiry, the user must re-authenticate through the OIDC flow. Refresh tokens are issued by OCP with a 30-day TTL (configurable via `tokenConfig`).

```bash
# View token TTL configuration
oc get oauth cluster -o yaml | grep -A10 tokenConfig

# Extend access token TTL (example: 48h)
oc patch oauth cluster --type=merge \
  -p '{"spec":{"tokenConfig":{"accessTokenMaxAgeSeconds":172800}}}'
```


```text title="Expected output"
tokenConfig:
  accessTokenInactivityTimeoutSeconds: 300
  accessTokenMaxAgeSeconds: 3600
  authorizeTokenMaxAgeSeconds: 300
  authorizeTokenInactivityTimeoutSeconds: 300
oauth.oauth.openshift.io/cluster patched
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "oauth" in group "oauth.openshift.io"` | Verify you are connected to an OpenShift cluster with `oc cluster-info` and have the correct API group installed. |
    | `Error from server (Forbidden): oauths.oauth.openshift.io "cluster" is forbidden: User "system:serviceaccount:default:deployer" cannot patch resource "oauths" in API group "oauth.openshift.io" at the cluster scope` | Use a cluster-admin account or bind the necessary RBAC role with `oc adm policy add-cluster-role-to-user cluster-admin <username>`. |
## Certificate-Based Authentication

Client certificates signed by the cluster CA are used by system components (scheduler, controller-manager, kubelets). Also useful for scripted automation that cannot interactively authenticate.

```bash
# Generate client cert config for a scripting user (uses cluster CA)
oc adm create-api-client-config \
  --certificate-authority=/etc/kubernetes/pki/ca.crt \
  --client-dir=/tmp/robot-certs \
  --user=robot-user \
  --groups=system:masters

# The resulting kubeconfig can be used without interactive login
export KUBECONFIG=/tmp/robot-certs/kubeconfig
oc get nodes

# Check which cert a component is using
oc get secret -n openshift-kube-controller-manager \
  kube-controller-manager-client-cert-key -o yaml
```


```text title="Expected output"
creating client certificate config in /tmp/robot-certs
wrote kubeconfig to /tmp/robot-certs/kubeconfig
wrote client cert to /tmp/robot-certs/robot-user.crt
wrote client key to /tmp/robot-certs/robot-user.key

NAME                                    STATUS   ROLES    AGE   VERSION
master-01.prod.internal                 Ready    master   127d  v1.27.6+f67aeb7
master-02.prod.internal                 Ready    master   126d  v1.27.6+f67aeb7
worker-01.prod.internal                 Ready    worker   89d   v1.27.6+f67aeb7
worker-02.prod.internal                 Ready    worker   89d   v1.27.6+f67aeb7

apiVersion: v1
kind: Secret
metadata:
  name: kube-controller-manager-client-cert-key
  namespace: openshift-kube-controller-manager
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURZakNDQWtvQ0NRRDJzMjRwVEg3...
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBM1...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: certificate authority file "/etc/kubernetes/pki/ca.crt" does not exist` | Verify the CA certificate path matches your cluster's PKI directory (often `/etc/kubernetes/pki` on control planes or mounted in containers). |
    | `error: unable to read certificate authority file: permission denied` | Run the command with appropriate privileges (sudo or as a user with read access to the PKI directory). |
    | `error: the server doesn't have a resource type "secret" in group ""` | Ensure you are connected to a valid OpenShift cluster and the kube-controller-manager namespace exists; check your KUBECONFIG context. |
## Token Management

### Checking and Rotating Tokens

```bash
# View current token stored in kubeconfig
oc config view --minify -o jsonpath='{.users[0].user.token}'

# Show token for the current session
oc whoami --show-token

# Create a short-lived bound service account token
oc create token myapp-sa -n my-project --expiration=3600    # 1 hour
oc create token myapp-sa -n my-project --expiration=86400   # 24 hours

# Legacy secret-based tokens (no expiry — avoid for new workloads)
oc get secret -n my-project | grep myapp-sa-token
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJvcGVuc2hpZnQtYXV0aGVudGljYXRpb24iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiYnVpbGRlci10b2tlbi1kdGo2aCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZWFjY291bnQubmFtZSI6ImJ1aWxkZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2VhY2NvdW50LnVpZCI6IjU4YzZkNzk5LWY0YTItNDcwYS04ZjA5LWE3ZDJmYzQ1YzEyYyJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJvcGVuc2hpZnQtYXV0aGVudGljYXRpb24iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiYnVpbGRlci10b2tlbi1kdGo2aCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZWFjY291bnQubmFtZSI6ImJ1aWxkZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2VhY2
```
### Service Account Token Types

| Type | Expiry | Audience | Created by |
|---|---|---|---|
| Legacy secret token | Never | Any | `kubernetes.io/service-account-token` Secret |
| Bound projected token | Configurable (default 1h) | Specific audience | `oc create token` or `volumes.projected.serviceAccountToken` |
| OCP OAuth token | 24h default | API server | `oc login` / OAuth flow |

### Listing and Revoking Tokens

```bash
# List all active OAuth access tokens (cluster-admin only)
oc get oauthaccesstokens

# Filter by user
oc get oauthaccesstokens -o json | \
  jq '.items[] | select(.userName=="alice") | {name: .metadata.name, expires: .expiresIn}'

# Revoke a specific token (immediate effect)
oc delete oauthaccesstoken <token-name>

# Revoke all tokens for a user (force re-login)
oc get oauthaccesstokens -o json | \
  jq -r '.items[] | select(.userName=="alice") | .metadata.name' | \
  xargs oc delete oauthaccesstoken

# Invalidate current session (client-side)
oc logout
```


```text title="Expected output"
NAME                             USERNAMES        CREATED              EXPIRES
sha256~abc123def456ghi789jkl     alice            2024-01-15T10:22:33Z 2024-01-22T10:22:33Z
sha256~xyz789uvw456rst123opq     bob              2024-01-14T14:55:12Z 2024-01-21T14:55:12Z
sha256~mnop456qrs789tuv012wxyz   alice            2024-01-13T09:11:44Z 2024-01-20T09:11:44Z
sha256~efgh012ijk345lmn678opqr   charlie          2024-01-12T16:33:21Z 2024-01-19T16:33:21Z

{
  "name": "sha256~abc123def456ghi789jkl",
  "expires": 604800
}
{
  "name": "sha256~mnop456qrs789tuv012wxyz",
  "expires": 604800
}

oauthaccesstoken.oauth.openshift.io "sha256~abc123def456ghi789jkl" deleted

oauthaccesstoken.oauth.openshift.io "sha256~abc123def456ghi789jkl" deleted
oauthaccesstoken.oauth.openshift.io "sha256~mnop456qrs789tuv012wxyz" deleted

Logging out...
Removed config entry for context "default/api-prod-cluster-01:6443/system:admin"
Logged out.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error from server (Forbidden): oauthaccesstokens.oauth.openshift.io is forbidden: User "alice" cannot list resource "oauthaccesstokens"` | Run the command with cluster-admin credentials or request a cluster administrator to execute the token revocation. |
    | `error: the server doesn't have a resource type "oauthaccesstoken"` | Verify the OpenShift API version supports OAuth token management (requires OpenShift 4.x) and check that the OAuth API server is running with `oc get clusteroperators | grep oauth`. |
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


```text title="Expected output"
Login successful.

You have access to 67 projects, the list has been truncated. You can list all projects with 'oc projects'

Using project "default".
clusterrolebinding.rbac.authorization.k8s.io/cluster-admin added: "alice"
NAME                                    STATUS   ROLES    AGE   VERSION
worker-01.prod.internal                 Ready    worker   45d   v1.27.8+4fab27b
worker-02.prod.internal                 Ready    worker   45d   v1.27.8+4fab27b
master-01.prod.internal                 Ready    master   46d   v1.27.8+4fab27b
master-02.prod.internal                 Ready    master   46d   v1.27.8+4fab27b
master-03.prod.internal                 Ready    master   46d   v1.27.8+4fab27b
NAME                                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
authentication                             4.13.12   True        False         False      2d      
baremetal                                  4.13.12   True        False         False      2d      
cloud-controller-manager                   4.13.12   True        False         False      2d      
secret "kubeadmin" deleted
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to connect to the server: dial tcp: lookup api.cluster.local on 8.8.8.8:53: no such host` | Verify the cluster API endpoint is reachable and your KUBECONFIG points to the correct cluster context. |
    | `Error from server (Forbidden): clusterrolebindings.rbac.authorization.k8s.io "cluster-admin" is forbidden: User "system:serviceaccount:kube-system:default" cannot create resource "clusterrolebindings"` | Ensure you are logged in as an existing cluster-admin user before attempting to grant cluster-admin to the new IDP user. |
    | `error: secrets "kubeadmin" not found` | The kubeadmin secret may have already been deleted in a previous operation; verify with `oc get secret -n kube-system | grep kubeadmin` before attempting deletion. |
## OAuth Configuration Reference

| Field | Description |
|---|---|
| `spec.tokenConfig.accessTokenMaxAgeSeconds` | OAuth token lifetime (default: 86400 = 24h) |
| `spec.tokenConfig.accessTokenInactivityTimeoutSeconds` | Idle timeout; token invalidated if unused |
| `spec.identityProviders[].mappingMethod` | `claim` (default) or `lookup`; controls user auto-provisioning |
| `spec.identityProviders[].name` | Display name shown on login page |

```bash
# Check OAuth server pod health
oc get pods -n openshift-authentication
oc logs -n openshift-authentication deployment/oauth-openshift | tail -50

# Check OAuth CR for all configured providers
oc get oauth cluster -o yaml

# List all identity objects created by login events
oc get identity

# List OCP user objects (auto-created on first login)
oc get users
```


```text title="Expected output"
NAME                                    READY   STATUS    RESTARTS   AGE
oauth-openshift-5d8c7f9b2-kl9m4         1/1     Running   0          12d
oauth-openshift-5d8c7f9b2-xr2pq         1/1     Running   0          12d
oauth-openshift-5d8c7f9b2-zt6nb         1/1     Running   0          12d
2024-01-15T09:23:14.521Z INFO  oauth-openshift: started successfully
2024-01-15T09:23:15.103Z INFO  Listening on 0.0.0.0:6443
2024-01-15T09:23:16.847Z INFO  OIDC provider initialized: issuer=https://oauth-openshift.openshift-authentication.svc:6443
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: ldap-provider
    type: LDAP
    ldap:
      url: ldap://ldap.example.com:389/cn=users,dc=example,dc=com
  - name: oidc-provider
    type: OpenID
    openID:
      clientID: openshift-client
      issuerURL: https://oidc.example.com
NAME                                          IDP NAME        IDP TYPE   USER NAME
ldap-user-1234567890abcdef                    ldap-provider   LDAP       jsmith
oidc-user-0987654321fedcba                    oidc-provider   OpenID     agarcia
system:serviceaccount:kube-system:default     -               -          -
NAME            UID                                    CREATION TIME
jsmith          12345678-1234-1234-1234-123456789abc   2024-01-10T14:22:33Z
agarcia         87654321-4321-4321-4321-abcdef123456   2024-01-12T08:15:47Z
kubeadmin       aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee   2023-12-01T06:00:00Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "oauth"` | Verify you are connected to an OpenShift cluster (not vanilla Kubernetes) with `oc cluster-info`. |
    | `No resources found in openshift-authentication namespace.` | Check that the openshift-authentication namespace exists and the OAuth operator is running with `oc get ns openshift-authentication` and `oc get clusteroperator authentication`. |
## See also

- [OpenShift — Access Control](../access-control/)
- [OpenShift — Hardening](../hardening/)

---
tags:
  - security
description: "etcd encryption at rest, Kubernetes secret encryption, TLS configuration, certificate management, Vault integration, image signature verification, and..."
---
# OpenShift — Encryption

<div class="kb-summary">
etcd encryption at rest, Kubernetes secret encryption, TLS configuration, certificate management, Vault integration, image signature verification, and custom PKI for OpenShift clusters.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

A: "Data at Rest" {shape: rectangle}
B: "etcd Encryption\nAPIServer CR: aescbc or aesgcm\nSecrets + ConfigMaps encrypted" {shape: rectangle}
C: "Data in Transit" {shape: rectangle}
D: "TLS — All API Traffic\nControl plane auto-managed\nIngress: custom wildcard cert" {shape: rectangle}
E: "Pod-Level Secrets" {shape: rectangle}
F: "App Secrets in Pods\nVault agent injector\nor Secrets Store CSI" {shape: rectangle}
G: "Storage" {shape: rectangle}
H: "CSI Volume Encryption\nProvider-managed keys\nor LUKS on RHCOS" {shape: rectangle}
I: "Encryption Layers" {shape: rectangle}

A -> B
C -> D
E -> F
G -> H
B -> I
D -> I
F -> I
H -> I
```

```d2
direction: down

encryption_options_reference: "Encryption Options Reference" {shape: rectangle}
enable_etcd_encryption_at_rest: "Enable etcd Encryption at Rest" {shape: rectangle}
custom_ingress_wildcard_certificate: "Custom Ingress (Wildcard) Certificate" {shape: rectangle}
custom_api_server_certificate: "Custom API Server Certificate" {shape: rectangle}
add_custom_ca_trust_bundle: "Add Custom CA Trust Bundle" {shape: rectangle}
secret_management_with_vault: "Secret Management with Vault" {shape: rectangle}

encryption_options_reference -> enable_etcd_encryption_at_rest: hardens
enable_etcd_encryption_at_rest -> custom_ingress_wildcard_certificate: hardens
custom_ingress_wildcard_certificate -> custom_api_server_certificate: hardens
custom_api_server_certificate -> add_custom_ca_trust_bundle: hardens
add_custom_ca_trust_bundle -> secret_management_with_vault: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption Options Reference

| Layer | Mechanism | Key Management | Configuration Location |
|---|---|---|---|
| etcd at rest | AES-GCM or AES-CBC | Auto-rotated by OCP | `APIServer` CR `spec.encryption.type` |
| API traffic | TLS 1.2/1.3 | Auto-managed by cluster-operators | Automatic; custom certs via `APIServer` CR |
| Ingress traffic | TLS wildcard cert | Manual rotation or cert-manager | `IngressController` CR `spec.defaultCertificate` |
| Pod secrets | Vault sidecar / CSI | Vault or external KMS | Vault policy + ServiceAccount annotation |
| Persistent volumes | CSI encryption or LUKS | Cloud KMS or RHCOS dm-crypt | StorageClass parameters |
| Image content | Signature verification | Sigstore / cosign keypairs | `ClusterImagePolicy` CR (OCP 4.13+) |

## Enable etcd Encryption at Rest

```bash
# Enable etcd encryption (encrypts Secrets and ConfigMaps in etcd)
# aesgcm: authenticated encryption — recommended
# aescbc: CBC mode — legacy; use only if aesgcm unsupported in your version
oc patch apiserver cluster --type merge \
  -p '{"spec":{"encryption":{"type":"aesgcm"}}}'

# Monitor progress (10-30 minutes on large clusters)
oc get apiserver cluster -o yaml | grep -A5 encryption

# Verify encryption is complete — check openshiftapiserver and kubeapiserver
oc get openshiftapiserver cluster -o yaml | grep -A10 encryption
oc get kubeapiserver cluster -o yaml | grep -A10 encryption
# Look for: Encrypted = true in conditions

# Confirm individual secret is encrypted in etcd
# Encrypted secrets carry this annotation:
oc get secret <name> -n <ns> -o yaml | \
  grep "etcd.encryption.kubernetes.io/hash"
# If the annotation is present → secret is stored encrypted in etcd

# Check encryption key status
oc get apiserver cluster -o jsonpath='{.status.conditions}' | python3 -m json.tool
```


```text title="Expected output"
apiserver.config.openshift.io/cluster patched
encryption:
  type: aesgcm
  migrationMode: immediate
  resources:
  - secrets
  - configmaps
status:
  conditions:
  - lastTransitionTime: "2024-01-15T14:32:18Z"
    message: "Encryption migration in progress: 45% complete"
    reason: EncryptionMigrationInProgress
    status: "True"
    type: EncryptionMigrationInProgress
  - lastTransitionTime: "2024-01-15T14:28:00Z"
    message: "Encryption enabled successfully"
    reason: EncryptionEnabled
    status: "True"
    type: Encrypted
encryption:
  type: aesgcm
  migrationMode: immediate
  resources:
  - secrets
  - configmaps
  state: Live
  conditions:
  - lastTransitionTime: "2024-01-15T14:35:22Z"
    message: "All resources encrypted"
    reason: EncryptionComplete
    status: "True"
    type: Encrypted
encryption:
  type: aesgcm
  migrationMode: immediate
  resources:
  - secrets
  - configmaps
  state: Live
  conditions:
  - lastTransitionTime: "2024-01-15T14:36:45Z"
    message: "All resources encrypted"
    reason: EncryptionComplete
    status: "True"
    type: Encrypted
etcd.encryption.kubernetes.io/hash: "sha256:a3f8d2c1e9b4f6a7c2d8e1f3a5b7c9d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0"
[
  {
    "lastTransitionTime": "2024-01-15T14:36:50Z",
    "message": "Encryption key rotation completed",
    "reason": "EncryptionKeyRotationComplete",
    "status": "True",
    "type": "EncryptionKeyRotationComplete"
  },
  {
    "lastTransitionTime": "2024-01-15T14:32:18Z",
    "message": "Encryption enabled and operational",
    "reason": "EncryptionOperational",
    "status": "True",
    "type": "EncryptionOperational"
  }
]
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "apiserver" in group "config.openshift.io"`** — Verify you are connected to an OpenShift 4.x cluster with `oc version` and confirm the API server CRD exists with `oc api-resources | grep apiserver`.
    **`Encrypted = false in conditions after 30+ minutes`** — Check etcd pod logs with `oc logs -n openshift-etcd etcd-<node>` for encryption errors and verify sufficient disk space with `oc describe node <node>`.
    **`etcd.encryption.kubernetes.io/hash annotation not found on secret`** — Wait for the encryption migration to complete (monitor with `oc get apiserver cluster -o jsonpath='{.status.conditions[?(@.
### etcd Encryption Key Rotation

Key rotation is automatic once encryption is enabled. OCP generates new keys periodically and re-encrypts all existing data. There is no manual rotation step required unless you are transitioning between algorithm types.

```bash
# Transition from aescbc to aesgcm (or to identity to disable)
oc patch apiserver cluster --type merge \
  -p '{"spec":{"encryption":{"type":"aesgcm"}}}'
# OCP will re-encrypt all data with new keys; monitor conditions
```


```text title="Expected output"
apiserver.config.openshift.io/cluster patched
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "apiserver" in group "config.openshift.io"`** — Verify you are connected to an OpenShift cluster with `oc cluster-info` and have sufficient permissions with `oc auth can-i patch apiserver`.
    **`Error from server (Forbidden): apiservers.config.openshift.io "cluster" is forbidden: User "system:serviceaccount:default:default" cannot patch resource "apiservers" in API group "config.openshift.io" at the cluster scope`** — Switch to a user with cluster-admin role using `oc login` with appropriate credentials or `oc adm policy add-cluster-role-to-user cluster-admin <username>`.
## Custom Ingress (Wildcard) Certificate

```bash
# 1. Create TLS secret with wildcard cert for *.apps.ocp.example.com
oc create secret tls custom-ingress-cert \
  --cert=wildcard.crt \
  --key=wildcard.key \
  -n openshift-ingress

# 2. Patch IngressController to use custom cert
oc patch ingresscontroller default -n openshift-ingress-operator \
  --type=merge \
  -p '{"spec":{"defaultCertificate":{"name":"custom-ingress-cert"}}}'

# 3. Verify router redeployed with new cert
oc get pods -n openshift-ingress -w

# 4. Verify cert served to clients
openssl s_client -connect console-openshift-console.apps.ocp.example.com:443 \
  </dev/null 2>/dev/null | openssl x509 -noout -subject -enddate
```


```text title="Expected output"
secret/custom-ingress-cert created
ingresscontroller.operator.openshift.io/default patched
NAME                              READY   STATUS    RESTARTS   AGE
router-default-5d8c9f4b2-kx9m2    1/1     Running   0          45s
router-default-5d8c9f4b2-lp2q8    1/1     Running   0          52s
subject=CN = *.apps.ocp.example.com, O = Example Inc, C = US
notAfter=Dec 15 10:23:45 2025 GMT
```

!!! warning "Common errors"
    **`error: tls.crt: no such file or directory`** — Ensure wildcard.crt and wildcard.key files exist in the current directory before running the create secret command.
    **`error: ingresscontroller.operator.openshift.io "default" not found`** — Verify the IngressController exists with `oc get ingresscontroller -n openshift-ingress-operator` and use the correct name.
    **`unable to load certificate`** — Confirm the certificate file is valid PEM format and the key matches the cert using `openssl x509 -in wildcard.crt -text -noout`.
## Custom API Server Certificate

```bash
# 1. Create TLS secret for api.ocp.example.com
oc create secret tls api-server-cert \
  --cert=api-server.crt \
  --key=api-server.key \
  -n openshift-config

# 2. Patch APIServer CR
oc patch apiserver cluster --type merge -p \
  '{"spec":{"servingCerts":{"namedCertificates":[{"names":["api.ocp.example.com"],"servingCertificate":{"name":"api-server-cert"}}]}}}'

# 3. Update kubeconfig after cert change
oc login https://api.ocp.example.com:6443

# 4. Update CA bundle in clients that verify the API cert
oc get cm kube-root-ca.crt -n openshift-config-managed -o yaml
```


```text title="Expected output"
secret/api-server-cert created
apiserver.config.openshift.io/cluster patched
Login successful.

You have access to the following projects and can switch between them with 'oc project <projectname>':

  * default
  * openshift-apiserver
  * openshift-config

Using project "default".
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-root-ca.crt
  namespace: openshift-config-managed
data:
  ca.crt: |
    -----BEGIN CERTIFICATE-----
    MIIDazCCAlOgAwIBAgIUK7m8z5+8vZ9K3pZ7xQ8vZ9K3pZ8wDQYJKoZIhvcNAQEL
    BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
    GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNDAxMTUxMDMwMDBaFw0yNTAx
    -----END CERTIFICATE-----
```

!!! warning "Common errors"
    **`error: unable to read certificate file "api-server.crt": no such file or directory`** — Verify the certificate and key files exist in the current directory with `ls -la api-server.crt api-server.key`.
    **`error: the server has asked for the client to provide credentials`** — Update your kubeconfig to trust the new certificate by downloading it from the cluster or adding the CA bundle to your local trust store.
    **`error: patch does not apply: spec.servingCerts not found`** — Ensure the APIServer CR exists and supports the servingCerts field by running `oc get apiserver cluster -o yaml` to verify the current schema.
## Add Custom CA Trust Bundle

```bash
# Add enterprise CA certificate for cluster-wide trust
oc create configmap custom-ca \
  --from-file=ca-bundle.crt=enterprise-ca.crt \
  -n openshift-config

oc patch proxy/cluster --type=merge \
  -p '{"spec":{"trustedCA":{"name":"custom-ca"}}}'

# CA propagates to all cluster components automatically
# Verify on a node:
oc debug node/<node> -- chroot /host -- \
  openssl verify -CAfile /etc/pki/tls/certs/ca-bundle.crt enterprise-ca.crt
```


```text title="Expected output"
configmap/custom-ca created
proxy.config.openshift.io/cluster patched
Entering debug mode for node/worker-node-02.prod.ocp.local. Type 'exit' to leave.
Starting pod/worker-node-02debug ...
Removing debug pod ...
Verify OK
```

!!! warning "Common errors"
    **`error: unable to read file "enterprise-ca.crt": no such file or directory`** — Ensure the enterprise CA certificate file exists in the current directory or provide the full path with `--from-file=ca-bundle.crt=/path/to/enterprise-ca.crt`.
    **`error: the server doesn't have a resource type "proxy"`** — Verify the cluster has the config.openshift.io API group available; this requires OpenShift 4.3+, and check that the proxy/cluster resource exists with `oc get proxy`.
    **`error: unable to connect to the server: dial tcp: lookup worker-node-02.prod.ocp.local on [IP]: no such host`** — Replace `<node>` with the actual node name from `oc get nodes` and ensure the node is in Ready state.
## Secret Management with Vault

Two integration patterns: sidecar injector (annotation-driven, no app changes) and CSI driver (projected volume, works with any workload).

### Vault Agent Sidecar Injector

```yaml
# Pod/Deployment annotation-based injection
# Prerequisites: Vault Agent Injector operator installed and Vault accessible
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "myapp"
        vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
        vault.hashicorp.com/agent-inject-template-config: |
          {{- with secret "secret/data/myapp/config" -}}
          DB_PASSWORD={{ .Data.data.password }}
          {{- end }}
```

```bash
# Configure Vault Kubernetes auth method
vault auth enable kubernetes
vault write auth/kubernetes/config \
  token_reviewer_jwt="$(oc exec -n vault vault-0 -- cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_host="https://kubernetes.default.svc:443" \
  kubernetes_ca_cert=@/tmp/cluster-ca.crt

# Create Vault role binding OCP service account
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=my-project \
  policies=myapp-policy \
  ttl=1h
```


```text title="Expected output"
Success! Enabled kubernetes auth method at: kubernetes/
Success! Data written to: auth/kubernetes/config
Success! Data written to: auth/kubernetes/role/myapp
```

!!! warning "Common errors"
    **`Error reading file: stat /tmp/cluster-ca.crt: no such file or directory`** — Extract the cluster CA certificate first with `oc extract secret/kube-root-ca.crt -n openshift-kube-apiserver --to=/tmp/`.
    **`Error writing data to auth/kubernetes/config: error validating token reviewer JWT: invalid bearer token`** — Ensure the vault-0 pod is running in the vault namespace and the service account has permission to review tokens with `oc adm policy add-cluster-role-to-user system:auth-delegator -z vault`.
    **`Error writing data to auth/kubernetes/role/myapp: permission denied`** — Verify you are authenticated to Vault with sufficient policy permissions using `vault token lookup` and check that your token has write access to `auth/kubernetes/role/*`.
### Secrets Store CSI Driver

```yaml
# SecretProviderClass pointing to Vault
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-db-creds
  namespace: my-project
spec:
  provider: vault
  parameters:
    vaultAddress: "https://vault.example.com"
    roleName: "myapp"
    objects: |
      - objectName: "db-password"
        secretPath: "secret/data/myapp/config"
        secretKey: "password"
```

## Image Signature Verification

OCP 4.13+ supports `ClusterImagePolicy` CRs backed by cosign/sigstore for verifying image provenance before scheduling.

```bash
# Create a ClusterImagePolicy that requires cosign signatures
oc apply -f - <<EOF
apiVersion: config.openshift.io/v1alpha1
kind: ClusterImagePolicy
metadata:
  name: require-signed-images
spec:
  scopes:
  - quay.io/myorg
  policy:
    rootOfTrust:
      policyType: PublicKey
      publicKey:
        keyData: <base64-encoded-public-key>
        rekorKeyData: <base64-encoded-rekor-key>
EOF

# Verify policy is active
oc get clusterimagepolicy

# ImageContentSourcePolicy: redirect image pulls to internal mirror
oc apply -f - <<EOF
apiVersion: operator.openshift.io/v1alpha1
kind: ImageContentSourcePolicy
metadata:
  name: mirror-config
spec:
  repositoryDigestMirrors:
  - source: registry.redhat.io
    mirrors:
    - mirror.example.com/redhat
  - source: quay.io
    mirrors:
    - mirror.example.com/quay
EOF
```


```text title="Expected output"
clusterimagepolicy.config.openshift.io/require-signed-images created
NAME                    AGE
require-signed-images   2s
imagecontentsourcepolicy.operator.openshift.io/mirror-config created
```

!!! warning "Common errors"
    **`error: resource mapping not found for name: "require-signed-images" namespace: "" from "": no matches for kind "ClusterImagePolicy" in version "config.openshift.io/v1alpha1"`** — Verify the ClusterImagePolicy CRD is installed by running `oc get crd | grep imagepolicy` and ensure your OpenShift version supports image signature verification (4.11+).
    **`error: unable to decode "": yaml: line 2: mapping values are not allowed in this context`** — Ensure the base64-encoded key values replace the placeholder strings exactly and contain no newlines; use `cat key.pub | base64 -w0` to encode without line breaks.
    **`The ImageContentSourcePolicy "mirror-config" is invalid: spec.repositoryDigestMirrors[0].mirrors: Invalid value: []string{nil}: must specify at least one mirror`** — Verify that `mirror.example.com/redhat` and `mirror.example.com/quay` are valid, accessible registry hostnames and not left as placeholders.
## cert-manager Operator

```bash
# Install cert-manager from OperatorHub, then:

# Let's Encrypt ClusterIssuer
cat <<EOF | oc apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
    - http01:
        ingress:
          class: openshift-default
EOF

# Request certificate
cat <<EOF | oc apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-app-cert
  namespace: my-app
spec:
  secretName: my-app-tls
  dnsNames:
  - myapp.apps.ocp.example.com
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
EOF

# Check certificate status
oc get certificate my-app-cert -n my-app
oc get certificaterequest -n my-app
oc describe certificate my-app-cert -n my-app | grep -A5 "Conditions"
```


```text title="Expected output"
clusterissuer.cert-manager.io/letsencrypt-prod created
certificate.cert-manager.io/my-app-cert created
NAME            READY   SECRET          AGE
my-app-cert     True    my-app-tls      2m34s
NAME                        READY   AGE
my-app-cert-1               True    2m31s
Conditions:
  Last Transition Time:  2024-01-15T14:23:47Z
  Message:               Certificate is up to date and has not expired
  Reason:                Ready
  Status:                True
  Type:                  Ready
```

!!! warning "Common errors"
    **`error: resource mapping not found for name: "letsencrypt-prod" namespace: "" from "STDIN": no matches for kind "ClusterIssuer" in version "cert-manager.io/v1"`** — Install cert-manager operator from OperatorHub first using `oc get operators | grep cert-manager` to verify installation.
    **`Certificate my-app-cert in namespace my-app is not ready: Waiting for HTTP-01 challenge propagation`** — Ensure the ingress class name matches your cluster's default ingress controller with `oc get ingressclass` and update the `class` field accordingly.
    **`error validating data: data[tls.crt] not found`** — Wait for the certificate to reach Ready status before referencing the secret; check progress with `oc describe certificaterequest -n my-app`.
## Certificate Lifecycle Reference

```bash
# List all cluster-internal TLS secrets managed by operators
oc get secret -A | grep "kubernetes.io/tls"

# Check expiry of a specific certificate
oc get secret <secret-name> -n <ns> -o jsonpath='{.data.tls\.crt}' | \
  base64 -d | openssl x509 -noout -enddate

# Force rotation of auto-managed control plane certs (use only if certs expired)
oc patch secret kube-apiserver-to-kubelet-signer \
  -n openshift-kube-apiserver-operator \
  -p '{"metadata":{"annotations":{"auth.openshift.io/certificate-not-after":null}}}'
# This triggers the cert operator to issue new certs; monitor with:
oc get co kube-apiserver -w
```


```text title="Expected output"
NAMESPACE                           NAME                                             TYPE                DATA   AGE
openshift-kube-apiserver           kube-apiserver-to-kubelet-signer                 kubernetes.io/tls   3      127d
openshift-kube-apiserver           kube-apiserver-csr-signer                        kubernetes.io/tls   3      127d
openshift-kube-controller-manager  kube-controller-manager-to-kubelet-signer        kubernetes.io/tls   3      127d
openshift-etcd                     etcd-peer-ca                                     kubernetes.io/tls   2      127d
openshift-service-ca               service-ca                                       kubernetes.io/tls   2      127d
openshift-ingress                  router-certs-default                             kubernetes.io/tls   2      89d
...

notAfter=Jan 15 14:32:18 2026 GMT

secret/kube-apiserver-to-kubelet-signer patched

NAME             AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
kube-apiserver   True        True          False      2m      CertificateRotation: Issuing new certificates
kube-apiserver   True        True          False      3m      CertificateRotation: Issuing new certificates
kube-apiserver   True        False         False      4m      Cluster operator is available
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "secret" or "secrets"`** — Verify you are connected to a valid OpenShift cluster with `oc cluster-info` and have cluster-admin permissions.
    **`error: Unexpected key in path: tls.crt`** — Use `tls\.crt` with escaped dot or change to `'{.data["tls.crt"]}'` in the jsonpath expression.
    **`command not found: openssl`** — Install openssl on your local machine with `apt-get install openssl` (Debian/Ubuntu) or `brew install openssl` (macOS).
## See also

- [OpenShift — Hardening](../hardening/)
- [OpenShift — Health Checks](../../operations/health-checks/)

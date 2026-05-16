# Tanzu — Encryption

---

## Kubernetes Secrets Encryption at Rest

By default, Kubernetes Secrets are stored in etcd as base64-encoded (not encrypted). Enable encryption:

```yaml
# On TKG management cluster — enable via cluster config:
ENCRYPT_CLUSTER_DATA: true

# For manual configuration, edit kube-apiserver flags:
# --encryption-provider-config=/etc/kubernetes/encryption-config.yaml

# encryption-config.yaml:
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-32-byte-key>
  - identity: {}
```

---

## TLS for All Kubernetes API Communication

All K8s API communication uses mTLS by default. For application-level TLS, use cert-manager:

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create a ClusterIssuer using a CA stored in a Secret
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: corp-ca-issuer
spec:
  ca:
    secretName: corp-ca-secret
EOF

# Request a certificate for an application
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
  namespace: production
spec:
  secretName: myapp-tls
  duration: 2160h  # 90 days
  renewBefore: 360h  # 15 days
  issuerRef:
    name: corp-ca-issuer
    kind: ClusterIssuer
  dnsNames:
  - myapp.corp.local
EOF
```

---

## vSAN Encryption for Persistent Volumes

Apply an encrypted storage policy to protect PV data at rest:

```
vCenter → Policies and Profiles → VM Storage Policies → Create
  Policy Name: vsan-encrypted
  Component: Encryption → Enable Encryption
  (requires KMS configured in vCenter)

Create StorageClass using this policy:
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: vsan-encrypted
provisioner: csi.vsphere.volume
parameters:
  storagepolicyname: "vsan-encrypted"
```

---

## Image Content Trust (Cosign)

Sign container images in Harbor using Cosign:

```bash
# Sign an image
cosign sign --key cosign.key harbor.corp.local/team-alpha/myapp:v1.0

# Verify a signature
cosign verify --key cosign.pub harbor.corp.local/team-alpha/myapp:v1.0

# Policy: require signed images (OPA Gatekeeper or Kyverno)
```

```yaml
# Kyverno policy — require Cosign-signed images
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-image-signature
    match:
      resources:
        kinds: [Pod]
    verifyImages:
    - imageReferences: ["harbor.corp.local/*"]
      attestors:
      - entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              <cosign-public-key>
              -----END PUBLIC KEY-----
```

---

## External Secrets (Vault Integration)

Avoid storing sensitive values in K8s Secrets — use External Secrets Operator to fetch from HashiCorp Vault:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: database-credentials
  data:
  - secretKey: password
    remoteRef:
      key: secret/production/database
      property: password
```

---

## RBAC to Restrict Secret Access

```bash
# Audit who can read secrets in a namespace
kubectl auth can-i get secrets --namespace production --as user@corp.local
kubectl auth can-i list secrets --namespace production --as user@corp.local

# Remove secret access from developer role (create custom ClusterRole)
# Do NOT give developers 'edit' ClusterRole if it includes secret access
# Use custom role excluding secrets:
kubectl create clusterrole dev-no-secrets \
  --verb=get,list,watch,create,update,patch,delete \
  --resource=deployments,services,configmaps,pods \
  --dry-run=client -o yaml
```

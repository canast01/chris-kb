# OpenShift — Encryption

<div class="kb-summary">
etcd encryption at rest, Kubernetes secret encryption, TLS configuration, certificate management, and custom PKI integration for OpenShift clusters.
</div>

```text
┌──────────────────────────────────── OpenShift Encryption ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   etcd encryption: enable on APIServer CR; AES-GCM or AES-CBC; applies to secrets/configmaps  │   │
│   │   All control plane TLS: auto-managed by cluster-operators; certs rotate automatically        │   │
│   │   Custom ingress cert: replace default wildcard *.apps cert with signed cert from enterprise CA│  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │    etcd Encryption at Rest  │  │     TLS Certificates         │  │     Secret Management       │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  APIServer.spec.encryption  │  │  Ingress: custom wildcard    │  │  External: Vault / AWS KMS  │  │
│   │  AES-GCM (recommended)      │  │  API server: custom SAN cert │  │  Sealed Secrets operator    │  │
│   │  Keys auto-rotated          │  │  CA trust bundle per cluster │  │  OCP Secrets encrypted post │  │
│   │  Applies to secrets, CMs    │  │  cert-manager operator avail │  │  etcd encryption enable     │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    AES-GCM      = Authenticated encryption; recommended over AES-CBC for etcd at-rest encryption      │
│    IngressController= OCP resource managing the router; references TLS secret for wildcard cert       │
│    APIServer CR = cluster.config.openshift.io/v1 APIServer; controls encryption and API TLS           │
│    cert-manager = Kubernetes operator that automates cert issuance and renewal via Let's Encrypt etc. │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Enable etcd Encryption at Rest

```bash
# Enable etcd encryption (encrypts Secrets and ConfigMaps in etcd)
oc patch apiserver cluster --type merge -p '{"spec":{"encryption":{"type":"aesgcm"}}}'

# Monitor progress (takes 10-30 minutes for large clusters)
oc get apiserver cluster -o yaml | grep -A5 encryption
oc get openshiftapiserver cluster -o yaml | grep -A10 "encryption"

# Verify encryption enabled
oc get secret -n openshift-config -o yaml | grep "encryption.apiserver.operator.openshift.io"
# Secrets will have annotation indicating they are encrypted

# Check encryption status
oc get etcd cluster -o yaml | grep -A20 "conditions"
```

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
openssl s_client -connect console-openshift-console.apps.ocp.example.com:443 </dev/null 2>/dev/null | \
  openssl x509 -noout -subject -enddate
```

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
oc login https://api.ocp.example.com:6443    # re-login to refresh
```

## Add Custom CA Trust Bundle

```bash
# Add enterprise CA certificate for cluster-wide trust
oc create configmap custom-ca \
  --from-file=ca-bundle.crt=enterprise-ca.crt \
  -n openshift-config

oc patch proxy/cluster --type=merge \
  -p '{"spec":{"trustedCA":{"name":"custom-ca"}}}'

# CA is now trusted by all cluster components
# Verify: oc debug node/<node> -- chroot /host -- cat /etc/pki/tls/certs/ca-bundle.crt
```

## cert-manager Operator

```bash
# Install cert-manager from OperatorHub
# Then create Issuer/ClusterIssuer and Certificate resources

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

oc get certificate my-app-cert -n my-app
oc get certificaterequest -n my-app
```

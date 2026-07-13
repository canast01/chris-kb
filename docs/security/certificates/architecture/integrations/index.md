---
tags:
  - architecture
  - security
description: "Venafi TPP (or TLS Protect Cloud) provides the centralised policy and automation layer across all certificate sources. ADCS serves as the enterprise CA..."
---
# Certificates — Integrations

<div class="kb-summary">
Venafi TPP (or TLS Protect Cloud) provides the centralised policy and automation layer across all certificate sources. ADCS serves as the enterprise CA backend for internal certificates.
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Certificate Integration Topology

```d2
direction: right

venafi: "Venafi TPP\n(central policy and lifecycle mgmt" {shape: rectangle}
adcs: "Microsoft ADCS\n(internal CA" {shape: rectangle}
vsphere: "VMware vSphere\n(auto-enrol ESXi / vCenter certs" {shape: rectangle}
f5: "F5 / NetScaler\n(LB cert deployment" {shape: rectangle}
snow: "ServiceNow\n(approval workflow" {shape: rectangle}
siem: "SIEM\n(issuance / revocation events" {shape: rectangle}
certManager: "cert-manager\n(Kubernetes in-cluster automation" {shape: rectangle}
leAcme: "Let's Encrypt ACME\n(public-facing services" {shape: rectangle}
hashiVault: "HashiCorp Vault PKI\n(service-to-service short-lived certs" {shape: rectangle}

venafi -> adcs
venafi -> vsphere
venafi -> f5
venafi -> snow
venafi -> siem
certManager -> leAcme
certManager -> hashiVault
certManager -> adcs
```

## Integration Map

| Integration | Purpose | Protocol |
|---|---|---|
| Venafi TPP ↔ ADCS | Issue internal certs via Microsoft CA | DCOM / RPC |
| Venafi TPP ↔ vSphere | Auto-enrol and renew vCenter/ESXi certs | REST API |
| Venafi TPP ↔ F5 / NetScaler | LB certificate deployment automation | REST + credential objects |
| Venafi TPP ↔ ServiceNow | Certificate request approval workflow | REST API |
| Venafi TPP ↔ SIEM | Issuance, renewal, revocation events | Syslog |
| HashiCorp Vault PKI | Short-lived certs for service-to-service mTLS | REST (Vault API) |
| cert-manager ↔ ADCS / Vault | Kubernetes in-cluster cert automation | ACME / Vault issuer |
| Let's Encrypt ACME | Public-facing service certificates | ACME (RFC 8555) |

## Venafi TPP — ADCS CA Integration

```powershell
# On the Venafi server — verify CA connector is reachable
# TPP UI → Configuration → Certificate Authorities → Test Connection

# ADCS template must have "Enroll" permission granted to the Venafi service account
# Certificate Templates → Right-click → Properties → Security → Add svc-venafi → Enroll
```

## HashiCorp Vault PKI

```bash
# Enable PKI secrets engine
vault secrets enable -path=pki pki
vault secrets tune -max-lease-ttl=87600h pki

# Generate or import CA
vault write pki/root/generate/internal common_name="corp.local Internal CA" ttl=87600h

# Create a role for issuing certs
vault write pki/roles/internal-services \
    allowed_domains="corp.local,svc.cluster.local" \
    allow_subdomains=true \
    max_ttl=720h

# Issue a certificate
vault write pki/issue/internal-services common_name="myservice.svc.cluster.local" ttl=168h
```


```text title="Expected output"
Success! Enabled the pki secrets engine at: pki/
Success! Tuned the secrets engine at: pki/
Key                     Value
---                     -----
certificate             -----BEGIN CERTIFICATE-----
                         MIIDnjCCAoYCCQDf8Z4ke7x1ODANBgkqhkiG9w0BAQsFADCBkDELMAkGA1UEBhMC
                         VVMxEzARBgNVBAgMCldhc2hpbmd0b24xEDAOBgNVBAcMB1NlYXR0bGUxEDAOBgNV
                         BAoMB0NvcnAgQ0ExGDAWBgNVBAsMD0ludGVybmFsIENBIFBLSTEhMB8GA1UEAwwY
                         Y29ycC5sb2NhbCBJbnRlcm5hbCBDQQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0t
issuing_ca              -----BEGIN CERTIFICATE-----
                         MIIDnjCCAoYCCQDf8Z4ke7x1ODANBgkqhkiG9w0BAQsFADCBkDELMAkGA1UEBhMC
                         ...
private_key             -----BEGIN RSA PRIVATE KEY-----
                         MIIEpAIBAAKCAQEA2x8vK3p9mQ4rT5kL8vN2pQ9xK3mZ6sT1wY8hJ2kP4vR6nM9p
                         ...
serial_number           df:f1:9e:24:7b:bc:75:38
Success! Data written to: pki/roles/internal-services
Key                Value
---                -----
certificate        -----BEGIN CERTIFICATE-----
                    MIIDpzCCAo+gAwIBAgIUZ7f9K2mN4xR8vK9pL2qT5sW8nN0wDQYJKoZIhvcNAQEL
                    BQAwgZAxCzAJBgNVBAYTAlVTMRMwEQYDVQQIDApXYXNoaW5ndG9uMRAwDgYDVQQH
                    DAdTZWF0dGxlMRAwDgYDVQQKDAdDb3JwIENBMRgwFgYDVQQLDA9JbnRlcm5hbCBD
                    QSBQS0kxITAfBgNVBAMMGGNvcnAubG9jYWwgSW50ZXJuYWwgQ0EwHhcNMjQwMTEy
                    MTUzMDQ1WhcNMjUwMTExMTUzMDQ1WjAtMSswKQYDVQQDEyJteXNlcnZpY2Uuc3Zj
                    LmN
```
## Kubernetes cert-manager

```yaml
# ClusterIssuer pointing at Vault PKI
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-issuer
spec:
  vault:
    server: https://vault.example.local:8200
    path: pki/sign/internal-services
    auth:
      kubernetes:
        role: cert-manager
        mountPath: /v1/auth/kubernetes
        serviceAccountRef:
          name: cert-manager
```

```bash
# Check certificate status in cluster
kubectl get certificates -A
kubectl describe certificate <name> -n <namespace>

# Check cert-manager logs for issuance errors
kubectl logs -n cert-manager deploy/cert-manager | tail -50
```


```text title="Expected output"
NAME                                    READY   SECRET                              AGE
ingress-tls-cert                        True    ingress-tls-secret                  45d
api-gateway-cert                        True    api-gateway-tls                     32d
internal-service-cert                   False   internal-service-tls                2d
webhook-cert                            True    webhook-tls-secret                  60d

Name:         api-gateway-cert
Namespace:    production
Labels:       app=api-gateway
Annotations:  cert-manager.io/issue-temporary-certificate: true
Status:
  Conditions:
    Last Transition Time:  2024-01-15T08:32:10Z
    Message:               Certificate is up to date and has not expired
    Reason:                Ready
    Status:                True
    Type:                  Ready
  Not After:               2025-04-15T08:32:09Z
  Not Before:              2024-01-15T08:32:09Z
  Renewal Time:            2025-03-16T08:32:09Z

I0115 14:22:45.123456   12847 controller.go:156] cert-manager/certificates controller synced successfully
I0115 14:22:46.234567   12847 sync.go:89] Syncing certificate default/tls-cert
I0115 14:22:47.345678   12847 issuer.go:201] Issuing certificate for "api.example.com"
I0115 14:22:52.456789   12847 acme.go:412] ACME challenge validation successful
I0115 14:22:53.567890   12847 sync.go:156] Certificate renewed successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "certificates"` | Ensure cert-manager CRDs are installed with `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.x.x/cert-manager.crds.yaml`. |
    | `Error from server (NotFound): certificates.cert-manager.io "<name>" not found` | Verify the certificate name and namespace are correct, and check that the certificate resource exists in the specified namespace. |
    | `Unable to connect to the server: dial tcp: lookup cert-manager on <IP>: no such host` | Confirm cert-manager pod is running with `kubectl get pods -n cert-manager` and that the cluster context is set correctly. |
## Let's Encrypt ACME (DNS-01 Challenge)

```bash
# Using certbot with Route53 DNS-01 challenge
certbot certonly \
  --dns-route53 \
  -d "*.corp.example.com" \
  --email certs@corp.example.com \
  --agree-tos \
  --non-interactive

# Auto-renewal via cron (certbot renew checks expiry < 30 days)
0 3 * * * /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx"
```


```text title="Expected output"
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator (dns-route53), Installer (None)
Starting new HTTPS connection (1): acme-v02.api.letsencrypt.org
Requesting a certificate for *.corp.example.com
Performing DNS-01 challenge for *.corp.example.com
Waiting for verification...
Cleaning up challenges
Subscribe to the EFF mailing list (email: certs@corp.example.com).

IMPORTANT NOTES:
 - Congratulations! Your certificate is ready at /etc/letsencrypt/live/corp.example.com/fullchain.pem
 - Your key file has been saved at /etc/letsencrypt/live/corp.example.com/privkey.pem
 - Your cert will expire on 2025-04-15. To automatically renew this cert in the future, run "certbot renew"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error while running dns-route53 for corp.example.com: Unable to locate credentials` | Ensure AWS credentials are configured via `aws configure` or IAM role is attached to the instance. |
    | `PluginError: dns-route53: Unexpected error determining Route53 hosted zone for corp.example.com` | Verify the Route53 hosted zone exists and the IAM user/role has `route53:ListHostedZones` and `route53:ChangeResourceRecordSets` permissions. |
    | `Error creating new order :: too many certificates already issued for exact set of domains` | Wait 7 days before retrying the same domain, or use `--force-renewal` only if certificate is expiring within 7 days. |
## ServiceNow Approval Workflow

Venafi TPP can trigger a ServiceNow workflow for certificates that require business approval:

1. Certificate request submitted via Venafi self-service portal or API.
2. TPP policy engine evaluates request — if approval required, raises a ServiceNow change/task.
3. Approver approves via ServiceNow → TPP receives callback → certificate issued.
4. Certificate deployed to target system via TPP driver.

## Expiry Alerting

```bash
# Check certificate expiry on a remote host
echo | openssl s_client -connect host.example.local:443 2>/dev/null | \
  openssl x509 -noout -dates

# Bulk expiry scan (Bash loop)
for host in vcenter nsxmgr aria-ops aria-auto; do
  expiry=$(echo | openssl s_client -connect ${host}.example.local:443 2>/dev/null | \
    openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "${host}: ${expiry}"
done
```


```text title="Expected output"
notBefore=Jan 15 08:23:47 2023 GMT
notAfter=Jan 15 08:23:47 2025 GMT
vcenter: Jan 15 08:23:47 2025 GMT
nsxmgr: Mar 22 14:56:12 2024 GMT
aria-ops: Dec 10 19:44:33 2025 GMT
aria-auto: Feb 28 11:18:05 2024 GMT
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `unable to get local issuer certificate` | Add the issuer's CA certificate to your system trust store or use `openssl s_client -connect host:443 -CAfile /path/to/ca.crt` to specify it explicitly. |
    | `connect: Connection refused` | Verify the host is reachable and HTTPS is listening on port 443 with `nc -zv host.example.local 443` before retrying. |
    | `(stdin) 1:error:0A000126:SSL routines:tls_choose_sigalg:no shared signature algorithms` | The remote host's TLS configuration is incompatible with your OpenSSL version; try adding `-tls1_2` flag to force a specific protocol version. |
Venafi TPP / Aria Operations integrations provide dashboard-level expiry visibility — raw CLI checks above are for ad-hoc verification.

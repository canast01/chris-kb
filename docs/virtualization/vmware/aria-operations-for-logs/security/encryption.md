---
tags:
  - aria-logs
  - security
  - vmware
---
# Aria Ops for Logs — Encryption

<div class="kb-summary">
Encryption reference covering TLS Certificate Replacement, Verifying Certificate Validity, Log Ingestion Transport Encryption, Data at Rest Encryption, TLS Configuration Hardening.

*Applies to: Aria Logs 8.x*
</div>
![Aria Ops for Logs — Encryption](../../../../assets/virtualization-vmware-aria-operations-for-logs-security-encr.svg)

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## TLS Certificate Replacement

Aria Operations for Logs ships with a self-signed certificate. Replace it with a CA-signed certificate for production before connecting any syslog sources or users.

**Via UI:**

---

## Log Ingestion Transport Encryption

Log data is forwarded to Aria Ops for Logs over several channels with varying encryption support:

| Protocol | Port | Encrypted | Recommended For |
|---|---|---|---|
| cfapi (TLS) | 9543 | Yes — TLS 1.2+ | LI Agent on Linux/Windows VMs |
| cfapi (no TLS) | 9000 | No | Lab only |
| Syslog TCP | 1514 | No (unless wrapped in TLS) | Legacy devices with TCP syslog |
| Syslog UDP | 514 | No | ESXi hosts (no TLS option on ESXi syslog) |

For sensitive environments, use the LI Agent (cfapi/TLS on port 9543) instead of raw syslog where possible. ESXi syslog over UDP 514 is accepted as a known limitation of the ESXi syslog implementation — ESXi does not support TLS for syslog.

Configure the LI Agent to use TLS:

```ini
# /var/lib/loginsight-agent/liagent.ini
[server]
hostname=vrli-prod-01.example.local
port=9543
proto=cfapi
ssl=yes
ssl_ca_path=/etc/ssl/certs/corp-ca.pem
```

---

## Data at Rest Encryption

Aria Ops for Logs stores log indices and raw data on the node's local disk (`/var/log/loginsight`). Native application-level encryption is not included. Apply encryption at the storage layer:

- **vSAN**: enable vSAN Data-at-Rest Encryption on the datastore hosting the VMs
- **SAN/NAS LUN encryption**: enable at the array level
- **VM Encryption (vSphere)**: encrypt the VM virtual disks via vSphere encryption policies

```powershell
# PowerCLI — verify if Aria Ops for Logs VMs have encrypted disks
Get-VM | Where-Object { $_.Name -like "vrli-*" } | Get-HardDisk |
  Select-Object @{N="VM";E={$_.Parent.Name}}, Name,
  @{N="Encrypted";E={$_.ExtensionData.Backing.KeyId -ne $null}}
```

---

## TLS Configuration Hardening

Ensure only TLS 1.2 and 1.3 are active. TLS 1.0 and 1.1 are disabled by default in Aria Ops for Logs 8.x.

Verify from an external scanner:

```bash
# Test that TLS 1.0 is rejected
openssl s_client -connect vrli-prod-01.example.local:443 -tls1 2>&1 | \
  grep -E "alert|error|CONNECTED"
# Expected: alert handshake failure (not CONNECTED)

# Confirm TLS 1.2 is accepted
openssl s_client -connect vrli-prod-01.example.local:443 -tls1_2 2>/dev/null | \
  grep "Protocol"
# Expected: Protocol : TLSv1.2
```


```text title="Expected output"
alert handshake failure
Protocol  : TLSv1.2
```

!!! warning "Common errors"
    **`unable to load client cert (no certs available)`** — Ensure the system's CA certificates are installed via `update-ca-certificates` or equivalent, or add `-CAfile /path/to/ca-bundle.crt` to the openssl command.
    **`connect: Connection refused`** — Verify the vrli-prod-01.example.local hostname resolves and port 443 is accessible; check DNS resolution with `nslookup vrli-prod-01.example.local` and firewall rules.
    **`Protocol  : TLSv1.0` (when TLS 1.0 should be rejected)`** — Disable TLS 1.0 on the Aria Operations for Logs appliance via the security settings in the web UI or by editing `/etc/ssl/openssl.cnf` to remove TLSv1 from the MinProtocol directive.
Use `testssl.sh` for a comprehensive scan before exposing the UI to any external network:

```bash
testssl.sh --severity HIGH vrli-prod-01.example.local:443
```


```text title="Expected output"
###########################################################
testssl.sh 3.2dev from https://github.com/drwetter/testssl.sh
(ec2c1f8 2024-01-15 22:47:42 UTC)

   This program is CAPTCHA-free, but please respect a certain amount of load,
   workflow is way too fast to be real. Doing up to 50 requests per second.

Testing vrli-prod-01.example.local:443 [10.42.18.55]

 Start 2024-01-22 14:32:10        -->> 10.42.18.55:443 (vrli-prod-01.example.local) <<--

 rDNS (10.42.18.55):     vrli-prod-01.example.local
 Service detected:       HTTPS

Certificate information:
 Subject:               CN=vrli-prod-01.example.local
 Issuer:                CN=VMware-Aria-CA,O=VMware Inc,C=US
 Public key type:       RSA
 Public key bits:       2048
 Signature algorithm:    sha256WithRSAEncryption
 Not valid before:      2023-11-10 08:15:00 UTC
 Not valid after:       2025-11-10 08:15:00 UTC

 HIGH SEVERITY FINDINGS:
 TLSv1.0                VULNERABLE (deprecated)
 TLSv1.1                VULNERABLE (deprecated)
 RC4                    VULNERABLE (weak cipher)

 Testing ciphers with "HIGH" and word "128" bits
 TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256   PASS
 TLS_RSA_WITH_AES_128_CBC_SHA             PASS

 End 2024-01-22 14:32:18        -->> 10.42.18.55:443 (vrli-prod-01.example.local) <<--

 Rating: C (WEAK)
```

!!! warning "Common errors"
    **`testssl.sh: command not found`** — Install testssl.sh from https://github.com/drwetter/testssl.sh or add it to your PATH.
    **`Unable to open a socket to vrli-prod-01.example.local:443`** — Verify the hostname resolves, the host is reachable, and port 443 is open (use `nc -zv vrli-prod-01.example.local 443`).
    **`SSL: CERTIFICATE_VERIFY_FAILED`** — This is expected for self-signed certificates in lab environments; testssl.sh will continue testing despite the verification failure.
## See also

- [Aria Ops for Logs — Hardening](../hardening/)
- [Aria Operations for Logs — Health Checks](../../operations/health-checks/)

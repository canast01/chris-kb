# IRE — Security

The IRE must maintain a higher security posture than production during a recovery operation, because production is compromised and the threat actor may still be active.

## Security Principles

| Principle | Implementation |
|---|---|
| **Assume breach of production** | No trust for any credential, token, or certificate from the production environment |
| **Least privilege** | IRE accounts scoped to minimum permissions needed for recovery tasks |
| **MFA everywhere** | Every IRE login requires MFA — no exceptions |
| **Audit everything** | All actions in the IRE are logged to an immutable audit store |
| **Time-limited access** | IRE accounts expire automatically; no permanent standing access |
| **No outbound internet** | IRE systems cannot initiate internet connections |

## Access Control

### IRE Account Provisioning

IRE accounts must be pre-provisioned before an incident — they cannot be created during an attack if identity infrastructure is compromised.

| Account type | Purpose | Storage |
|---|---|---|
| IRE admin (break-glass) | Full IRE management | Sealed envelope in physical safe; one per IRE lead |
| IR engineer accounts | Day-to-day recovery operations | Pre-created in IRE identity store |
| App team read-only | Business validation in clean room | Pre-created; scoped to clean room only |
| Backup system service account | Backup retrieval | Pre-created; read-only on backup store |

```powershell
# Verify IRE local admin accounts are not shared with production
$prodAdmins = (Invoke-Command -ComputerName prod-dc01 { Get-ADGroupMember Administrators }).Name
$ireAdmins  = (Invoke-Command -ComputerName ire-dc01  { Get-ADGroupMember Administrators }).Name
Compare-Object $prodAdmins $ireAdmins -IncludeEqual | Where-Object {$_.SideIndicator -eq "=="}
# Should return empty — no overlapping accounts
```

```bash
# Verify jump host has session recording enabled (example: HashiCorp Vault SSH helper)
vault secrets enable ssh
vault write ssh/config/ca generate_signing_key=true
vault write ssh/roles/ire-operator allow_user_certificates=true \
  default_extensions='{"permit-pty":"","permit-user-rc":""}' \
  key_type=ca max_ttl=4h

# All SSH sessions to IRE recorded via:
# - HashiCorp Vault SSH + tlog, or
# - CyberArk PSM, or
# - Azure Bastion (session recording in Storage Account)
```

## Certificate and Key Management

Do not import or use production certificates in the IRE.

```bash
# Generate fresh self-signed CA for IRE (valid only for recovery duration)
openssl genrsa -out ire-ca.key 4096
openssl req -new -x509 -key ire-ca.key -out ire-ca.crt -days 30 \
  -subj "/CN=IRE-CA-Temporary/O=IR-Team/C=AU"

# Issue IRE server certificates from this CA
openssl genrsa -out ire-server.key 2048
openssl req -new -key ire-server.key -out ire-server.csr \
  -subj "/CN=ire-mgmt.local/O=IR-Team"
openssl x509 -req -in ire-server.csr -CA ire-ca.crt -CAkey ire-ca.key \
  -CAcreateserial -out ire-server.crt -days 30
```

## Audit Logging

All IRE activity must be logged to an immutable store that is not accessible from production.

```bash
# Syslog forwarding to isolated log server (IRE-internal only)
# /etc/rsyslog.d/ire-audit.conf
*.* @@10.200.254.10:514   # IRE syslog server — no route to production

# Azure: route IRE activity logs to separate Log Analytics workspace
az monitor diagnostic-settings create \
  --resource /subscriptions/<ire-sub-id>/resourceGroups/ire-rg \
  --name "ire-audit" \
  --workspace <ire-log-analytics-workspace-id> \
  --logs '[{"category":"Administrative","enabled":true},{"category":"Security","enabled":true}]'
```

### Key Events to Monitor During Recovery

| Event | Log source | Alert |
|---|---|---|
| Failed login to IRE systems | Windows Security Event 4625 / Linux auth.log | Immediate alert if > 3 failures |
| Privilege escalation | Windows Event 4672 / sudo log | Alert on unexpected accounts |
| Outbound connection attempt | Firewall deny log | Alert on any denied outbound |
| New account created | AD event 4720 / useradd | Alert if not pre-authorized |
| Backup store access | Storage access log | Alert if accessed outside recovery window |

## Decommissioning the IRE

After recovery is complete:

1. Revoke all IRE credentials (including break-glass — generate new ones and re-seal).
2. Delete IRE VMs or revert to pre-recovery snapshot.
3. Archive audit logs to a long-term immutable store.
4. Conduct a lessons-learned review within 5 business days.
5. Update IRE runbooks with any gaps identified during the incident.

```bash
# Azure: deallocate and delete IRE VMs after sign-off
az vm list --resource-group ire-rg --output table
az vm delete --resource-group ire-rg --name <ire-vm> --yes --no-wait

# Rotate break-glass account passwords
$newPass = [System.Web.Security.Membership]::GeneratePassword(32, 6)
Set-ADAccountPassword -Identity ire-breakglass -NewPassword (ConvertTo-SecureString $newPass -AsPlainText -Force)
# Print and seal in envelope — never store in digital form
```

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| IRE account locked out | Pre-created password expired | Implement password-never-expires for break-glass; use PAM vault for engineer accounts |
| Audit logs inaccessible during incident | Log server in production network | Pre-deploy dedicated IRE log server; never rely on production SIEM during recovery |
| Jump host unavailable | Jump host in production VNet / compromised | Deploy jump host in IRE VNet; use cloud-based Bastion as backup access path |
| IRE systems joined to production AD | Pre-provisioning error | Unjoin from production domain; join IRE domain or use local accounts only |

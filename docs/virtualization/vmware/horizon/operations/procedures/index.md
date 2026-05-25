# Horizon — Procedures

```text
  Common Operational Procedures
┌──────────────────────────────────────────────────────────────┐
│  Create Pool     │  Push Image      │  Manage Sessions       │
│  ┌────────────┐  │  ┌────────────┐  │  ┌──────────────────┐  │
│  │Golden image│  │  │Update      │  │  │Force logoff      │  │
│  │ + snapshot │  │  │snapshot in │  │  │Disconnect stale  │  │
│  │      │     │  │  │pool config │  │  │Send message      │  │
│  │      ▼     │  │  │      │     │  │  └──────────────────┘  │
│  │ Instant    │  │  │      ▼     │  │                        │
│  │ Clone pool │  │  │ Rolling    │  │  Entitlements          │
│  │ provision  │  │  │ refresh    │  │  ┌──────────────────┐  │
│  └────────────┘  │  └────────────┘  │  │AD group → pool   │  │
│                  │                  │  │mapping           │  │
│  Add CS Replica  │  Handle Error VM │  └──────────────────┘  │
│  ┌────────────┐  │  ┌────────────┐  │                        │
│  │Install +   │  │  │Reset or    │  │                        │
│  │Join to pod │  │  │delete + re-│  │                        │
│  └────────────┘  │  │provision   │  │                        │
│                  │  └────────────┘  │                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Create an Instant Clone Desktop Pool

**Prerequisites:** Golden image VM with Horizon Agent installed, parent snapshot taken, vCenter service account configured.

```yaml
Horizon Console → Inventory → Desktops → Add Desktop Pool
  Type: Automated Desktop Pool
  User Assignment: Floating or Dedicated
  vCenter: select your vCenter
  Desktop Pool ID: pool-win10-float
  Display Name: Windows 10 — Floating Pool
  Template: select parent VM
  Snapshot: select the snapshot taken after Agent install
  vSphere cluster / resource pool / datastore: select appropriately
  Naming Pattern: win10-{n:fixed=3}   (e.g., win10-001)
  Pool size: Minimum: 5, Maximum: 50, Headroom: 5
  Protocol: Blast Extreme (primary), PCoIP (backup)
  Power policy: Ensure VMs are always powered on (for Instant Clone)
```

---

## Entitle an AD Group to a Pool

```text
Horizon Console → Inventory → Desktops → [pool name] → Entitlements
  Add Entitlement → select AD group or user
  e.g.: CORP\Horizon-Pool-Win10 → Add
```

Users in the group can now connect to the pool from Horizon Client or HTML access.

---

## Push a Golden Image Update to an Instant Clone Pool

```yaml
Horizon Console → Inventory → Desktops → [pool name] → Edit
  Advanced Storage → Change Parent VM or Snapshot
  Select: new parent snapshot
  Schedule: immediate or scheduled maintenance window
  Mode: Rolling restart (users get new image on next login)
  OR: Force restart (immediately recycles all desktops — causes session disruption)
```

---

## Add a New Connection Server Replica

```powershell
# On new Windows Server:
VMware-Horizon-Connection-Server-x86_64-<version>.exe /silent /norestart `
  /v"VDM_SERVER_INSTANCE_TYPE=2 `
  VDM_INITIAL_ADMIN_SID=<domain-admin-SID> `
  VDM_INITIAL_ADMIN_PASSWORD=<first-CS-admin-password>"
```

After install:
```text
Horizon Console → Settings → Servers → Connection Servers
  New server should appear — verify green status
  Install/replace SSL certificate to match other Connection Servers
```

---

## Configure UAG for External Access

UAG Admin UI (https://uag.example.local:9443):

```text
Configure Manually
  Network Settings: set IPs for each NIC (Internet, Management, Backend)
  Edge Service Settings → Horizon → Enable
    Connection Server URL: https://horizon-cs01.example.local:443
    Connection Server thumbprint: sha1:<thumbprint>
    Blast port: 8443
    PCoIP port: 4172
    Tunnel: Enabled
```

```bash
# Get Connection Server certificate thumbprint:
echo | openssl s_client -connect horizon-cs01.example.local:443 2>/dev/null \
  | openssl x509 -fingerprint -sha1 -noout
```

---

## Enable True SSO

True SSO allows users to authenticate once at UAG (via SAML/AD) and get a short-lived certificate for desktop login — no password re-entry.

```yaml
Requirements:
  - VMware Identity Manager (vIDM) or Workspace ONE
  - Microsoft CA (Enterprise CA) for certificate template
  - Enrollment Server role installed on Connection Server

Horizon Console → Settings → True SSO
  Enable True SSO
  Add Enrollment Server
  Configure Certificate Template (must match template on CA)
```

---

## Add an App Volumes AppStack to a Pool

```text
App Volumes Manager → AppStacks → [AppStack name] → Assign
  Assignment type: Group
  AD Group: CORP\AppStack-AdobeReader
  Delivery: On Login (attach when user logs into desktop)
```

The AppStack VMDK will mount at the next user login for members of that group.

---

## Handle a Stuck Desktop in Error State

```powershell
Connect-HVServer -Server horizon-cs01.example.local -Credential (Get-Credential)

# List desktops in error state
Get-HVDesktop | Where-Object { $_.Base.BasicState -eq "ERROR" } |
  Select-Object -ExpandProperty Base | Select Name, BasicState

# Reset a specific desktop (reboots the VM)
Reset-HVMachine -HVMachineName "win10-042"

# Delete an error-state desktop (Instant Clone pools reprovision automatically)
Remove-HVDesktop -VMName "win10-042" -Confirm:$false
```

---

## Set DEM Configuration Migration Policy

DEM manages user profile and environment settings. Configure import/export policies:

```bash
DEM Management Console → User Environment → [configuration] → Condition
  Set condition to: always apply (or per AD group membership)
  Import on login: Yes
  Export on logout: Yes
```

For roaming profile migration from legacy profiles, configure DEM import from the old profile path.

---

## Decommission a Desktop Pool

```powershell
Horizon Console → Inventory → Desktops → [pool] → Disable
  Disable provisioning: prevent new desktops from being created
  Remove entitlements: prevent new sessions
  Wait for all sessions to end (or force-logoff)

# Force logoff all sessions in the pool:
Get-HVLocalSession | Where-Object { $_.NamesData.DesktopPoolCN -eq "pool-win10-float" } |
  Invoke-HVSessionLogoff

# Once sessions are zero:
Horizon Console → Inventory → Desktops → [pool] → Delete
  Option: Delete VMs from vCenter (recommended)
```

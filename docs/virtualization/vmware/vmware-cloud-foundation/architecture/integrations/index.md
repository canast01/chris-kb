# VCF — Integrations

## Integration Summary

| Integration | Method | Notes |
|---|---|---|
| Aria Operations | VCF Management Pack | Install MP on Aria Ops; add SDDC Manager as source |
| Aria Automation | Cloud Account (VCF type) | Requires vCenter and NSX credentials per domain |
| NSX Federation | Global Manager | Cross-site; deploy Global Manager outside VCF lifecycle |
| Active Directory | SDDC Manager Identity Source | LDAP/LDAPS under Administration → Single Sign-On |
| SIEM / Syslog | Syslog from SDDC Manager | Configure under Administration → Syslog |
| Backup tools | VM-level via vCenter | No native VCF backup integration — use Veeam/NetBackup via vCenter |

---

## Aria Operations

The VCF Management Pack for Aria Operations provides topology views, vSAN health, and capacity analytics scoped to VCF domain constructs.

**Setup:**

1. Download the VCF Management Pack from VMware Solution Exchange.
2. Aria Operations → Administration → Solutions → Import Management Pack.
3. Add a VCF account: provide SDDC Manager FQDN and admin credentials.
4. Aria Operations discovers vCenter, NSX, and vSAN components from SDDC Manager automatically.

**What it surfaces:**

- Domain health rollup per workload domain
- vSAN capacity and performance per cluster
- Certificate expiry across all managed components
- LCM compliance — which domains have pending bundle updates

---

## Aria Automation

Aria Automation connects to VCF workload domains as cloud accounts, enabling IaC VM provisioning on SDDC Manager-managed clusters.

**Setup:**

1. Aria Automation → Infrastructure → Cloud Accounts → Add → vCenter (or VCF).
2. Provide the workload domain vCenter FQDN and a service account with the vCenter Admin or CloudAdmin role.
3. Add the NSX-T Manager for the domain to enable network provisioning.
4. Create a Cloud Zone scoped to the workload domain clusters.

**Service account minimum permissions:**

- vCenter: `CloudAdmin` role on the relevant cluster(s)
- NSX: `Enterprise Admin` or a scoped role with segment and security group create/delete rights

---

## Active Directory Integration

SDDC Manager uses AD for operator authentication. Each workload domain vCenter is also typically joined to the same AD identity source.

**Add AD identity source to SDDC Manager:**

```
SDDC Manager → Administration → Single Sign-On
→ Add Identity Source → Active Directory over LDAP
→ Enter domain FQDN, LDAPS server, bind account DN and password
→ Test connection → Save
```

**Assign roles to AD groups:**

```
SDDC Manager → Administration → Users and Groups
→ Add → enter AD group name → assign ADMIN / OPERATOR / VIEWER role
```

**Test AD connectivity from SDDC Manager appliance:**

```bash
ldapsearch -H ldaps://<dc-ip>:636 -x -D "<bind-account-dn>" -W \
  -b "dc=domain,dc=com" "(sAMAccountName=<test-user>)"
```

---

## NSX Federation (Multi-Site VCF)

NSX Federation allows a single NSX policy plane to span multiple VCF instances across sites via a Global Manager (GM).

**Key design points:**

- The Global Manager is deployed outside VCF LCM — it is not upgraded via SDDC Manager.
- Local NSX Managers in each VCF instance handle data-plane operations.
- Stretched segments, global gateway policies, and security policies are defined at the GM level.
- GM upgrade is planned separately from each VCF site's NSX upgrade cycle.

---

## Backup Integration

VCF does not provide a native VM backup solution. VM backup is handled at the vCenter layer per workload domain.

**Veeam B&R:**

1. Add each workload domain vCenter as a Managed Server in Veeam.
2. VMs appear in Veeam inventory as standard vSphere VMs.
3. Ensure backup proxies have access to vSAN datastores in each domain.

**SDDC Manager configuration backup** (separate from VM data backup):

```
SDDC Manager → Administration → Backup → Configure
→ Set SFTP target → schedule daily → retain 7+ restore points
```

---

## SIEM and Syslog Integration

```
SDDC Manager → Administration → Syslog → Add Syslog Server
→ Protocol: TLS (recommended) or UDP/TCP → Port: 6514 or 514
```

**Verify forwarding is working:**

1. Perform a test action in SDDC Manager (e.g., browse a domain, rotate a password).
2. Confirm the event appears in the SIEM within a few minutes.
3. Check that the SIEM source IP matches the SDDC Manager appliance IP.

**vCenter syslog per workload domain (PowerCLI):**

```powershell
# Configure syslog forwarding on all ESXi hosts in a cluster
Get-Cluster "ClusterName" | Get-VMHost | ForEach-Object {
  Set-VMHostSysLogServer -VMHost $_ -SysLogServer "udp://<siem-ip>:514"
  Restart-VMHostService -VMHost $_ -Key "syslog" -Confirm:$false
}
```

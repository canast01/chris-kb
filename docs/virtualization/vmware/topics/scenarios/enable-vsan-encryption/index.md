# Enable vSAN Encryption

<div class="kb-summary">
Enabling vSAN data-at-rest encryption triggers a full rebuild of the entire vSAN datastore. Every
object on every disk is re-encrypted end-to-end. On a large cluster this takes hours to days and
must not be interrupted. The key provider must be configured and backed up before starting — losing
the key means losing access to all encrypted data. Plan for a dedicated maintenance window and
ensure the cluster has at least 30% free space before enabling.
</div>

```text
┌────────────────────────────────── Enable vSAN Encryption — Procedure Flow ────────────────────────────────────────┐
│                                                                                                       │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  START: Choose key provider — Native Key Provider (NKP) for simplicity, external KMS for compliance       ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                          ┌───────────────────────────┼───────────────────────────┐                    │
│                          ▼                           ▼                           ▼                    │
│          ┌─────────────────────────┐   ┌─────────────────────────┐  ┌─────────────────────────┐       │
│          │  Option A: Configure    │   │  Option B: Configure    │  │  Pre-encryption checks: │       │
│          │  NKP in vCenter;        │   │  external KMS: address, │  │  vSAN 100% healthy,     │       │
│          │  back up NKP offline    │   │  port 5696, cert import │  │  ≥ 30% free space       │       │
│          └────────────┬────────────┘   └────────────┬────────────┘  └────────────┬────────────┘       │
│                       └────────────────────────────┬─┘──────────────────────────┘                     │
│                                                    ▼                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Enable encryption: vCenter → Cluster → Configure → vSAN → Services → Data-At-Rest Encryption → Enable    ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Full rebuild begins: monitor resyncing objects — do NOT put any host in maintenance mode during rebuild   ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Rebuild complete: verify encryption status, re-export NKP backup, validate vSAN health all green         ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vSAN | Applies data-at-rest encryption to all objects; manages the rebuild process |
| vCenter Server | Cluster configuration entry point; hosts Key Provider management UI |
| Native Key Provider (NKP) | vCenter-managed key provider — no external KMS required; keys stored in vCenter DB |
| External KMS | Third-party key management server (KMIP protocol) for FIPS/compliance environments |
| ESXi | Executes the encryption I/O on each host's disk groups during the rebuild |

---

## 1. Choose the Key Provider

Two options — choose based on compliance requirements:

| Option | When to use | Dependency |
|---|---|---|
| Native Key Provider (NKP) | General use — simplest setup; keys managed by vCenter | vCenter must be healthy at all times to decrypt data |
| External KMS | FIPS 140-2 compliance, KMIP standard required, or key management must be separate from VMware | Dedicated KMS appliance required; must be highly available |

If unsure: use NKP. The external KMS path adds operational complexity (KMS appliance HA, certificate
management, firewall rules) that is only warranted for specific compliance requirements.

---

## 2. Configure Native Key Provider (NKP)

vCenter → select the vSAN cluster → **Configure** → **Key Providers** → **Add** → **Native Key
Provider** → give it a name (e.g., `vSAN-NKP-prod`).

**Immediately back up the NKP.** This is the most critical step in the entire procedure. The NKP
backup is a password-protected file that is the only recovery path if the vCenter database is lost
while encrypted data is on disk.

vCenter → **Key Providers** → select the NKP → **Back Up** → enter a strong backup password →
download the backup file.

Store the backup:

- **Not on the vCenter VM** — if vCenter is lost, you cannot access the backup
- **Not on the vSAN datastore** — if encryption is the problem, the datastore may be inaccessible
- **On an offline secure medium** — USB drive or file share outside the VMware environment, with
  access restricted to backup administrators

---

## 3. Configure External KMS (If Using External)

vCenter → select the cluster → **Configure** → **Key Providers** → **Add** → **Standard Key
Provider**.

Provide:

- KMS server name and IP address
- KMS port (default: TCP 5696 — the KMIP standard port)
- KMS credentials (client certificate or username/password depending on KMS vendor)

After adding the KMS: **Test Connection** must return green before proceeding. Import the KMS server
TLS certificate into vCenter to establish trust.

```bash
# Verify KMS port is reachable from vCenter appliance
# Run from vCenter appliance shell
nc -zv <kms-server-ip> 5696
```

If the KMS is clustered for HA: add both KMS nodes to vCenter. vCenter will use the first
available node.

---

## 4. Pre-Encryption Checks

vSAN health must be completely green before enabling encryption. A partially degraded cluster
combined with a full encryption rebuild can reduce vSAN below minimum fault tolerance, causing
object unavailability.

```powershell
# Check vSAN cluster health — all tests must be green
Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system" | `
  Select -ExpandProperty OverallHealth

# Check current vSAN capacity — need at least 30% free before starting
Get-Datastore "vsanDatastore" | Select Name, FreeSpaceGB, CapacityGB
```

```bash
# Check resync queue — must be 0 before enabling encryption
esxcli vsan debug resync summary get
```

Requirements before proceeding:

| Check | Requirement |
|---|---|
| vSAN Skyline Health | All tests green — no warnings or errors |
| vSAN resync queue | 0 bytes remaining |
| vSAN free space | At least 30% free (rebuild requires scratch space for re-encryption) |
| Key provider status | Connected and tested (green) |
| Cluster hosts | All hosts connected — no hosts in maintenance mode |

Do not proceed if any check fails. The encryption rebuild cannot be paused once started.

---

## 5. Enable Encryption

vCenter → select the vSAN cluster → **Configure** → **vSAN** → **Services** → **Data-At-Rest
Encryption** → **Edit** → toggle **Encryption** to enabled → select the Key Provider →
**Apply**.

vCenter will display a warning that enabling encryption triggers a full data rebuild and that this
operation cannot be paused. Confirm the warning.

The rebuild begins immediately on all hosts in the cluster. All VMs continue running during the
rebuild — this is not a maintenance window in the sense of VM downtime, but it is a maintenance
window in the sense that no other storage maintenance should be performed.

---

## 6. Monitor the Rebuild

vCenter → **vSAN** → **Monitor** → **Resyncing Objects**.

The resyncing objects view shows total bytes remaining and per-object status. This view updates
every few minutes.

```bash
# Monitor from ESXi CLI — shows bytes to resync and estimated completion
esxcli vsan debug resync summary get
```

Reference rebuild times (approximate — varies significantly with cluster I/O load):

| Cluster used capacity | Approximate rebuild time |
|---|---|
| 1 TB | 1-3 hours |
| 5 TB | 4-10 hours |
| 10 TB | 8-24 hours |
| 50 TB+ | Multiple days |

During the rebuild — do not do any of the following:

- Put any host in maintenance mode
- Add or remove disks from any host
- Remove any host from the cluster
- Run any other vSAN resync operations (e.g., policy changes on large VMs)
- Run Storage vMotion operations on large VMDKs

Any of these operations adds to the resync queue and extends the rebuild time. In the worst case,
concurrent operations can saturate the vSAN rebuild bandwidth and cause the rebuild to stall.

---

## 7. Verify Encryption Status After Rebuild

Once the resyncing objects count reaches 0, verify that encryption is fully applied.

```bash
# From any ESXi host in the cluster
# Check that vSAN objects show encrypted state
esxcli vsan debug object list | grep -i encrypt

# Or query encryption status directly
esxcli vsan encryption get
```

From vCenter: **Cluster** → **Configure** → **vSAN** → **Services** → **Data-At-Rest Encryption**
should show **Enabled** with the key provider name and status **Active**.

```powershell
# Confirm vSAN health is still all green after rebuild
Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system" | `
  Select -ExpandProperty OverallHealth
```

---

## 8. Post-Encryption Key Backup

After encryption is confirmed active, export the NKP backup again. The first backup (taken before
enabling encryption) captured the key before it was in active use. The post-encryption backup
captures the key in its current active state and should replace the pre-encryption backup.

vCenter → **Key Providers** → select the NKP → **Back Up** → download and store as per the
backup storage guidance in Step 2.

Label the backup file with the date and cluster name. Establish a schedule to refresh the NKP
backup whenever the key is rotated.

---

## Post-Task Validation

| Check | Location | Expected Result |
|---|---|---|
| Encryption status | vCenter → Cluster → vSAN → Services | Enabled, key provider Active |
| vSAN Skyline Health | vCenter → Cluster → vSAN → Skyline Health | All tests green |
| Resync queue | `esxcli vsan debug resync summary get` | 0 bytes remaining |
| Key provider connectivity | vCenter → Key Providers | Connected, no errors |
| NKP backup stored | Offline secure storage | Post-encryption backup saved |
| vSAN free space | vCenter → Datastore | Within normal range (no unexpected consumption) |

---

## Common Mistakes

- **Starting encryption without 30% free space.** The rebuild requires scratch space to create
  re-encrypted copies of objects before removing the originals. If space runs out mid-rebuild, the
  cluster enters a critically degraded state that requires emergency intervention to resolve.
- **Not backing up the NKP before enabling encryption.** If vCenter is lost before the backup is
  taken and the NKP key is gone, all encrypted data is permanently unrecoverable.
- **Interrupting the rebuild by putting a host in maintenance mode.** Entering maintenance mode
  during the encryption rebuild causes objects on that host's disk group to become temporarily
  inaccessible. In a stretched cluster or a cluster already at minimum fault tolerance, this causes
  VM unavailability.
- **Using vSAN encryption when VM encryption was actually needed.** vSAN encryption protects data
  at rest on the disk — it does not encrypt data in memory or in transit. If the requirement is to
  encrypt specific VMs independently (for multi-tenancy or compliance per-VM), use VM Encryption
  Storage Policy instead of vSAN cluster-level encryption.

---

## Related Scenarios

- Host Maintenance and Patching
- vSAN Disk or Component Failure
- Storage vMotion / Datastore Migration
- Capacity Planning

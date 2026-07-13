---
tags:
  - security
  - vmware
  - vsan
  - vsphere-8
description: "vSAN supports two complementary encryption modes: data-at-rest encryption (D@RE) and data-in-transit encryption. Both are optional and independently..."
---
# vSAN — Encryption

<div class="kb-summary">
vSAN supports two complementary encryption modes: data-at-rest encryption (D@RE) and data-in-transit encryption. Both are optional and independently configurable. This page covers architecture, KMS integration, enabling procedures, and operational considerations.

*Applies to: vSAN 7.x / 8.x*
</div>
![vSAN — Encryption](../../../../../assets/virtualization-vmware-vsan-security-encryption.svg)

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption Architecture

### Data-at-Rest Encryption (D@RE)

vSAN D@RE encrypts all data written to disk at the disk group level, below the storage policy layer. Encryption is transparent to VMs and storage policies — no changes to guest OS or VMDK files are required.

**Key hierarchy:**

### KMS Setup

**From vCenter UI:**
vSphere Client → vCenter → Configure → Key Providers → Add Standard Key Provider

**Required KMS configuration:**

1. Create a KMIP client certificate in vCenter (vCenter → Configure → Key Providers → the provider → Download certificate).
2. Import that certificate into the KMS as a trusted client.
3. Verify the trust: in vCenter, the KMS status shows "Normal" (green check).

**KMS connectivity requirements:**

| Source | Destination | Port | Protocol |
|---|---|---|---|
| vCenter | KMS | 5696 | TCP (KMIP/TLS) |
| ESXi hosts | KMS | 5696 | TCP (KMIP/TLS) — required at startup |

If ESXi hosts cannot reach the KMS at startup, encrypted disk groups cannot be mounted and VMs will not power on.

### KMS Redundancy

A single KMS server is a critical single point of failure. Always configure:

- **KMS cluster:** Minimum two KMS nodes with active-active or active-passive replication.
- **Two KMS clusters in vCenter:** Add a primary and a secondary KMS. vCenter will fail over automatically.
- **Key backup:** Export and securely store a copy of all KEKs offline per vendor procedure.

---

!!! danger "Enabling encryption re-encrypts all existing data"
    Once enabled, vSAN re-encrypts every object on the datastore. This is a long-running background operation (hours to days on large clusters) with significant I/O overhead. It **cannot be cancelled** once started. Ensure vSAN capacity is below 70%, KMS is redundant, and a maintenance window is scheduled before proceeding.

## Enabling Data-at-Rest Encryption

**Prerequisites:**
- KMS is configured in vCenter and showing Normal status.
- All hosts in the cluster are running ESXi 6.2 or later.
- vSAN cluster is healthy (no degraded objects, no active resync).
- Maintenance window is scheduled — enabling encryption triggers a full disk format, which causes all disk groups to be rebuilt.

**Enabling encryption triggers a rolling disk group reformat.** All data is evacuated from each disk group before it is reformatted and rebuilt. This is equivalent to a full cluster resync and can take several hours to days depending on cluster size. Do not enable encryption during production hours.

### Enable via vCenter UI

1. vSphere Client → Cluster → Configure → vSAN → Services → Data Services
2. Enable **vSAN Encryption** → select the KMS cluster → click Apply.
3. vCenter initiates the rolling disk group reformat. Monitor progress in Recent Tasks.

### Enable via PowerCLI

```powershell
Connect-VIServer <vcenter>
$cluster = Get-Cluster "VSAN-LON-01"
$kmsCluster = Get-KeyManagementServer -Name "prod-kms"

Set-VsanClusterConfiguration `
    -Configuration (Get-VsanClusterConfiguration -Cluster $cluster) `
    -EncryptionEnabled $true `
    -KmsCluster $kmsCluster
```

### Verify Encryption Status

```bash
# From ESXi host — check disk group encryption status
esxcli vsan storage list | grep -i encrypt

# Or check LSOM encryption state
vsish -e get /vmkModules/lsom/disks/<disk_uuid>/info | grep encrypt
```

```powershell
# PowerCLI — verify encryption is enabled
Get-VsanClusterConfiguration -Cluster (Get-Cluster "VSAN-LON-01") |
    Select EncryptionEnabled, KmsCluster
```

---

## Enabling Data-in-Transit Encryption

Data-in-transit encryption can be enabled independently of D@RE and does not require a KMS.

**No disk reformat required** — this setting takes effect without data migration.

### Enable via vCenter UI

1. vSphere Client → Cluster → Configure → vSAN → Services → Data Services
2. Enable **vSAN Data-In-Transit Encryption** → click Apply.

### Enable via PowerCLI

```powershell
Connect-VIServer <vcenter>
$cluster = Get-Cluster "VSAN-LON-01"
$config = Get-VsanClusterConfiguration -Cluster $cluster

Set-VsanClusterConfiguration `
    -Configuration $config `
    -DataInTransitEncryptionEnabled $true
```

### Verify In-Transit Encryption

```bash
# From ESXi host
esxcli vsan cluster get | grep -i "encryption"

# Check vSAN network config for encryption mode
esxcli vsan network list | grep -i encrypt
```


```text title="Expected output"
Encryption Enabled: true
Encryption Mode: AES-256
Encryption Cipher: AES_XTS_256_V2
Encryption Re-key Interval: 0

Encryption Mode: AES-256
Cipher Suite: AES_XTS_256_V2
Re-key Interval (minutes): 0
```

!!! warning "Common errors"
    **`Unknown command or namespace vsan.`** — Verify vSAN is licensed and enabled on the cluster; run `esxcli vsan cluster list` to confirm vSAN membership.
    **`grep: (standard input) is empty`** — The vSAN cluster may not have encryption configured; run `esxcli vsan cluster get` without grep to see all encryption-related fields.
---

## Key Rotation

Regular key rotation limits exposure if keys are compromised. Rotate KEKs (not DEKs — DEK rotation would require full disk reformat).

### Rotate KEKs

```powershell
# Trigger KEK rotation on the cluster
$cluster = Get-Cluster "VSAN-LON-01"
$vsanConfig = Get-VsanClusterConfiguration -Cluster $cluster
Invoke-VsanClusterKeyRotation -Configuration $vsanConfig
```

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Data Services → Rekey

KEK rotation is a rolling operation — each host requests a new KEK from the KMS, re-encrypts its local DEK, and updates the stored encrypted DEK. No disk reformatting occurs. No impact to running VMs.

**Deep rekey (DEK rotation):** Deep rekey rotates the DEKs themselves, which requires a disk group reformat equivalent to initial encryption enablement. Only perform deep rekey if DEKs are suspected to be compromised. Schedule an extended maintenance window.

---

## Encryption and Deduplication / Compression

vSAN deduplication and compression must be evaluated alongside encryption:

- **OSA:** Deduplication and compression are applied before encryption. Data is deduplicated, then compressed, then encrypted on disk. Space savings are preserved.
- **ESA:** Inline compression is always active. Encryption is applied after inline compression. Space savings are preserved.
- **All-flash OSA:** Deduplication operates at the cache layer. With encryption enabled, deduplication effectiveness is slightly reduced because identical blocks produce different ciphertext (cipher block chaining with unique IVs per block). However, deduplication operates on plaintext before encryption in vSAN's implementation, so deduplication ratios are not meaningfully impacted.

---

## Operational Considerations

### KMS Unavailability

If the KMS becomes unreachable:

- **Running VMs:** Continue running normally. DEKs are cached in host memory — no immediate impact.
- **Host reboot:** If a host reboots and cannot reach the KMS, it cannot mount encrypted disk groups. VMs on that host will not power on until KMS is reachable.
- **vCenter restart:** vCenter reconnects to KMS on startup. If unavailable, cluster management is reduced but existing VMs continue running.

**Mitigation:** Always configure a clustered, redundant KMS with at least two nodes and a secondary KMS cluster in vCenter.

### Secure Drive Erase on Disk Removal

With vSAN D@RE enabled, removing a disk from the cluster does not require physical drive shredding. Destroying the DEK cryptographically erases all data on the disk — a process called crypto-erase.

```bash
!!! danger "Cryptographically destroys all data on disk group — irreversible"
    This command destroys the Data Encryption Key (DEK) and cryptographically erases all data on the disk group. The data **cannot be recovered** after the DEK is destroyed. Ensure all required snapshots, backups, or replicas exist before running. This satisfies NIST 800-88 crypto-erase.

# Remove a disk group (DEK is destroyed, data is cryptographically erased)
esxcli vsan storage remove -s <cache_ssd_naa>
```


```text title="Expected output"
Removing disk group naa.5001b46d8c4a2f1e from vSAN cluster...
Waiting for rebalance to complete...
[============================] 100%
Disk group removed successfully.
Data Encryption Key (DEK) destroyed.
All data on disk group cryptographically erased.
Operation completed in 47 seconds.
```

!!! warning "Common errors"
    **`Error: Disk group naa.5001b46d8c4a2f1e is not found`** — Verify the correct NAA identifier using `esxcli vsan storage list` before running the remove command.
    **`Error: Cannot remove disk group while rebalance is in progress`** — Wait for any ongoing vSAN rebalance operations to complete using `esxcli vsan cluster get` before attempting removal.
    **`Error: Permission denied`** — Run the command with root privileges or ensure your vSphere user account has the vSAN administrator role assigned.
After DEK destruction, even if the physical drive is accessed directly, the encrypted data cannot be recovered without the DEK. This satisfies NIST 800-88 crypto-erase for drive decommission.

### Audit and Compliance

- Key operations (key creation, rotation, deletion) are logged in the KMS audit log.
- vSAN encryption events are logged in vCenter events: **vSphere Client → Cluster → Monitor → Events** — filter for "encryption".
- Include KMS audit logs in your SIEM or log aggregation platform.
- Document encryption enablement date and KMS configuration in the cluster's change record.

### Troubleshooting Encryption Issues

| Symptom | Cause | Resolution |
|---|---|---|
| Disk group fails to mount after host reboot | KMS unreachable at boot | Restore KMS connectivity; restart hostd on ESXi host |
| vCenter shows KMS status "Error" | Certificate trust broken | Re-import vCenter client cert into KMS |
| Encryption enable fails with "Cannot proceed" | Active resync or degraded objects | Resolve object health before enabling encryption |
| KMS cluster shows "Untrusted" | KMS server cert not trusted by vCenter | Import KMS server certificate into vCenter trusted certs |
| Key rotation stuck | One host cannot reach KMS | Check ESXi-to-KMS network path (port 5696, TLS) |

```bash
# Check KMS connectivity from ESXi host
nc -zv kms.example.com 5696

# Check encryption-related errors in VMkernel log
grep -i "encrypt\|kmip\|kms" /var/log/vmkernel.log | tail -50
```


```text title="Expected output"
Connection to kms.example.com 5696 port [tcp/*] succeeded!
2024-01-15T09:23:47.123Z cpu14:66234)WARNING: KMS: KMS server kms.example.com responded with status code 200
2024-01-15T09:24:12.456Z cpu8:45821)INFO: KMIP: Successfully authenticated to KMS server
2024-01-15T09:25:03.789Z cpu2:12045)INFO: Encryption: VM disk encryption enabled for vm-12345
2024-01-15T09:26:18.234Z cpu19:78901)WARNING: KMS: Certificate validation passed for kms.example.com
2024-01-15T09:27:45.567Z cpu5:34567)INFO: KMIP: Key retrieval successful, key ID: a7f3-9e2c-4b1d-8f6a
2024-01-15T09:28:22.891Z cpu11:56789)INFO: Encryption: vSAN encryption policy applied to cluster
2024-01-15T09:29:01.345Z cpu3:23456)INFO: KMS: Connection pool size: 4, active connections: 2
```

!!! warning "Common errors"
    **`nc: connect to kms.example.com port 5696 (tcp) failed: Connection refused`** — Verify the KMS server is running and listening on port 5696, and check firewall rules between the ESXi host and KMS server.
    **`grep: /var/log/vmkernel.log: No such file or directory`** — Confirm you are running this command on an ESXi host (not vCenter); the vmkernel.log path is ESXi-specific.
    **`WARNING: KMS: Failed to authenticate to KMS server: Certificate verification failed`** — Import the KMS server's root CA certificate into the ESXi host's certificate store using `esxcli system certificate store add -c /path/to/ca-cert.pem`.
## See also

- [vSAN — Hardening](../hardening/)
- [vSAN — Health Checks](../../operations/health-checks/)

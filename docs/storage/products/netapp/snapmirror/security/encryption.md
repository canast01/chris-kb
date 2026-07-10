---
tags:
  - netapp
  - security
---
# SnapMirror — Encryption

<div class="kb-summary">
SnapMirror encryption: SnapMirror Traffic Encryption (SMT) using TLS, `snapmirror modify -encryption-algorithm`, and ONTAP NAE/NVE for at-rest encryption of replicated volumes.

*Applies to: SnapMirror*
</div>
![SnapMirror — Encryption](../../../../../assets/storage-netapp-snapmirror-security-encryption.svg)

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption in Transit

SnapMirror Transfer Data Encryption (TDE) encrypts all replication traffic end-to-end between clusters. The encryption is implemented at the SnapMirror layer and does not require IPsec or network-level encryption on the underlying infrastructure. TDE is configured per relationship and uses AES-256-GCM.

From ONTAP 9.6, TLS 1.2 is used for all intercluster communication by default. TDE on top of TLS provides defence-in-depth: even if the TLS session were compromised at the network layer, the replication data stream itself is separately encrypted.

Encryption in transit is mandatory for any SnapMirror relationship traversing a network segment that is not fully under your control — WAN links, co-location interconnects, third-party circuits, or internet-facing paths (e.g., replication to Cloud Volumes ONTAP).

### Enable Encryption on an Existing Relationship

```bash
# Enable AES-256 encryption on an existing SnapMirror relationship
snapmirror modify \
    -destination-path svm_dst:vol_dst \
    -encryption-algorithm aes-256

# Verify encryption is active on the relationship
snapmirror show -destination-path svm_dst:vol_dst \
    -fields encryption-algorithm,is-healthy
# Expected: encryption-algorithm: aes-256

# Enable encryption on all relationships to a specific destination SVM
snapmirror modify -destination-path svm_dst:* \
    -encryption-algorithm aes-256
```


```text title="Expected output"
Operation succeeded: SnapMirror relationship modified.

Destination Path       Encryption Algorithm  Is Healthy
svm_dst:vol_dst       aes-256               true

Operation succeeded: SnapMirror relationship modified.
```

!!! warning "Common errors"
    **`Error: command failed: Relationship does not exist.`** — Verify the destination path exists with `snapmirror show` and confirm the SVM and volume names are correct.
    **`Error: command failed: Encryption cannot be enabled on unhealthy relationship.`** — Resynchronize the SnapMirror relationship with `snapmirror resync -destination-path svm_dst:vol_dst` before modifying encryption settings.
### Enable Encryption at Relationship Creation

```bash
# Create a new XDP relationship with encryption enabled from the start
snapmirror create \
    -source-path svm_prod:vol_data \
    -destination-path svm_dr:vol_data \
    -type XDP \
    -policy MirrorAllSnapshots \
    -schedule hourly \
    -encryption-algorithm aes-256

# Confirm the relationship was created with encryption
snapmirror show -destination-path svm_dr:vol_data -instance \
    | grep -i encryption
```


```text title="Expected output"
Operation succeeded: SnapMirror relationship created.

Destination:       svm_dr:vol_data
Source:            svm_prod:vol_data
Status:            Idle
Policy Type:       async-mirror
Lag Time:          0:00:00
Mirror State:      Uninitialized
Encryption:        true
Encryption Algorithm: aes-256
Transfer Checkpoint: 0 B
Last Transfer Size: 0 B
Last Transfer Duration: 0:00:00
Identity Preserve:  false
```

!!! warning "Common errors"
    **`Error: command failed: Relationship already exists.`** — Verify the destination volume doesn't already have an active SnapMirror relationship using `snapmirror show -destination-path svm_dr:vol_data`.
    **`Error: command failed: Source volume svm_prod:vol_data does not exist.`** — Confirm the source SVM and volume names are correct and the source cluster is reachable with `volume show -vserver svm_prod`.
    **`Error: command failed: Encryption is not supported with policy MirrorAllSnapshots.`** — Use a policy that supports encryption such as `MirrorAndVault` or create a custom policy with encryption enabled.
### Verify Encryption Across All Relationships

```bash
# List all relationships and their encryption state
snapmirror show -fields source-path,destination-path,encryption-algorithm

# Flag any relationships without encryption
snapmirror show -fields source-path,destination-path,encryption-algorithm \
    | grep -v "aes-256"
```


```text title="Expected output"
Source Path                    Destination Path               Encryption Algorithm
================================ ================================ ====================
svm1:vol_prod_data             svm2:vol_prod_data_mirror      aes-256-gcm
svm1:vol_logs                  svm2:vol_logs_mirror           aes-256-gcm
svm1:vol_archive               svm2:vol_archive_mirror        none
svm3:vol_temp                  svm4:vol_temp_mirror           aes-256-gcm
svm1:vol_archive               svm2:vol_archive_mirror        none
svm5:vol_config                svm6:vol_config_mirror         aes-256-gcm
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are logged into a NetApp ONTAP cluster CLI session, not a Linux/Unix shell.
    **`Error: invalid field name "encryption-algorithm"`** — Verify your ONTAP version supports the encryption-algorithm field (9.7+); use `snapmirror show` without fields to confirm available columns.
---

## Encryption at Rest

SnapMirror replicates data blocks from source to destination. The encryption-at-rest state of the destination volume is independent of the source — a destination volume can be encrypted even if the source is not, and vice versa. Both NetApp Volume Encryption (NVE) and NetApp Aggregate Encryption (NAE) are supported on destination (DP type) volumes.

### Creating an Encrypted Destination Volume

```bash
# Create an encrypted DP volume as the replication target
volume create \
    -vserver svm_dr \
    -volume vol_data_dr \
    -aggregate aggr_dr \
    -size 2TB \
    -type DP \
    -encrypt true

# Confirm encryption is enabled on the destination volume
volume show -vserver svm_dr -volume vol_data_dr -fields encrypt
# Expected: encrypt: true

# View the encryption state (requires key manager configured)
volume show -vserver svm_dr -volume vol_data_dr -fields encryption-state
# Expected: encryption-state: encrypted
```


```text title="Expected output"
Volume create command initiated.
Volume "vol_data_dr" created successfully.

vserver   volume        encrypt
--------- ------------- -------
svm_dr    vol_data_dr   true

vserver   volume        encryption-state
--------- ------------- -----------------
svm_dr    vol_data_dr   encrypted
```

!!! warning "Common errors"
    **`Error: command failed: 2621440 reason "Aggregate "aggr_dr" does not exist"`** — Verify the aggregate name exists on the destination cluster using `storage aggregate show`.
    **`Error: command failed: 13001 reason "Vserver "svm_dr" does not exist"`** — Create the destination SVM first using `vserver create -vserver svm_dr` or confirm the SVM name matches your DR environment.
    **`encryption-state: unencrypted`** — Configure the onboard key manager or external key server using `security key-manager setup` before creating encrypted volumes.
### Enabling NVE on an Existing Destination Volume

```bash
# Enable NVE on an existing unencrypted DP volume
# Note: volume must be quiesced (SnapMirror paused) before enabling NVE
snapmirror quiesce -destination-path svm_dr:vol_data_dr

volume encryption conversion start \
    -vserver svm_dr \
    -volume vol_data_dr

# Monitor conversion progress
volume encryption conversion show \
    -vserver svm_dr \
    -volume vol_data_dr

# Resume replication after conversion completes
snapmirror resume -destination-path svm_dr:vol_data_dr
```


```text title="Expected output"
Operation succeeded: SnapMirror destination quiesced.
Volume encryption conversion started for volume vol_data_dr on Vserver svm_dr.

Vserver     Volume         Conversion Progress State
----------- -------------- ------------------- ----------
svm_dr      vol_data_dr    87%                 in_progress

Vserver     Volume         Conversion Progress State
----------- -------------- ------------------- ----------
svm_dr      vol_data_dr    100%                completed

Operation succeeded: SnapMirror destination resumed.
```

!!! warning "Common errors"
    **`Error: command failed: volume encryption conversion start: Volume vol_data_dr is not quiesced`** — Run `snapmirror quiesce -destination-path svm_dr:vol_data_dr` before attempting encryption conversion.
    **`Error: command failed: snapmirror quiesce: SnapMirror relationship does not exist for destination svm_dr:vol_data_dr`** — Verify the SnapMirror relationship exists and use the correct destination path format `vserver:volume`.
    **`Error: command failed: volume encryption conversion start: Volume vol_data_dr is already encrypted`** — Check if NVE is already enabled on the volume using `volume encryption show -vserver svm_dr -volume vol_data_dr`.
---

## Key Management for Encrypted Destination Volumes

Destination volumes encrypted with NVE or NAE require a key manager to be configured on the destination cluster. The key manager can be either:

- **ONTAP Key Manager (OKM)** — built-in key manager suitable for non-regulated environments; keys stored on the cluster itself
- **External KMIP key manager** — external key management (Thales, Entrust, IBM, HashiCorp Vault) for regulated environments; required for FIPS and most compliance frameworks

```bash
# Verify key manager is configured on the destination cluster
security key-manager show

# For external KMIP key manager — show configured servers
security key-manager external show

# Check that keys are available for the destination volume
volume encryption show -vserver svm_dr -volume vol_data_dr \
    -fields key-id,encryption-state
```


```text title="Expected output"
Key Manager Configured: yes
Key Manager Type: external

Server Address                Port  Timeout (secs)  Username
-----------                  ----  ---------------  --------
kmip-server-01.corp.local    5696  60               admin
kmip-server-02.corp.local    5696  60               admin

Vserver     Volume        Key ID                               Encryption State
-------     ------        -------                              -----------------
svm_dr      vol_data_dr   550e8400-e29b-41d4-a716-446655440000 enabled
```

!!! warning "Common errors"
    **`Error: command not found: security key-manager show`** — Verify you are connected to a NetApp ONTAP cluster with sufficient privileges (run `cluster show` first to confirm connection).
    **`Error: No matching entries were found for the specified query`** — Ensure the destination SVM name and volume name are correct by running `volume show -vserver svm_dr` to list available volumes.
The source and destination clusters can use different key managers independently — encryption at the destination is entirely managed by the destination cluster's key manager configuration.

---

## SnapMirror Synchronous and SMBC Encryption

For SnapMirror Synchronous and SMBC (AutomatedFailOver) relationships, the same encryption controls apply. Because synchronous replication is latency-sensitive, verify that the AES-256 overhead is accounted for in the inter-site latency budget.

```bash
# Enable encryption on a SnapMirror Synchronous relationship
snapmirror modify \
    -destination-path svm_dr:vol_data \
    -encryption-algorithm aes-256 \
    -type sync

# Check SMBC consistency group relationship encryption
snapmirror show -type automatedfailover \
    -fields encryption-algorithm
```


```text title="Expected output"
Operation succeeded: SnapMirror relationship modified.
Encryption algorithm set to aes-256 for svm_dr:vol_data

Source Destination                Encryption Algorithm
------ -------------------------- --------------------
svm_src svm_dr:vol_data            aes-256
svm_src svm_dr:vol_data_2          aes-256
svm_src svm_dr:vol_data_3          none
svm_src svm_dr:vol_data_4          aes-256
...
```

!!! warning "Common errors"
    **`Error: This operation is not supported on relationships of type "sync"`** — Encryption cannot be modified on synchronous SnapMirror relationships; use asynchronous relationships instead.
    **`Error: command not found: snapmirror`** — Ensure you are logged into the ONTAP cluster CLI and have appropriate admin privileges.
---

## Compliance Mapping

| Requirement | ONTAP Control | Configuration |
|---|---|---|
| Data in transit — PCI-DSS, HIPAA | SnapMirror TDE (AES-256) | `snapmirror modify -encryption-algorithm aes-256` |
| Data at rest — PCI-DSS, HIPAA | NVE or NAE on destination volume | `volume create -encrypt true` or `volume encryption conversion start` |
| Key management — FIPS 140-2 | External KMIP with FIPS-certified HSM | `security key-manager external enable` |
| Transport TLS version | ONTAP intercluster TLS 1.2 minimum | `security config modify -min-protocol-version TLSv1.2` |
| Audit trail for key operations | ONTAP audit log | `security audit log show -cmdname "security key-manager"` |

---

## See also

- [Snapmirror — Hardening](../hardening/)
- [Snapmirror — Authentication](../authentication/)
- [Snapmirror — Access Control](../access-control/)

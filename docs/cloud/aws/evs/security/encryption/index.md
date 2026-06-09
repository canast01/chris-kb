# Amazon EVS — Encryption

<div class="kb-summary">
EVS encryption: vSAN encryption at rest, VM encryption via vSphere Encryption, TLS for all VCF management APIs, AWS KMS integration, and in-transit encryption for vMotion and vSAN traffic.
</div>

```text
┌─────────────────────────────────────── Amazon EVS — Encryption ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   vSAN encryption: cluster-level; requires KMS; AWS KMS + vSphere Native Key Provider        │    │
│   │   VM encryption: per-VM or per-policy; uses same KMS; independent of vSAN encryption         │    │
│   │   In-transit: vMotion encrypted by default (AES-256); vSAN uses NVMe-oF with TCP/TLS         │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## vSAN Encryption at Rest

```powershell
# Prerequisites:
# 1. Configure vSphere Native Key Provider (NKP) — built into vCenter 7.0 U2+
#    OR connect an external KMS (e.g., HashiCorp Vault, Thales, AWS CloudHSM)

# Option A: vSphere Native Key Provider (NKP) — simplest for EVS
# vCenter UI → Administration → Key Providers → Add Native Key Provider
# Backed up with vCenter; no external KMS dependency

# Enable vSAN encryption via PowerCLI
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
$vsanConfig = Get-VsanClusterConfiguration -Cluster $cluster
Set-VsanClusterConfiguration -VsanClusterConfiguration $vsanConfig -EncryptionEnabled $true
# Note: enabling encryption triggers full data rekey; 30-60 min for small clusters

# Verify encryption status
Get-VsanClusterConfiguration -Cluster $cluster | Select EncryptionEnabled
```

## AWS KMS Integration (External KMS)

```bash
# For compliance requirements needing hardware-backed keys (AWS KMS with CloudHSM):
# KMS custom key store → CloudHSM cluster → backed by dedicated HSM hardware

# Create KMS key for vSAN/VM encryption
aws kms create-key \
  --description "EVS vSAN Encryption Key" \
  --key-usage ENCRYPT_DECRYPT \
  --key-spec SYMMETRIC_DEFAULT \
  --tags TagKey=Project,TagValue=evs

# Get key ID for vCenter KMS configuration
aws kms describe-key --key-id <key-id> --query 'KeyMetadata.[KeyId,Arn]'

# Configure external KMS in vCenter
# vCenter → Administration → Key Providers → Add Standard Key Provider
# KMS vendor: select appropriate vendor (Thales, IBM, etc.)
# For AWS KMS native: use vSphere Native Key Provider backed by AWS KMS via custom key store
```

## VM Encryption Policy

```powershell
# Create VM Storage Policy with encryption
$policy = New-SpbmStoragePolicy -Name "VM-Encrypted" -Description "Encrypted VM policy"

# Associate encryption capability with policy
$rule = New-SpbmRule -AnyOfRuleSets @(
  New-SpbmRuleSet -AllOfRules @(
    New-SpbmRule -Capability (Get-SpbmCapability -Name "vmencryption.enabled") -Value $true
  )
)
Set-SpbmStoragePolicy -StoragePolicy $policy -RuleSet $rule

# Apply policy to VM
Set-VM -VM (Get-VM "my-vm") -StoragePolicy "VM-Encrypted"
# This triggers encryption of VM home + all disks — backup the VM first
```

## In-Transit Encryption

```bash
# vMotion encryption — enabled per VM or globally
# PowerCLI: Set-VM -VM $vm -EncryptedVMotion "Required"
# Options: Disabled, Opportunistic (default, encrypts if supported), Required (enforced)

# vSAN in-transit (data-in-transit encryption)
# Available in vSAN 7.0+ via vSAN Data-in-Transit Encryption
# PowerCLI:
$vsanConfig = Get-VsanClusterConfiguration -Cluster (Get-Cluster)
Set-VsanClusterConfiguration -VsanClusterConfiguration $vsanConfig \
  -DataInTransitEncryptionEnabled $true

# VCF management traffic — all APIs use TLS 1.2+ by default
# Verify TLS version on vCenter
openssl s_client -connect $VCENTER:443 </dev/null 2>/dev/null | grep -E "Protocol|Cipher"

# NSX-T management API — TLS 1.2 required
curl -sk --tlsv1.2 -u "admin:$NSX_PASSWORD" "$NSX_URL/api/v1/cluster/status" | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('mgmt_cluster_status',{}).get('status'))"
```

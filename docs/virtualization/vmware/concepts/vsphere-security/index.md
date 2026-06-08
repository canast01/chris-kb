# vSphere Security — Encryption, Identity, and VM Hardening

vSphere security covers a wide range of features from encrypting VM data at rest and in flight, to attestation of ESXi host integrity, to locking down administrative access. This page covers the security features tested on the VCP-DCV 8 exam — including VM Encryption, vSphere Trust Authority, vTPM, VBS, identity federation, lockdown mode, and Secure Boot.

---

## VM Encryption

vSphere VM Encryption (introduced in vSphere 6.5) encrypts VM data at rest — virtual machine disk files (VMDK), VM configuration files (VMX), and VM swap files.

### How VM Encryption Works

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    vSphere VM Encryption Flow                                                         │
│                                                                                                       │
│  ┌──────────┐   1. Request DEK     ┌───────────────────────────┐                                      │
│  │ vCenter  │ ──────────────────►  │  KMS (Key Provider)       │                                      │
│  │          │ ◄──────────────────  │  External or Native       │                                      │
│  │          │   2. Return KEK+DEK  └───────────────────────────┘                                      │
│  └────┬─────┘                                                                                         │
│       │ 3. Push encrypted DEK to ESXi host                                                            │
│       ▼                                                                                               │
│  ┌──────────┐                                                                                         │
│  │ ESXi     │  4. ESXi VMkernel decrypts DEK using KEK                                                │
│  │ Host     │     then uses DEK to encrypt/decrypt VM I/O                                             │
│  │          │                                                                                         │
│  │  [VM]    │  5. Data written to VMDK is always encrypted                                            │
│  │  VMDK    │     at the disk layer — transparent to guest OS                                         │
│  └──────────┘                                                                                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

KEK = Key Encrypting Key (managed by KMS, never stored on ESXi)
DEK = Data Encrypting Key (generated per VM, encrypted by KEK)
```

### What Gets Encrypted

| Component | Encrypted? | Notes |
|---|---|---|
| VMDK (virtual disk) | Yes | All data at rest |
| VMX (VM config file) | Yes | Contains vTPM secrets, credentials |
| VM swap file | Yes | Swap is encrypted (important exam point) |
| VM snapshot delta disks | Yes | Inherits encryption from parent |
| vMotion traffic | Optional | Encrypted vMotion — see below |
| Memory contents (RAM) | No | RAM is not encrypted at rest |

> **VCP-DCV Exam Note:** VM swap files ARE encrypted when VM Encryption is enabled. This is notable because early VMware documentation was ambiguous. On the exam, if asked what VM Encryption protects, include swap files. RAM contents are not encrypted (the guest OS can still read its own memory).

### KMS Integration

vCenter connects to a Key Management Server (KMS) to obtain keys. The KMS stores the Key Encrypting Keys (KEKs); vCenter and ESXi never store KEKs persistently.

**Key provider types:**

| Provider Type | Requires external KMS | Notes |
|---|---|---|
| Native Key Provider | No | Built into vCenter; keys stored in vCenter DB; simpler but keys tied to vCenter |
| Standard Key Provider | Yes | Connects to external KMIP-compliant KMS (HyTrust, Thales, IBM SKLM) |

> **VCP-DCV Exam Note:** The Native Key Provider does NOT require an external KMS server. It is the easiest way to enable VM Encryption and vTPM. However, if vCenter is lost without a backup of the Native Key Provider keys, encrypted VMs cannot be decrypted. Always export and back up the Native Key Provider. The Standard Key Provider requires an external KMIP 1.1+ compliant server.

### Encrypted vMotion

vMotion traffic can be encrypted independently of VM Encryption:
- Options: **Disabled**, **Opportunistic** (encrypt if both hosts support it), **Required** (refuse migration if encryption not possible)
- Configured per VM in VM Edit Settings → vMotion encryption
- Uses AES-256 GCM; negligible performance impact on modern hardware

### Encryption Policies

Storage policies can include an encryption component. Create a VM Storage Policy with the "VM Encryption" rule to automatically encrypt VMs placed on compliant datastores.

---

## vSphere Trust Authority (vTA)

vSphere Trust Authority (introduced in vSphere 7.0) provides a way to attest the integrity of ESXi hosts and control key release based on that attestation. It is designed for highly regulated environments where you need proof that the ESXi host software has not been tampered with before releasing encryption keys.

### Architecture

vTA uses two separate clusters:

```text
┌─────────────────────────┐      ┌──────────────────────────────────────────────────────────────────────┐
│  Trust Authority Cluster│      │      Trusted Cluster                                                 │
│  (TA hosts)             │      │  (workload hosts)                                                    │
│                         │      │                                                                      │
│  Runs:                  │      │  ESXi hosts that want keys                                           │
│  - Attestation service  │      │  must prove their identity                                           │
│  - Key Provider service │      │                                                                      │
│                         │      │  Host presents:                                                      │
│  Holds trusted          │◄─────│  - TPM 2.0 attestation quote                                         │
│  inventory:             │      │  - Boot measurements (PCR vals)                                      │
│  - Approved ESXi images │      │                                                                      │
│  - Approved TPM certs   │      │  TA verifies against inventory                                       │
│                         │      │  and releases keys if trusted                                        │
└─────────────────────────┘      └──────────────────────────────────────────────────────────────────────┘
```

### When to Use vTA

- Environments with strict regulatory requirements (PCI-DSS, HIPAA, government)
- When you need cryptographic proof that ESXi hosts are running approved software
- When you want to prevent key release to hosts with unauthorized software changes
- Air-gapped or high-security infrastructure where third-party KMS cannot be used

vTA is complex to deploy and requires TPM 2.0 chips in all workload hosts. For most environments, the Standard or Native Key Provider without vTA attestation is sufficient.

---

## Key Management — Key Rotation and Lifecycle

### Key Hierarchy

```text
KMS holds: Key Encrypting Key (KEK) [never leaves KMS]
    │
    │ Encrypts
    ▼
vCenter holds: Encrypted DEK (Data Encrypting Key)
    │
    │ Decrypted by ESXi at VM startup using KEK from KMS
    ▼
ESXi uses: Plaintext DEK in memory only (never written to disk)
    │
    │ Encrypts all I/O
    ▼
Storage: Encrypted VMDK, VMX, swap
```

### Key Rotation

**Shallow rekey** — generates a new DEK for the VM without decrypting and re-encrypting all disk data. Fast; requires the VM to be powered on.

**Deep rekey** — decrypts and re-encrypts all VM disk data with a new DEK. Slow (proportional to disk size); can be done while VM is running (online) or powered off.

```text
vSphere Client:
  VM → Actions → VM Policies → Re-encrypt (Shallow)
  VM → Actions → VM Policies → Re-encrypt (Deep)
```

---

## Virtual Trusted Platform Module (vTPM)

A vTPM is a software emulation of a physical TPM 2.0 chip, providing TPM functionality to a virtual machine without requiring a physical TPM on the guest hardware.

### What vTPM Enables

| Use case | Detail |
|---|---|
| Windows 11 requirement | Windows 11 requires TPM 2.0 — vTPM satisfies this |
| VM Secure Boot | vTPM stores Secure Boot keys for the guest OS |
| BitLocker encryption | BitLocker can seal keys in vTPM |
| Measured boot | Boot measurements stored in vTPM PCR registers |
| Application secrets | Guest applications can use vTPM for key storage |

### vTPM Requirements

| Requirement | Detail |
|---|---|
| ESXi version | ESXi 6.7 or later |
| vCenter | Required (manages vTPM key operations) |
| Key provider | Native or Standard Key Provider must be configured |
| VM firmware | EFI (UEFI) — not BIOS |
| RDM | Physical RDMs are not supported on vTPM VMs |
| Snapshots | Supported (vTPM state is included in snapshot) |

> **VCP-DCV Exam Note:** vTPM requires EFI firmware — you cannot add a vTPM to a VM using BIOS firmware. You must change the VM firmware to EFI before adding vTPM (requires power off). Also, a Key Provider (Native or Standard) must be configured in vCenter before vTPM can be added to any VM. Without a key provider, the "Add vTPM" option is greyed out.

### vTPM vs Physical TPM

| Feature | vTPM | Physical TPM |
|---|---|---|
| Lives in | Software (VMX file) | Hardware chip on motherboard |
| Follows VM | Yes (with VM files) | No (stays with physical host) |
| Required for ESXi Secure Boot | No (uses UEFI Secure Boot) | Yes (for vTA attestation) |
| Required for VM Secure Boot | Yes | No |
| Backed up with VM | Yes | No |

---

## BIOS vs UEFI Firmware

Each VM has a firmware type that determines how it boots and what security features are available.

### Comparison

| Feature | BIOS | EFI (UEFI) |
|---|---|---|
| Boot process | MBR → bootloader | UEFI firmware → EFI partition → bootloader |
| Secure Boot support | No | Yes |
| vTPM support | No | Yes |
| VBS support | No | Yes |
| Disk partition scheme | MBR (max 2 TB) | GPT (no practical limit) |
| Windows 11 support | No | Yes |
| Max boot disk | 2 TB | 64 TB+ |

### Changing Firmware Type

The firmware type can only be changed when the VM is powered off. Changing from BIOS to UEFI on an existing OS may break the boot — the OS partition table and bootloader must be converted separately.

```text
vSphere Client (VM must be powered off):
  VM → Edit Settings → VM Options → Boot Options → Firmware
  → Change from BIOS to EFI

PowerCLI:
  $spec = New-Object VMware.Vim.VirtualMachineConfigSpec
  $spec.firmware = "efi"
  (Get-VM "PROD-VM01").ExtensionData.ReconfigVM($spec)
```

> **VCP-DCV Exam Note:** Changing from BIOS to EFI does NOT automatically install or convert the operating system. A Windows VM will likely fail to boot after a firmware change unless you have also converted the disk from MBR to GPT. On the exam, know that UEFI is required for Secure Boot, vTPM, and VBS — but the firmware change itself requires a power-off.

---

## Virtualization-Based Security (VBS)

VBS is a Windows security feature (Windows 10 1607+ / Windows Server 2016+) that uses the hypervisor to create an isolated secure world within the guest OS itself. Hyper-V technology implements VBS inside Windows — vSphere exposes the necessary nested virtualization features to support this.

### What VBS Provides

- **Credential Guard** — protects Windows credential hashes in isolated secure world
- **HVCI (Hypervisor-Protected Code Integrity)** — prevents unsigned kernel code from running
- **Device Guard** — policy-based application whitelisting enforced by hypervisor

### VBS Requirements in vSphere

| Requirement | Detail |
|---|---|
| VM firmware | EFI (UEFI) |
| vTPM | Required (for key storage) |
| Secure Boot | Must be enabled on the VM |
| CPU | Intel VT-x with EPT or AMD-V with RVI |
| VM hardware version | 14 or later (vSphere 6.7+) |
| Windows version | Windows 10 1607+ or Windows Server 2016+ |

> **VCP-DCV Exam Note:** VBS requires UEFI firmware, vTPM, and Secure Boot — all three must be present. There is a measurable performance overhead (typically 5-15% on compute-intensive workloads) because the hypervisor must handle additional context switches between the normal and secure worlds. Enable VBS only on VMs that need Windows security features like Credential Guard.

### Enabling VBS

```text
vSphere Client (VM must be powered off):
  VM → Edit Settings → VM Options → Security → 
  Enable Virtualization Based Security: Yes

  This automatically enables:
  - EFI firmware requirement
  - Secure Boot
  - vTPM (if not already present)
  - I/O MMU (required for DMA protection)
```

---

## Identity Federation

Traditional vCenter authentication uses LDAP identity sources (Active Directory, OpenLDAP) where vCenter directly queries the directory. Identity Federation replaces this with an external Identity Provider (IdP) using OIDC/OAuth 2.0.

### How Identity Federation Works

```text
Admin browser ──────► vCenter login page
                             │
                    Redirect to external IdP
                             │
                             ▼
                    ┌──────────────────┐
                    │  External IdP    │
                    │  (Okta, ADFS,    │
                    │   Azure AD)      │
                    └────────┬─────────┘
                             │ IdP authenticates user
                             │ Issues ID token (JWT)
                             ▼
                    vCenter receives token
                    Validates token signature
                    Maps groups → vCenter roles
                             │
                             ▼
                    Admin logged in to vCenter
```

### Federation vs Traditional LDAP

| Feature | Traditional LDAP | Identity Federation (OIDC) |
|---|---|---|
| Protocol | LDAP/LDAPS | OIDC / OAuth 2.0 |
| Credential handling | vCenter queries AD directly | IdP handles credentials — vCenter never sees password |
| MFA support | Requires additional integration | Native (IdP enforces MFA) |
| SSO across apps | Limited | Yes — same IdP session |
| vCenter sees user password | Yes (bind credentials) | No |
| Supported IdPs | AD, OpenLDAP | Okta, ADFS, Azure AD, PingFederate |

> **VCP-DCV Exam Note:** With Identity Federation, vCenter acts as an OAuth 2.0 client — it never receives the user's password. Authentication happens entirely at the IdP. This is a security improvement over LDAP where vCenter must have bind credentials to query Active Directory. Federation also enables native MFA enforcement at the IdP level without additional vCenter configuration.

### Configuring Federation

```text
vSphere Client:
  vCenter → Administration → Single Sign On → Configuration →
  Identity Provider → Set up Federation

  Required inputs:
  - Client ID (from IdP registration)
  - Client Secret
  - IdP discovery URL (OpenID Connect metadata endpoint)
  - Redirect URI (provided by vCenter)
```

---

## Lockdown Mode

Lockdown mode restricts administrative access to an ESXi host so that all management must go through vCenter, not directly to the host.

### Lockdown Mode Levels

| Mode | Direct SSH | DCUI | vCenter API | ESXCLI (via vCenter) |
|---|---|---|---|---|
| Disabled | Yes | Yes | Yes | Yes |
| Normal lockdown | No | Yes (limited) | Yes | Yes |
| Strict lockdown | No | No | Yes | Yes |

**Normal lockdown** — Direct SSH login is blocked. The DCUI (Direct Console User Interface — the physical/iKVM console) remains accessible for emergency access. Users on the DCUI exception list can log in.

**Strict lockdown** — Even the DCUI is disabled. The host is completely sealed from direct access. If vCenter is unavailable, the only recovery path is physical console access and disabling lockdown mode from the DCUI (which is itself disabled — so a host network outage + strict lockdown = potentially inaccessible host).

> **VCP-DCV Exam Note:** In strict lockdown mode, even local console (DCUI) access is blocked. The exception users list still applies for API access via vCenter but not for DCUI. If both strict lockdown AND vCenter are unavailable, the only recovery is to reboot the host and break into the boot process. For most environments, normal lockdown is the recommended setting.

### Exception Users

The exception users list (configured in vCenter for each host) defines accounts that can directly access the host even in lockdown mode via the vSphere API:

```text
vSphere Client:
  Host → Configure → Security Profile → Lockdown Mode →
  Edit → Exception Users → Add accounts
```

Typical exception users: monitoring service accounts (Aria Operations), backup agents.

---

## Secure Boot for ESXi

Secure Boot is a UEFI firmware feature that verifies digital signatures at each stage of the boot process. For ESXi, it ensures that only cryptographically signed software is loaded.

### ESXi Boot Chain with Secure Boot

```text
1. UEFI Firmware
   Verifies bootloader signature against UEFI Secure Boot database (db)
        │
        ▼
2. ESXi Bootloader (mboot.efi)
   Signature checked by UEFI
        │
        ▼
3. VMkernel (vmkernel.gz)
   Signature checked by mboot.efi
        │
        ▼
4. ESXi Base System (esxbase.tgz)
   All VIBs must be signed at acceptance level "VMwareCertified"
   or "VMwareAccepted"
        │
        ▼
5. Third-party drivers and VIBs
   Must be signed — unsigned VIBs cause boot failure
```

### What Secure Boot Prevents

- Bootkit malware that modifies the bootloader
- Unsigned kernel modules being loaded (prevents rootkits)
- Tampered ESXi installation images
- Third-party unsigned VIBs from loading

> **VCP-DCV Exam Note:** Enabling Secure Boot on ESXi will cause the host to fail to boot if any installed VIBs are not signed at an acceptable acceptance level. Before enabling Secure Boot, run the check: `esxcli software vib list | grep -v "VMwareCertified\|VMwareAccepted\|PartnerSupported"` to identify any unsigned VIBs that would block the boot.

### Secure Boot Requirements for ESXi

| Requirement | Detail |
|---|---|
| Host firmware | UEFI (not legacy BIOS) |
| UEFI version | UEFI 2.3.1 or later |
| ESXi version | ESXi 6.5+ |
| VIB acceptance level | VMwareCertified, VMwareAccepted, or PartnerSupported |
| vTA (optional) | Not required for basic Secure Boot; required for TPM attestation |

```bash
# Verify Secure Boot status on ESXi host
esxcli system settings encryption get

# Check VIB acceptance levels (ensure no unsigned VIBs before enabling Secure Boot)
esxcli software vib list --rebooting-image | awk '{print $1, $5}'
```

---

## Security Architecture Summary

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                  vSphere Security Layers                                                              │
│                                                                                                       │
│  Layer 1: Infrastructure Access Control                                                               │
│    Lockdown mode → blocks direct ESXi access                                                          │
│    Identity Federation → centralised IdP, no password at vCenter                                      │
│    RBAC roles → least-privilege access in vCenter                                                     │
│                                                                                                       │
│  Layer 2: Host Integrity                                                                              │
│    UEFI Secure Boot → boot chain signature verification                                               │
│    vSphere Trust Authority → TPM attestation before key release                                       │
│                                                                                                       │
│  Layer 3: VM Data Protection                                                                          │
│    VM Encryption → VMDK + VMX + swap encrypted at rest                                                │
│    Encrypted vMotion → data encrypted in transit                                                      │
│    vTPM → VM-level TPM for guest OS security features                                                 │
│                                                                                                       │
│  Layer 4: Guest OS Hardening                                                                          │
│    VBS → Credential Guard, HVCI inside Windows guests                                                 │
│    VM Secure Boot → UEFI + vTPM enforces signed guest bootchain                                       │
│    VMXNET3 + pvSCSI → paravirtual drivers (smaller attack surface)                                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference — Key Facts for VCP-DCV

| Topic | Key fact |
|---|---|
| VM swap encrypted? | Yes — swap IS encrypted with VM Encryption |
| Native Key Provider requires external KMS? | No — keys stored in vCenter database |
| Standard Key Provider protocol | KMIP 1.1 or later |
| vTPM requires firmware type | EFI (UEFI) — not BIOS |
| vTPM requires key provider? | Yes — Native or Standard must be configured |
| VBS requires | EFI firmware + vTPM + Secure Boot (all three) |
| Lockdown normal vs strict | Normal: DCUI accessible; Strict: DCUI blocked |
| Identity Federation protocol | OIDC / OAuth 2.0 |
| Secure Boot blocks | Unsigned VIBs cause boot failure |
| vTA requires | TPM 2.0 in all workload hosts |
| Encrypted vMotion options | Disabled / Opportunistic / Required |
| Key rotation shallow vs deep | Shallow: new DEK, no re-encrypt; Deep: full disk re-encrypt |

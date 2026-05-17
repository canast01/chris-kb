# RASR — Architecture

<div class="kb-summary">
Dell RASR (Recovery and System Restore) bare-metal recovery for Windows Server — WinPE boot media, sector-level image capture, and iDRAC virtual media integration.
</div>

![RASR Architecture](../../../../assets/rasr-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Recovery workflow, WinPE environment, Dell hardware integration, and RASR vs alternatives.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>iDRAC virtual media, OpenManage, and network share integration.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Image naming, share layout, rotation policy, and testing schedule.</span></a>
</div>

| Component | Role |
|---|---|
| RASR Agent | Windows service on protected server; orchestrates image capture |
| RASR Boot Media | WinPE USB or ISO with PERC/NIC drivers; used for bare-metal recovery |
| Recovery Image | Compressed sector-level snapshot stored on SMB share |
| Network Recovery Share | SMB share where images are stored and retrieved |
| iDRAC Virtual Media | Mounts RASR ISO remotely — enables headless bare-metal recovery |

```mermaid
flowchart TD
  FAIL(["Server Failure"]) --> IDRAC["iDRAC mounts RASR ISO\n(virtual media)"]
  IDRAC --> WINPE["WinPE Environment\nloads PERC + NIC drivers"]
  WINPE --> MAP["Map SMB share\nnet use Z: \\\\nas\\rasr-images"]
  MAP --> SEL["Select recovery image"]
  SEL --> REST["Image written to disk\npartition table restored"]
  REST --> BOOT["Reboot → Windows starts\nfrom restored image"]
  BOOT --> VALID(["Post-restore validation"])
  classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef terminal fill:#15803d,stroke:#166534,color:#fff
  class IDRAC,WINPE,MAP,SEL,REST,BOOT action
  class FAIL,VALID terminal
```

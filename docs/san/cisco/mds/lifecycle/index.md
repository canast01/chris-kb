# Cisco MDS Lifecycle

NX-OS versions for MDS 9000 are tracked on the Cisco Software Advisor and aligned with the HCL requirements of connected hosts and storage arrays. EPLD (FPGA) firmware is updated separately from NX-OS and is required when upgrading across certain major NX-OS versions. Upgrades can use the `install all` command for a controlled upgrade (reloads the switch) or ISSU (In-Service Software Upgrade) on director platforms meeting the ISSU prerequisites. End-of-sale and end-of-support dates are tracked in the CMDB with alerts triggered 18 months before end-of-support.

| Upgrade Method | Applicability | Notes |
|---|---|---|
| `install all` | All platforms | Reloads switch; plan maintenance window |
| ISSU | Director (9706/9710) | Non-disruptive; strict prerequisites apply |
| EPLD upgrade | All platforms | Required for some NX-OS major version jumps |

# Veeam Lifecycle

Veeam releases major versions annually (e.g., VBR 12, 12.1, 12.2) with cumulative patches (P-releases) throughout the year. N-1 minor version support means a VBR 12.0 proxy is supported when the Backup Server runs 12.1, but N-2 is not supported and will produce upgrade warnings. Veeam ONE must match the VBR major version. Upgrade order: Veeam Backup Server first, then Backup Proxies, then Repository agents (Veeam Agent for Linux/Windows on managed repositories).

| Component | Upgrade Order | Notes |
|---|---|---|
| Veeam Backup Server | 1st | Config DB backed up automatically pre-upgrade |
| Veeam ONE | 2nd (if deployed) | Must match VBR major version |
| Backup Proxies | 3rd | Managed via VBR console |
| Repository Agents | 4th | Linux/Windows agents updated via VBR |

- License model: per-socket (legacy) or Veeam Universal License (VUL) per-workload — track consumed instances vs purchased in the VBR license report.
- EOL versions: check veeam.com/product-lifecycle for the current support matrix.
- Config DB backup: run `Veeam Backup & Replication > Main Menu > Export Configuration` before every upgrade.

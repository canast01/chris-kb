# CyberArk Architecture

CyberArk Privileged Access Manager (PAM) is built around the Digital Vault, an encrypted, hardened credential store that is the sole authoritative source for managed passwords and SSH keys. The Central Policy Manager (CPM) connects to target systems to rotate credentials automatically on schedule or on-demand, while the Privileged Session Manager (PSM) proxies and records privileged sessions without exposing credentials to the user. Password Vault Web Access (PVWA) provides the web UI and REST API gateway; in enterprise deployments the Vault runs as an HA pair with a Disaster Recovery (DR) vault replica for business continuity.

| Component | Role | Typical Count |
|---|---|---|
| Digital Vault | Encrypted credential store, core engine | 2 (primary + DR) |
| CPM (Central Policy Manager) | Automated password rotation | 1–2 per site |
| PSM (Privileged Session Manager) | Session proxy, recording, isolation | 2+ (load-balanced) |
| PVWA (Password Vault Web Access) | Web UI and REST API | 2+ (load-balanced) |
| PSMP | SSH proxy for Linux privileged access | 1–2 per site |
| CyberArk SaaS (PAM – Self-Hosted vs. Cloud) | Managed SaaS alternative to on-prem Vault | N/A |

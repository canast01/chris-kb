# CloudIQ — Encryption

> Part of the [CloudIQ](../../) reference.

---

| Layer | Protection |
|---|---|
| Telemetry in transit (SCG to Dell) | TLS 1.2 or higher; certificate-pinned connection from SCG to Dell SRS endpoint |
| Telemetry at rest (Dell cloud) | Encrypted at rest in Dell's cloud infrastructure |
| Portal access | HTTPS (TLS 1.2+); sessions protected by Dell's cloud infrastructure |
| Data content | Telemetry contains configuration metadata and performance statistics only — no user data, file contents, or host data is transmitted |

CloudIQ telemetry does not include: file names, directory paths, user credentials, application data, or any content stored on the managed arrays.

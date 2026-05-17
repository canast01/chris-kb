# FOD — Encryption

> Part of the [Flex on Demand](../../) reference.

---

## Encryption Controls

| Control | Detail |
|---|---|
| **Telemetry transmission** | Capacity metrics are forwarded from the array to CloudIQ via the Secure Connect Gateway (SCG) over TLS 1.2 or higher. The payload contains only capacity counters — no user data, file contents, or host identifiers are transmitted. |
| **APEX Console access** | The APEX Console web UI and its underlying REST API are served exclusively over HTTPS (TLS 1.2+). Certificate management is handled by Dell's cloud infrastructure; no customer-managed certificate is required. |
| **SCG communication security** | The SCG appliance initiates all outbound connections to Dell's cloud endpoints. It uses certificate pinning to validate Dell's cloud TLS certificates, preventing man-in-the-middle interception. Inbound connections from Dell to the SCG are not required and should be blocked at the perimeter firewall. |
| **Data-at-rest** | FOD is a metering and billing overlay; it does not own storage volumes. Data-at-rest encryption is governed entirely by the underlying array (PowerStore, PowerMax, Unity XT, etc.). Refer to the respective platform's security documentation for encryption configuration — for example, PowerStore supports D@RE using self-encrypting drives managed through Unisphere. |
| **API encryption** | All APEX API calls (OAuth token exchange and subsequent requests) are made over HTTPS. API credentials are bearer tokens scoped to a service account; credentials in transit are protected by the same TLS layer as the console. |
| **Internal array-to-SCG path** | Communication between the array and the co-located or remote SCG appliance travels over the management network segment. Place the SCG on a VLAN that is accessible to the array management interface only; do not route SCG traffic through untrusted segments. |

## Key Points

- No user data or file content ever leaves the array through the FOD telemetry path.
- TLS 1.2 is the minimum enforced by Dell's endpoints; TLS 1.0 and 1.1 are not accepted.
- Data-at-rest encryption for stored data is a platform-level control, not a FOD control.
- If SCG uses a proxy for outbound internet access, ensure the proxy does not perform TLS inspection on Dell cloud endpoints — certificate pinning will cause the connection to fail.

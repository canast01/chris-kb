# Superna Eyeglass — Encryption

The Eyeglass management console must be accessible only via HTTPS — HTTP access should be disabled or redirected. All communication between Eyeglass and the PowerScale OneFS API uses HTTPS (ports 8080/443).

| Control | Detail |
|---|---|
| Console access | HTTPS only; HTTP access disabled or redirected |
| API token management | Store in secrets manager; rotate on schedule and on personnel change |

API tokens used by automation scripts must be stored in a secrets manager (e.g. CyberArk, HashiCorp Vault) and rotated on a defined schedule. Tokens should not be stored in plaintext in scripts or version control.

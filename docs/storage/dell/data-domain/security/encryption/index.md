# Data Domain — Encryption

## Encryption at Rest (D@RE)

Data Domain supports software-based encryption of all on-disk data.

```bash
# Check current encryption status
encryption status

# Enable encryption (must be done before data is written — cannot encrypt retroactively)
encryption enable

# Configure key management — DDOS supports:
#   - Internal key manager (built-in, no external dependency)
#   - RSA DPM (Dell Key Management)
#   - KMIP-compatible external key managers (Thales, Vormetric, etc.)

# Set key manager to internal (default for standalone deployments)
encryption change-key-manager internal

# View current key manager configuration
encryption show config
```

**Important:** Enabling encryption after data is already written requires a full filesystem rebuild. Always enable D@RE at initial commissioning before writing any backup data.

DDOS D@RE is FIPS 140-2 certified (AES-256 in CBC mode).

## FIPS Compliance

DDOS is FIPS 140-2 validated for the D@RE encryption module. To confirm:

```bash
encryption status  # look for "FIPS Mode: Enabled" in the output
system show        # confirm DDOS version — cross-reference with NIST CMVP certificate
```

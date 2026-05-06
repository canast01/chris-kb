# Venafi Standards

The Venafi policy tree is structured as folders by environment (e.g., `\VED\Policy\Internal\Production`, `\VED\Policy\External\Public`), with consistent naming for policy folders and certificate objects using lowercase-hyphenated identifiers including environment, FQDN, and purpose. Validity period standards are 1–3 years for internal certificates and 1 year for external/public-facing certificates.

Key algorithm requirements are RSA-4096 or ECDSA P-256 minimum. All certificates must include Subject Alternative Names (SANs); Common Name alone is not sufficient. Wildcards are permitted for internal domains but restricted for external certificates and must receive explicit policy approval.

| Standard | Requirement |
|---|---|
| Internal validity | 1–3 years |
| External validity | 1 year maximum |
| Key algorithm | RSA-4096 or ECDSA P-256 |
| Hash algorithm | SHA-256 minimum |
| SAN usage | Mandatory on all certificates |
| Wildcards (external) | Restricted — approval required |

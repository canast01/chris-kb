# Certificates Lifecycle

The certificate lifecycle spans six stages: enrolment (request generation and submission), issuance (CA signs and returns the certificate), installation (deploy to the target service), monitoring (track validity and upcoming expiry), renewal (re-issue before expiry — triggered at 80% of validity period), and revocation (invalidate before expiry when compromise or decommission occurs). Auto-renewal should be configured wherever possible via Venafi, ACME, or cert-manager.

CA certificate renewal requires coordinating with all relying parties before the old CA certificate expires. Root CA key ceremonies must follow a formal procedure with witnessed key generation, HSM escrow, and cross-signing if replacing a Root CA.

| Stage | Trigger | Owner |
|---|---|---|
| Enrolment | Service provisioning or renewal request | Application / infra team |
| Issuance | CA receives valid CSR | CA (automated or manual) |
| Installation | Certificate issued | Application / infra team |
| Renewal | 80% of validity elapsed | Automated (Venafi / ACME) |
| Revocation | Compromise, decommission, or policy violation | Certificate owner + CA admin |
| CA renewal | Before CA cert expiry | PKI team |

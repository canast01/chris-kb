# Certificates Operations

Weekly operations include reviewing the certificate expiry dashboard for certificates expiring within 30, 60, and 90 days, checking CRL and OCSP responder availability for all CAs, verifying CA service health (for ADCS: check Certificate Services in Server Manager and confirm the service is running), and confirming auto-renewal jobs completed successfully. Monthly, audit newly issued certificates against naming and validity standards.

OCSP and CRL freshness must be checked proactively — a stale CRL can cause widespread certificate validation failures across services that depend on it.

**Weekly checklist:**

- [ ] Review expiry dashboard — 30 / 60 / 90-day buckets
- [ ] Check CRL freshness and OCSP responder health for each CA
- [ ] Verify ADCS Certificate Services is running (`Get-Service -Name CertSvc`)
- [ ] Confirm auto-renewal jobs (Venafi / ACME) completed without error
- [ ] Review any newly discovered unmanaged certificates

**Monthly checklist:**

- [ ] Audit newly issued certificates against naming and validity standards
- [ ] Review wildcard certificate usage
- [ ] Confirm CA certificate expiry dates and plan renewals if within 6 months

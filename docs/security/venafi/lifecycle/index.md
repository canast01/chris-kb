# Venafi Lifecycle

Venafi TPP follows a version matrix that must be validated against CA integration compatibility and supported OneFlow / REST API versions before each upgrade. The upgrade procedure is: take a full database backup, upgrade the primary Policy Server, validate functionality, then upgrade the secondary. Edge versioning is managed separately and must remain compatible with the TPP version in use.

EOL tracking should be maintained against Venafi's published support lifecycle. Migration from TPP to TLS Protect Cloud (VaaS) requires policy tree export, CA re-integration, and re-enrolment of managed certificates in the cloud platform.

| Stage | Action |
|---|---|
| Pre-upgrade | Full DB backup, CA integration compatibility check |
| Upgrade | Primary Policy Server → validate → secondary |
| Post-upgrade | Validate certificate workflows, CA connectivity, Edge Proxy registration |
| EOL tracking | Review Venafi support lifecycle quarterly |
| TPP → VaaS migration | Policy export, CA re-integration, certificate re-enrolment |

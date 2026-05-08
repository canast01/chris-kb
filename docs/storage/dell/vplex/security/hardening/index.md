# Dell VPLEX — Hardening

> Security baselines and compliance configuration for Dell VPLEX.

## Hardening Checklist

- [ ] Change default VMS local account passwords immediately after deployment
- [ ] Replace the default self-signed TLS certificate on Unisphere for VPLEX with a corporate CA-signed certificate
- [ ] Enforce SSH key authentication for VMS access; disable password-based SSH for the `service` account in production
- [ ] Restrict VMS management access to the management network VLAN; block direct internet access to VMS
- [ ] Create named service accounts for automation; do not use the `service` account interactively for routine tasks
- [ ] Enable syslog forwarding from VMS to the SIEM for management action auditing
- [ ] Remove or disable unused local accounts on VMS
- [ ] Keep GeoSynchrony firmware on a supported release; refer to the version matrix in Install & Upgrade
- [ ] Review storage views quarterly to remove orphaned initiators from decommissioned hosts
- [ ] Back up the VMS VM before every change; verify backup integrity
- [ ] Ensure the Witness VM is deployed in a separate failure domain and managed on a separate management network segment from the VPLEX clusters

# Linux Standards

Hostnames follow the convention `<site>-<role>-<nn>` (e.g., `lon-app-01`), assigned at provisioning and never changed post-deployment. All servers use a standard partition layout with dedicated volumes for `/`, `/var`, `/tmp`, `/home`, and swap, managed via LVM to allow future resizing. Package management uses `dnf`/`yum` on RHEL and `apt` on Ubuntu, with repositories locked to approved mirrors. SSH is configured for key-based authentication only (`PasswordAuthentication no`), NTP is configured against internal time servers, and syslog is forwarded to the central logging platform.

| Item | Standard |
|---|---|
| Hostname format | `<site>-<role>-<nn>` |
| Auth method | SSH key only |
| NTP | Internal NTP servers |
| Syslog | Forward to central syslog |
| Package repos | Approved internal mirrors |

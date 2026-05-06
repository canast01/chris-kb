# Linux Vendor Support

Red Hat support cases are opened via the Red Hat Customer Portal (access.redhat.com) using the team's subscription account. Ubuntu/Canonical support is accessed through Ubuntu Advantage (ubuntu.com/advantage). When opening a case, collect a `sosreport` on RHEL (`sosreport` command, output in `/var/tmp/`) or use `ubuntu-bug` on Ubuntu for automated data collection. Kernel crash dump analysis requires `kdump` to be configured and crash dumps available in `/var/crash/`. Support entitlement can be verified with `subscription-manager status` (RHEL) or `ua status` (Ubuntu).

- RHEL: Red Hat Customer Portal — access.redhat.com
- Ubuntu: Ubuntu Advantage — ubuntu.com/advantage
- Diagnostic bundle (RHEL): `sosreport` → `/var/tmp/sosreport-*.tar.xz`
- Diagnostic bundle (Ubuntu): `ubuntu-bug` or `apport-collect`
- Entitlement check (RHEL): `subscription-manager status`
- Entitlement check (Ubuntu): `ua status`
- Crash dump: `kdump` service, dumps in `/var/crash/`

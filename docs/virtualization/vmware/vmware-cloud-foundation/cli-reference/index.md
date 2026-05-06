# VMware Cloud Foundation CLI Reference

VCF CLI operations are spread across the SoS (Support and Operations Suite) utility on SDDC Manager, the SDDC Manager REST API, the `vcf-support-bundle` tool, and direct SSH commands on individual components. SoS is the primary health-check and diagnostic tool and is run from the SDDC Manager appliance. Password management for VCF-managed credentials is performed via the `password-manager` service or the SDDC Manager UI.

| Command | Description |
|---|---|
| `python3 /opt/vmware/sddc-support/sos --health-summary` | Run SoS full health check across all domains |
| `python3 /opt/vmware/sddc-support/sos --health-check --domain <name>` | Run health check for a specific workload domain |
| `python3 /opt/vmware/sddc-support/sos --help` | List all SoS flags and options |
| `vcf-support-bundle --type lcm` | Collect LCM-specific support bundle |
| `vcf-support-bundle --type sddc` | Collect full SDDC Manager support bundle |
| `curl -sk -u 'admin:<pass>' https://sddc-mgr/v1/domains` | List all VCF domains via API |
| `curl -sk -u 'admin:<pass>' https://sddc-mgr/v1/clusters` | List all clusters via API |
| `curl -sk -u 'admin:<pass>' https://sddc-mgr/v1/credentials` | List managed credentials via API |
| `systemctl status sddc-manager` | Check SDDC Manager service status |
| `tail -f /var/log/vmware/vcf/lcm/lcm-debug.log` | Follow LCM debug log on SDDC Manager |

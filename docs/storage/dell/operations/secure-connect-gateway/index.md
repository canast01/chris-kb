# Secure Connect Gateway — Operations

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Bash multi-site SCG health poller, Python device registration diff tool, and Ansible SCG remediation playbook.</span>
</a>

</div>

## Purpose

Operational runbook for managing the Secure Connect Gateway fleet across multiple sites. SCG is the critical telemetry and support-access broker — a failed SCG silently stops CloudIQ data, disables SupportAssist auto-case creation, and blocks Dell remote support access. This page covers daily operations, incident response, and change procedures for the SCG estate.

## Common Checks

- **SCG service health**: Confirm the `dell-scg` service is running on all SCG appliances (or VMs)
- **Outbound connectivity**: Test that each SCG can reach `esrs.emc.com` and `cloudiq.dell.com` on port 443
- **Device registration count**: Compare registered device count in SCG GUI against the expected inventory — missing devices indicate a registration issue
- **Version currency**: Confirm all SCG appliances are on the current recommended version (check Dell support advisories)
- **Certificate expiry**: Review the SCG appliance TLS certificate expiry date — expired certs break all device registrations
- **CloudIQ telemetry continuity**: Confirm no storage systems show as offline in CloudIQ, which indicates SCG connectivity loss

## Incident Response

### SCG appliance unreachable

1. Confirm the SCG VM is powered on and the management IP is pingable
2. Check the SCG service: `systemctl status dell-scg`; restart if stopped: `systemctl restart dell-scg`
3. Test outbound connectivity: `curl -sv https://esrs.emc.com` — look for TLS handshake success
4. If VM is powered off or unresponsive, power on via hypervisor console; check for disk/memory resource exhaustion
5. Once SCG is healthy, confirm devices re-establish connectivity in the SCG GUI within 5–15 minutes
6. Check CloudIQ to confirm telemetry resumes; note the gap start/end times for billing reconciliation if FOD/STaaS is in use

### Device showing disconnected in SCG

1. Log into the SCG GUI → Devices and identify the disconnected device
2. Confirm the device management IP is reachable from the SCG appliance: `ping <device-ip>`
3. Re-register the device from the array management interface:
   - **PowerMax**: `symcfg -esrs register` or via Unisphere Administration → Remote Support
   - **Unity**: Unisphere → Settings → Remote Support → Configure
   - **PowerScale**: `isi esrs modify --enabled true`
4. Confirm the device returns to Connected state in the SCG GUI
5. Verify CloudIQ resumes receiving telemetry from the device

## Change Notes

For SCG upgrades:

- **Approval**: SCG upgrades are low-risk but require a maintenance window notification — telemetry gaps of up to 15 minutes can occur during restart
- **Rollback plan**: Download and retain the current SCG version OVA/package before upgrading; VM snapshot if running on vSphere
- **Validation steps**: After upgrade, confirm SCG version in GUI, all devices return to Connected state, and CloudIQ shows no telemetry gap beyond the maintenance window

For new SCG deployments:

- **Pre-work**: Confirm DNS resolution for `esrs.emc.com` and `cloudiq.dell.com` from the SCG network segment; confirm port 443 outbound is open
- **Deployment**: Deploy OVA to vSphere; run initial setup wizard; register SCG with Dell ESRS
- **Post-work**: Register all arrays at the site as primary or secondary SCG; confirm all appear in SCG GUI and CloudIQ

## Best Practices

- Deploy at least two SCG appliances per site and register arrays to both as primary/secondary — single-SCG sites have a monitoring blind spot whenever the SCG is patched or rebooted
- Automate SCG health checks via the local REST API and alert on service unavailability within 15 minutes
- Keep a record of which arrays are registered to which SCG — the SCG GUI shows this but it is not exported easily; maintain a runbook table
- Test SCG failover annually by intentionally stopping the primary SCG and confirming arrays reconnect to the secondary within 10 minutes

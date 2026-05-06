# Brocade Fabric OS Vendor Support

Support for Fabric OS is handled through the Broadcom Support Portal (support.broadcom.com), where service requests are opened against the relevant switch serial number and support contract. When opening a case, run `supportsave` on the affected switch to collect the full diagnostic bundle (logs, configs, port data, and event history), which is uploaded to the case. Required information includes the Fabric OS version (`version` command), fabric topology, zone count, and a description of the failure event with timestamps. Support contract entitlement is verified via the switch serial number on the Broadcom portal.

- Support portal: support.broadcom.com
- Diagnostic bundle: `supportsave` — generates a compressed archive to the configured FTP/SCP server
- Required for case: FOS version, fabric topology diagram, zone count, error log excerpts
- Serial number: `chassisshow` or label on switch chassis
- Entitlement check: serial number lookup on Broadcom portal

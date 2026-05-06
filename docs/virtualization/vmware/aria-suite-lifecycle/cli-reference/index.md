# Aria Suite Lifecycle CLI Reference

The primary CLI tool on the LCM appliance is `vracli`, which provides sub-commands for certificate management, cluster status, service control, and configuration. SSH access to the LCM appliance uses the `vidm` user for VIDM nodes and `root` for the LCM appliance itself (key-based auth recommended). All `vracli` commands must be run as root on the LCM appliance.

| Command | Description |
|---|---|
| `vracli status` | Show overall LCM appliance and managed service status |
| `vracli cluster status` | Display cluster node health and quorum state |
| `vracli certificate list` | List certificates stored in the Locker |
| `vracli certificate import --cert <file> --key <file>` | Import a certificate/key pair into the Locker |
| `vracli services list` | List all registered LCM-managed services and their state |
| `vracli services restart <service>` | Restart a named LCM service |
| `vracli proxy set --host <host> --port <port>` | Configure outbound proxy for bundle downloads |
| `vracli proxy show` | Display current proxy configuration |
| `journalctl -u lcm --since "1 hour ago"` | Stream recent LCM service journal logs |
| `tail -f /var/log/lcm/lcm-app.log` | Follow the main LCM application log |

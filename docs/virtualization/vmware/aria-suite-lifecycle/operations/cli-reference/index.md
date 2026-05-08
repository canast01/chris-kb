# Aria Suite Lifecycle — CLI Reference

The primary CLI tool on the LCM appliance is `vracli`, which provides sub-commands for certificate management, cluster status, service control, and configuration. SSH to the LCM appliance as root. All `vracli` commands must be run as root on the LCM appliance.

---

## Appliance Status

```bash
# Show overall LCM appliance and service health
vracli status

# Show cluster node health and quorum state
vracli cluster status

# Show registered services and their versions
vracli services list

# Show currently installed product versions
vracli version
```

---

## Services

```bash
# List all LCM-managed services and state
vracli services list

# Restart a named LCM service
vracli services restart <service_name>

# Stop a service
vracli services stop <service_name>

# Start a service
vracli services start <service_name>

# Show logs for a service
journalctl -u <service_name> --since "1 hour ago"
```

---

## Certificates

The Locker stores certificates used by Aria products. Manage them here before triggering certificate replacement operations in LCM.

```bash
# List all certificates in the Locker
vracli certificate list

# Show detail for a certificate
vracli certificate show --alias <alias>

# Import a certificate and key pair
vracli certificate import --cert <cert.pem> --key <key.pem> --alias <alias>

# Delete a certificate from the Locker
vracli certificate delete --alias <alias>

# Check certificate expiry
vracli certificate list | grep -E "alias|expiry"
```

---

## Proxy & Network

```bash
# Show current proxy configuration
vracli proxy show

# Set outbound proxy for bundle downloads
vracli proxy set --host <proxy_host> --port <proxy_port>

# Clear proxy
vracli proxy clear

# Show network configuration
vracli network show

# Update DNS servers
vracli network dns set --servers <dns1>,<dns2>
```

---

## NTP & Time

```bash
# Show current NTP configuration
vracli ntp show

# Set NTP servers
vracli ntp set <ntp_server1> <ntp_server2>

# Verify time sync
timedatectl status

# Force NTP sync
chronyc makestep
```

---

## Logs

```bash
# Follow the main LCM application log
tail -f /var/log/lcm/lcm-app.log

# Follow the LCM debug log
tail -f /var/log/lcm/lcm-debug.log

# Collect a support bundle
vracli support-bundle

# View recent system journal
journalctl --since "2 hours ago" -u lcm
```

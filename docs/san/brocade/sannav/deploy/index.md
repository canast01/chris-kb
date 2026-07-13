---
tags:
  - deployment
  - san
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
deploy_sannav_ova_or_install: "Deploy SANnav OVA or Install" {shape: rectangle}
initial_configuration: "Initial Configuration" {shape: rectangle}
add_first_fabric: "Add First Fabric" {shape: rectangle}
configure_alert_notifications: "Configure Alert Notifications" {shape: rectangle}
set_up_performance_monitoring: "Set Up Performance Monitoring" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> deploy_sannav_ova_or_install
deploy_sannav_ova_or_install -> initial_configuration
initial_configuration -> add_first_fabric
add_first_fabric -> configure_alert_notifications
configure_alert_notifications -> set_up_performance_monitoring
set_up_performance_monitoring -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# SANnav — Initial Deployment

This guide covers deploying Brocade SANnav Management Portal from installation through validated fabric discovery and monitoring. SANnav replaces the legacy Brocade Network Advisor (BNA) and provides centralized SAN management, zoning, analytics, and alert handling.

---

## Prerequisites

**VM requirements (SANnav Management Portal):**

- 4 vCPU, 16 GB RAM, 200 GB disk (thin-provisioned is fine; OS needs the first 100 GB and analytics data grows over time)
- VMware ESXi 7.0 or later (OVA deployment) or physical Linux server
- RHEL 8/9 or SLES 15 for the non-OVA installation path
- Static IP address with FQDN resolvable from all Brocade switches and management workstations

**OS requirements (Linux install path):**

- `java-11-openjdk` (SANnav bundles its own JRE in the installer but confirming Java compatibility avoids post-install issues)
- Ports open inbound on the SANnav server:
  - TCP 443: HTTPS browser access
  - TCP 80: HTTP redirect to HTTPS
  - UDP 162: SNMP trap receive
  - TCP 2377, 7946, 4789: SANnav internal clustering (if deploying HA SANnav)
- Outbound from SANnav to Brocade switches:
  - TCP 22: SSH (for configuration management)
  - UDP 161: SNMP
  - TCP 80/443: REST API access to FOS 9.x switches

**Brocade switch requirements:**

- Fabric OS 8.2.1 or later (FOS 9.x recommended for full analytics support)
- SNMP enabled on each switch with a community string matching what SANnav will use
- SSH enabled on each switch
- Admin credentials available for each switch

---

## Deploy SANnav OVA or Install

**OVA deployment (VMware):**

1. Download the SANnav OVA from the Broadcom Support Portal (search for "SANnav Management Portal OVA").
2. In vSphere Client, right-click the target cluster and select **Deploy OVF Template**.
3. Upload the OVA file and follow the wizard:
   - Select the destination datastore and network (place on the management VLAN).
   - Set VM name (e.g., `sannav-mgmt-01`).
4. After deployment, power on the VM.
5. Open the VM console and log in with default credentials (shown in the Broadcom SANnav release notes — typically `admin` / `password`).
6. Run the initial network configuration script:

```bash
/opt/sannav/tools/networkconfig.sh
# Set: IP address, netmask, gateway, DNS, hostname
```


```text title="Expected output"
SANnav Network Configuration Tool v8.2.1
=========================================

Current Network Settings:
  Interface: eth0
  IP Address: 192.168.1.50
  Netmask: 255.255.255.0
  Gateway: 192.168.1.1
  DNS Servers: 8.8.8.8, 8.8.4.4
  Hostname: sannav-prod-01

Enter new IP address [192.168.1.50]: 
Enter netmask [255.255.255.0]: 
Enter gateway [192.168.1.1]: 
Enter DNS servers (comma-separated) [8.8.8.8, 8.8.4.4]: 
Enter hostname [sannav-prod-01]: 

Validating configuration...
Applying network settings...
Network configuration updated successfully.
Restarting network services...
Done. Please verify connectivity.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Permission denied` | Run the script with sudo: `sudo /opt/sannav/tools/networkconfig.sh` |
    | `Error: Invalid IP address format` | Enter a valid IPv4 address in dotted-decimal notation (e.g., 192.168.1.100). |
    | `Error: /opt/sannav/tools/networkconfig.sh: No such file or directory` | Verify SANnav is installed in /opt/sannav and the tools directory exists. |
7. Restart the network service and verify the SANnav web interface is accessible.

**RPM/DEB install (Linux):**

1. Download the SANnav installer package from Broadcom Support.
2. Transfer to the Linux host and install:

```bash
rpm -ivh SANnav-<version>.x86_64.rpm
# or for Debian-based:
dpkg -i SANnav-<version>.amd64.deb
```


```text title="Expected output"
Preparing...                          ################################# [100%]
Updating / installing...
   1:SANnav-9.2.1-1                   ################################# [100%]
SANnav installation completed successfully.
Installed: SANnav-9.2.1-1.x86_64
Installation log written to /var/log/sannav_install.log
Starting SANnav services...
sannav-server started (PID: 4827)
sannav-database started (PID: 4829)
Web UI available at https://localhost:8443
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: Failed dependencies: libc.so.6(GLIBC_2.17)(64bit) is needed by SANnav` | Upgrade glibc to a compatible version or use a newer OS distribution that meets SANnav's minimum requirements. |
    | `E: Unable to locate package SANnav` | Verify the package file path is correct and the repository is configured, or download the .deb file directly from Brocade's support portal. |
    | `error: cannot open Packages database in /var/lib/rpm` | Run `rpm --rebuilddb` to repair the RPM database, then retry the installation. |
3. Run the post-install configuration:

```bash
/opt/sannav/tools/postinstall.sh
```


```text title="Expected output"
SANnav Post-Installation Script v8.2.1
======================================
Checking system requirements...
  ✓ OS: Red Hat Enterprise Linux 8.6
  ✓ Disk space: 45GB available (required: 20GB)
  ✓ Memory: 32GB (required: 16GB)
  ✓ Java version: 11.0.15

Initializing database...
  Creating schema... done
  Loading initial data... done
  Setting permissions... done

Configuring Brocade fabric connectivity...
  Discovering switches... found 12 switches
  Validating credentials... passed
  Registering agents... 12/12 complete

Starting services...
  sannav-server: started (PID 4821)
  sannav-collector: started (PID 4835)
  sannav-web: started (PID 4847)

Post-installation complete. Access SANnav at https://localhost:8443
Default credentials: admin / changeme (change immediately)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: Database connection failed: Connection refused on port 5432` | Ensure PostgreSQL is running with `systemctl start postgresql` before executing postinstall.sh. |
    | `ERROR: Insufficient disk space: 8GB available, 20GB required` | Free up disk space or mount additional storage before retrying the script. |
    | `ERROR: Java not found or version < 11 detected` | Install Java 11+ with `yum install java-11-openjdk-devel` and set JAVA_HOME environment variable. |
4. Start the SANnav service:

```bash
systemctl enable --now sannav
```


```text title="Expected output"
Created symlink /etc/systemd/system/multi-user.target.wants/sannav.service → /usr/lib/systemd/system/sannav.service.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit sannav.service could not be found.` | Verify the sannav service file exists at /usr/lib/systemd/system/sannav.service or install the sannav package. |
    | `Failed to enable unit: Unit file /etc/systemd/system/sannav.service is masked.` | Unmask the service with `systemctl unmask sannav` before enabling it. |
---

## Initial Configuration

After the service starts, access SANnav at `https://<sannav_ip>`.

1. Log in with the default admin account and change the password immediately.
2. Navigate to **Settings > System Settings** and configure:
   - **System name:** Set a descriptive name (e.g., `SANnav-Prod`).
   - **Time zone:** Set to match your data center time zone.
   - **NTP server:** Enter the NTP server address.
   - **Email server (SMTP):** Enter the relay server and default alert recipient email.

3. Navigate to **Settings > Users** and create role-based accounts:
   - `sannav_admin` — Full administrative access
   - `sannav_readonly` — Read-only for operations staff who need visibility without change permissions

4. Configure LDAP or Active Directory integration (optional but recommended):
   - Navigate to **Settings > Authentication > LDAP**.
   - Enter your LDAP server URL, bind DN, and user search base.
   - Map LDAP groups to SANnav roles.

5. Apply a TLS certificate to replace the self-signed certificate:
   - Navigate to **Settings > Security > Certificates**.
   - Upload a PEM-encoded certificate and private key signed by your internal CA.

---

## Add First Fabric

SANnav discovers a fabric by connecting to one switch — it then auto-discovers all other switches in the fabric via the name server.

1. Navigate to **Discover > SAN Fabric Discovery > Add Fabric**.
2. Enter:
   - **IP address or hostname:** The management IP of one switch in the target fabric
   - **Admin username:** `admin`
   - **Admin password:** The switch admin password
   - **SNMP community string:** The read community string configured on the switch (default: `Secret C0de` on FOS — verify with `snmpConfig` on the switch)
3. Click **Discover**. SANnav connects to the switch, authenticates, and queries the fabric for all other connected switches.
4. SANnav auto-discovers all switches in the fabric and adds them to the inventory.
5. Verify all switches appear in **Fabric Summary** with status **Online**.

**Troubleshoot discovery failures:**

- SSH timeout: verify TCP 22 is reachable from SANnav to the switch; verify SSH is enabled on the switch (`sshutil status`)
- SNMP failure: verify the community string matches (`snmpConfig --show` on the switch)
- Firewall: confirm no ACL is blocking SANnav's management IP from reaching the switch management interface

---

## Configure Alert Notifications

SANnav alert policies define which events generate notifications and at what threshold.

1. Navigate to **Monitoring > Alert Policies > Create Policy**.
2. Name the policy (e.g., `critical_fabric_alerts`).
3. Select event types to include:
   - Port link down
   - ISL down
   - Fabric segmentation
   - CRC error threshold exceeded
   - Port utilization > 80% sustained
   - FC login failures (potential misconfiguration or hardware failure)
4. Set the notification method:
   - **Email:** Enter one or more recipient addresses (use a team distribution list)
   - **SNMP trap:** Enter the IP of your NMS if you forward to a central monitoring platform
5. Set severity threshold: generate alerts for **Warning** and above.
6. Click **Save** and assign the policy to all discovered fabrics.

**Test the alert:**

```bash
# Simulate a port event by disabling a non-production port on a switch:
portDisable <port_number>
# SANnav should generate a "Port Link Down" alert within 30 seconds
portEnable <port_number>
```


```text title="Expected output"
Port 47 disabled successfully
Port state change detected: Port 47 (Brocade-6505, slot 1) - Link Down
SANnav Alert Generated: Port Link Down - Severity: Warning - Timestamp: 2024-01-15 14:23:47 UTC
Alert ID: ALR-2847392-5F1C
Port 47 enabled successfully
Port state change detected: Port 47 (Brocade-6505, slot 1) - Link Up
SANnav Alert Generated: Port Link Up - Severity: Informational - Timestamp: 2024-01-15 14:24:12 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portDisable: command not found` | Source the Brocade CLI environment or use the full path to the portDisable utility (typically `/opt/brocade/bin/portDisable`). |
    | `Error: Port 47 is in use by active zone members` | Use `zoneDisable` to temporarily deactivate the zone before disabling the port, or select a different non-production port. |
    | `SANnav Alert not generated within timeout` | Verify SANnav is running with `systemctl status sannav` and check network connectivity between the switch and SANnav server. |
---

## Set Up Performance Monitoring

SANnav collects per-port utilization, IOPS, and error statistics from Fabric OS switches.

1. Navigate to **Analytics > Performance Monitoring**.
2. Enable **Port Performance Monitoring** for the discovered fabric:
   - Select the fabric and click **Enable Monitoring**.
   - Set polling interval: 30 seconds (default; lower intervals increase database growth).
3. SANnav begins collecting data. Wait 5 minutes, then navigate to **Analytics > Dashboards > Port Utilization** to verify data is populating.
4. Create a performance alert for high-utilization ports:
   - Navigate to **Monitoring > Thresholds > Create Threshold**.
   - Set: Port Tx Utilization > 80% for more than 5 consecutive polling intervals.
   - Attach to the critical alert policy created above.

**Review traffic heatmap:**

Navigate to **Analytics > Traffic > Heatmap**. This shows which switch-to-switch ISLs carry the most traffic, helping identify potential congestion before it becomes a problem.

---

## Validate

1. All fabric switches appear in **Fabric Summary** with status **Online** and correct domain IDs.
2. Navigate to **SAN Fabric > Zone View** and confirm the active zone configuration matches what was configured on the switches.
3. Send a test alert:
   - Navigate to **Settings > Notifications > Test Email**.
   - Confirm the test email arrives at the alert recipient.
4. Verify performance data is collecting:
   - Navigate to **Analytics > Port Utilization** and confirm graphs show 30-second interval data.
5. Confirm SANnav is receiving SNMP traps:
   - On a switch, generate a test trap: `snmpMibCapSet` → trigger a severity-1 event by briefly disabling and re-enabling a non-production port.
   - SANnav **Events** log should show the corresponding event within 30 seconds.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Sannav — Procedures](../operations/procedures/)
- [Sannav — Common Issues](../troubleshooting/common-issues/)
- [Sannav — How It Works](../architecture/how-it-works/)

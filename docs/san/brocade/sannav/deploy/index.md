---
tags:
  - deployment
  - san
search:
  boost: 1.5
---
# SANnav — Initial Deployment

```text
┌──────────────────────────────── Brocade SANnav — Deployment Overview ─────────────────────────────────┐
│                                                                                                       │
│   SANnav replaces Brocade Network Advisor (BNA) for centralized SAN management and analytics          │
│   Deployment: OVA on ESXi 7.0+ or RPM/DEB install on RHEL 8/9 or SLES 15                              │
│   Requires: static IP with FQDN resolvable from all managed Brocade switches                          │
│                                                                                                       │
│   VM requirements                                                                                     │
│   4 vCPU, 16 GB RAM, 200 GB disk; VMware ESXi 7.0+ or physical Linux host                             │
│   Ports inbound: TCP 443 (HTTPS), UDP 162 (SNMP traps), TCP 22 outbound to switches                   │
│   Switch prereqs: FOS 8.2.1+ (9.x recommended), SNMP and SSH enabled, admin credentials               │
│                                                                                                       │
│   Initial configuration                                                                               │
│   Deploy OVA or install RPM; run networkconfig.sh or postinstall.sh to set IP/hostname                │
│   Set: system name, time zone, NTP, SMTP relay for alerts                                             │
│   Create RBAC accounts (sannav_admin, sannav_readonly); optionally configure LDAP                     │
│   Replace self-signed TLS certificate with internal CA-signed certificate                             │
│                                                                                                       │
│   Fabric discovery                                                                                    │
│   Discover > Add Fabric: enter one switch IP — SANnav auto-discovers all switches in the fabric       │
│   Troubleshoot: SSH reachability (TCP 22), SNMP community string mismatch, firewall ACLs              │
│   Verify: all switches appear in Fabric Summary with status Online                                    │
│                                                                                                       │
│   Monitoring and alerts                                                                               │
│   Alert policies: link-down, ISL-down, fabric segmentation, CRC threshold, port utilisation >80%      │
│   Performance monitoring: enable per-port stats (30s polling); review utilisation and heatmaps        │
│   Test: disable a non-production port; SANnav should generate the alert within 30 seconds             │
│                                                                                                       │
│   Key terms:                                                                                          │
│   FOS          = Fabric OS; operating system running on Brocade SAN switches                          │
│   SNMP trap    = unsolicited alert sent from switch to SANnav when an event occurs                    │
│   Fabric discovery = SANnav queries name server on seed switch to find all fabric members             │
│   CRC error    = Cyclic Redundancy Check error; indicates physical layer or cable problem             │
│   ISL          = Inter-Switch Link; E_Port connection between switches in the same fabric             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

7. Restart the network service and verify the SANnav web interface is accessible.

**RPM/DEB install (Linux):**

1. Download the SANnav installer package from Broadcom Support.
2. Transfer to the Linux host and install:

```bash
rpm -ivh SANnav-<version>.x86_64.rpm
# or for Debian-based:
dpkg -i SANnav-<version>.amd64.deb
```

3. Run the post-install configuration:

```bash
/opt/sannav/tools/postinstall.sh
```

4. Start the SANnav service:

```bash
systemctl enable --now sannav
```

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

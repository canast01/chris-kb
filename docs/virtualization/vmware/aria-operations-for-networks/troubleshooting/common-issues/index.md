# Aria Operations for Networks — Common Issues

---

## Collector Shows Disconnected

**Symptoms:** Collector listed in Settings → Infrastructure → Collectors as "Disconnected" or "Not Reachable"

**Diagnosis steps:**

```bash
# From Collector VM — test connectivity to Platform VM
curl -sk https://<platform-vm-ip>/api/ni/auth/token
nc -vz <platform-vm-ip> 443

# Check Collector services
ssh admin@<collector-vm-ip>
sudo systemctl status hms
sudo systemctl start hms   # restart if stopped

# Check Collector disk usage (stops uploading when >85% full)
df -h
sudo journalctl --vacuum-size=1G   # free journal space
```

If pairing key was regenerated:
```text
Platform UI → Settings → Infrastructure → Collectors → Generate New Pairing Key
Redeploy Collector OVA → enter new pairing key
```

---

## vCenter Sync Failing

**Symptoms:** Data source shows "Authentication failed" or "Certificate not trusted"

1. **Password changed on service account:**
   ```
   Settings → Data Sources → [vCenter] → Edit → update password → Save
   ```

2. **vCenter certificate renewed/replaced:**
   ```
   Settings → Data Sources → [vCenter] → Edit → Accept new certificate thumbprint
   ```

3. **Service account lost permissions:**
   ```
   vCenter → Administration → Global Permissions
   Verify svc-vrni-vc@corp.local has Read Only on root (propagating)
   ```

---

## NSX Topology Not Visible

**Symptoms:** VMs visible but NSX overlay segments, logical routers, and DFW rules are absent

1. **NSX data source not added:**
   ```
   Settings → Data Sources → NSX-T Managers → Add
   ```

2. **Insufficient API permissions:**
   ```
   NSX-T → System → User Management → verify Auditor role on svc-vrni-nsx
   ```

3. **NSX version not supported by this vRNI release:** Check vRNI release notes for NSX compatibility matrix

4. **NSX Manager unreachable from Collector:**
   ```bash
   # From Collector VM:
   curl -sk -u admin:<pass> https://<nsx-manager>/api/v1/cluster/status
   ```

---

## No Flows Visible

**Symptoms:** Flow queries return empty; application maps show no traffic

1. **NetFlow not configured on switches:**
   ```
   # Cisco IOS-XE: verify exporter
   show flow exporter
   show flow monitor cache
   # Should show flows destined to Collector IP
   ```

2. **UDP 2055 not reaching Collector:**
   ```bash
   # On Collector VM, capture traffic:
   sudo tcpdump -i eth0 -n udp port 2055 -c 20
   # If no packets appear — firewall is blocking UDP 2055
   ```

3. **ESXi IPFIX not enabled on vDS:**
   ```
   vCenter → Networking → [dvSwitch] → Configure → Netflow/IPFIX
   Verify: Collector IP = Collector VM IP, Port = 2055
   Active flow timeout: 60 seconds
   ```

---

## Flow Data Is Stale

**Symptoms:** Search results show only old flows; "Last Updated" timestamp is hours/days old

1. **Collector disk full:**
   ```bash
   ssh admin@<collector-vm>
   df -h
   sudo journalctl --vacuum-size=1G
   sudo systemctl restart hms
   ```

2. **Platform VM disk full:**
   ```bash
   ssh ubuntu@<platform-vm>
   df -h
   # If /data > 90%: clear old config backups, expand VMDK
   ```

3. **Collector overwhelmed:** High flow rate exceeding Collector capacity — add a second Collector and redistribute data sources

---

## UI Is Slow

**Symptoms:** Dashboard takes >30 seconds; searches time out

1. **Browser cache:** Clear cache (Ctrl+Shift+R)

2. **Platform VM resource contention:**
   ```
   vCenter → [Platform VM] → Monitor → Performance → CPU Ready %
   # If CPU ready > 5%, the VM is waiting for CPU — move host or adjust reservations
   ```

3. **Query too broad:** Searches like `flows` without source/time filter scan millions of records — add filters: `flows where source_vm.name = 'X' order by time desc`

---

## License Expired

**Symptoms:** Banner "License has expired" on login; data collection may be halted

```text
Settings → License → Enter new license key
```

After entering new key, verify data source collection resumes (check last-sync timestamps in Settings → Data Sources).

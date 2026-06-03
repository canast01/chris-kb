```text
┌─────────────────────────────────────────────────────────────────┐
│  Symptom                  Check                  Fix                                                  │
│  ┌─────────────────┐      ┌──────────────────┐                                                        │
│  │ RPO Violation   │─────►│ Bandwidth?        │─► QoS / raise                                         │
│  │ (amber/red)     │      │ ESXi CPU ready %? │   RPO value                                           │
│  │                 │      │ VRA disk full?    │─► expand VMDK                                         │
│  └─────────────────┘      └──────────────────┘                                                        │
│  ┌─────────────────┐      ┌──────────────────┐                                                        │
│  │ Site Pair       │─────►│ VRA services up?  │─► start hms/                                          │
│  │ Disconnected    │      │ TCP 44046 open?   │   vrms                                                │
│  │                 │      │ Cert expired?     │─► refresh                                             │
│  └─────────────────┘      └──────────────────┘   thumbprints                                          │
│  ┌─────────────────┐      ┌──────────────────┐                                                        │
│  │ Conn Refused /  │─────►│ TCP 31031 open?   │─► firewall                                            │
│  │ Initial Sync    │      │ Route to VRA?     │   rule / seed                                         │
│  │ Stalled         │      │ Seed available?   │   pre-copy                                            │
│  └─────────────────┘      └──────────────────┘                                                        │
│  ┌─────────────────┐      ┌──────────────────┐                                                        │
│  │ No Datastore    │─────►│ Target datastore  │─► mount DS /                                          │
│  │ Available       │      │ mounted? space?   │   free space                                          │
│  └─────────────────┘      └──────────────────┘                                                        │
└─────────────────────────────────────────────────────────────────┘
```
```text
   Configure Replication → Step 4: Seeds → Use existing data
   ```

3. **Schedule full sync during low-traffic window**: VR throttles to available bandwidth

---

## Replication Fails with "Connection Refused" / "Connection Timeout"

**Symptoms:** Replication status error: network connectivity to target VRA

```

```bash
# From source ESXi host shell:
nc -vz vra-amsterdam.example.local 31031
# If connection refused → firewall blocking TCP 31031
# If timeout → no route to target VRA

# Verify from ESXi:
vmkping -I vmk0 <target-VRA-IP>
```
```bash
ssh admin@vra-london.example.local
df -h
# Check /opt partition — VRA appliance partition

# Clear old log files if disk is full:
sudo find /opt/vmware/logs -name "*.log" -mtime +30 -delete
sudo journalctl --vacuum-size=500M
```
```bash
vCenter → [VRA VM] → Edit Settings → Disk → increase size
Then expand filesystem inside VRA:
  sudo growpart /dev/sda 1
  sudo resize2fs /dev/sda1
```

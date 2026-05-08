# Aria Suite Lifecycle — Common Issues

## Installation Failures

```bash
# Check LCM installer log
tail -200 /var/log/vmware/vrlcm/lcm-install.log

# Verify DNS resolution for all product FQDNs from LCM node
for fqdn in vrops.example.com vra.example.com wsa.example.com; do
  echo -n "$fqdn: "; nslookup $fqdn | grep "Address" | tail -1
done

# Check disk space before install
df -h /data /var/log /tmp

# Verify NTP sync (required for certificate operations)
chronyc tracking | grep "System time"
```

| Error Code | Meaning | Resolution |
|---|---|---|
| `VRLCM_ERR_001` | DNS resolution failure | Fix DNS records; verify from LCM node |
| `VRLCM_ERR_012` | Insufficient disk space | Free space on `/data`; min 50 GB free |
| `VRLCM_ERR_023` | OVA checksum mismatch | Re-download bundle; verify SHA256 |
| `VRLCM_ERR_031` | vCenter connectivity failure | Check credentials and firewall to port 443 |

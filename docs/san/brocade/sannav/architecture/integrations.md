---
tags:
  - architecture
  - san
---
# Brocade SANnav — Integrations
![Brocade SANnav — Integrations](../../../../assets/san-brocade-sannav-architecture-integrations.svg)


```bash
# SSH to SANnav appliance
ssh admin@sannav-mgmt.corp.example.com

# Edit rsyslog configuration
sudo vi /etc/rsyslog.d/sannav-forward.conf

# Add:
*.* @10.10.3.50:514        # UDP syslog
# or
*.* @@10.10.3.50:514       # TCP syslog (more reliable)

# Restart rsyslog
sudo systemctl restart rsyslog

# Verify forwarding
logger -t sannav-test "Test syslog message from SANnav"
# Check SIEM for the test message
```


---

```d2
direction: right

center: "SANnav" {shape: hexagon}
component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

center -> component_a
center -> component_b
center -> component_c
```

## See also

- [Sannav — How It Works](how-it-works/)
- [Sannav — Design Standards](design-standards/)

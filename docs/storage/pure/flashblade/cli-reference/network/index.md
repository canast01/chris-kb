# Network

> Part of the [Pure FlashBlade CLI Reference](../).

---

## Network

```bash
# Network interfaces
purefb network-interface show
purefb network-interface show --name <if_name>

# Subnets
purefb subnet show
purefb subnet create --name <subnet> --prefix <cidr> --gateway <gw>

# DNS
purefb dns show
purefb dns update --nameservers <ip1,ip2>

# NTP
purefb ntp show
purefb ntp update --ntpservers <ntp_ip>
```

# Logs

> Part of the [VMware ESXi CLI Reference](../).

---

## Logs

```bash
# Live tailing
tail -f /var/log/vmkernel.log
tail -f /var/log/hostd.log
tail -f /var/log/vpxa.log
tail -f /var/log/vobd.log
tail -f /var/log/esxi.log
tail -f /var/log/syslog.log

# Grep for issues
grep -i "error" /var/log/vmkernel.log
grep -i "warning" /var/log/hostd.log
grep -i "disconnected" /var/log/vpxa.log
grep -i "lost connectivity" /var/log/vmkernel.log
grep <vm_name> /var/log/vmkernel.log

# Log locations
ls /var/log/
ls /scratch/log/
```

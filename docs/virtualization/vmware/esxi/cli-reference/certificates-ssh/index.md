# Certificates & SSH

> Part of the [VMware ESXi CLI Reference](../).

---

## Certificates

```bash
# View current cert
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -dates
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -subject
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -fingerprint

# Regenerate self-signed cert
/sbin/generate-certificates

# List cert files
ls -la /etc/vmware/ssl/
```

---

## SSH

```bash
# Enable / disable SSH via vim-cmd
vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/disable_ssh

# Enable / disable SSH via service
/etc/init.d/SSH start
/etc/init.d/SSH stop

# Enable SSH via esxcli firewall
esxcli network firewall ruleset set --enabled true --ruleset-id sshServer
```

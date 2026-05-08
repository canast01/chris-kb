# NetBackup — Authentication

## NetBackup Certificate Authority

All clients authenticate to the master server via certificates issued by the NetBackup CA:

```bash
# List all certificates in the NetBackup CA
nbcertcmd -listCACertDetails

# Re-issue client certificate (if expired or lost)
nbcertcmd -getCertificate -server <master_server> -force

# Check certificate expiry across all clients
nbcertcmd -listCerts | grep -E "Host|Expiry"
```

Certificates expire by default after 5 years — set up monitoring to alert 90 days before expiry.

# Dell ECS — Hardening

## Hardening Checklist

- [ ] Change the default `sysadmin` password immediately after initial deployment
- [ ] Replace self-signed TLS certificates on the Management API (4443) and S3 endpoint (443) with certificates signed by the corporate CA
- [ ] Disable HTTP (port 9021) in production; require HTTPS for all S3 access
- [ ] Enable TLS 1.2 minimum on all endpoints; disable TLS 1.0 and 1.1
- [ ] Create named management service accounts; disable or restrict the `sysadmin` account from use in automation
- [ ] Apply namespace quotas; do not allow namespaces with no quota in production
- [ ] Enable bucket-level access logging for namespaces with compliance or audit requirements
- [ ] Configure syslog forwarding to the SIEM for all ECS management and access events
- [ ] Enable Object Lock (WORM) on buckets designated for compliance or immutable backup data
- [ ] Restrict ECS Portal (port 443) and Management API (port 4443) access to management network VLANs via firewall rules
- [ ] Review and disable unused API protocols (Swift, Atmos, CAS) on namespaces that only require S3
- [ ] Rotate object user secret keys every 12 months and update consuming applications

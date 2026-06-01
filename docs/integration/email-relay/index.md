# Email Relay


<div class="kb-summary">
> Covers Postfix SMTP relay configuration for outbound application and system mail.
</div>

---

## Architecture

A typical deployment routes application-generated mail through a local Postfix relay, which forwards to a smarthost or cloud email service (AWS SES, SendGrid). This decouples application SMTP configuration from the upstream provider and centralises authentication and delivery policy.

Key properties of this pattern:
- Applications configure a single static SMTP target (the relay) — no per-app credential management
- The relay handles authentication, TLS negotiation, and retry queuing toward the smarthost
- All outbound mail is visible in a single log and queue on the relay host

---

## Configuration — `/etc/postfix/main.cf`

| Parameter | Example Value | Purpose |
|---|---|---|
| `relayhost` | `[email-smtp.us-east-1.amazonaws.com]:587` | Upstream smarthost and port. Brackets suppress MX lookup. |
| `mynetworks` | `127.0.0.0/8 10.0.0.0/8` | IP ranges permitted to relay through this Postfix instance. Restrict to loopback and internal app subnets. |
| `smtp_sasl_auth_enable` | `yes` | Enable SASL authentication toward the smarthost. |
| `smtp_sasl_password_maps` | `hash:/etc/postfix/sasl_passwd` | Path to the credential map file for smarthost authentication. |
| `smtp_sasl_security_options` | `noanonymous` | Reject anonymous SASL mechanisms. |
| `smtp_tls_security_level` | `encrypt` | Require TLS for all outbound SMTP connections. Use `encrypt` (mandatory) rather than `may` (opportunistic). |
| `smtp_tls_note_starttls_offer` | `yes` | Log when the smarthost offers STARTTLS, useful for debugging TLS negotiation. |
| `inet_interfaces` | `loopback-only` | Accept connections on loopback only when the relay is local. Set to a specific IP if relay serves multiple hosts. |
| `myhostname` | `relay.internal.example.com` | FQDN used in EHLO/HELO. Must resolve from the smarthost to avoid rejection. |
| `message_size_limit` | `10240000` | Maximum message size in bytes (10 MB shown). Adjust to match smarthost limits. |

After editing `main.cf`, reload without dropping the queue:

```bash
postfix reload
```
```text
┌────────────────────────────────── Integration — Email Relay (SMTP) ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Configure SMTP relay so monitoring, backup, and infrastructure appliances send email     │   │
│   │           Use authenticated SMTP relay; never configure an open relay; TLS required           │   │
│   │           Test: telnet/openssl to relay port; send a test alert after config change           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 SMTP Config                  │  │                Common Issues                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          Relay host: smtp.internal           │  │         Connection refused = FW/port        │   │
│   │             Port: 587 (STARTTLS)             │  │           Auth fail = check creds           │   │
│   │             Auth: PLAIN or LOGIN             │  │           TLS error = add relay CA          │   │
│   │             From: alerts@domain              │  │          Relay denied = check allow         │   │
│   │             Test: send test mail             │  │           SPF fail = add relay IP           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    STARTTLS     = Upgrade plain SMTP connection to TLS on port 587; required for auth                 │
│    Open relay   = SMTP server accepting mail for any domain; used for spam; never configure           │
│    SPF          = Sender Policy Framework; DNS TXT record listing authorised sending IPs              │
│    Port 25      = SMTP; blocked by most cloud providers for outbound; use 587 or 465                  │
│    Port 587     = Submission port; requires authentication; preferred for relay config                │
│    Relay allow  = List of IPs permitted to relay through SMTP server without auth (use sparingly)     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

---

## Daily Operational Commands

| Check | Command | Notes |
|---|---|---|
| Verify SMTP service running | `systemctl status postfix` | Expect `active (running)`. If stopped, check `journalctl -u postfix -n 50`. |
| Check mail queue status | `mailq` | Empty queue is normal. A growing deferred queue indicates a delivery problem to the smarthost. |
| Count queued messages | `postqueue -p \| grep -c '^[0-9A-F]'` | Quick count of queued message IDs. |
| Review recent delivery log | `grep postfix /var/log/mail.log \| tail -n 100` | Look for `status=sent`, `status=deferred`, or `status=bounced` entries. |
| Flush deferred queue | `postqueue -f` | Force retry of all deferred messages. Use after fixing a delivery issue. |
| Test SMTP connectivity to smarthost | `openssl s_client -starttls smtp -connect email-smtp.us-east-1.amazonaws.com:587` | Validates TLS handshake and certificate. |
| Send a test message | `echo "Test" \| mail -s "relay test" ops@example.com` | End-to-end test from the relay host. |

---

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Messages stuck in deferred queue | `mailq` shows `Connection refused` or `Timeout` toward smarthost | Verify smarthost hostname and port in `relayhost`. Check firewall rules allow outbound TCP 587 from the relay host. |
| Authentication failure to smarthost | Log shows `SASL authentication failed` | Confirm credentials in `/etc/postfix/sasl_passwd` are current. Re-hash with `postmap /etc/postfix/sasl_passwd` after any edit. |
| TLS negotiation error | Log shows `TLS handshake failed` or `certificate verify failed` | Check `smtp_tls_security_level`. If the smarthost cert has changed, update the CA bundle at `/etc/ssl/certs/ca-certificates.crt`. |
| Relay access denied (550) | Log shows `Relay access denied` for a source IP | The sending host IP is not in `mynetworks`. Add it and reload Postfix. |
| Bounce: unknown user | Log shows `550 5.1.1 user unknown` from the upstream MX | The destination address does not exist. Confirm the recipient address with the requester. |
| Messages sent but not received | No bounce, queue empty, but mail not delivered | Check smarthost dashboard (SES/SendGrid) for delivery status and suppression list. The message may have been accepted but marked as spam by the destination. |
| High queue volume | `mailq` shows hundreds of messages | Check for a looping alert or application generating excessive mail. Review sender address in the queue with `postqueue -p`. |

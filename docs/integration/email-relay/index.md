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

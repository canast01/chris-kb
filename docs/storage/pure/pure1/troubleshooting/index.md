---
tags:
  - pure
  - troubleshooting
---
# Pure1 — Troubleshooting

```bash
# Step 1: Check array connectivity from Purity CLI
purearray list --connection
# If pure1.purestorage.com shows "disconnected":

# Step 2: Verify network configuration
purearray list --network
# Confirm management IP, gateway, DNS are correct

# Step 3: Test outbound HTTPS connectivity
# From the array support shell (requires Pure support):
curl -v https://pure1.purestorage.com

# Step 4: Check if a proxy is required and configured
purearray list | grep proxy
# If proxy is needed but not set:
purearray set --proxy https://<proxy-host>:<port>

# Step 5: Check firewall rules
# Array management IP must have outbound TCP 443 to pure1.purestorage.com
# Verify with network team if connectivity test fails
```
```text
┌─────────────────────────────────────── Pure1 — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Phonehome Issues               │  │             Alert / Data Issues             │   │
│   │            Check TCP 443 outbound            │  │             Verify array status             │   │
│   │            Verify DNS resolution             │  │                Check data age               │   │
│   │            purearray setattr show            │  │              Check alert config             │   │
│   │             Re-enable phonehome              │  │            Test webhook delivery            │   │
│   │             Check proxy settings             │  │                Open TAC case                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Troubleshoot from array CLI (purearray) and pure1.purestorage.com UI                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Disconnected = Array shows Disconnected in Pure1; phonehome not received > 5 min                     │
│  TCP 443 test = From array: curl -s https://pure1.purestorage.com >/dev/null; check rc                │
│  DNS resolution = Array must resolve pure1.purestorage.com; check array DNS settings                  │
│  purearray setattr show = View phonehome enabled/disabled state on FlashArray                         │
│  Re-enable phonehome = purearray setattr --phonehome true on FlashArray CLI                           │
│  Proxy settings = purearray setattr --proxy http://proxy:port if array uses proxy                     │
│  Data age = Time since last phonehome; check in Pure1 > array detail                                  │
│  Alert config = Verify email and webhook targets in Pure1 > Admin > Notifications                     │
│  Webhook test = Pure1 UI has a test button; verify delivery to endpoint                               │
│  TAC case = support.purestorage.com; include array serial and phonehome status                        │
│  FlashBlade phonehome = pureauthapp setattr --phonehome true on FlashBlade CLI                        │
│  Firewall rule = Allow outbound TCP 443 from array mgmt IP to pure1.purestorage.com                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
1. Pure1 > Administration > Notifications > [Rule]
   - Verify the rule is enabled
   - Confirm the webhook URL / email address is current
   - Check rule scope: does it cover the affected array's tags?

2. Test the notification rule manually:
   Actions > Test Notification

3. For PagerDuty: verify the integration routing key has not been rotated/changed

4. For email: check spam/junk folders; verify the relay server is operational

5. Check Pure1 notification delivery log:
   Administration > Notifications > Delivery Log
```
```text
1. Confirm the API token has not been rotated without updating the secrets manager
2. Verify the service account is not disabled:
   Pure1 > Administration > API Registration > [Account] > Status
3. Confirm the private key file is correct and not corrupted
4. Re-generate a new API token if needed:
   Administration > API Registration > [Account] > Rotate Key
5. Update the secrets manager with the new key
```

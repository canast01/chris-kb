---
tags:
  - pure
  - troubleshooting
search:
  boost: 1.5
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

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> verify_resolution: investigate
verify_resolution -> resolution
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Alerts](../alerts/)
- [Architecture](../architecture/)
- [Capacity](../capacity/)
- [Cli Reference](../cli-reference/)
- [Deploy](../deploy/)
- [Design Standards](../design-standards/)
- [Health](../health/)
- [Integration](../integration/)
- [Learning Path](../learning-path/)
- [Lifecycle](../lifecycle/)
- [Operations](../operations/)
- [Performance](../performance/)
- [Scripts](../scripts/)
- [Security](../security/)
- [Support](../support/)
- [Vendor Support](../vendor-support/)
- [Pure1 — Overview](../)

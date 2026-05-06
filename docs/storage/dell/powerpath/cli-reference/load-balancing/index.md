# Load Balancing & Policies

> Part of the Dell PowerPath CLI Reference.

---

```bash
# Show load balancing policy
powermt display dev=emcpower<n> | grep -i policy

# Set policy on a device
powermt set policy=<policy> dev=emcpower<n>
# Policies: co (CLARiiON Optimized), rr (Round Robin), si (Single Initiator), etc.

# Set globally
powermt set policy=co dev=all class=clariion
```

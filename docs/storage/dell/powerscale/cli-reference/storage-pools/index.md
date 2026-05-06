# Storage Pools & Tiers

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# Storage pools
isi storagepool nodepools list
isi storagepool nodepools view <pool_name>
isi storagepool tiers list
isi storagepool tiers view <tier_name>

# File pool policies
isi filepool policies list
isi filepool policies view <policy_name>
isi filepool default-policy view

# SmartPools status
isi job status | grep -i pool
```

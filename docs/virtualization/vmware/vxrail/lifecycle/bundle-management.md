---
tags:
  - vxrail
---
# VxRail — Bundle Management
![VxRail — Bundle Management](../../../../assets/virtualization-vmware-vxrail-lifecycle-bundle-management.svg)




```text
                           │  upload via UI or SCP
```


```text
                           │  automatic
┌────────────────────────────────────────────────── ▼ ──────────────────────────────────────────────────┐
│  Validation                                                                                           │
│  checksum · version matrix · node compatibility                                                       │
│  PASS → bundle staged                                                                                 │
│  FAIL → error detail, do not proceed                                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                           │  on LCM start
```

```bash
# Add environment-specific commands here
```

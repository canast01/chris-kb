```text
```
```text
┌─────────────────────────────────────────────────────────────┐
│  Dell Support Portal / Offline Source                                                                 │
│  Download VxRail Composite Bundle (.zip)                                                              │
└──────────────────────────┬──────────────────────────────────┘
```

```text
                           │  upload via UI or SCP
```
```text
┌──────────────────────────▼──────────────────────────────────┐
│  VxRail Manager — Bundle Upload                                                                       │
│  System → Lifecycle → Upload Bundle                                                                   │
└──────────────────────────┬──────────────────────────────────┘
```

```text
                           │  automatic
┌──────────────────────────▼──────────────────────────────────┐
│  Validation                                                                                           │
│  checksum · version matrix · node compatibility                                                       │
│  PASS → bundle staged                                                                                 │
│  FAIL → error detail, do not proceed                                                                  │
└──────────────────────────┬──────────────────────────────────┘
                           │  on LCM start
```
```text
┌──────────────────────────▼──────────────────────────────────┐
│  Stage → Apply                                                                                        │
│  VxRail Manager extracts components → applies node-by-node                                            │
│  firmware + ESXi + vSAN updated in certified combination                                              │
└─────────────────────────────────────────────────────────────┘
```
```bash
# Add environment-specific commands here
```

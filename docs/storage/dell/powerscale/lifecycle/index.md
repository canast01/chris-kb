# PowerScale Lifecycle

## Software Version Matrix

| OneFS Release | Notes |
|---|---|
| 9.8.x | Current GA; enhanced S3 multi-part improvements, CloudPools updates |
| 9.7.x | Generally available; improved SmartQuota reporting and CloudIQ v2 support |
| 9.5.x | Long-term support; widely deployed; recommended upgrade target if on 9.3 or earlier |
| 9.4.x | General availability ended; upgrade to 9.5 or later recommended |
| 9.3.x | End of standard support; security patches only |
| 8.2.x | Extended support only; upgrade required for continued support |
| 8.1.x and earlier | End of service life; no patches available |

Always verify upgrade path support in the Dell Upgrade Advisor before initiating.

## Upgrade Paths

- **Patch-level upgrades** (e.g., 9.5.0.x → 9.5.0.y): apply via `isi upgrade patch apply`; non-disruptive rolling node upgrade.
- **Minor version upgrades** (e.g., 9.5.x → 9.7.x): must go through supported intermediate versions if skipping releases. Use the Dell Upgrade Advisor to confirm supported path.
- **Major version upgrades** (e.g., 8.2.x → 9.5.x): requires careful planning; some node hardware may not support target OneFS version. Contact Dell Support for a compatibility check.

Recommended upgrade sequence:

1. Run `isi status` and resolve all node/drive errors.
2. Pause all SyncIQ policies.
3. Download the upgrade image to `/ifs/data/upgrades/` and verify checksum.
4. Run the upgrade pre-check: `isi upgrade cluster pre-upgrade-check`.
5. Initiate parallel upgrade (preferred for 9.x): `isi upgrade cluster upgrade --parallel`.
6. Monitor with `isi upgrade view`.
7. After completion, run `isi status`, resume SyncIQ policies, and verify client access.

## Refresh Planning

| Trigger | Action |
|---|---|
| Cluster capacity above 80% usable | Plan node expansion; order and integrate new nodes per hardware compatibility matrix |
| Node hardware reaching 7-year mark | Evaluate node replacement; PowerScale allows non-disruptive rolling node retirement |
| OneFS N-2 behind current GA | Schedule upgrade; N-2 or older loses proactive support priority |
| New node family released with significant performance gain | Evaluate mixed-node cluster strategy; add new node type as a separate pool |
| SyncIQ bandwidth consistently saturated | Upgrade WAN circuit or shift to a closer DR site |

## EOL Tracking

| Component | Status |
|---|---|
| OneFS 8.1.x and below | End of service life — no support |
| OneFS 8.2.x | Extended support only — no new fixes |
| OneFS 9.3.x | End of standard support — security patches only |
| OneFS 9.5.x | Active LTS — full support |
| OneFS 9.7.x / 9.8.x | Current GA — full support |

Node hardware EOL is announced 12–18 months in advance via Dell EOL notification. Nodes can be decommissioned from a live cluster non-disruptively using `isi devices node smartfail`.

Check current status: https://www.dell.com/support/home/en-us/product-support/product/isilon-onefs/drivers

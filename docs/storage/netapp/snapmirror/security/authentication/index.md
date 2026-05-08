# SnapMirror — Authentication

> Part of the [SnapMirror Security](../) reference.

---

## Intercluster Authentication

Cluster peering uses a pre-shared passphrase negotiated at peer establishment time. The passphrase is used once to authenticate the relationship; subsequent replication traffic uses TLS-encrypted channels. From ONTAP 9.6 onwards, all intercluster communication is TLS encrypted by default. Cluster peer relationships should be reviewed annually and stale peers removed.

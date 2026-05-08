# SnapMirror — Encryption

> Part of the [SnapMirror Security](../) reference.

---

## Encryption in Transit

SnapMirror Transfer Data Encryption (TDE) encrypts replication traffic end-to-end between clusters. Encryption is configured per relationship and does not require IPsec on the network layer.

```bash
# Enable encryption on an existing SnapMirror relationship
snapmirror modify -destination-path svm_dst:vol_dst -encryption-algorithm aes-256

# Verify encryption is enabled
snapmirror show -destination-path svm_dst:vol_dst -fields encryption-algorithm
```

Encryption in transit is mandatory for any replication relationship crossing a network segment that is not fully controlled (e.g., WAN links, third-party interconnects).

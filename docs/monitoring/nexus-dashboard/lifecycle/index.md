# Nexus Dashboard Lifecycle

Nexus Dashboard supports rolling upgrades within the cluster, upgrading one node at a time to maintain service availability. Before upgrading, verify compatibility between the target ND version and the installed service versions (NDFC, NDI) using the Cisco Nexus Dashboard Compatibility Matrix. ACI and NX-OS firmware compatibility must also be checked against the target ND version prior to fabric upgrades. EOL dates for ND versions are published on the Cisco EOL/EOS page. Upgrade packages are downloaded from software.cisco.com.

| Activity | Method / Reference |
|---|---|
| Compatibility check | Cisco ND Compatibility Matrix |
| Upgrade | Rolling node upgrade via ND Admin UI |
| Firmware compatibility | Cisco HCL / IMT |
| EOL tracking | Cisco EOL/EOS notices (cisco.com/go/eos) |
| Upgrade packages | software.cisco.com |

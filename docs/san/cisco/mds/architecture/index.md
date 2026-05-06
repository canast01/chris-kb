# Cisco MDS Architecture

Cisco MDS 9000 series switches run NX-OS and support both Fibre Channel and FCoE, providing scalable SAN fabric services for enterprise environments. VSANs (Virtual SANs) are the core isolation mechanism, allowing multiple logical fabrics to share physical infrastructure while maintaining separate name servers, zoning databases, and fabric login tables. Common models include the MDS 9132T and 9148T (fixed configuration), 9396T (high-density), and 9706/9710 directors for large-scale deployments. FC services include FCNS (name server), FLOGI/PLOGI database tracking, and port-channel ISLs for redundant inter-switch connectivity.

| Model | Type | Max Ports |
|---|---|---|
| MDS 9132T | Fixed | 32x 32G FC |
| MDS 9148T | Fixed | 48x 32G FC |
| MDS 9396T | Fixed | 96x 32G FC |
| MDS 9706 | Director | Up to 384 FC ports |
| MDS 9710 | Director | Up to 576 FC ports |

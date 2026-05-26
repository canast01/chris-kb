# NetBackup — Hardening

## NetBackup Security Architecture

```mermaid
flowchart TD
    subgraph accessControl [Access Control]
        nbac["NBAC\nRole-based access\nAD group mappings"]
        opscenterRBAC["OpsCenter RBAC\nBackup admin group only"]
    end

    subgraph authLayer [Authentication & Certificates]
        nbuCA["NetBackup CA\nclient certificates\nfor all hosts"]
        cyberArk["CyberArk AAM\nruntime credential\nretrieval"]
    end

    subgraph networkSecurity [Network Security]
        fw["Firewall rules\n1556, 13724, 13782\nonly from authorised subnets"]
        ssh["SSH restricted to\nmanagement jump hosts"]
        pbx["PBX disabled\non client hosts"]
    end

    subgraph auditLogging [Audit & Monitoring]
        audit["nbauditreport\nweekly review"]
        siem["SIEM forwarding\nnblog syslog output"]
    end

    master["Primary Server"]
    master --> nbac
    master --> nbuCA
    master --> cyberArk
    master --> fw
    master --> ssh
    master --> audit
    audit --> siem

    classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef sec fill:#be123c,stroke:#9f1239,color:#fff
    classDef mon fill:#b45309,stroke:#92400e,color:#fff
    class master ctrl
    class nbac,opscenterRBAC,nbuCA,cyberArk,fw,ssh,pbx sec
    class audit,siem mon
```
```

Forward to SIEM: configure `nblog` syslog output or use a log shipper agent pointing to `/usr/openv/netbackup/logs/audit/`.

## Firewall Ports

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Master | Media, Clients | 13724, 13782 | bpcd, bpbrm |
| Clients | Master | 1556 | vnetd |
| OpsCenter | Master | 1556 | Reporting |
| Admin workstation | Admin Console | 1556 | Management |

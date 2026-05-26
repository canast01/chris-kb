# Commvault — Diagnostics

## Diagnostic Flow

```mermaid
flowchart TD
    alert(["Job failure or alert\nreceived"])
    alert --> jobId["Identify Job ID\nfrom Job Controller\nor email alert"]
    jobId --> jobDetail["qlist jobs -j <jobid>\nor Command Center\nJob detail view"]
    jobDetail --> errCode["Note error code\nand affected client"]
    errCode --> q1{Error category}

    q1 -->|"Client\nconnectivity"| clientLog["Check client log\nclBackup.log on client\nor CVMA.log"]
    q1 -->|"Storage / DDB\nissue"| ddbCheck["qlist ddb\ncheck DDB space\n+ CVMA.log on MA"]
    q1 -->|"Unknown /\ncomplex"| bundle["Collect support bundle\nqsystem log export\n-path C:\\cv_support_bundle"]

    clientLog --> ready["qoperation execscript\n-sn QS_CheckReadiness"]
    ddbCheck --> ddbVerify["qoperation execscript\n-sn QS_DDBVerify"]
    bundle --> escalate["Open support case\nwith bundle + job ID"]

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class jobId,jobDetail,errCode,clientLog,ddbCheck,bundle,ready,ddbVerify,escalate action
    class q1 decision
    class alert terminal
```

## Support Bundle Collection

Before opening a support case, collect the support bundle on the CommServe:

```bash
# On CommServe (run as administrator)
qsystem log export -path C:\cv_support_bundle

# Alternatively via Command Center:
# Settings > Support > Generate Support Bundle
```

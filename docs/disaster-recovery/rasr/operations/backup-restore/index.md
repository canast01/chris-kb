# RASR — Backup & Restore

## Creating a System Image

### Prerequisites

- RASR Agent installed and running (`DellRASR` service).
- Sufficient space on the destination network share (typically 1.5–2x the used space on the OS volume).
- Service account with write access to the backup share.
- Server has network connectivity to the NAS target.

### Creating an Image via RASR Console (GUI)

1. Open **Dell RASR** from Start Menu → **Dell** → **Recovery and System Restore**.
2. Click **Create Recovery Image**.
3. Select volumes to include (at minimum: System Reserved, C:\ drive).
4. Set the destination:
   - **Local media** (USB drive): Select the drive letter.
   - **Network share**: Enter `\\nas01\rasr-images\SERVER01` → authenticate with service account.
5. Optionally configure compression level (Balanced or High).
6. Click **Create** — the wizard shows progress and elapsed time.
7. Confirm the image was written successfully and note the image filename.

### Creating an Image via Command Line

```cmd
:: Basic image to network share
rasrutil.exe /backup /dest \\nas01\rasr-images\SERVER01 /user DOMAIN\svc-rasr /pass P@ssw0rd!

:: With compression and verbose output
rasrutil.exe /backup /dest \\nas01\rasr-images\SERVER01 /compress /log C:\Logs\rasr-backup.log /user DOMAIN\svc-rasr /pass P@ssw0rd!
```

---

## Scheduling Automated Backups

RASR does not include a native scheduler with a GUI. Use **Windows Task Scheduler** to automate image creation.

### Creating a Scheduled Task

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Program Files\Dell\RASR\rasrutil.exe" `
    -Argument "/backup /dest \\nas01\rasr-images\$env:COMPUTERNAME /compress /user DOMAIN\svc-rasr /pass P@ssw0rd! /log C:\Logs\rasr-backup.log"

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "02:00AM"

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "RASR Weekly Backup" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "Weekly RASR system image backup to NAS"
```

### Recommended Backup Schedule

| Frequency | Scope | Retention |
|---|---|---|
| Weekly (Sunday 02:00) | Full system image | Keep 4 (rolling 4 weeks) |
| Monthly (1st Sunday) | Full system image | Keep 12 (rolling 12 months) |
| Pre-change | Full system image | Keep until change confirmed stable |

---

## Restore Procedure

### Phase 1 — Boot from RASR Media

**Option A: Physical USB**

Insert the RASR boot USB into the server. On POST, press **F11** (Dell boot menu) and select the USB drive.

**Option B: iDRAC Virtual Media (remote recovery)**

```bash
# Mount ISO via racadm
racadm remoteimage -c -u <idrac-user> -p <idrac-pass> \
  -l //nas01.example.com/rasr-media/RASR_WinSrv2022.iso

racadm set iDRAC.ServerBoot.BootOnce 1
racadm set iDRAC.ServerBoot.FirstBootDevice VCD-DVD
racadm serveraction powercycle
```

### Phase 2 — WinPE Environment

The server boots into the RASR WinPE environment. The RASR recovery wizard launches automatically. If it does not, open a command prompt and run:

```cmd
X:\Dell\RASR\rasrwizard.exe
```

### Phase 3 — Map Network Share

Before selecting an image, connect to the network share where images are stored:

```cmd
net use Z: \\nas01.example.com\rasr-images /user:DOMAIN\svc-rasr P@ssw0rd!
```

Verify the image directory is accessible:

```cmd
dir Z:\SERVER01\
```

### Phase 4 — Select Image and Restore

1. In the RASR wizard, click **Restore from Image**.
2. Browse to `Z:\SERVER01\` and select the desired `.rasr` image file.
3. Select the target disk (the wizard shows disk size and current partition layout).
4. Confirm the restore will overwrite the target disk.
5. Click **Restore** — progress bar shows bytes written and estimated time remaining.

**Typical restore times:**

| Image Size | 1 Gbps Network | 10 Gbps Network |
|---|---|---|
| 50 GB | ~45 min | ~8 min |
| 100 GB | ~90 min | ~15 min |
| 200 GB | ~3 hrs | ~30 min |

### Phase 5 — Reboot and Validate

1. After the wizard confirms completion, eject the RASR media or disconnect virtual media in iDRAC.
2. Reboot the server.
3. Monitor boot via iDRAC console.
4. Log in and proceed with post-restore validation.

---

## Bare-Metal Restore to Replacement Hardware

When restoring to a different physical server (e.g., hardware replacement), additional steps are required:

1. Ensure the replacement server is the same model or at minimum uses the same storage controller and NIC model.
2. RASR WinPE includes Dell hardware driver packs — most same-generation hardware is supported.
3. If the replacement is a different model, manually inject drivers into WinPE before restore:

```cmd
:: In WinPE — inject missing driver
Dism /Image:C:\ /Add-Driver /Driver:X:\drivers\perc_h755.inf
```

4. After restore, if Windows fails to boot due to missing drivers:
   - Boot into Windows Recovery Environment (WinRE).
   - Use `dism /online /Add-Driver` to inject the correct storage/NIC driver.

---

## Restore Decision Flowchart

```mermaid
flowchart TD
    A([Server Unavailable]) --> B{Boot possible?}
    B --> |Yes| C[Boot to RASR Console\nfrom running OS]
    B --> |No| D{Physical access?}

    D --> |Yes| E[Insert RASR USB\nBoot from USB]
    D --> |No - remote| F[Mount ISO via iDRAC\nBoot from Virtual Media]

    C --> G[Select Recovery Image\nfrom mapped share]
    E --> H[WinPE Loads]
    F --> H

    H --> I[Map network share\nnet use Z: ...]
    I --> G

    G --> J{Same hardware?}
    J --> |Yes| K[In-place restore\nto original disks]
    J --> |No - replacement HW| L[Bare-metal restore\n+ driver validation]

    K --> M[Restore runs\nimage written to disk]
    L --> M

    M --> N[Eject media\nReboot server]
    N --> O{Windows boots?}
    O --> |Yes| P[Post-restore validation]
    O --> |No| Q[Boot into WinRE\nInject missing drivers]
    Q --> N

    P --> R([Recovery Complete])
```

---

## Post-Restore Validation Checklist

| # | Check | Command / Method |
|---|---|---|
| 1 | Server boots to login prompt | iDRAC console |
| 2 | OS version and patch level correct | `winver` |
| 3 | Hostname correct | `hostname` |
| 4 | IP address / DNS correct | `ipconfig /all` |
| 5 | Domain membership intact | `whoami /fqdn` or `systeminfo \| findstr /i domain` |
| 6 | Secure channel to DC valid | `Test-ComputerSecureChannel -Verbose` |
| 7 | Critical services running | `Get-Service \| Where Status -eq "Stopped"` |
| 8 | Application functional | Application-specific health check |
| 9 | Event Log — no critical boot errors | Event Viewer → System → Error/Critical |
| 10 | RASR Agent service running | `Get-Service DellRASR` |
| 11 | New backup image created post-restore | Run RASR backup immediately |
| 12 | Recovery documented in ITSM | Incident/change record updated |

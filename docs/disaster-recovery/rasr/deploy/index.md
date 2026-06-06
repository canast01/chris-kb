# RASR — Initial Deployment

Dell PowerProtect Cyber Recovery (formerly RASR — Rapid Access System Recovery) is Dell's cyber vault solution. It pairs PowerProtect Data Manager (PPDM) with CyberSense to create an isolated, AI-verified recovery vault that protects critical data from ransomware and insider threats. This page walks through a greenfield deployment from OVA to a validated first recovery copy.

---

## Prerequisites

Confirm the following before starting the deployment:

**Infrastructure:**

- PowerProtect Data Manager (PPDM) appliance licence — production instance already deployed and managing backups
- Isolated vault vCenter or standalone ESXi host — this vCenter must have no connectivity to the production network during normal operations
- CyberSense licence obtained from Dell (node-locked to the vault PPDM instance)
- Minimum vault hardware: 4 vCPU / 16 GB RAM / 1 TB datastore for PPDM appliance; additional capacity for CyberSense VM (8 vCPU / 32 GB RAM)

**Networking:**

- Vault management network (VLAN isolated from production) with static IP allocation for PPDM and CyberSense
- Firewall or air-gap mechanism between production and vault — the vault network must be lockable on demand
- Replication path: TCP 7000 and TCP 7443 open from production PPDM to vault PPDM during the replication window only
- DNS entries resolvable within the vault: vault PPDM FQDN, CyberSense FQDN

**Agents and assets:**

- Windows Agent or Linux Agent installed on all protected systems (PPDM agent package)
- Asset discovery completed on production PPDM — all assets visible before configuring replication

---

## Deploy PowerProtect Data Manager

1. Download the PPDM OVA from Dell support (match version to production PPDM — versions must be identical for replication).
2. Log in to the vault vCenter → **Actions → Deploy OVF Template** → select the PPDM OVA.
3. Assign to the vault cluster/host and vault datastore — do not place on any shared storage that is accessible from production.
4. Complete the OVF properties form:
   - Management IP, subnet mask, default gateway
   - DNS server (vault DNS or hosts-file fallback)
   - NTP server reachable from the vault
   - Admin password (16+ chars, record in vault credentials store)
5. Power on the VM → wait 10–15 minutes for first-boot initialisation.
6. Open `https://<vault-ppdm-ip>` → complete the **Initial Setup Wizard**:
   - Accept EULA
   - Verify network settings
   - Set time zone and NTP sync
   - Activate licence (upload the Dell licence file)
7. Confirm the PPDM dashboard loads and shows zero assets (expected at this stage).

---

## Configure the Vault Network

The vault network isolation is the security boundary of the entire solution. A misconfigured network defeats the purpose of a cyber vault.

1. Create a dedicated VLAN for vault traffic (recommended: separate physical switch or locked-down VLAN with no inter-VLAN routing to production by default).
2. Configure the perimeter firewall or network access controller (NAC) with two modes:
   - **Closed (default):** No routes between production and vault. All inter-site firewall rules denied.
   - **Open (replication window):** TCP 7000 and TCP 7443 allowed from production PPDM IP to vault PPDM IP for the duration of the scheduled replication window only.
3. Add a firewall rule allowing HTTPS (TCP 443) inbound to vault PPDM from the operations management station only — limit source IPs.
4. Test isolation in closed mode:
   - From production PPDM: `ping <vault-ppdm-ip>` — must fail (no route).
   - From vault PPDM: `ping <production-ppdm-ip>` — must fail.
5. Test replication path in open mode (simulate by temporarily opening firewall rules):
   - TCP 7000 and 7443 reachable from production PPDM to vault PPDM.
   - Close again after test.

---

## Set Up CyberSense

CyberSense provides AI-powered content inspection of recovery copies to classify them as clean or suspect before a recovery is approved.

1. Deploy a Windows Server 2019/2022 VM inside the vault network (CyberSense requires Windows — it cannot run on Linux).
2. Download the CyberSense installer from Dell support — match the version to the PPDM vault version.
3. Run the installer on the Windows VM:
   - Accept defaults for installation path
   - Enter the CyberSense licence key when prompted
   - Set the CyberSense service account credentials
4. Open `https://<cybersense-ip>:443` and complete initial setup.
5. Connect CyberSense to vault PPDM:
   - CyberSense UI → **Settings → PPDM Integration** → enter vault PPDM FQDN and admin credentials → **Test Connection** → Save.
6. Configure scan policies:
   - CyberSense → **Policies → New Policy** → select asset types (Files, Databases, Exchange)
   - Set scan schedule (recommend: scan every new recovery copy within 2 hours of replication)
   - Enable full-content entropy analysis (detects encryption) and file-signature analysis (detects corruption)
7. Verify CyberSense appears as connected in vault PPDM → **Settings → Cyber Recovery → CyberSense Status: Connected**.

---

## Configure Replication from Production PPDM

Replication copies backup data from the production PPDM into the vault and applies Integrity Lock (immutability) on arrival.

1. Log in to **production** PPDM.
2. Navigate to **Configure → System Settings → Replication**.
3. Select **Add Replication Target**:
   - Target PPDM address: vault PPDM FQDN or IP
   - Credentials: vault PPDM admin account
   - Port: 7000 (verify firewall is open in test/open mode)
   - **Test Connection** → confirm success → Save.
4. Configure Integrity Lock on the replication target:
   - Replication target settings → **Integrity Lock** → Enabled
   - Lock period: minimum 14 days (adjust to policy — NIST CSF recommendation is 30 days for critical assets)
   - Once set, lock period cannot be shortened without Dell support involvement.
5. Schedule replication windows to align with vault network open windows:
   - Recommended: nightly replication window 02:00–05:00 local time
   - Production PPDM → Replication Target → **Edit Schedule** → set start/end times

---

## Create First Cyber Recovery Copy

1. Log in to **production** PPDM → **Protection → Protection Policies**.
2. Select **New Policy** → name it (e.g., `CR-Critical-Assets-v1`).
3. Add assets:
   - Add VMs, databases, or file systems as required
   - Confirm agents are installed and assets show as Protected
4. Enable Cyber Recovery:
   - Policy settings → **Cyber Recovery → Enabled**
   - Select the vault PPDM replication target configured in the previous step
   - Set retention on the vault copy (recommended: 60 days minimum)
5. Set primary backup schedule (e.g., daily at 22:00) and replication schedule (nightly after backup completes).
6. **Save and Run Now** to trigger the first backup and replication.
7. Monitor replication progress:
   - Production PPDM → **Monitor → Jobs** → verify replication job completes without errors
   - Vault PPDM → **Protection → Recovery Copies** → new copy appears with Integrity Lock icon
8. Confirm CyberSense scan triggered automatically — vault PPDM → **Cyber Recovery → Scan Status** → scan completes → **Clean** classification.

---

## Validate Recovery

Testing the recovery path before an incident is mandatory — an untested cyber vault provides false assurance.

1. Log in to **vault PPDM**.
2. Navigate to **Restore → Asset Recovery**.
3. Select a protected asset → browse to a recent recovery copy with **Clean** CyberSense status.
4. Select **Image Access** (non-destructive, read-only mount — does not power on the VM into the production network):
   - Specify target ESXi host within the vault
   - Confirm network: assign to an isolated test port group (no production VLAN)
   - Launch Image Access session
5. Verify the VM or file system is accessible within the vault:
   - For VMs: confirm OS boots, application services start, data integrity intact
   - For file systems: spot-check critical files and directory structure
6. Review CyberSense classification for the recovery point used — confirm **Clean** (no ransomware indicators, no entropy anomalies).
7. End the Image Access session → vault PPDM → **Image Access → Terminate Session**.
8. Document the recovery test result: date, asset, recovery point timestamp, CyberSense classification, tester sign-off.

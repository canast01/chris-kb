# Jira — Initial Deployment

<div class="kb-summary">
Step-by-step guide to installing Jira Data Center, configuring the database connection, setting up user authentication, and validating the deployment.
</div>

## Prerequisites

Before installing Jira, confirm the following are in place.

**JDK:**

- Jira Data Center requires Eclipse Temurin (formerly AdoptOpenJDK) 11 or 17
- Do not use the system JDK — install Temurin in a dedicated path
- Verify: `java -version` must return the correct version after installation

**Database — PostgreSQL (recommended) or MySQL:**

| Component | Requirement |
|---|---|
| PostgreSQL | 14.x or 15.x (check Jira compatibility matrix) |
| MySQL | 8.0.x (with specific driver — check Atlassian docs) |
| Database name | `jira` (or as preferred) |
| Database user | Dedicated `jira` user with CREATE/ALTER/DROP on the `jira` database |
| Encoding | UTF-8 |
| Collation | C (PostgreSQL) |

**System resources — minimum 8 GB RAM:**

| Parameter | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| vCPU | 4 | 8 |
| App disk | 50 GB | 100 GB |
| Home/data disk | 200 GB | 500 GB |

**OS:**

- RHEL 8/9 or Ubuntu 22.04 LTS
- Static IP, DNS forward and reverse records, NTP synchronised
- `ulimit -n` must be ≥ 65536 — set in `/etc/security/limits.conf`

**Ports:**

- 8080/TCP — Jira HTTP (proxied to 443 by nginx/Apache)
- 8443/TCP — Jira HTTPS (if TLS termination is on Jira itself)
- 40001/TCP, 40011/TCP — Jira Data Center cluster communication

---

## Download and Install Jira

1. Download the Jira Data Center Linux installer from `https://www.atlassian.com/software/jira/download`.
2. Make the installer executable and run it:
   ```bash
   chmod +x atlassian-jira-software-X.Y.Z-x64.bin
   sudo ./atlassian-jira-software-X.Y.Z-x64.bin
   ```
3. Follow the installer prompts:
   - **Installation type:** Custom (to control install and home directory paths)
   - **Install directory:** `/opt/atlassian/jira`
   - **Home directory:** `/var/atlassian/application-data/jira`
   - **TCP ports:** accept defaults (8080, 8005, 8443) unless conflicts exist
   - **Start Jira automatically:** yes
4. The installer creates the `jira` system user and starts the service.
5. Confirm Jira is running:
   ```bash
   sudo systemctl status jira
   ```
6. Check the Jira startup log for errors:
   ```bash
   tail -f /opt/atlassian/jira/logs/catalina.out
   ```

---

## Configure Database Connection

Before visiting the web UI, set up the PostgreSQL database.

**Create the database and user (run as postgres):**

```bash
sudo -u postgres psql
CREATE USER jira WITH PASSWORD 'secure-password-here';
CREATE DATABASE jira OWNER jira ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE jira TO jira;
\q
```

**Run the Jira setup wizard:**

1. Open a browser to `http://<jira-server>:8080`.
2. On the **Set up application** screen, select **I'll set it up myself**.
3. On the **Set up database** screen:
   - Select **My own database**
   - Database type: **PostgreSQL**
   - Hostname: `localhost` (or DB server IP)
   - Port: `5432`
   - Database name: `jira`
   - Username: `jira`
   - Password: the password set above
4. Click **Test Connection** — must return **Connection Successful**.
5. Click **Next** — Jira will now create all required tables (takes 5–15 minutes).

---

## Configure Application Properties

1. On the **Application Properties** screen:
   - **Application Title:** your organisation name + "Jira" (e.g. `Acme Jira`)
   - **Mode:** Private
   - **Base URL:** set the externally accessible URL (e.g. `https://jira.company.local`) — this must match the DNS entry and proxy config
2. Click **Next**.
3. On the **Licence** screen, enter the Jira Data Center licence key (obtain from `my.atlassian.com`).
4. Click **Next**.
5. On the **Administrator account** screen, create the initial admin user:
   - Username: `admin`
   - Full name: `Jira Admin`
   - Email: operations mailbox address
   - Password: strong password (store in the team password manager)
6. Click **Next** then **Finish**.
7. Jira redirects to the dashboard after setup completes.

**Set JVM heap (recommended):**

Edit `/opt/atlassian/jira/bin/setenv.sh`:

```bash
# For 16 GB server
JVM_MINIMUM_MEMORY="2048m"
JVM_MAXIMUM_MEMORY="8192m"
```

Restart Jira: `sudo systemctl restart jira`

---

## Create First Project

1. Log in to Jira as the admin account.
2. Click **Projects → Create Project**.
3. Select the project type:
   - **Scrum** — for development teams using sprints
   - **Kanban** — for operations teams with continuous flow
   - **Business** — for non-development projects
4. Enter the **Project Name** and **Project Key** (short identifier used in issue numbers, e.g. `OPS`).
5. Click **Create**.
6. The project board opens — confirm the board loads and issue creation works by clicking **Create** and submitting a test issue.

---

## Configure User Authentication (LDAP/SSO)

**LDAP/Active Directory:**

1. Navigate to **Administration (cog icon) → User management → User directories**.
2. Click **Add directory** and select **Microsoft Active Directory** or **LDAP**.
3. Configure the connection:
   - **Server:** LDAP server FQDN (e.g. `dc01.company.local`)
   - **Port:** 389 (LDAP) or 636 (LDAPS — recommended)
   - **Bind DN:** service account DN (e.g. `CN=svc-jira,OU=ServiceAccounts,DC=company,DC=local`)
   - **Bind password:** service account password
   - **Base DN:** base OU for user search (e.g. `OU=Users,DC=company,DC=local`)
4. Under **Schema settings**, verify the user object class and username attribute match your directory schema (`sAMAccountName` for AD).
5. Click **Test Settings** — must return a successful bind and user count.
6. Click **Save and Test**.
7. Set the directory order so LDAP is above the internal directory if LDAP is the primary auth source.

**SAML SSO (Jira Data Center):**

1. Navigate to **Administration → System → SAML 2.0 single sign-on**.
2. Enter the IdP metadata URL or upload the metadata XML.
3. Configure the user attribute mapping (NameID to Jira username).
4. Test with a non-admin account before enabling SSO for all users.

---

## Install Required Plugins

1. Navigate to **Administration → Manage apps → Find new apps**.
2. Search for and install the following recommended apps:

| App | Purpose |
|---|---|
| **ScriptRunner for Jira** | Groovy scripting for workflow automation |
| **Jira Misc Workflow Extensions (JMWE)** | Additional workflow conditions and validators |
| **BigPicture** | Portfolio and project roadmap view |
| **Insight (now Assets)** | CMDB/asset management (included in Jira Service Management) |

3. After installing each app, click **Enable** and confirm it shows **Enabled** in the app list.
4. Apply any required app licences from the app vendor or `my.atlassian.com`.

---

## Validate Deployment

Run through the following checks before handing the instance to users.

**Application health:**

```bash
# Check Jira process
sudo systemctl status jira

# Check no OOM errors in the last boot cycle
sudo journalctl -u jira --since today | grep -i "out of memory"

# Confirm Jira responds
curl -I http://localhost:8080/status
# Expected: HTTP 200, {"state":"RUNNING"}
```

**Web UI:**

- Log in as admin and as an LDAP user — both must succeed
- Create a test issue in the first project and confirm it appears in the backlog
- Search using JQL: `project = OPS ORDER BY created DESC` — results must return

**Database:**

```bash
sudo -u postgres psql -d jira -c "SELECT count(*) FROM app_user;"
# Should return the user count — confirms schema is populated
```

**Email (if SMTP configured):**

- Navigate to **Administration → System → Mail → Send test email**
- Confirm delivery to the configured test address

**Plugins:**

- Navigate to **Administration → Manage apps → Manage apps** — all installed apps show **Enabled**, no **Error** status

---
tags:
  - deployment
  - jira
search:
  boost: 1.5
description: "Step-by-step guide to installing Jira Data Center, configuring the database connection, setting up user authentication, and validating the deployment."
---
# Jira — Initial Deployment

<div class="kb-summary">
Step-by-step guide to installing Jira Data Center, configuring the database connection, setting up user authentication, and validating the deployment.

*Applies to: Jira 9.x / Cloud*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
download_and_install_jira: "Download and Install Jira" {shape: rectangle}
configure_database_connection: "Configure Database Connection" {shape: rectangle}
configure_application_properties: "Configure Application Properties" {shape: rectangle}
create_first_project: "Create First Project" {shape: rectangle}
configure_user_authentication_ldapss: "Configure User Authentication (LDAP/SSO)" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> download_and_install_jira
download_and_install_jira -> configure_database_connection
configure_database_connection -> configure_application_properties
configure_application_properties -> create_first_project
create_first_project -> configure_user_authentication_ldapss
configure_user_authentication_ldapss -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

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


```text title="Expected output"
psql (14.8 (Ubuntu 14.8-1.pgdg22.04+1))
Type "help" for help.

postgres=# CREATE USER jira WITH PASSWORD 'secure-password-here';
CREATE ROLE
postgres=# CREATE DATABASE jira OWNER jira ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;
CREATE DATABASE
postgres=# GRANT ALL PRIVILEGES ON DATABASE jira TO jira;
GRANT
postgres=# \q
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: role "jira" already exists` | Drop the existing role with `DROP ROLE jira;` before recreating it, or use `CREATE USER IF NOT EXISTS jira` (PostgreSQL 10+). |
    | `FATAL: Ident authentication failed for user "postgres"` | Ensure you're running the command as the postgres system user with `sudo -u postgres` or configure pg_hba.conf to allow password authentication. |
    | `ERROR: database "jira" already exists` | Drop the existing database with `DROP DATABASE jira;` first, or use `CREATE DATABASE IF NOT EXISTS jira`. |
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: JVM_MINIMUM_MEMORY: command not found` | Ensure you are running these commands in a bash shell context, not pasting them into a non-shell environment. |
    | `export: command not found` | If these variables need to be persistent across sessions, prefix each line with `export` (e.g., `export JVM_MINIMUM_MEMORY="2048m"`). |
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


```text title="Expected output"
● jira.service - Atlassian Jira
     Loaded: loaded (/etc/systemd/system/jira.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2h 14min ago
       Docs: https://confluence.atlassian.com/jira
    Process: 4521 ExecStart=/opt/jira/bin/start-jira.sh (code=exited, status=0/SUCCESS)
   Main PID: 4589 (java)
      Tasks: 47 (limit: 4096)
     Memory: 2.8G
        CPU: 18min 34.231s
     CGroup: /system.slice/jira.service
             └─4589 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Djava.awt.headless=true...

HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
X-AREQUESTED-WITH: XMLHttpRequest
Content-Type: application/json
Content-Length: 28
Date: Mon, 15 Jan 2024 11:38:12 GMT

{"state":"RUNNING","version":"9.12.4"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit jira.service could not be found.` | Verify the Jira systemd service file exists at `/etc/systemd/system/jira.service` and run `sudo systemctl daemon-reload`. |
    | `curl: (7) Failed to connect to localhost port 8080: Connection refused` | Check that Jira is actually running with `sudo systemctl start jira` and wait 30–60 seconds for the application to fully initialize. |
    | `HTTP/1.1 503 Service Unavailable` | Jira is starting up; wait 2–3 minutes and retry, or check `/opt/jira/logs/catalina.out` for startup errors. |
**Web UI:**

- Log in as admin and as an LDAP user — both must succeed
- Create a test issue in the first project and confirm it appears in the backlog
- Search using JQL: `project = OPS ORDER BY created DESC` — results must return

**Database:**

```bash
sudo -u postgres psql -d jira -c "SELECT count(*) FROM app_user;"
# Should return the user count — confirms schema is populated
```


```text title="Expected output"
count
-------
  1247
(1 row)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: FATAL: role "postgres" does not exist` | Verify the PostgreSQL superuser name with `sudo -u postgres psql -l` or use the correct role name in the `-u` flag. |
    | `psql: error: FATAL: database "jira" does not exist` | Confirm the JIRA database exists by running `sudo -u postgres psql -l` and create it if missing with `createdb -U postgres jira`. |
    | `psql: error: ERROR: relation "app_user" does not exist` | Ensure the JIRA schema has been initialized by running the JIRA database setup script or checking that the application has completed its first-run configuration. |
**Email (if SMTP configured):**

- Navigate to **Administration → System → Mail → Send test email**
- Confirm delivery to the configured test address

**Plugins:**

- Navigate to **Administration → Manage apps → Manage apps** — all installed apps show **Enabled**, no **Error** status

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Jira — Procedures](../operations/procedures/)
- [Jira — Common Issues](../troubleshooting/common-issues/)
- [Jira — How It Works](../architecture/how-it-works/)

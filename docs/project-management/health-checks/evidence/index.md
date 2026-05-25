# Evidence Capture and Audit Trail

## Overview

Evidence capture creates a verifiable record of infrastructure state at a given point in time. This is essential for change audits, incident post-mortems, compliance reviews, and dispute resolution. Screenshots and command output saved only in memory are lost the moment the session ends.

---

## What Counts as Evidence

| Evidence Type          | Examples                                                     |
|------------------------|--------------------------------------------------------------|
| Command output         | Terminal output saved to file; `tee` captures                |
| Screenshots            | Dashboard state, alert conditions, config screens            |
| Log extracts           | Time-stamped log snippets covering the relevant window       |
| Configuration exports  | YAML/JSON/text config files exported before and after change |
| Monitoring graphs      | Exported PNG/PDF from Grafana, Datadog, CloudWatch           |
| Ticket updates         | Timestamped comments in ServiceNow, Jira, etc.               |

All evidence must include a timestamp (either in the content itself or in the filename).

---

## Naming Convention

Use a consistent naming convention so evidence can be located quickly.

```text
<date>_<type>_<system>_<context>.<ext>

Examples:
2026-05-07_screenshot_grafana_prod-cpu-pre-change.png
2026-05-07_output_df-h_prod-web01.txt
2026-05-07_config_nginx_prod-lb01-pre-change.conf
```

Avoid spaces in filenames. Use hyphens or underscores.

---

## Evidence Storage

| Storage Location        | Use Case                                   | Retention     |
|-------------------------|--------------------------------------------|---------------|
| Change ticket (attached)| Per-change evidence                        | Ticket lifecycle |
| Incident ticket (attached)| Incident-related evidence               | Ticket lifecycle |
| Shared drive / wiki     | Health check logs, audit exports           | 12 months     |
| Version control (Git)   | Config file diffs                          | Indefinitely  |
| S3 / blob storage       | Large log archives, graph exports          | Per policy    |

Do not store evidence only on a personal laptop or local desktop. If you are unavailable, someone else must be able to find it.

---

## Evidence Capture Checklist

For change windows:

- [ ] Pre-change state captured: service health, config, disk, relevant metrics
- [ ] Screenshots timestamped and named per convention
- [ ] Command output saved to file, not just viewed in terminal
- [ ] Evidence uploaded to the change ticket before implementation begins
- [ ] Post-change evidence captured using the same checks as pre-change
- [ ] Before/after comparison documented in ticket notes

For incidents:

- [ ] Initial alert / notification screenshot captured
- [ ] Timeline of key actions recorded in the incident ticket as they happen
- [ ] Relevant log extracts saved before they are rotated or overwritten
- [ ] Final state screenshot taken once service is restored

---

## Audit Trail Requirements

For compliance and regulatory purposes, the audit trail must show:

- Who took what action, and when
- What the state of the system was before and after
- What decisions were made and by whom

Timestamps in evidence must match the timezone used in the ticketing system. If your terminal uses UTC and your ticket system uses local time, note the offset explicitly.

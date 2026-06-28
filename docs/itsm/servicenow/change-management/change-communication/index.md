---
tags:
  - servicenow
---
# Change Communication

```yaml
Subject: [Planned Maintenance] <Service Name> — <Date> <Start Time> UTC

Service:        <service-name>
Window:         <start-datetime UTC> to <end-datetime UTC>
Expected impact: <None / Degraded performance / Service interruption>
Duration:       <estimated duration>
Change:         <one sentence description>
Rollback:       <one sentence rollback summary>
Contact:        <implementer name and channel>

If you have questions or concerns please reply by <date 2 days before window>.
```

```bash
[CHANGE-ROLLBACK] ITSM-XXXX
Rolling back <service-name> change due to: <brief reason>
Estimated rollback duration: <time>
Service expected restored by: <time>
```

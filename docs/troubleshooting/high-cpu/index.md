# High CPU Troubleshooting

## Overview

High CPU utilization can cause performance degradation, latency, and service instability across applications and infrastructure.

## Symptoms

- System slow response
- High load average
- Application timeouts
- Monitoring alerts

## Health Commands

```bash
top
htop
ps aux --sort=-%cpu | head
uptime
```

## Troubleshooting Workflow

1. Identify process consuming CPU
2. Confirm recent changes or deployments
3. Review logs
4. Validate resource limits
5. Restart or scale service if required

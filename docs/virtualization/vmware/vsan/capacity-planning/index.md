# vSAN Capacity Planning

## Minimum Free Space Guidance

25–30% free capacity recommended

Below 20%:
- Resync slows
- Rebuild risk increases
- Maintenance risk increases

## Slack Space Rule

Keep enough capacity for:

1 host failure
OR
1 disk group rebuild

## Capacity Formula

Usable Capacity = Raw Capacity ÷ FTT policy

Example:

Raw = 100 TB  
FTT=1 RAID1  

Usable ≈ 50 TB

## Risk Indicators

- Resync backlog
- Reduced rebuild speed
- Component limit warnings
- Capacity alarms

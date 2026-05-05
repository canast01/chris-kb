# DNS and NTP Validation

## Why This Matters

Time or DNS issues cause:

Host disconnect  
Certificate errors  
Authentication failure  
Cluster instability

## Validation

Forward lookup works  
Reverse lookup works  
NTP synchronized  
Time consistent across hosts

## Commands

nslookup hostname
ntpq -p
esxcli system ntp get
date

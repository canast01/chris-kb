# SAN Connectivity (iSCSI / FC)

> Part of the [VMware ESXi CLI Reference](../).

---

## iSCSI

```bash
esxcli iscsi adapter list
esxcli iscsi adapter get -A vmhba64
esxcli iscsi adapter discovery sendtarget list -A vmhba64
esxcli iscsi adapter discovery sendtarget add --address <ip>:<port> -A vmhba64
esxcli iscsi adapter discovery sendtarget remove --address <ip>:<port> -A vmhba64
esxcli iscsi session list
esxcli iscsi logicalnetworkportal list -A vmhba64
```

---

## Fibre Channel

```bash
esxcli storage san fc list
esxcli storage san fc stats get -A vmhba0
esxcli storage san iscsi list
```

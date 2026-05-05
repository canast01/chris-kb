# Virtualization Command Cheat Sheets

## ESXi

~~~bash
esxcli system version get
esxcli network ip interface list
esxcli storage core path list
~~~

## vCenter

~~~bash
service-control --status
vmon-cli --list
~~~

## vSAN

~~~bash
esxcli vsan health cluster list
esxcli vsan storage list
~~~

## NSX

~~~bash
get logical-switch
get edge-cluster
~~~

## VxRail

~~~bash
vxrail cluster info
vxrail health status
~~~

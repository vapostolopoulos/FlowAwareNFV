Here are the groups of vpps to be launched in the system. They are connected 
like this:

1. vpp1-vpp2-vpp3
2. vpp4-vpp5-vpp6-vpp7-vpp8
3. vpp9-vpp10-vpp11-vpp12-vpp13-vpp14-vpp15

Each group is also connected to vpprouter1 and vpprouter2. Vpprouter1 is used
to connect each group to the host for testing purposes (ping) and vpprouter2 
for forwarding back the traffic.

You can launch whatever combination you want but each group must be whole. 

You have to manually launch each vpp e.g. ./vpprouter1.conf, ./vpprouter2.conf,
vpp1.conf, etc. After launching router1,2 and the group(s) you want you must 
add static routes to vpprouter1 and 2. This is done for testing purposes and 
that is why it is not preconfigured. You have to add these static routes 
depending on the group you would like to ping:

-vpprouter1
$ sudo vppctl -s /run/vpp/cli-vpprouter1.sock 

 Add routes to group 1,2,3 respectively:
	vpp# ip route add 10.10.2.0/24 via 10.10.3.2
	vpp# ip route add 10.10.2.0/24 via 10.10.6.2
	vpp# ip route add 10.10.2.0/24 via 10.10.12.2

 Delete routes to group1,2,3 respectively:
	vpp# ip route delete 10.10.2.0/24 via 10.10.3.2
	vpp# ip route delete 10.10.2.0/24 via 10.10.6.2
	vpp# ip route delete 10.10.2.0/24 via 10.10.12.2

-vpprouter2
$ sudo vppctl -s /run/vpp/cli-vpprouter2.sock 

 Add routes to group 1,2,3 respectively:
	vpp# ip route add 10.10.1.0/24 via 10.10.2.4
	vpp# ip route add 10.10.1.0/24 via 10.10.11.1
	vpp# ip route add 10.10.1.0/24 via 10.10.19.1

 Delete routes to group1,2,3 respectively:
	vpp# ip route delete 10.10.1.0/24 via 10.10.2.4
	vpp# ip route delete 10.10.1.0/24 via 10.10.11.1
	vpp# ip route delete 10.10.1.0/24 via 10.10.19.1

Test connecticity from host:
$ ping 10.10.2.3

Wait for a few seconds on first try for ping to succeed.

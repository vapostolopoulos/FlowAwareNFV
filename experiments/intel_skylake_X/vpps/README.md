Here are the groups of vpps to be launched in the system. They are connected 
like this:

1. vpp1-vpp2-vpp3
2. vpp4-vpp5-vpp6-vpp7-vpp8
3. vpp9-vpp10-vpp11-vpp12-vpp13-vpp14-vpp15

Each group is also connected to vpprouter1 and vpprouter2 for routing and
testing purposes.

You can launch whatever combination you want but each group must be whole. 

IMPORANT: Vpps are preconfigured to be placed in a "ping pong" scenario between
NUMA nodes for testing purposes.

You have to manually launch each vpp e.g. ./vpprouter1.conf, ./vpprouter2.conf,
vpp1.conf, etc. 



TEST CONNECTIVITY T-REX

After launching vpprouter1,2 and the group(s) you want you must add static
routes in vpprouter1 table. This is done for testing purposes and that is why it
is not preconfigured. You have to add these static routes depending on the group
you would like to send traffic through T-REX:

$ sudo vppctl -s /run/vpp/cli-vpprouter1.sock 
 
Add routes to group 1,2,3 respectively:
1. vpp# ip route add 16.0.0.0/8 via 10.10.3.2 [weight n]
2. vpp# ip route add 16.0.0.0/8 via 10.10.6.2 [weight n]
3. vpp# ip route add 16.0.0.0/8 via 10.10.12.2 [weight n]

Delete routes to group1,2,3 respectively:
1. vpp# ip route delete 16.0.0.0/8 via 10.10.3.2 [weight n]
2. vpp# ip route delete 16.0.0.0/8 via 10.10.6.2 [weight n]
3. vpp# ip route delete 16.0.0.0/8 via 10.10.12.2 [weight n]



TEST CONNECTIVITY MANUALLY (PING)

After launching vpprouter1,2 and the group(s) you want you must add static
routes in vpprouter1 and 2 tables. This is done for testing purposes and that is
why it is not preconfigured. You have to add these static routes depending on
the group you would like to ping:

-vpprouter1
$ sudo vppctl -s /run/vpp/cli-vpprouter1.sock 

Add routes to group 1,2,3 respectively:
1. vpp# ip route add 10.10.2.0/24 via 10.10.3.2
2. vpp# ip route add 10.10.2.0/24 via 10.10.6.2
3. vpp# ip route add 10.10.2.0/24 via 10.10.12.2

Delete routes to group1,2,3 respectively:
1. vpp# ip route delete 10.10.2.0/24 via 10.10.3.2
2. vpp# ip route delete 10.10.2.0/24 via 10.10.6.2
3. vpp# ip route delete 10.10.2.0/24 via 10.10.12.2

-vpprouter2
$ sudo vppctl -s /run/vpp/cli-vpprouter2.sock 

Add routes to group 1,2,3 respectively:
1. vpp# ip route add 10.10.1.0/24 via 10.10.2.4
2. vpp# ip route add 10.10.1.0/24 via 10.10.11.1
3. vpp# ip route add 10.10.1.0/24 via 10.10.19.1

Delete routes to group1,2,3 respectively:
1. vpp# ip route delete 10.10.1.0/24 via 10.10.2.4
2. vpp# ip route delete 10.10.1.0/24 via 10.10.11.1
3. vpp# ip route delete 10.10.1.0/24 via 10.10.19.1

Test connecticity from host:
$ ping 10.10.2.3

Wait for a few seconds on first try for ping to succeed.

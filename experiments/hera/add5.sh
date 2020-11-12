#!/bin/bash

#Add static route to 5vpp chain
sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 10.10.2.0/24 via 10.10.6.2
sudo vppctl -s /run/vpp/cli-vpprouter2.sock ip route add 10.10.1.0/24 via 10.10.11.1

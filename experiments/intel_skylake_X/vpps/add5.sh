#!/bin/bash

#Add static route to 5vpp chain
sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.6.2

#!/bin/bash

#Add static route to 7vpp chain
sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.12.2

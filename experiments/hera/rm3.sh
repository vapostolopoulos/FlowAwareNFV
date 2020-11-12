#!/bin/bash

#Delete static route to 3vpp chain
sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route del 10.10.2.0/24 via 10.10.3.2
sudo vppctl -s /run/vpp/cli-vpprouter2.sock ip route del 10.10.1.0/24 via 10.10.2.4

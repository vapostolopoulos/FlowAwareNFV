#!/bin/bash

#Delete static route to 3vpp chain
sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route del 48.0.0.0/8 via 10.10.3.2

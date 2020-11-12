#!/bin/bash

#Delete static route to 5vpp chain
sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route del 48.0.0.0/8 via 10.10.12.2

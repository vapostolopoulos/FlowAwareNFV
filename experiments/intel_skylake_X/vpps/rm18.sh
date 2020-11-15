#!/bin/bash

#Delete static route to vpp18 of diamond
sudo vppctl -s /run/vpp/cli-vpp16.sock ip route del 48.0.0.0/8 via 10.10.22.2

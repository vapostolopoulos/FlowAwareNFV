#A script to pin all vpps to cpu 0

import psutil

for p in psutil.process_iter(['name']):
    if p.info['name'].startswith("vpp"):
        p.cpu_affinity([0])

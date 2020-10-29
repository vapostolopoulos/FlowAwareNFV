import psutil

for p in psutil.process_iter(['name']):
    if p.info['name'].startswith("vpp"):
        p.cpu_affinity([0])

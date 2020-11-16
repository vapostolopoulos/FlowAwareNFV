import random
import os
import time

random.seed(1)
for i in range(10):
    a = random.randrange(0, 101)
    b = random.randrange(0, 101)

    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.3.2 weight {a}")
    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.6.2 weight {b}")
    print(f"VppChain 3 has weight {a}")
    print(f"VppChain 5 has weight {b}")
    time.sleep(10)
    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.3.2 weight {a}")
    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.6.2 weight {b}")

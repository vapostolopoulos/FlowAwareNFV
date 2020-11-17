import random
import os
import time

os.system("../vpps/rm3.sh")
os.system("../vpps/rm5.sh")

random.seed(1)
for i in range(10):
    a = random.randrange(0, 101)
    b = random.randrange(0, 101)
    if i % 2 == 0 and a > b:
        a, b = b, a
    elif i % 2 and b > a:
        a, b = b, a        

    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.3.2 weight {a}")
    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route add 48.0.0.0/8 via 10.10.6.2 weight {b}")
    print(f"Measurement {i+1}")
    print(f"VppChain 3 has weight {a}")
    print(f"VppChain 5 has weight {b}")
    print()
    time.sleep(10)
    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route del 48.0.0.0/8 via 10.10.3.2 weight {a}")
    os.system(f"sudo vppctl -s /run/vpp/cli-vpprouter1.sock ip route del 48.0.0.0/8 via 10.10.6.2 weight {b}")
os.system("../vpps/add3.sh")
os.system("../vpps/add5.sh")

import os
import time

os.system("../vpps/rm3.sh")
os.system("../vpps/rm5.sh")
os.system("../vpps/rm7.sh")


for i in range(10):
    print(f"Measurement {i+1}")

    os.system("../vpps/add3.sh")
    print("Traffic on chain3")
    time.sleep(10)
    os.system("../vpps/rm3.sh")

    os.system("../vpps/add5.sh")
    print("Traffic on chain5")
    time.sleep(10)
    os.system("../vpps/rm5.sh")

    os.system("../vpps/add7.sh")
    print("Traffic on chain7")
    time.sleep(10)
    os.system("../vpps/rm7.sh")


    print()

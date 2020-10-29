#A script to get statistics of vpps

from vpp_papi.vpp_stats import VPPStats
import time
import os

directory = os.fsencode('/run/vpp')
sorted_dir = sorted(os.listdir(directory))

while (1):
    for file in sorted_dir:
        filename = os.fsdecode(file)
        if filename.startswith("stats-vpp"):
            stats = VPPStats('/run/vpp/' + filename)
            dir = stats.ls('^/if')

            counters = stats.dump(dir)
    
            print('{}'.format(filename))
            j = 0
            for i in counters['/if/names'] :
                if i.startswith("local"):
                    j += 1
                    continue
                print('{} RX: {}'.format(i, counters['/if/rx'][0][j]))
                str1 = ('TX: {}'.format(counters['/if/tx'][0][j]))
                print(' ' * len(i) + ' ' + str1)
                j += 1

            stats.disconnect()
    
            print()
#        else:
#            continue
    print("------------------------------------------------------------------------------------------------------------")
    print()
    time.sleep(5)

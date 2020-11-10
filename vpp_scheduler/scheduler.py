import psutil
from vpp_papi.vpp_stats import VPPStats
from copy import deepcopy
import time


# Which NUMA node is a network interface close to?
# $ lspci | grep -i eth   # find device
# $ lspci -v -s 18:00.0 | grep NUMA  # give device pci address
#
# cpu_info = [[#cpu, #numa, unavailable], [#cpu, #numa, unavailable], etc]
# $ lscpu -e=cpu, node
#

# hera
# Hyperthreaded unwanted, thus on global_cpu_info we mark every second row with unavailibality
global_cpu_info = [
                    [0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 0],
                    [4, 0, 0], [5, 0, 0], [6, 0, 0], [7, 0, 0],

                    [8, 1, 0], [9, 1, 0], [10, 1, 0], [11, 1, 0],
                    [12, 1, 0], [13, 1, 0], [14, 1, 0], [15, 1, 0],

                    [16, 2, 0], [17, 2, 0], [18, 2, 0], [19, 2, 0],
                    [20, 2, 0], [21, 2, 0], [22, 2, 0], [23, 2, 0],

                    [24, 3, 0], [25, 3, 0], [26, 3, 0], [27, 3, 0],
                    [28, 3, 0], [29, 3, 0], [30, 3, 0], [31, 3, 0]
                ]

numa_node_latencies = [
                        [0, 1, 2, 3],
                        [1, 0, 2, 3],
                        [2, 0, 1, 3],
                        [3, 0, 1, 2]
                    ]

numa_node_close_to_card = 0

'''
# intel skylake
# Hyperthreaded unwanted, thus on global_cpu_info we don't include siblings 48-71 of 0-23 and 72-95 of 24-47
global_cpu_info = [
                    [0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 0],
                    [4, 0, 0], [5, 0, 0], [6, 0, 0], [7, 0, 0],
                    [8, 0, 0], [9, 0, 0], [10, 0, 0], [11, 0, 0],
                    [12, 0, 0], [13, 0, 0], [14, 0, 0], [15, 0, 0],
                    [16, 0, 0], [17, 0, 0], [18, 0, 0], [19, 0, 0],
                    [20, 0, 0], [21, 0, 0], [22, 0, 0], [23, 0, 0],
                                                      
                    [24, 1, 0], [25, 1, 0], [26, 1, 0], [27, 1, 0],
                    [28, 1, 0], [29, 1, 0], [30, 1, 0], [31, 1, 0],
                    [32, 1, 0], [33, 1, 0], [34, 1, 0], [35, 1, 0],
                    [36, 1, 0], [37, 1, 0], [38, 1, 0], [39, 1, 0],
                    [40, 1, 0], [41, 1, 0], [42, 1, 0], [43, 1, 0],
                    [44, 1, 0], [45, 1, 0], [46, 1, 0], [47, 1, 0]
                ]

numa_node_latencies = [
                        [0, 1],
                        [1, 0]
                    ]

numa_node_close_to_card = 0
'''

s = set()
for cpu in global_cpu_info:
    s.add(cpu[1])
global_count_numa_cpus = [0] * len(s)
for cpu in global_cpu_info:
    if cpu[2] == 0:
        global_count_numa_cpus[cpu[1]] += 1

cpu_info = deepcopy(global_cpu_info)
count_numa_cpus = deepcopy(global_count_numa_cpus)
old_vppDict = {}

farest_numa_node_from_card = numa_node_latencies[numa_node_close_to_card][-1]
farest_cpu = -1
for cpu in global_cpu_info:
    if cpu[1] == farest_numa_node_from_card and cpu[2] == 0:
        farest_cpu = cpu[0]

################################################################################

# Input parsing into list of lists
print('''Provide the VPPs you would like to schedule into a list of lists according to their interconnection.
        e.g. '[[vpp1, vpp2, vpp3], [vpp1, vpp4, vpp3], [vpp5, vpp6, vpp7]]':\n''')

inputlist = []
strs = input().replace(' ', '').replace('[', '').replace('],', ' ').replace(']', ' ').split()
for i in strs:
    x = i.split(',')
    inputlist.append([j for j in x])

for vppgroup in inputlist:
    for vpp in vppgroup:
        old_vppDict[vpp] = {'packets': 0, 'scheduled': -1}

################################################################################

# Create dictionary with 'pid', 'packets', 'scheduled' for each VPP
while 1:

    vppDict = {}

    for vppgroup in inputlist:
        for vpp in vppgroup:
            if vpp in vppDict:
                vppDict[vpp]['groups'].append(vppgroup)
            else:
                vppDict[vpp] = {'pid': -1, 'packets': 0, 'groups': [vppgroup], 'scheduled': -1}

    for vpp in vppDict:
        with open('/run/vpp/' + vpp + '.pid', 'r') as pidfile:
            for number in pidfile:
                pid = int(number)

        stats = VPPStats('/run/vpp/stats-' + vpp + '.sock')
        dir1 = stats.ls('^/if')
        counters = stats.dump(dir1)
        packets = 0
        for i in counters['/if/tx'][0]:
            packets += i['packets']
        stats.disconnect()

        new_packets = packets - old_vppDict[vpp]['packets']
        vppDict[vpp]['pid'], vppDict[vpp]['packets'] = pid, new_packets

################################################################################

    # Create the list based on which the scheduling will be performed

    vppgroupDict = {}
    for vppgroup in inputlist:
        key = str(vppgroup)
        packets = 0
        length = len(vppgroup)
        for vpp in vppgroup:
            packets += vppDict[vpp]['packets']
        vppgroupDict[key] = {'packets': packets / length, 'numa_to_pin': -1, 'length': length}


    sortedList = [x[0] for x in sorted(vppgroupDict.items(), key=lambda item: (item[1]['packets'], item[1]['length']), reverse=True)]

################################################################################

    # Scheduling Algorithm
    print_flag = False
    for vppgroup_str in sortedList:
        vppgroup_to_schedule = 0
        for vppgroup in inputlist:
            if str(vppgroup) == vppgroup_str:
                vppgroup_to_schedule = vppgroup
                break

        if vppgroup_to_schedule:
            vppgroup_length = len(vppgroup_to_schedule)
            for vpp_to_schedule in vppgroup_to_schedule:
                if vppDict[vpp_to_schedule]['scheduled'] != -1:
                    vppgroup_length -= 1

            if vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin'] == -1:
                numa_node_latency = numa_node_latencies[numa_node_close_to_card]
            else:
                numa_node_latency = numa_node_latencies[vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin']]
            flag = False
            for numa_to_pin in numa_node_latency:
                if vppgroup_length <= count_numa_cpus[numa_to_pin]:
                    vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin'] = numa_to_pin
                    flag = True
                    break
                else:
                    vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin'] = -1

            for vpp_to_schedule in vppgroup_to_schedule:
                if vppDict[vpp_to_schedule]['packets'] == 0:
                    vppDict[vpp_to_schedule]['scheduled'] = farest_cpu
                    # Actually pin vpp to farest_cpu here
                    if farest_cpu != old_vppDict[vpp_to_schedule]['scheduled']:
                        p = psutil.Process(vppDict[vpp_to_schedule]['pid'])
                        p.cpu_affinity([farest_cpu])
                        print(f"{vpp_to_schedule} scheduled to cpu {farest_cpu}")
                        print_flag = True

                elif vppDict[vpp_to_schedule]['scheduled'] != -1:
                    continue
                else:
                    cpu_to_pin = -1
                    if flag:
                        for cpu in cpu_info:
                            if cpu[1] == vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin'] and cpu[2] == 0:
                                cpu_to_pin = cpu[0]
                                break
                    else:
                        for numa_to_pin in numa_node_latencies[numa_node_close_to_card]:
                            for cpu in cpu_info:
                                if cpu[2] == 0 and cpu[1] == numa_to_pin:
                                    cpu_to_pin = cpu[0]
                                    vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin'] = cpu[1]
                                    break
                            if cpu_to_pin != -1:
                                break

                    if cpu_to_pin != -1:
                        # Actually pin vpp to cpu here
                        if cpu_to_pin != old_vppDict[vpp_to_schedule]['scheduled']:
                            p = psutil.Process(vppDict[vpp_to_schedule]['pid'])
                            p.cpu_affinity([cpu_to_pin])
                            print(f"{vpp_to_schedule} has been scheduled to cpu {cpu_to_pin} numa node "
                                  f"{vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin']}")
                            print_flag = True

                        vppDict[vpp_to_schedule]['scheduled'] = cpu_to_pin
                        cpu_info[vppDict[vpp_to_schedule]['scheduled']][2] = 1
                        count_numa_cpus[vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin']] -= 1

                        if len(vppDict[vpp_to_schedule]['groups']) > 1:
                            for vpp_group in vppDict[vpp_to_schedule]['groups']:
                                if vpp_group != vppgroup_to_schedule:
                                    vppgroupDict[str(vpp_group)]['numa_to_pin'] \
                                        = vppgroupDict[str(vppgroup_to_schedule)]['numa_to_pin']
                    else:
                        print(f"No more CPUs available! {vpp_to_schedule} has been scheduled to cpu {farest_cpu} :(")
                        # Actually pin vpp to cpu 31
                        p = psutil.Process(vppDict[vpp_to_schedule]['pid'])
                        p.cpu_affinity([farest_cpu])
                        print_flag = True

    cpu_info = deepcopy(global_cpu_info)
    count_numa_cpus = deepcopy(global_count_numa_cpus)

    if print_flag:
        print("=========================================================================")

    for vpp in vppDict:
        old_vppDict[vpp]['packets'] += vppDict[vpp]['packets']
        old_vppDict[vpp]['scheduled'] = vppDict[vpp]['scheduled']
    time.sleep(2)

################################################################################

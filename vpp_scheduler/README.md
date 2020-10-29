cleanup.sh: kill all vpp-procs in the system, including sockets, open files etc

get_physical_cpus.py: get number of physical cores in the system

get_stats.py: get statistics of all vpps, excluding vpprouter1 and 2

pin_all_to_cpu_0: pin all vpps to cpu 0

sheduler.py: schedule vpps according to their traffic excluding vpprouter1 and 2.
Before running the scheduler you should update variables "global_cpu_info", 
"numa_node_latencies" and "numa_node_close_to_card" in source code according to
your system. For more information about this check beginning of "scheduler.py".

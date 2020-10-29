from cpu_cores import CPUCoresCounter
import os

# We build an instance for the current operating system
instance = CPUCoresCounter.factory()

# Get the number of total real cpu cores
print('physical cpus: {}'.format(instance.get_physical_cores_count()))
print('logical cpus: {}'.format(os.cpu_count()))

# Get the number of total physical processors
print('processors: {}'.format(instance.get_physical_processors_count()))

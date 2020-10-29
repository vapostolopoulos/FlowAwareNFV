After starting trex server:

1. cd /your/path/to/trex/vX.XX/ 
2. ./trex-console, in order to connect to TRex console
3. start -f stl/traffic_generator.py -m 6000mbps --port 0, in order to start 
   traffic generator (try values of -m argument in order to reach the highest applicable rate)
4. if the packets sent and received aren't almost equal try to give more cores to the process of trex-vm on host
5. cd /your/path/to/trex-cli/, the folder where you stored the attached files   
6. export PYTHONPATH=/your/path/to/trex/vX.XX/automation/trex_control_plane/interactive/trex/:$PYTHONPATH 
7. export PYTHONPATH=/your/path/to/trex/vX.XX/automation/trex_control_plane/interactive/trex/examples/stl:$PYTHONPATH
8. python ./trex_stats_collector.py, in order to connect to TRex server and collect the statistics 

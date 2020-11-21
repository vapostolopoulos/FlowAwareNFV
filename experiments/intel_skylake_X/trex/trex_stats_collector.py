import stl_path
from trex.stl.api import *


import os
import time


def trex_stats (c, tx_port, rx_port):
    """ Retrieves trex stats from active pgid and stores them in a tmp.json file
        Args:
            c :  TRex stateless client
            tx_port (int): transmission port
            rx_port (int): receiving port

        Returns:
            status (bool): True for success
    """
    c.clear_stats()

    pgids = c.get_active_pgids()
    print ("Currently used pgids: {0}".format(pgids))
    pgid = pgids['latency'][0]

    time.sleep(1)
    c.wait_on_traffic(ports = [rx_port])

    full_stats = c.get_stats()
    tx_port_stats = full_stats.get(tx_port)
    rx_port_stats = full_stats.get(rx_port)

    pgid_stats = c.get_pgid_stats(pgids['latency'])
    global_lat_stats = pgid_stats['latency']
    lat_stats = global_lat_stats.get(pgid)

    lat = lat_stats['latency']
    jitter = lat['jitter']
    avg = lat['average']
    tot_max = lat['total_max']
    tot_min = lat['total_min']
    last_max = lat['last_max']  # last 0.5 sec window maximum latency (usec)
    hist = lat ['histogram']
    drop_rate_bps = full_stats.get('global')['rx_drop_bps']

    if c.get_warnings():
        print("\n\n*** Retrieving stats had warnings ****\n\n")
        for w in c.get_warnings():
            print(w)
        return False

    try:
        f = open("tmp.json", 'w')

        stats_dict = {"jitter-us":jitter, "average-latency-us":avg, "total-max-us": tot_max, "total-min-us": tot_min, "last-max-us": last_max, "drop-rate-bps":drop_rate_bps}

        tx_port_dict = {"rx_bps_L2_port_" + str(tx_port): tx_port_stats['rx_bps'], "rx_bps_L1_port_" + str(tx_port): tx_port_stats['rx_bps_L1'], "rx_pps_port_" + str(tx_port): tx_port_stats['rx_pps'], "tx_bps_L2_port_" + str(tx_port): tx_port_stats['tx_bps'], "tx_bps_L1_port_" + str(tx_port): tx_port_stats['tx_bps_L1'], "tx_pps_port_" + str(tx_port): tx_port_stats['tx_pps']}

        rx_port_dict = {"rx_bps_L2_port_" + str(rx_port): rx_port_stats['rx_bps'], "rx_bps_L1_port_" + str(rx_port): rx_port_stats['rx_bps_L1'], "rx_pps_port_" + str(rx_port): rx_port_stats['rx_pps'], "tx_bps_L2_port_" + str(rx_port): rx_port_stats['tx_bps'], "tx_bps_L1_port_" + str(rx_port): rx_port_stats['tx_bps_L1'], "tx_pps_port_" + str(rx_port): rx_port_stats['tx_pps']}

        f.write("tx_stats:>" + str(tx_port_dict) + "\n")
        f.write("rx_stats:>" + str(rx_port_dict) + "\n")
        f.write("global_stats:>" + str(stats_dict) + "\n")
        f.write("histogram_json:>" + str(fix_hist_format(hist)) + "\n")
        print("Average: {}".format(avg)) 
        os.system("echo {} >> lat.txt".format(avg))

        return True
    finally:
        f.close()
    

def fix_hist_format(hist):
    """ Changes the format of histogram 
        Args:
            hist (dict): a dictionary of histogram

        Returns:
            fixed_hist (dict): the dictionary of histogram with fixed format
    """

    list_dict = []
    l = hist.keys()
    l=sorted(l)
    i = 0
    range_end_previous = 0

    for sample in l:
        range_start = sample

        if i != 0:
            if range_start != range_end_previous:
                while range_start != range_end_previous:
                    new_range_start = range_end_previous
                    if new_range_start == 0:
                        range_end = 10
                    else:
                        range_end  = new_range_start + pow(10, (len(str(new_range_start))-1))

                    val = 0 
                    print ("    Packets with latency between {0} and {1}:{2} ".format(new_range_start, range_end, val))
                    list_dict.insert(len(list_dict), {"value":range_end,"count":val})
                    range_end_previous = range_end
                

        if range_start == 0:
            range_end = 10
        else:
            range_end  = range_start + pow(10, (len(str(range_start))-1))

        val = hist[sample]
        print ("    Packets with latency between {0} and {1}:{2} ".format(range_start, range_end, val))

        if val < 0:
            val = 0
        list_dict.insert(len(list_dict), {"value":range_end,"count":val})
        range_end_previous = range_end
        i += 1

    fixed_hist = {"histogram":list_dict}
    return fixed_hist


def collect_trex_stats():
    """ Connects to trex server and retrieve stats for active stream
        Args:
            -
        Returns:
            -
    """
    try:
        c = STLClient(verbose_level = 'error')

        c.connect()
        c.reset(ports = [1])

        print((" is connected? : {0}".format(c.is_connected())))
        print((" number of ports {0}".format(c.get_port_count())))
        print((" acquired_ports {0}".format(c.get_acquired_ports())))

        while True:
            check = trex_stats(c, 0, 1)
            if check:
                os.rename("tmp.json", 'trex_stats.json')

    except STLError as e:
        print(e)

    finally:
        c.disconnect()

def main():
    collect_trex_stats()

if __name__ == '__main__':
    main()

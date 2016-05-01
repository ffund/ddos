#!/usr/bin/python

"""Script to capture packets and calculate per-source bandwidth."""

import sys
import argparse
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

import numpy as np
import matplotlib.pyplot as plt

names = {"10.10.1.1": "Client",
        "10.10.2.1": "Attacker 1",
        "10.10.3.1": "Attacker 2",
        "10.10.4.1": "Attacker 3",
        "10.10.5.1": "Attacker 4",
        "10.10.6.1": "Attacker 5",
        "10.10.7.1": "Attacker 6",
        "10.10.8.1": "Attacker 7",
        "10.10.9.1": "Attacker 8",
        "10.10.10.1": "Attacker 9",
        "10.10.11.1": "Attacker 10",
        "10.10.12.1": "Attacker 11",
        "10.10.13.1": "Attacker 12",
        "Total": "Total Bandwidth"
    }

def main(interface, show, duration, bins, output):
    """Sniffs packets on the given interface for given duration and calculates per-source bandwidth"""
    try:
        capture = sniff(iface=interface, filter='udp and port 8999', timeout=duration)
    except Exception as err:
        return str(err)
    if not capture:
        return "Capture Error: Filter did not capture any packets, did you use the correct interface?"

    t0 = capture[0].time
    binCount = 1 + duration*1000/bins
    
    sources = {'Total': [0]*binCount}

    for p in capture:
        print p.summary()
        if p[IP].src not in sources:
            sources[p[IP].src] = [0]*binCount
        sources[p[IP].src][int(1000*(p.time-t0)/bins)] += 8*p[IP].len/1000.0
        sources['Total'][int(1000*(p.time-t0)/bins)] += 8*p[IP].len/1000.0

    x = [i*bins/1000.0 for i in range(binCount)]
    for src in sources:
        plt.plot(x, [i/bins for i in sources[src]], label=names[src])

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.ylim(0, 1.05)
    plt.xlabel('Time')
    plt.xlabel('Bandwidth')
    plt.yticks(np.arange(0, 1.05, 0.05))
    plt.grid()
    plt.savefig(output+'.png', dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=True, bbox_inches='tight', pad_inches=0.3,
                    frameon=None)

    plt.clf()

    for src in ["10.10.1.1"]:
        plt.plot(x, [i/bins for i in sources[src]], label=names[src])

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.ylim(0, 0.12)
    plt.xlabel('Time')
    plt.xlabel('Bandwidth')
    plt.yticks(np.arange(0, 0.12, 0.01))
    plt.grid()
    plt.savefig(output+'_client.png', dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=True, bbox_inches='tight', pad_inches=0.3,
                    frameon=None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("interface",
            help="Specify the interface that connects the router to the server",
            type=str)
    parser.add_argument("--show",
            help="Shows matplotlib output when used", action='store_true')
    parser.add_argument("--bins",
            help="Bin length in milli seconds", type=int, default=80)
    parser.add_argument("--output",
            help="Output file name", type=str)
    parser.add_argument("duration",
            help="Specify the duration of capture", type=int)
    args = parser.parse_args()

    sys.exit(main(args.interface, args.show, args.duration, args.bins, args.output))

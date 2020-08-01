#!/usr/bin/env python3

from sys import argv
from Interface import Interface
from Capture import Capture
import signal
from scapy.all import *

"""
Global variables
"""
interface = None
capture = None

"""
Detect CTRL+C to save progress
"""
def sigintHandler(sig, frame):
    global interface
    global capture
    if capture.fileName != None:
        print("\r[-] Saving before exit ...")
        capture.save()
        print("[+] Captured probes saved")
    interface.stopChannelHopper()
    interface.disableMonitor()
    print("\rBye ...")
    exit(0)

"""
Grab information from wireless package
"""
def probeParser(pkt):
    global capture
    # Check if it is a 802.11 package
    if pkt.haslayer(Dot11):
        # Check it is a management frame
        if pkt.type == 0:
            # Check it is a probe request
            if pkt.subtype == 4:
                # Check that the SSID is not empty (Discard broadcast)
                if pkt.info:
                    capture.addConnection(pkt.addr2, pkt.info.decode('utf-8'))

"""
Show banner
"""
def banner():
    msg = """
██████╗ ██████╗  ██████╗ ██████╗ ███████╗    ██████╗  █████╗ ██████╗  █████╗ ██████╗     ██╗   ██╗ ██╗
██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗    ██║   ██║███║
██████╔╝██████╔╝██║   ██║██████╔╝█████╗      ██████╔╝███████║██║  ██║███████║██████╔╝    ██║   ██║╚██║
██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝      ██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗    ╚██╗ ██╔╝ ██║
██║     ██║  ██║╚██████╔╝██████╔╝███████╗    ██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║     ╚████╔╝  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝      ╚═══╝   ╚═╝
                                                                                                      """
    print(msg)

"""
Entry point
"""
def main(parser):
    global interface
    global capture
    banner()
    argc = len(argv)
    if argc == 2 or argc == 3:
        interface = Interface(argv[1])
        capture = Capture(fileName=(argv[2] if argc == 3 else None))
        signal.signal(signal.SIGINT, sigintHandler)
        interface.enableMonitor()
        interface.startChannelHopper()
        print("[+] Sniffing probe requests")
        sniff(iface=interface.name, prn=parser)
    else:
        print("Usage: ./probes.py <MONITOR_INTERFACE> [OUTPUT_FILE]")

if __name__ == "__main__":
    main(probeParser)

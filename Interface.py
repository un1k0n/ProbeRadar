from os import system
from time import sleep
import threading

class Interface:
    def __init__(self, interface):
        self.name = interface
        self.hopperRunning = False
        self.hopperThread = None
    def enableMonitor(self):
        system("ifconfig {0} down && iwconfig {0} mode monitor && ifconfig {0} up".format(self.name))
        print("[+] Enabled monitor mode")
    def disableMonitor(self):
        system("ifconfig {0} down && iwconfig {0} mode managed && ifconfig {0} up".format(self.name))
        print("[+] Disabled monitor mode")
    def startChannelHopper(self):
        def channelHopper():
            while self.hopperRunning:
                for channel in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                    sleep(1)
                    system("iw dev {0} set channel {1}".format(self.name, channel))
        self.hopperThread = threading.Thread(target=channelHopper)
        self.hopperRunning = True
        self.hopperThread.start()
        print("[+] Started channel hopper thread")
    def stopChannelHopper(self):
        if self.hopperThread != None:
            self.hopperRunning = False
            print("\r[-] Stopping channel hopper thread ...")
            self.hopperThread.join()
            print("[+] Stopped channel hopper thread")


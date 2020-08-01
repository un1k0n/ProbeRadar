from os import system
from Mac import Mac
from json import dumps

class Capture:
    def __init__(self, fileName=None):
        self.captures = {}
        self.fileName = fileName
        self.mac = Mac()
    def showNetworks(self):
        system("clear")
        print("*-{0}-*-{1}-*-{2}-*".format("-"*20, "-"*17, "-"*70))
        print("| {0} | {1} | {2} |".format("        SSID        ", "       MAC       ", "                                Vendor                                "))
        print("|-{0}-|-{1}-|-{2}-|".format("-"*20, "-"*17, "-"*70))
        for ssid, devices in self.captures.items():
            print("| {0} | {1} | {2} |".format(ssid.ljust(20), devices[0], self.mac.getVendor(devices[0]).ljust(70)))
            for i in range(1,len(devices)):
                print("| {0} | {1} | {2} |".format(" "*20, devices[i], self.mac.getVendor(devices[0]).ljust(70)))
            print("*-{0}-*-{1}-*-{2}-*".format("-"*20, "-"*17, "-"*70))
    def addConnection(self, mac, ssid):
        if ssid not in self.captures:
            self.captures[ssid] = []
        if mac not in self.captures[ssid]:
            self.captures[ssid].append(mac)
        self.showNetworks()
    def save(self):
        with open(self.fileName, "w") as f:
            f.write(dumps(self.captures, indent=4, sort_keys=True))

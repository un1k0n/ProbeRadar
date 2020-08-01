from json import loads

class Mac:
    def __init__(self):
        with open("vendors.json") as f:
            self.vendors = loads(f.read())
    def getVendor(self, mac):
        macInit = mac[0:8].replace(":", "").upper()
        if macInit in self.vendors:
            return self.vendors[macInit]
        else:
            return ""

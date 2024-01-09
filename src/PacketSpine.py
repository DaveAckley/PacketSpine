import SerLoop

import sys

class PacketSpine:
    def __init__(self,name,configfile):
        self.name = name
        self.sl = SerLoop.SerLoop('/dev/ttyUSB0',configfile)

    def update(self):
        while True:
            count = self.sl.update()
            if count > 0:
                break
        

def main():
    if len(sys.argv) != 2:
        raise ValueError("Need exactly one argument (config file path)");
    configfile = sys.argv[1]
    ps = PacketSpine("PSPN",configfile)
    print(ps)
    ps.update()

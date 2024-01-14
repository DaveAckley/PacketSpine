import random

import SerLoop
import Utils

import sys

class PacketSpine:
    def __init__(self,mrs,name):
        self.mrs = mrs
        self.name = name
        self.sl = SerLoop.SerLoop('/dev/ttyUSB0')

        self.nonce = random.randint(1,254)
        self.loopLen = 0    # assume nobody's out there at first
        self.flagSPacketSeen() # assume the loop's good to start

    def flagSPacketSeen(self):
        self.sawSPacket = True 
        
    def sendSPacket(self,hops,dest):
        packetFormat = b'%cW%c%cS0'
        packet = packetFormat % (Utils.intToSignedByte(hops),
                                 Utils.intToSignedByte(dest),
                                 self.nonce)
        self.sendPacket(packet)
        
    def initSM(self): # Buffer up all outbound S packets for a simulation step
        if not self.sawSPacket:
            self.loopLen += 1
            print("LOOPLEN NOW",self.loopLen)
        self.sawSPacket = False

        if self.nonce >= 255:
            self.nonce = 1
        else:
            self.nonce += 1
        print("INNONC",self.nonce)
        # First send a packet that should come back unhandled
        self.sendSPacket(self.loopLen,self.loopLen)

        # Then send loopLen 'real' packets
        for i in range(self.loopLen):
            hops = self.loopLen - i - 1
            dest = hops
            self.sendSPacket(hops,dest)

    def registerPacketProcessor(self,pproc):
        return self.sl.registerPacketProcessor(pproc)

    def update(self):
        return self.sl.update()

    def sendPacket(self,packet):
        return self.sl.sendPacket(packet)

def main():
    if len(sys.argv) != 2:
        print("(Wanted exactly one argument (config file path))");
    else:
        configfile = sys.argv[1]
    ps = PacketSpine("PSPN")
    print(ps)
    while True:
        count = ps.update()
        if count > 0:
            break

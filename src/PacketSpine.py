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
        self.flagIPacketSeen() # assume the loop's good to start
        self.flagOPacketSeen() # assume the loop's good to start

    def resetStats(self):
        self.sl.resetStats()

    def getStats(self):
        return self.sl.getStats()

    def getBufferSizes(self):
        return self.sl.getBufferSizes()

    def flagIPacketSeen(self):
        self.sawIPacket = True 

    def flagOPacketSeen(self):
        self.sawOPacket = True 
        
    def sendBroadcastPacket(self,payload = b''):
        packetFormat = b'%c%b'
        packet = packetFormat % (0x7e, payload)
        print("BCPACKET",packet)
        self.sendPacket(packet)

    def sendIPacket(self,hops,dest,payload = b''):
        packetFormat = b'%cW%c%cI%b'
        packet = packetFormat % (Utils.intToSignedByte(hops),
                                 Utils.intToSignedByte(dest),
                                 self.nonce,
                                 payload)
        #print("sendIPpacketGOGO",packet)
        self.sendPacket(packet)
        
    def initSM(self): # Buffer up all outbound S packets for a simulation step
        #if not self.sawIPacket and self.sawOPacket:
        #    self.updateLoopLengthIfNeeded(self.loopLen + 1)
        self.sawIPacket = False
        self.sawOPacket = False

        wr = self.mrs

        if self.nonce >= 255:
            self.nonce = 1
        else:
            self.nonce += 1
        print("INNONC",self.nonce)
        # First send a no-payload packet that should come back unhandled
        self.sendIPacket(self.loopLen,self.loopLen) 

        # Then send loopLen 'real' packets
        for i in range(self.loopLen):
            hops = self.loopLen - i - 1
            dest = hops
            payload = wr.GetPayloadForTile(dest)
            self.sendIPacket(hops,dest,payload)
            #print("PACSPI",payload)

    def updateLoopLengthIfNeeded(self,length):
        if length != self.loopLen:
            print("LOOPLENGTH UPDATE:",self.loopLen,"->",length)
            self.loopLen = length

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

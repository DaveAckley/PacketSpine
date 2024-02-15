import re
import PacketIO
import PacketDispatcher

class SerLoop:
    def __init__(self,serdev):
        self.pio = PacketIO.PacketIO(serdev)
        self.tiles = []

        self.dispatcher = PacketDispatcher.PacketDispatcher()
        self.resetStats()

    def resetStats(self):
        self.pio.resetStats()

    def getStats(self):
        return self.pio.getStats()

    def getBufferSizes(self):
        return self.pio.getBufferSizes()

    def registerPacketProcessor(self,pproc):
        return self.dispatcher.registerPacketProcessor(pproc)

    def loadConfig(self):
        idx = 0
        with open(self.configFile) as file:
            for line in file:
                if re.match('\s*#',line):
                    continue
                line = line.rstrip()
                args = line.split(maxsplit=2)
                if len(args) < 2:
                    raise ValueError(f"Bad config file {self.configFile} line: {line}");
                (xpos, ypos, *rest) = args
                self.tiles.append((idx,xpos,ypos,rest))
                idx += 1
        print(idx,"entries in config file",self.configFile)
        tileCount = len(self.tiles)
        print(tileCount, "CONFIG\n","\n ".join([ str(x) for x in self.tiles]))

    def sendPacket(self,packet):
        self.pio.writePacket(packet)
        
    def update(self):
        self.pio.update()
        count = 0
        while True:
            inpacket = self.pio.pendingPacket()
            if inpacket == None:
                break
            self.dispatcher.tryHandle(inpacket)
            #print("WHANDLED",inpacket)
            count = count + 1
        return count

    def close(self):
        self.pio.close()
        

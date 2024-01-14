class PacketDispatcher:
    def __init__(self):
        self.processors = []
        self.processorMap = {}   # proc -> idx

    def registerPacketProcessor(self,pproc):
        idx = self.processorMap.get(pproc)
        if idx != None:
            print("WARNING: REREG",pproc,idx)
        idx = len(self.processors)
        self.processors.append(pproc)
        self.processorMap[pproc] = idx
        print("REGPPROC",self.processorMap)

    def tryHandle(self,packet):
        for pproc in self.processors:
            match = pproc.matches(packet)
            if match != None:
                return pproc.handle(packet,match)
        print("ENOMETH",packet)



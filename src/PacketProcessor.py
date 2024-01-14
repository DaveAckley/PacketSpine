from abc import ABC, abstractmethod

class PacketProcessor(ABC):

    def __init__(self,mrs,name):
        self.mrs = mrs
        self.name = name

    @abstractmethod
    def matches(self,packet):
        return None

    @abstractmethod
    def handle(self,packet,match):
        pass

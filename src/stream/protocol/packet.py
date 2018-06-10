from enum import Enum


class Packet:

    def send(self, cefstream, socket):
        pass

    def receive(self, cefstream, socket):
        pass

    @staticmethod
    def get_bound(self):
        pass

    @staticmethod
    def get_packet_id(self):
        pass


class Bound(Enum):

    SERVER_BOUND = 0x01
    CLIENT_BOUND = 0x02


class ServerboundPacket(Packet):

    @staticmethod
    def get_bound(self):
        return Bound.SERVER_BOUND


class ClientboundPacket(Packet):

    @staticmethod
    def get_bound(self):
        return Bound.CLIENT_BOUND

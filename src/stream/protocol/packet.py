from enum import Enum

from overrides import overrides


class Packet:

    def send(self, cefstream, socket):
        pass

    def receive(self, cefstream, socket):
        pass

    @staticmethod
    def get_bound():
        pass

    @staticmethod
    def get_packet_id():
        pass


class Bound(Enum):

    SERVER_BOUND = 0x01
    CLIENT_BOUND = 0x02


class ServerboundPacket(Packet):

    @staticmethod
    @overrides
    def get_bound():
        return Bound.SERVER_BOUND


class ClientboundPacket(Packet):

    @staticmethod
    @overrides
    def get_bound():
        return Bound.CLIENT_BOUND

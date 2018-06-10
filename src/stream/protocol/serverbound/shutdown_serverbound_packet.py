from overrides import overrides

from src.stream.protocol.packet import ServerboundPacket
from src.stream.protocol.packets import Packets


class ShutdownServerboundPacket(ServerboundPacket):

    @overrides
    def receive(self, cefstream, socket):
        pass

    @staticmethod
    @overrides
    def get_packet_id():
        return Packets.SHUTDOWN_SERVERBOUND_PACKET

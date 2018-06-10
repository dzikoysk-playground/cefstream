from src.stream.protocol.packet import ServerboundPacket
from src.stream.protocol.packets import Packets


class ShutdownServerboundPacket(ServerboundPacket):

    def receive(self, cefstream, socket):
        pass

    @staticmethod
    def get_packet_id(self):
        return Packets.SHUTDOWN_SERVERBOUND_PACKET

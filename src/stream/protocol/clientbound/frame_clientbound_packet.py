from struct import pack
from overrides import overrides

from src.stream.protocol.packet import ClientboundPacket
from src.stream.protocol.packets import Packets


class FrameClientboundPacket(ClientboundPacket):

    def __init__(self, buffer_string):
        self.buffer_string = buffer_string

    @overrides
    def send(self, cefstream, socket):
        socket.send(pack('!I', len(self.buffer_string)))
        socket.send(self.buffer_string)

    @staticmethod
    @overrides
    def get_packet_id():
        return Packets.FRAME_CLIENTBOUND_PACKET

from struct import pack
from overrides import overrides

from src.stream.protocol.packet import ClientboundPacket
from src.stream.protocol.packets import Packets


class FrameClientboundPacket(ClientboundPacket):

    def __init__(self, buffer_string):
        self.buffer_string = buffer_string

    @overrides
    def send(self, cefstream, server, client):
        response = pack('!I', self.get_packet_id().value)
        response += pack('!I', len(self.buffer_string))
        response += self.buffer_string
        server.sendto(response, client)

    @staticmethod
    @overrides
    def get_packet_id():
        return Packets.FRAME_CLIENTBOUND_PACKET

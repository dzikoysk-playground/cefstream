from src.stream.protocol.packet import ClientboundPacket
from src.stream.protocol.packets import Packets


class FrameClientboundPacket(ClientboundPacket):

    def __init__(self, frame):
        self.frame = frame

    def send(self, cefstream, socket):
        socket.send(len(self.frame))
        socket.send(self.frame)
        pass

    @staticmethod
    def get_packet_id(self):
        return Packets.FRAME_CLIENTBOUND_PACKET

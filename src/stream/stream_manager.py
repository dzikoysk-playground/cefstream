from socket import *


class StreamManager:

    def __init__(self, cefstream):
        self.cefstream = cefstream
        self.socket = None

    def launch(self):
        port = self.cefstream.get_port()
        self.cefstream.get_logger().info('Streaming Socket *::{port}'.format(port=port))

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', port))

    def listen(self):
        packets = vars()['ServerboundPacket'].__subclasses__()

        while True:
            packet_id = self.socket.recvfrom(1)
            received_packet_class = None

            for packet in packets:
                if packet.get_packet_id() in packet_id:
                    received_packet_class = packet
                    break

            if received_packet_class in None:
                self.cefstream.get_logger().warn("Unknown packet " + packet_id)
                continue

            packet = received_packet_class()
            packet.receive(self.cefstream, self.socket)

            self.cefstream.get_logger().info("Message: " + packet_id)

    def send(self, packet):
        packet.send(self)
        return True

    def shutdown(self):
        self.socket.close()

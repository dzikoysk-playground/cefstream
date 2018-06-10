from socket import *
from struct import pack
from threading import Thread

from src.stream.protocol.packet import ServerboundPacket


class StreamManager:

    def __init__(self, cefstream):
        self.cefstream = cefstream
        self.server = None
        self.client = None
        self.packets = []

    def launch(self):
        port = self.cefstream.get_port()
        self.cefstream.get_logger().info('Streaming Socket *::{port}'.format(port=port))

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_SNDBUF, 1024 * 1024 * 8)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        self.listen()

    def listen(self):
        client, address = self.server.accept()
        self.cefstream.get_logger().info('Connection: {address}'.format(address=str(address)))

        client_thread = Thread(target=self.listen_client, args=(self, client, address), name='ClientThread::{address}'.format(address=str(address)))
        client_thread.start()

        self.client = client
        self.cefstream.get_logger().info('Listening for packets')

        while True:
            if len(self.packets) == 0:
                continue

            self.cefstream.get_logger().info('Packets: {size}'.format(size=len(self.packets)))

            for packet in self.packets:
                client.send(pack('!i', packet.get_packet_id().value))
                packet.send(self.cefstream, client)

            self.packets.clear()

    def listen_client(self, stream_manager, client, address):
        packets = ServerboundPacket.__subclasses__()

        while True:
            packet_id = client.recvfrom(1)
            received_packet_class = None

            for packet in packets:
                if packet.get_packet_id() in packet_id:
                    received_packet_class = packet
                    break

            if received_packet_class in None:
                self.cefstream.get_logger().warn("Unknown packet " + packet_id)
                continue

            packet = received_packet_class()
            packet.receive(self.cefstream, self.server)

            self.cefstream.get_logger().info("Message: " + packet_id)

    def send(self, packet):
        if self.client is None:
            return

        self.packets.append(packet)

    def shutdown(self):
        self.server.close()

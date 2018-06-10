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

        self.server = socket(AF_INET, SOCK_DGRAM)
        self.server.bind(('127.0.0.1', port))
        self.listen()

    def listen(self):
        data, address = self.server.recvfrom(1024)
        self.cefstream.get_logger().info('Connection: {address}'.format(address=str(address)))

        client_thread = Thread(target=self.listen_client, args=(self, address), name='ClientThread::{address}'.format(address=str(address)))
        client_thread.start()

        self.client = address
        self.cefstream.get_logger().info('Listening for packets')

    def listen_client(self, stream_manager, address):
        packets = ServerboundPacket.__subclasses__()

        while True:
            packet_id = self.server.recvfrom(1)
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

        # packet.send(self.cefstream, self.server, self.client)

    def shutdown(self):
        self.server.close()

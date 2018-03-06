import sys
import getopt
from socket import *


class StreamManager:

    def __init__(self, cefstream):
        self.cefstream = cefstream
        self.socket = None

    def launch(self):
        port = self.get_port()
        self.cefstream.get_logger().info('Streaming Socket *::{port}'.format(port=port))
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', port))

    def listen(self):
        while True:
            message, address = self.socket.recvfrom(1024)
            self.cefstream.get_logger().info("Message: " + message)

    def shutdown(self):
        self.socket.close()

    def get_port(self):
        try:
            opts, args = getopt.getopt(sys.argv, "hg:d:")
        except getopt.GetoptError:
            self.cefstream.get_logger().info('Invalid arguments')
            sys.exit(2)
        for opt, arg in opts:
            if opt in '-p':
                return arg
        self.cefstream.get_logger().info('Using default port number (*::10000)')
        return 10000

import getopt

from socket import *


class StreamManager:

    def __init__(self):
        self.socket = None

    def launch(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', self.get_port()))
        self.socket.listen(5)

    def shutdown(self):
        self.socket.close()

    @staticmethod
    def get_port():
        try:
            opts, args = getopt.getopt(sys.argv, "hg:d:")
        except getopt.GetoptError:
            print('Invalid arguments')
            sys.exit(2)
        for opt, arg in opts:
            if opt in '-p':
                return arg

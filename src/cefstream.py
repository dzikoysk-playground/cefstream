import atexit
import sys
import logging
from threading import Thread
from src.cef.cef_manager import CefManager
from src.stream.stream_manager import StreamManager


class CefStream:

    cefstream_logger = logging.getLogger('cefstream')

    def __init__(self):
        logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(threadName)s] %(message)s', level='INFO')
        self.cef_manager = CefManager(self)
        self.stream_manager = StreamManager(self)

    def launch(self):
        atexit.register(self.shutdown)
        sys.excepthook = self.cef_manager.get_native_cef().ExceptHook

        cef_thread = Thread(target=self.cef_manager.launch, name="CefThread")
        cef_thread.start()

        stream_thread = Thread(target=self.stream_manager.launch, name="StreamThread")
        stream_thread.start()

    def shutdown(self):
        CefStream.get_logger().info("Shutting down")
        self.stream_manager.shutdown()
        self.cef_manager.shutdown()
        sys.exit(0)

    @staticmethod
    def get_logger():
        return CefStream.cefstream_logger


if __name__ == '__main__':
    cef_stream = CefStream()
    cef_stream.launch()

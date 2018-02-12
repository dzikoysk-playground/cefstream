import sys

from threading import Thread
from multiprocessing import Pool

from src.cef.cef_manager import CefManager
from src.stream.stream_manager import StreamManager


class CefStream:

    def __init__(self):
        self.cef_manager = CefManager(self)
        self.stream_manager = StreamManager(self)

    def launch(self):
        sys.excepthook = self.cef_manager.get_native_cef().ExceptHook
        cef_thread = Thread(target=self.cef_manager.launch())
        stream_thread = Thread(target=self.stream_manager.launch())
        cef_thread.start()
        stream_thread.start()

    def shutdown(self):
        self.stream_manager.shutdown()
        self.cef_manager.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    cef_stream = CefStream()
    cef_stream.launch()

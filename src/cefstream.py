import sys

from src.cef.cef_manager import CefManager
from src.stream.stream_manager import StreamManager


class CefStream:

    def __init__(self):
        self.cef_manager = CefManager()
        self.stream_manager = StreamManager()

    def launch(self):
        self.cef_manager.initialize()
        sys.excepthook = self.cef_manager.get_native_cef().ExceptHook


if __name__ == '__main__':
    cef_stream = CefStream()
    cef_stream.launch()

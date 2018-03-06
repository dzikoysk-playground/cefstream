import platform
import threading
from cefpython3 import cefpython as cef
from threading import Thread
from multiprocessing import Pool
from time import sleep


class CefManager:

    def __init__(self, cefstream):
        self.cefstream = cefstream
        self.browsers = dict()
        self.fps_period = 1
        self.running = True

    def launch(self):
        self.check_versions()

        self.cefstream.get_logger().info('Initializing CEF')
        cef.Initialize()
        self.set_fps(60)

        self.create_browser(identifier='dzikoysk.net', url='https://dzikoysk.net/')
        self.message_loop()

    def message_loop(self):
        self.cefstream.get_logger().info("Calling message loop")

        while self.running:
            cef.MessageLoopWork()
            sleep(self.fps_period)

        self.shutdown_cef()

    def shutdown_cef(self):
        self.cefstream.get_logger().info("Shutting down CEF")
        self.shutdown()
        cef.Shutdown()

    def shutdown(self):
        self.running = False

    def create_browser(self, identifier, url):
        cef_browser = CefBrowser(manager=self, identifier=identifier, url=url)
        self.browsers[identifier] = cef_browser
        return cef_browser

    def set_fps(self, fps):
        self.fps_period = 1.0 / float(fps)
        self.cefstream.get_logger().info("FPS period updated to {fps_period} ({fps}fps)".format(fps_period=self.fps_period, fps=fps))

    def get_browser(self, identifier):
        return self.browsers[identifier]

    def check_versions(self):
        self.cefstream.get_logger().info("CEF Python {ver}".format(ver=cef.__version__))
        self.cefstream.get_logger().info("Python {ver} {arch}".format(ver=platform.python_version(), arch=platform.architecture()[0]))
        assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"

    @staticmethod
    def get_native_cef():
        return cef


class CefBrowser:

    def __init__(self, manager, identifier, url):
        self.manager = manager
        self.identifier = identifier
        self.nativeBrowser = cef.CreateBrowserSync(window_title="cefstream - " + identifier, url=url)

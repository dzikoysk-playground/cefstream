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
        self.running = True

    def launch(self):
        self.check_versions()
        cef.Initialize()
        self.create_browser(identifier='dzikoysk.net', url='https://dzikoysk.net/')
        self.keep_alive()

    def keep_alive(self):
        keep_alive_thread = Thread(target=self.message_loop())
        keep_alive_thread.start()

    def message_loop(self):
        while self.running:
            cef.MessageLoopWork()
            sleep(0.017)
        cef.Shutdown()

    def shutdown(self):
        self.running = False

    def create_browser(self, identifier, url):
        cef_browser = CefBrowser(url=url)
        self.browsers[identifier] = cef_browser
        return cef_browser

    def get_browser(self, identifier):
        return self.browsers[identifier]

    @staticmethod
    def check_versions():
        print("[cefstream] CEF Python {ver}".format(ver=cef.__version__))
        print("[cefstream] Python {ver} {arch}".format(ver=platform.python_version(), arch=platform.architecture()[0]))
        assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"

    @staticmethod
    def get_native_cef():
        return cef


class CefBrowser:

    def __init__(self, url):
        self.nativeBrowser = cef.CreateBrowserSync(url=url)

from cefpython3 import cefpython as cef

import platform

class CefManager:

    def __init__(self):
        self.browsers = dict()

    def initialize(self):
        self.check_versions()
        cef.Initialize()
        self.create_browser(identifier='1', url='https://google.pl/')
        self.create_browser(identifier='2', url='https://dzikoysk.net/')
        self.keep_alive()

    def keep_alive(self):
        cef.MessageLoop()
        cef.Shutdown()

    def shutdown(self):
        pass

    def create_browser(self, identifier, url):
        cef_browser = CefBrowser(url=url)
        self.browsers[identifier] = cef_browser
        return cef_browser

    def get_browser(self, identifier):
        return self.browsers[identifier]

    @staticmethod
    def check_versions():
        print("[cef_manager.py] CEF Python {ver}".format(ver=cef.__version__))
        print("[cef_manager.py] Python {ver} {arch}".format(ver=platform.python_version(), arch=platform.architecture()[0]))
        assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"

    @staticmethod
    def get_native_cef():
        return cef


class CefBrowser:

    def __init__(self, url):
        self.nativeBrowser = cef.CreateBrowserSync(url=url)

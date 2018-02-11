from cefpython3 import cefpython as cef


class CefManager:

    def __init__(self):
        self.browsers = dict()

    def initialize(self):
        cef.Initialize()

    def keep_alive(self):
        cef.MessageLoop()
        cef.Shutdown()

    def create_browser(self, identifier):
        cef_browser = CefBrowser()
        self.browsers[identifier] = cef_browser
        return cef_browser

    def get_browser(self, identifier):
        return self.browsers[identifier]

    @staticmethod
    def get_native_cef():
        return cef


class CefBrowser:

    def __init__(self):
        self.nativeBrowser = cef.CreateBrowserSync()
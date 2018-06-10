import platform

from time import sleep
from cefpython3 import cefpython as cef

from src.cef.cef_render_handler import CefRenderHandler
from src.stream.protocol.clientbound.frame_clientbound_packet import FrameClientboundPacket


class CefManager:

    def __init__(self, cefstream):
        self.cefstream = cefstream
        self.browser = None
        self.fps_period = 1
        self.running = True

    def launch(self):
        self.check_versions()
        self.cefstream.get_logger().info('Initializing CEF')

        settings = {
            "windowless_rendering_enabled": True
        }
        cef.Initialize(settings=settings)

        self.set_fps(55)
        self.create_browser(identifier='dzikoysk.net', url='https://google.com/')
        self.message_loop()

    def message_loop(self):
        self.cefstream.get_logger().info("Calling message loop")

        while self.running:
            cef.MessageLoopWork()

        self.shutdown_cef()

    def shutdown_cef(self):
        self.cefstream.get_logger().info("Shutting down CEF")
        self.shutdown()
        cef.Shutdown()

    def shutdown(self):
        self.running = False

    def create_browser(self, identifier, url):
        self.browser = CefBrowser(manager=self, identifier=identifier, url=url)
        return self.browser

    def set_fps(self, fps):
        self.fps_period = 1.0 / float(fps)
        self.cefstream.get_logger().info("FPS period updated to {fps_period} ({fps}fps)".format(fps_period=self.fps_period, fps=fps))

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

        window_info = cef.WindowInfo()
        window_info.SetAsOffscreen(0)

        browser_settings = {
            "windowless_frame_rate": 55
        }

        self.nativeBrowser = cef.CreateBrowserSync(window_info=window_info, window_title="cefstream - " + identifier, url=url, settings=browser_settings)
        self.nativeBrowser.SetClientHandler(CefRenderHandler(manager.cefstream, self))
        self.nativeBrowser.SendFocusEvent(True)
        self.nativeBrowser.WasResized()

    def get_buffer_string(self):
        return self.nativeBrowser.GetUserData("OnPaint.buffer_string")
from cefpython3 import cefpython as cef
from overrides import overrides

from src.stream.protocol.clientbound.frame_clientbound_packet import FrameClientboundPacket


class RenderHandler:

    # noinspection PyPep8Naming
    def GetViewRect(self, rect_out, **_):
        pass

    # noinspection PyPep8Naming
    def OnPaint(self, browser, element_type, paint_buffer, **_):
        pass


class CefRenderHandler(RenderHandler):

    viewport_size = (1600, 900)

    def __init__(self, cefstream, cef_manager):
        self.cefstream = cefstream
        self.cef_manager = cef_manager
        self.stream_manager = cefstream.get_stream_manager()

    @overrides
    def GetViewRect(self, rect_out, **_):
        rect_out.extend([0, 0, self.viewport_size[0], self.viewport_size[1]])
        return True

    @overrides
    def OnPaint(self, browser, element_type, paint_buffer, **_):
        if element_type == cef.PET_VIEW:
            packet = FrameClientboundPacket(paint_buffer.GetString(mode="bgra", origin="top-left"))
            self.cefstream.get_stream_manager().send(packet)
            return True
        else:
            raise Exception("Unsupported element_type in OnPaint")

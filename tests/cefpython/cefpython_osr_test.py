import sys
import tkinter as tk
from threading import Thread
from cefpython3 import cefpython as cef


class CefRenderHandler:

    viewport_size = (1600, 900)

    def GetViewRect(self, rect_out, **_):
        rect_out.extend([0, 0, self.viewport_size[0], self.viewport_size[1]])
        return True

    def OnPaint(self, browser, element_type, paint_buffer, **_):
        if element_type == cef.PET_VIEW:
            return True
        else:
            raise Exception("Unsupported element_type in OnPaint")


def create_window():
    # Pretend the process
    window = tk.Tk()
    window.title('My Window')
    window.geometry('0x0')
    window.mainloop()


#
# Stats:
#   CPU ~ 40/50%
#   Memory ~150MB
#
# Extra:
#   Parameters: --disable-gpu --disable-gpu-compositing --enable-begin-frame-scheduling
#
if __name__ == '__main__':
    # Launch cef
    sys.excepthook = cef.ExceptHook

    cef_settings = {
        "windowless_rendering_enabled": True
    }
    cef.Initialize(settings=cef_settings)

    window_info = cef.WindowInfo()
    window_info.SetAsOffscreen(0)

    browser_settings = {
        "windowless_frame_rate": 60
    }

    browser = cef.CreateBrowserSync(window_info=window_info, settings=browser_settings, window_title="cefstream - osr test", url='https://dzikoysk.net')
    browser.SetClientHandler(CefRenderHandler())
    browser.SendFocusEvent(True)
    browser.WasResized()

    tk_thread = Thread(target=create_window, name='TkThread')
    tk_thread.start()

    cef.MessageLoop()


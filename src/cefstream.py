# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v55.3+.

import sys

from cefpython3 import cefpython as cef


def main():
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    create_browser()
    cef.MessageLoop()
    cef.Shutdown()


def create_browser():
    browser = cef.CreateBrowserSync(url="https://www.google.com/", window_title="Hello World!")


if __name__ == '__main__':
    main()

from cefpython3 import cefpython as cef

#
# Stats:
#   CPU ~20%
#   Memory 100MB
#
if __name__ == '__main__':
    cef.Initialize()
    cef.CreateBrowserSync(window_title="cefstream - simple test", url='https://dzikoysk.net')
    cef.MessageLoop()

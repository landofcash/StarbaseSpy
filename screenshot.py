import win32gui
import win32ui
from ctypes import windll
from PIL import Image

def crop_social(im):
    im=im.crop((int(im.width*0.23),int(im.height*0.21),int(im.width*0.74),int(im.height*0.82))) #300 160 -- 960 630
    return im


def make_screenshot(wname, fname, do_crop_social=True):
    #print("Screenshot of "+wname + " will be saved into "+fname)
    hwnd = win32gui.FindWindow(None, wname)
    windll.user32.SetProcessDPIAware()
    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    #print(f"left:{left} top:{top} right:{right} bot:{bot}")
    left, top = win32gui.ClientToScreen(hwnd, (left, top))
    right, bot = win32gui.ClientToScreen(hwnd,(right, bot))
    #print(f"left:{left} top:{top} right:{right} bot:{bot}")
    w = int((right - left))
    h = int((bot - top))
    #print(f"w:{w} h:{h}")
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    #print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer('RGB',(bmpinfo['bmWidth'], bmpinfo['bmHeight']),bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        if do_crop_social:
            im=crop_social(im)
        im.save(fname)
        return im
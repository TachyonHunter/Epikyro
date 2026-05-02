import ctypes

def LoadFont():
    ctypes.windll.gdi32.AddFontResourceW("Aptos.ttf")
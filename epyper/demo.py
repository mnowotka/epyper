from epyper.displayController import displayImg
from epyper.displayCOGProcess import Display
from epyper import bsp
from PIL import Image
import epyper
import os
import itertools

def toBytes(bits):
    return [sum([[0,1][byte[b]>0] << b for b in reversed(range(0,8))])
               for byte in reversed(zip(*(iter(bits),) * 8))
        ]

def demo():
    print "Starting E-paper demo"

    bsp.init()
    oldImg = [0] * (176*33)

    while True:

        print "EA Image"
        eaLogo = Image.open(os.path.join(os.path.dirname(os.path.abspath(epyper.__file__)), "eaLogo.png"))
        eaData = toBytes(list(eaLogo.getdata()))
        displayImg(Display.EPD_TYPE_270, eaData, oldImg)
        oldImg = eaData

        bsp.delayMs(10000)

        print "PD Image"
        pdLogo = Image.open(os.path.join(os.path.dirname(os.path.abspath(epyper.__file__)), "pdLogo.png"))
        pdData = toBytes(list(pdLogo.getdata()))
        displayImg(Display.EPD_TYPE_270, pdData, oldImg)
        oldImg = pdData

        bsp.delayMs(10000)

from epyper.displayController import displayImg
from epyper.displayCOGProcess import Display
from epyper import bsp
from PIL import Image
import epyper
import os
import itertools

def toBytes(bits):
    return [sum([[0,1][byte[b]>0] << (7-b) for b in range(0,8)])
               for byte in zip(*(iter(bits),) * 8)
        ]

def demo():
    print "Starting E-paper demo"

    bsp.init()
    oldImg = bytearray(176*33)

    while True:

        print "EA Image"
        eaLogo = Image.open(os.path.join(os.path.dirname(os.path.abspath(epyper.__file__)), "eaLogo.png"))
        eaData = toBytes(bytearray(eaLogo.convert("1").getdata()))
        displayImg(Display.EPD_TYPE_270, eaData, oldImg)
        oldImg = eaData

        bsp.delayMs(10000)

        print "PD Image"
        pdLogo = Image.open(os.path.join(os.path.dirname(os.path.abspath(epyper.__file__)), "pdLogo.png"))
        pdData = toBytes(bytearray(pdLogo.convert("1").getdata()))
        displayImg(Display.EPD_TYPE_270, pdData, oldImg)
        oldImg = pdData

        bsp.delayMs(10000)

from epyper.displayController import displayImg
from epyper.displayCOGProcess import Display
from epyper import bsp
from PIL import Image
import epyper
import os

def demo():
    print "Starting E-paper demo"

    bsp.init()
    oldImg = [0] * (176*33)

    while True:

        print "EA Image"
        eaLogo = Image.open(os.path.join(os.path.dirname(os.path.abspath(epyper.__file__)), "eaLogo.png"))
        eaLogo = eaLogo.transpose(Image.FLIP_LEFT_RIGHT)
        eaData = list(eaLogo.rotate(180).getdata())
        displayImg(Display.EPD_TYPE_270, eaData, oldImg)
        oldImg = eaData

        bsp.delayMs(10000)

        print "PD Image"
        eaLogo = Image.open(os.path.join(os.path.dirname(os.path.abspath(epyper.__file__)), "pdLogo.png"))
        pdLogo = pdLogo.transpose(Image.FLIP_LEFT_RIGHT)
        pdData = list(pdLogo.rotate(180).getdata())
        displayImg(Display.EPD_TYPE_270, pdData, oldImg)
        oldImg = pdData

        bsp.delayMs(10000)

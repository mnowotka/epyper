from epyper.displayController import displayImg
from epyper.displayCOGProcess import Display
from epyper.pdLogo import pdLogo
from epyper.eaLogo import eaLogo
from epyper import bsp

def demo():
    print "Starting E-paper demo"

    bsp.init()
    oldImg = [0] * (176*33)

    while True:

        print "EA Image"
        displayImg(Display.EPD_TYPE_270, eaLogo, oldImg)
        oldImg = eaLogo

        bsp.delayMs(10000)

        print "PD Image"
        displayImg(Display.EPD_TYPE_270, pdLogo, oldImg)
        oldImg = pdLogo

        bsp.delayMs(10000)

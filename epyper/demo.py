from epyper.displayController import DisplayController
from epyper.displayCOGProcess import Display
from epyper import bsp
from PIL import Image
import epyper
import os

#-------------------------------------------------------------------------------

def demo():
    print "Starting E-paper demo"
    display = DisplayController(Display.EPD_TYPE_270)

    while True:

        print "EA Image"
        eaLogo = Image.open(os.path.join(os.path.dirname(
            os.path.abspath(epyper.__file__)), "samples", "eaLogo.png"))
                            
        display.displayImg(eaLogo)

        bsp.delayMs(10000)

        print "PD Image"
        pdLogo = Image.open(os.path.join(os.path.dirname(
            os.path.abspath(epyper.__file__)), "samples", "pdLogo.png"))
                            
        display.displayImg(pdLogo)

        bsp.delayMs(10000)
        
#-------------------------------------------------------------------------------        

from epyper.displayCOGProcess import Display

def displayImg(EPDType, newImg, prevImg):
    display = Display(EPDType)
    
    try:
        # always initialize display (has been powered off before)
        display.hwInit()
        display.powerOn()
        display.initializeDriver()

        # display new picture, but first remove old one
        display.display(newImg, prevImg)
        
    finally:    
        # power down display - picture still displayed
        display.powerOff()


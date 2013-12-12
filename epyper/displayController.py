from epyper.displayCOGProcess import Display
from epyper import bsp

#-------------------------------------------------------------------------------

class DisplayController():

#-------------------------------------------------------------------------------

    def __init__(self, EPDType):
        bsp.init()
        self.display = Display(EPDType)
        params = self.display.COG_Params
        size = params.horizontal * params.vertical
        self.prevImg = bytearray(size)
        self.newImg = bytearray(size)
        self.size = (params.horizontal * 8, params.vertical)

#-------------------------------------------------------------------------------
        
    def toBytes(self, bits):
        return [sum([[0,1][byte[b]>0] << (7-b) for b in range(0,8)])
                   for byte in zip(*(iter(bits),) * 8)
            ]    

#-------------------------------------------------------------------------------

    def displayImg(self, img):
        if img.size != self.size:
            print "image has a wrong size, should be %s, is %s" % \
                                                    (str(self.size), img.size)
            return
            
        self.newImg = self.toBytes(bytearray(img.convert("1").getdata()))
        
        try:
            # always initialize display (has been powered off before)
            self.display.hwInit()
            self.display.powerOn()
            self.display.initializeDriver()

            # display new picture, but first remove old one
            self.display.display(self.newImg, self.prevImg)
            self.prevImg = self.newImg
            
        finally:    
            # power down display - picture still displayed
            self.display.powerOff()

#-------------------------------------------------------------------------------


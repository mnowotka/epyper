from epyper import displayCOGProcess as cog

def displayImg(EPDType, newImg, prevImg):
    # always initialize display (has been powered off before)
    cog.hwInit()
    cog.powerOn()
    cog.initializeDriver(EPDType)

    # display new picture, but first remove old one
    cog.display(newImg, prevImg)

    # power down display - picture still displayed
    cog.powerOff()


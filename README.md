epyper
======

Python driver for Embedded Artists 2.7 inch E-paper Display Module:

http://www.embeddedartists.com/products/displays/lcd_27_epaper.php. 

It's based on original C code available here:

http://www.embeddedartists.com/sites/default/files/support/displays/epaper/epaper_pi_130307.tar.gz

Rationale
--------

How to use it?
--------

    #necessary imports first
    from PIL import Image
    from epyper.displayCOGProcess import Display
    from epyper.displayController import DisplayController
    
    #create DisplayController instance specifying display type as an argument
    display = DisplayController(Display.EPD_TYPE_270)
    
    #open some image
    im = Image.open("some_image.png")
    
    #display it!
    display.displayImg(im)
    
Dependencies
--------
 * [WiringPi2-Python] (https://github.com/WiringPi/WiringPi2-Python)
 * [Pillow] (https://github.com/python-imaging/Pillow)

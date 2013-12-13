epyper
======

Python driver for Embedded Artists 2.7 inch E-paper Display Module:

http://www.embeddedartists.com/products/displays/lcd_27_epaper.php. 

It's based on original C code available here:

http://www.embeddedartists.com/sites/default/files/support/displays/epaper/epaper_pi_130307.tar.gz

Rationale
--------

So you got you new shiny E-paper display from Embeded Artists. You plug it to your rPi to display some images. But how? Example C code is not very easy to adapt. All images included in C demo are written as byte tables in C header files. Function for displaying an image takes pointers to `int8_t`... In order to display new image you need to remember and old one. WTF!?!? You just wanted to display a png or jpg from your disk or web. And preferably do so in python. If that's your story then `epyper` is just for you.

`Epyper` provides high level python interface for displaying images on e-paper. The most important class is `DisplayController`, which provides `displayImg` method accepting PIL `Image` to be displayed. The image need to have proper size. It doesn't necessary needs to be black and with only - color images will be converted but the effect may be dissapointing so it's better to provide b&w or convert itbefore handing it to the `DisplayController`. 

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

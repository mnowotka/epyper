from epyper import bsp

#-------------------------------------------------------------------------------
# Public functions
#-------------------------------------------------------------------------------

def cs_high():
    # CS_SET_HIGH;
    bsp.pinOut(bsp.pins.PIN_6, 1)

#-------------------------------------------------------------------------------

def cs_low():
    # CS_SET_LOW;
    bsp.pinOut(bsp.pins.PIN_6, 0)

#-------------------------------------------------------------------------------

def rst_high():
    # RST_SET_HIGH;
    bsp.pinOut(bsp.pins.PIN_12, 1)

#-------------------------------------------------------------------------------

def rst_low():
    # RST_SET_LOW;
    bsp.pinOut(bsp.pins.PIN_12, 0)

#-------------------------------------------------------------------------------

def discharge_high():
    # DISCHARGE_SET_HIGH;
    bsp.pinOut(bsp.pins.PIN_14, 1)

#-------------------------------------------------------------------------------

def discharge_low():
    # DISCHARGE_SET_LOW;
    bsp.pinOut(bsp.pins.PIN_14, 0)

#-------------------------------------------------------------------------------

def panelon_off():
    # PANELON_SET_LOW;
    bsp.pinOut(bsp.pins.PIN_13, 0)

#-------------------------------------------------------------------------------

def panelon_on():
    # PANELON_SET_HIGH;
    bsp.pinOut(bsp.pins.PIN_13, 1)

#-------------------------------------------------------------------------------

def border_high():
    # BORDER_SET_HIGH;
    pass

#-------------------------------------------------------------------------------

def border_low():
    # BORDER_SET_LOW;
    pass

#-------------------------------------------------------------------------------

def delay_ms(time):
    bsp.delayMs(time)

#-------------------------------------------------------------------------------

def get_temperature():
    return bsp.getTemp()

#-------------------------------------------------------------------------------

def getCurrentTimeTick():
    return bsp.getMsTicks() 

#-------------------------------------------------------------------------------

def pwm_active(delayInMs):
    numOfIterations = delayInMs * 100
    # PWM_DIR_OUT;
    bsp.setPinMode(bsp.pins.PIN_11, bsp.pinMode.OUTPUT)
    while numOfIterations > 0:
        # PWM_SET_HIGH;
        bsp.pinOut(bsp.pins.PIN_11, 1)
        bsp.delayUs(5)     #100kHz (96kHz ideal)
        # PWM_SET_LOW;
        bsp.pinOut(bsp.pins.PIN_11, 0)
        bsp.delayUs(5)
        numOfIterations -= 1

#-------------------------------------------------------------------------------
# SPI  Configuration
#-------------------------------------------------------------------------------

def spi_detach():
    pass

#-------------------------------------------------------------------------------
    
def spi_init():
    bsp.spiInit()

#-------------------------------------------------------------------------------

def spi_send(register, data):
    #cs_high()
    #bsp.delayUs(10)
    cs_low()
    
    buf = chr(0x70)
    buf += chr(register)
    bsp.writeToDisplay(buf)
    
    cs_high()
    bsp.delayUs(10)
    cs_low()
    
    buf = chr(0x72) + buf[1:]
    bsp.writeToDisplay(buf)
    bsp.writeToDisplay(data)
    cs_high()
    bsp.delayUs(10)

#-------------------------------------------------------------------------------

def spi_send_byte(register, data):
    #cs_high()
    #bsp.delayUs(10)
    cs_low()
    buf = chr(0x70)
    buf += chr(register)
    bsp.writeToDisplay(buf)
    
    cs_high()
    bsp.delayUs(10)
    cs_low()
    
    buf = chr(0x72)
    buf += chr(data)
    bsp.writeToDisplay(buf)
    cs_high()
    bsp.delayUs(10)
    
#-------------------------------------------------------------------------------

def initDisplayHardware():
    # RST_DIR_OUT;
    bsp.setPinMode(bsp.pins.PIN_12, bsp.pinMode.OUTPUT)
    # DISCHARGE_DIR_OUT;
    bsp.setPinMode(bsp.pins.PIN_14, bsp.pinMode.OUTPUT)
    # CS_DIR_OUT;
    bsp.setPinMode(bsp.pins.PIN_6, bsp.pinMode.OUTPUT)
    # PANELON_DIR_OUT;
    bsp.setPinMode(bsp.pins.PIN_13, bsp.pinMode.OUTPUT)
    # DRIVERBUSY_DIR_IN;
    bsp.setPinMode(bsp.pins.PIN_7, bsp.pinMode.INPUT)
    # BORDER_DIR_OUT;

    panelon_off()
    spi_init()
    cs_low()
    pwm_active(0)    #set output low
    rst_low()
    discharge_low()

#-------------------------------------------------------------------------------

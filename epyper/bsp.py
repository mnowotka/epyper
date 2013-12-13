import wiringpi2
from epyper.enum import enum

pins = enum(
    PIN_6 = 0,
    PIN_7 = 1,
    PIN_8 = 2,
    PIN_11 = 3,
    PIN_12 = 4,
    PIN_13 = 5,
    PIN_14 = 6,
    PIN_SZ = 7
)

pinMode = enum(
    INPUT = 0,
    OUTPUT = 1
)

#-------------------------------------------------------------------------------
# Typedefs and defines
#-------------------------------------------------------------------------------

LOW = 0
HIGH = 1 

LM75A_I2C_ADDR = 0x49
LM75A_CMD_TEMP = 0x00
DISPLAY_BUF_SZ = 256

#-------------------------------------------------------------------------------
# Local variables
#-------------------------------------------------------------------------------

# I2C device handle
gI2cFd = -1

pinMap = {
  # [SEC] -> [PI GPIO#]
  pins.PIN_6 : 6,  # CS
  pins.PIN_7 : 0,  # Busy
  pins.PIN_8 : -1,  # Not Used
  pins.PIN_11 : 1,  # PWM
  pins.PIN_12 : 5,  # RST
  pins.PIN_13 : 3,  # PWR_Ctrl
  pins.PIN_14 : 4,  # DISCHARGE
}

displayBuf = [0] * DISPLAY_BUF_SZ

#-------------------------------------------------------------------------------
# Local functions
#-------------------------------------------------------------------------------

def lm75a_readTemp():
    temp = [0] * 2
    t = 0

    wiringpi2.wiringPiI2CWrite(gI2cFd, LM75A_CMD_TEMP)
    temp[0] = wiringpi2.wiringPiI2CRead(gI2cFd)
    temp[1] = wiringpi2.wiringPiI2CRead(gI2cFd)

    # 11 MSB bits used. Celcius is calculated as Temp data * 1/8
    t = ((temp[0] << 8) | (temp[1]))

    return ((t * 100) >> 8)
    
#-------------------------------------------------------------------------------
# Public functions
#-------------------------------------------------------------------------------

def init():
    """   
       BSP initialize function. Must be called before any other BSP related
       functions.
    
    """
    global gI2cFd

    if wiringpi2.wiringPiSetup() < 0:
        print "bsp_init: failed to initialize wiringPi"
        return -1
        
    gI2cFd = wiringpi2.wiringPiI2CSetup(LM75A_I2C_ADDR)
    
    if gI2cFd < 0:
        print "bsp_init: failed to initialize I2C"
        return -1
    
    if wiringpi2.wiringPiSPISetup(0, 1000000) < 0:
        print "bsp_init: failed to initialize SPI"
        return -1
    
    return 0

#-------------------------------------------------------------------------------

def getMsTicks():
    """   
       Get number of milliseconds
    
    """
    return wiringpi2.millis() 
    
#-------------------------------------------------------------------------------

def spiInit():
    """   
       Initialize SPI
    
    """
    pass # initialized in bsp_init

#-------------------------------------------------------------------------------

def writeToDisplay(data):
    """   
       Write data to the display
    
    """
    length = len(data)
    if length > DISPLAY_BUF_SZ:
        print "bsp_writeToDisplay: ERROR len=%d > %d" % (length, DISPLAY_BUF_SZ)
        return

    #TODO: can hang here...
    wiringpi2.wiringPiSPIDataRW(0, data)

#-------------------------------------------------------------------------------

def delayMs(ms):
    """   
       Delay specified number of milliseconds
       
       Params:
           [in] ms - number of milliseconds to delay
    
    """
    wiringpi2.delay(ms)
    
#-------------------------------------------------------------------------------

def delayUs(us):
    """   
       Delay specified number of microseconds

       Params:
           [in] us - number of microseconds to delay
    
    """
    wiringpi2.delayMicroseconds(us)

#-------------------------------------------------------------------------------

def getTemp():
    """   
       Read temperature

       Params:
           [out] temperature - (int16_t) temperature in Celsius
    
    """
    lm75a_readTemp()
    delayMs(5)
    return int(lm75a_readTemp()/100)
    
#-------------------------------------------------------------------------------

def setPinMode(pin, mode):
    """   
       Set the PIN mode of a specific pin
    
    """
    m = pinMode.INPUT
    p = 0

    if pin >= pins.PIN_SZ:
        return

    if mode == pinMode.OUTPUT:
        m = pinMode.OUTPUT
    
    p = pinMap[pin]

    wiringpi2.pinMode(p, m)


#-------------------------------------------------------------------------------

def pinOut(pin, value):
    """   
       Set PIN to high (1) or low (0) value
    
    """
    p = 0
    v = LOW

    if pin >= pins.PIN_SZ:
        return

    if value != 0:
        v = HIGH

    p = pinMap[pin]

    wiringpi2.digitalWrite(p, v)
    
#-------------------------------------------------------------------------------
    
   


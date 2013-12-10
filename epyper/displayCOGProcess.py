from epyper.enum import enum
from epyper import displayHardwareDriver as epd

BLACK0 = 0x03
BLACK1 = 0x0C
BLACK2 = 0x30
BLACK3 = 0xc0
WHITE0 = 0x02
WHITE1 = 0x08
WHITE2 = 0x20
WHITE3 = 0x80

NOTHING = 0x00
SCANON = 0xC0
lineDataSize = 111

EPDType = enum(
  EPDType_144 = 0,      #1.44" display
  EPDType_200 = 1,      #2.0"  display
  EPDType_270 = 2       #2.7"  display
)

EPD_TYPE_144 = 0
EPD_TYPE_200 = 1
EPD_TYPE_270 = 2

class COG_LineData:
    def __init__(self, typeIndex):
        if typeIndex == EPD_TYPE_144:
            self.even = [0x00] * 16
            self.scan = [0x00] * 24
            self.odd = [0x00] * 16
        elif typeIndex == EPD_TYPE_200:
            self.even = [0x00] * 25
            self.scan = [0x00] * 24
            self.odd = [0x00] * 25
        elif typeIndex == EPD_TYPE_270:
            self.even = [0x00] * 33
            self.scan = [0x00] * 44
            self.odd = [0x00] * 33                      
        
class COG_Parameters:
    def __init__(self, channelSelect, voltageLevel, horizontal, vertical, 
                                          dataLineSize, frameTime, stageTime):
        self.channelSelect = channelSelect
        self.voltageLevel = voltageLevel
        self.horizontal = horizontal
        self.vertical = vertical
        self.dataLineSize = dataLineSize
        self.frameTime = frameTime
        self.stageTime = stageTime
        
COG_Params = []

#-------------------------------------------------------------------------------
# Defines and typedefs
#-------------------------------------------------------------------------------

COG_Params.append(
    COG_Parameters( #for 1.44"
        [0x00,0x00,0x00,0x00,0x00,0x0f,0xff,0x00],
        0x03,
        128/8,
        96,
        ((128+96)*2)/8,
        43,
        480
    )
)

COG_Params.append(
    COG_Parameters( #for 2.0"
        [0x00,0x00,0x00,0x00,0x01,0xFF,0xE0,0x00],
        0x03,
        200/8,
        96,
        (((200+96)*2)/8)+1,
        53,
        480
    )
)

COG_Params.append(
    COG_Parameters( #for 2.7"
        [0x00,0x00,0x00,0x7F,0xFF,0xFE,0x00,0x00],
        0x00,
        264/8,
        176,
        (((264+176)*2)/8)+1,
        105,
        630
    )
)

scanTable = [0xC0, 0x30, 0x0C, 0x03]

#-------------------------------------------------------------------------------
# Local variables
#-------------------------------------------------------------------------------

stageTime = 480
COG_Line = None
EPD_Type_Index = 0
currentframe = 0
dataLineEven = 0
dataLineOdd = 0
dataLineScan = 0

#-------------------------------------------------------------------------------
# Local functions
#-------------------------------------------------------------------------------

def setTemperature_Factor(EPD_Type_Index):
    global stageTime
    temperature = epd.get_temperature()

    print "temperature = %s" % temperature

    if temperature < -10:
        stageTime = COG_Params[EPD_Type_Index].stageTime * 17
    elif temperature < -5:
         stageTime = COG_Params[EPD_Type_Index].stageTime * 12
    elif temperature < 5:
         stageTime = COG_Params[EPD_Type_Index].stageTime * 8
    elif temperature < 10:
         stageTime = COG_Params[EPD_Type_Index].stageTime * 4
    elif temperature < 15:
         stageTime = COG_Params[EPD_Type_Index].stageTime * 3
    elif temperature < 20:
         stageTime = COG_Params[EPD_Type_Index].stageTime * 2
    elif temperature < 40:
         stageTime = COG_Params[EPD_Type_Index].stageTime * 1
    else:
         stageTime = (COG_Params[EPD_Type_Index].stageTime * 7)/10
    print "stageTime = %s" % stageTime

#-------------------------------------------------------------------------------
         
def driver_TypeSelect(typeIndex):
    global dataLineEven, dataLineOdd, dataLineScan, COG_Line
    COG_Line = COG_LineData(typeIndex)
    dataLineEven=COG_Line.even
    dataLineOdd=COG_Line.odd
    dataLineScan=COG_Line.scan

#-------------------------------------------------------------------------------

def sendData(data):
    voltageLevel = COG_Params[EPD_Type_Index].voltageLevel
    frameTime = COG_Params[EPD_Type_Index].frameTime
    currentframe = int(COG_Params[EPD_Type_Index].frameTime)
    startClock = epd.getCurrentTimeTick()
    cnt = 1
    
    while cnt:
        cnt -= 1
        for line in data:
            epd.spi_send_byte(0x04, voltageLevel)
            epd.spi_send(0x0a, line)
            epd.spi_send_byte(0x02, 0x2F)
        currentframe = epd.getCurrentTimeTick() - startClock + frameTime
        if stageTime > currentframe:
            break

    while stageTime > (epd.getCurrentTimeTick() - startClock):
        continue

#-------------------------------------------------------------------------------

def display_Stage_1(previousPicture):
    global dataLineOdd, dataLineEven, dataLineScan, currentframe
    dataBuffer = []
    idx = 0
    for i in range(COG_Params[EPD_Type_Index].vertical): # for every line
        k = COG_Params[EPD_Type_Index].horizontal - 1
        for j in range (COG_Params[EPD_Type_Index].horizontal): # check every bit in the line
            tempByte = previousPicture[idx]
            idx += 1
            dataLineOdd[j] = (WHITE3 if (tempByte & 0x80) else BLACK3) | \
                             (WHITE2 if (tempByte & 0x20) else BLACK2) | \
                             (WHITE1 if (tempByte & 0x08) else BLACK1) | \
                             (WHITE0 if (tempByte & 0x02) else BLACK0)

            dataLineEven[k] = (WHITE3 if (tempByte & 0x01) else BLACK3) | \
                              (WHITE2 if (tempByte & 0x04) else BLACK2) | \
                              (WHITE1 if (tempByte & 0x10) else BLACK1) | \
                              (WHITE0 if (tempByte & 0x40) else BLACK0)
            k -= 1

        dataLineScan[i>>2] = scanTable[i%4]
        data = dataLineEven + dataLineScan + dataLineOdd
        data += [0] * ( COG_Params[EPD_Type_Index].dataLineSize - len(data))
        dataBuffer.append(str(bytearray(data)))
        dataLineScan[i>>2] = 0
    return dataBuffer      

#-------------------------------------------------------------------------------
            
def display_Stage_2(previousPicture):
    global dataLineOdd, dataLineEven, dataLineScan, currentframe
    dataBuffer = []
    idx = 0
    for i in range(COG_Params[EPD_Type_Index].vertical):
        k = COG_Params[EPD_Type_Index].horizontal - 1
        for j in range(COG_Params[EPD_Type_Index].horizontal): #make every bit in the line black
            tempByte = previousPicture[idx]
            idx += 1
            dataLineOdd[j] = (NOTHING if (tempByte & 0x80) else WHITE3) | \
                             (NOTHING if (tempByte & 0x20) else WHITE2) | \
                             (NOTHING if (tempByte & 0x08) else WHITE1) | \
                             (NOTHING if (tempByte & 0x02) else WHITE0)
            dataLineEven[k] = (NOTHING if (tempByte & 0x01) else WHITE3) | \
                              (NOTHING if (tempByte & 0x04) else WHITE2) | \
                              (NOTHING if (tempByte & 0x10) else WHITE1) | \
                              (NOTHING if (tempByte & 0x40) else WHITE0)
            k -= 1                  

        dataLineScan[i>>2] = scanTable[i%4]
        data = dataLineEven + dataLineScan + dataLineOdd
        data += [0] * ( COG_Params[EPD_Type_Index].dataLineSize - len(data))
        dataBuffer.append(str(bytearray(data)))
        dataLineScan[i>>2] = 0
    return dataBuffer       
            
#-------------------------------------------------------------------------------

def display_Stage_3(picture):
    global dataLineOdd, dataLineEven, dataLineScan, currentframe
    dataBuffer = []
    idx = 0
    for i in range(COG_Params[EPD_Type_Index].vertical): # for every line
        k = COG_Params[EPD_Type_Index].horizontal - 1
        for j in range(COG_Params[EPD_Type_Index].horizontal): # check every bit in the line
            tempByte = picture[idx]
            idx += 1
            dataLineOdd[j] = (BLACK3 if (tempByte & 0x80) else NOTHING) | \
                             (BLACK2 if (tempByte & 0x20) else NOTHING) | \
                             (BLACK1 if (tempByte & 0x08) else NOTHING) | \
                             (BLACK0 if (tempByte & 0x02) else NOTHING)

            dataLineEven[k] = (BLACK3 if (tempByte & 0x01) else NOTHING) | \
                              (BLACK2 if (tempByte & 0x04) else NOTHING) | \
                              (BLACK1 if (tempByte & 0x10) else NOTHING) | \
                              (BLACK0 if (tempByte & 0x40) else NOTHING)
            k -= 1                  

        dataLineScan[i>>2] = scanTable[i%4]
        data = dataLineEven + dataLineScan + dataLineOdd
        data += [0] * ( COG_Params[EPD_Type_Index].dataLineSize - len(data))
        dataBuffer.append(str(bytearray(data)))
        dataLineScan[i>>2] = 0
    return dataBuffer
            
#------------------------------------------------------------------------------- 

def display_Stage_4(picture):
    global dataLineOdd, dataLineEven, dataLineScan, currentframe
    dataBuffer = []
    idx = 0
    for i in range(COG_Params[EPD_Type_Index].vertical): # for every line
        k = COG_Params[EPD_Type_Index].horizontal - 1
        for j in range(COG_Params[EPD_Type_Index].horizontal):
            tempByte = picture[idx]
            idx += 1
            dataLineOdd[j] = (WHITE3 if (tempByte & 0x80) else BLACK3 ) | \
                             (WHITE2 if (tempByte & 0x20) else BLACK2 ) | \
                             (WHITE1 if (tempByte & 0x08) else BLACK1 ) | \
                             (WHITE0 if (tempByte & 0x02) else BLACK0 )

            dataLineEven[k] = (WHITE3 if (tempByte & 0x01) else BLACK3 ) | \
                              (WHITE2 if (tempByte & 0x04) else BLACK2 ) | \
                              (WHITE1 if (tempByte & 0x10) else BLACK1 ) | \
                              (WHITE0 if (tempByte & 0x40) else BLACK0 )

            k -= 1                  

        dataLineScan[i>>2] = scanTable[i%4]
        data = dataLineEven + dataLineScan + dataLineOdd
        data += [0] * ( COG_Params[EPD_Type_Index].dataLineSize - len(data))
        dataBuffer.append(str(bytearray(data)))
        dataLineScan[i>>2] = 0
    return dataBuffer

#------------------------------------------------------------------------------- 
# Public functions
#-------------------------------------------------------------------------------

def hwInit():
    epd.initDisplayHardware()

#-------------------------------------------------------------------------------

def powerOn():

    epd.discharge_low()
    epd.rst_low()
    epd.cs_low()
    epd.spi_init()
    epd.pwm_active(5)
    epd.panelon_on()
    epd.pwm_active(10)
    epd.cs_high()
    epd.rst_high()
    epd.pwm_active(5)
    epd.rst_low()
    epd.pwm_active(5)
    epd.rst_high()
    epd.pwm_active(5)                                                          

#-------------------------------------------------------------------------------

def initializeDriver(EPDIndex):

    global EPD_Type_Index, COG_Line
    sendBuffer = [0] * 2
    EPD_Type_Index = EPDIndex
           
    driver_TypeSelect(EPDIndex)
    k = 0

    setTemperature_Factor(EPDIndex)

    epd.spi_send(0x01, str(bytearray(COG_Params[EPDIndex].channelSelect)))

    epd.spi_send_byte(0x06, 0xff)
    epd.spi_send_byte(0x07, 0x9d)
    epd.spi_send_byte(0x08, 0x00)

    sendBuffer[0] = 0xd0
    sendBuffer[1] = 0x00
    epd.spi_send(0x09, str(bytearray(sendBuffer)))

    epd.spi_send_byte(0x04, COG_Params[EPDIndex].voltageLevel)

    epd.spi_send_byte(0x03, 0x01)
    epd.spi_send_byte(0x03, 0x00)

    epd.pwm_active(5)

    epd.spi_send_byte(0x05, 0x01)
        
    epd.pwm_active(30)

    epd.spi_send_byte(0x05, 0x03)
    epd.delay_ms(30)
    epd.spi_send_byte(0x05, 0x0f)
    epd.delay_ms(30)
    epd.spi_send_byte(0x02, 0x24)

#-------------------------------------------------------------------------------
    
def display(newImg, prevImg):
    data = []
    data.append(display_Stage_1(prevImg))
    data.append(display_Stage_2(prevImg))
    data.append(display_Stage_3(newImg))
    data.append(display_Stage_4(newImg))
    data.append(display_Stage_1(newImg))
    data.append(display_Stage_1(newImg))
    data.append(display_Stage_1(newImg))
    for chunk in data:
        sendData(chunk)

#-------------------------------------------------------------------------------

def powerOff():

    epd.spi_send_byte(0x03, 0x01)
    epd.spi_send_byte(0x02, 0x05)
    epd.spi_send_byte(0x05, 0x0E)
    epd.spi_send_byte(0x05, 0x02)
    epd.spi_send_byte(0x04, 0x0C)
    epd.delay_ms(120)
    epd.spi_send_byte(0x05, 0x00)
    epd.spi_send_byte(0x07, 0x0D)
    epd.spi_send_byte(0x04, 0x50)
    epd.delay_ms(40)
    epd.spi_send_byte(0x04, 0xA0)
    epd.delay_ms(40)
    epd.spi_send_byte(0x04, 0x00)

    epd.rst_low()
    epd.cs_low()
    epd.spi_detach()
    epd.panelon_off()

    epd.discharge_high()
    epd.delay_ms(150)
    epd.discharge_low()

#-------------------------------------------------------------------------------

from epyper.enum import enum
from epyper import displayHardwareDriver as epd

#-------------------------------------------------------------------------------

class COG_Parameters():
    def __init__(self, channelSelect, voltageLevel, horizontal, vertical, 
                                          dataLineSize, frameTime, stageTime):
        self.channelSelect = channelSelect
        self.voltageLevel = voltageLevel
        self.horizontal = horizontal
        self.vertical = vertical
        self.dataLineSize = dataLineSize
        self.frameTime = frameTime
        self.stageTime = stageTime

#-------------------------------------------------------------------------------

class Display():

    BLACK0 = 0x03
    BLACK1 = 0x0C
    BLACK2 = 0x30
    BLACK3 = 0xc0
    WHITE0 = 0x02
    WHITE1 = 0x08
    WHITE2 = 0x20
    WHITE3 = 0x80
    NOTHING = 0x00

    PATTERNS = [
        bytearray([WHITE3, WHITE2, WHITE1, WHITE0]),
        bytearray([NOTHING, NOTHING, NOTHING, NOTHING]),
        bytearray([BLACK3, BLACK2, BLACK1, BLACK0])    
    ]

    TESTS = [
        bytearray([0x80, 0x20, 0x08, 0x02]),
        bytearray([0x01, 0x04, 0x10, 0x40])
    ]

    EPD_TYPE_144 = 0
    EPD_TYPE_200 = 1
    EPD_TYPE_270 = 2
    
    scanTable = bytearray([0xC0, 0x30, 0x0C, 0x03])

#-------------------------------------------------------------------------------

    def __init__(self, typeIndex):
    
        self.EPD_Type_Index = typeIndex
    
        if typeIndex == self.EPD_TYPE_144:
            self.even = bytearray(16)
            self.scan = bytearray(24)
            self.odd = bytearray(16)
            
            self.COG_Params = COG_Parameters( #for 1.44"
                    bytearray([0x00,0x00,0x00,0x00,0x00,0x0f,0xff,0x00]),
                    0x03,
                    128/8,
                    96,
                    ((128+96)*2)/8,
                    43,
                    480
                )
            
        elif typeIndex == self.EPD_TYPE_200:
            self.even = bytearray(25)
            self.scan = bytearray(24)
            self.odd = bytearray(25)
            
            self.COG_Params = COG_Parameters( #for 2.0"
                    bytearray([0x00,0x00,0x00,0x00,0x01,0xFF,0xE0,0x00]),
                    0x03,
                    200/8,
                    96,
                    (((200+96)*2)/8)+1,
                    53,
                    480
                )            
            
        elif typeIndex == self.EPD_TYPE_270:
            self.even = bytearray(33)
            self.scan = bytearray(44)
            self.odd = bytearray(33)                      
        
            self.COG_Params = COG_Parameters( #for 2.7"
                    bytearray([0x00,0x00,0x00,0x7F,0xFF,0xFE,0x00,0x00]),
                    0x00,
                    264/8,
                    176,
                    (((264+176)*2)/8)+1,
                    105,
                    630
                )

        self.aux_buffer = bytearray(len(self.even) + len(self.scan) + \
                                                                 len(self.odd))
        
#-------------------------------------------------------------------------------
# Local functions
#-------------------------------------------------------------------------------

    def setTemperature_Factor(self):
        temperature = epd.get_temperature()

        if temperature < -10:
            self.stageTime = self.COG_Params.stageTime * 17
        elif temperature < -5:
            self.stageTime = self.COG_Params.stageTime * 12
        elif temperature < 5:
            self.stageTime = self.COG_Params.stageTime * 8
        elif temperature < 10:
            self.stageTime = self.COG_Params.stageTime * 6
        elif temperature < 15:
            self.stageTime = self.COG_Params.stageTime * 5
        elif temperature < 20:
            self.stageTime = self.COG_Params.stageTime * 4
        elif temperature < 40:
            self.stageTime = self.COG_Params.stageTime * 3
        else:
            self.stageTime = (self.COG_Params.stageTime * 7)/10

#-------------------------------------------------------------------------------

    def sendData(self, stage, data):
        voltageLevel = self.COG_Params.voltageLevel
        ft = self.COG_Params.frameTime
        currentTime = 0
        frameTime = 0 
        frameCounter = 0
        startClock = epd.getCurrentTimeTick()
        
        while True:
            frameCounter += 1
            for line in data:
                self.aux_buffer[:] = line[:]
                epd.spi_send_byte(0x04, voltageLevel)
                epd.spi_send(0x0a, str(self.aux_buffer))
                epd.spi_send_byte(0x02, 0x2F)
            while True:
                currentTime = epd.getCurrentTimeTick() - startClock
                frameTime = currentTime - frameTime
                if frameTime > ft:
                    break
            
            if stage != 3 or currentTime > self.stageTime:
                break

#-------------------------------------------------------------------------------

    def displayImg(self, previousPicture, stage):
        dataBuffer = []
        idx = 0
        pre = self.PATTERNS[stage-1]
        post = self.PATTERNS[(stage+1) % len(self.PATTERNS)]
        for i in range(self.COG_Params.vertical): # for every line
            k = self.COG_Params.horizontal - 1
            for j in range (self.COG_Params.horizontal): # check every bit in the line
                tempByte = previousPicture[idx]
                idx += 1
                self.odd[j] = 0
                self.even[k] = 0
                for s in range(len(pre)):
                    self.odd[j] |= pre[s] if (tempByte & self.TESTS[0][s]) else post[s]
                    self.even[k] |= pre[s] if (tempByte & self.TESTS[1][s]) else post[s]
                k -= 1

            self.scan[i>>2] = self.scanTable[i%4]
            data = self.even + self.scan + self.odd
            data += bytearray(self.COG_Params.dataLineSize - len(data))
            dataBuffer.append(str(data))
            self.scan[i>>2] = self.NOTHING
        return dataBuffer      
            
#------------------------------------------------------------------------------- 
# Public functions
#-------------------------------------------------------------------------------

    def hwInit(self):
        epd.initDisplayHardware()

#-------------------------------------------------------------------------------

    def powerOn(self):

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

    def initializeDriver(self):
        sendBuffer = bytearray(2)
        self.setTemperature_Factor()

        epd.spi_send(0x01, str(self.COG_Params.channelSelect))

        epd.spi_send_byte(0x06, 0xff)
        epd.spi_send_byte(0x07, 0x9d)
        epd.spi_send_byte(0x08, 0x00)

        sendBuffer[0] = 0xd0
        sendBuffer[1] = 0x00
        
        epd.spi_send(0x09, str(sendBuffer))
        epd.spi_send_byte(0x04, self.COG_Params.voltageLevel)
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
    
    def display(self, newImg, prevImg):
        data = []
        for i in range(4):
            data.append(self.displayImg(prevImg if i < 2 else newImg, i%3+1))
        for stage, chunk in enumerate(data):
            self.sendData(stage, chunk)

#-------------------------------------------------------------------------------

    def powerOff(self):

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

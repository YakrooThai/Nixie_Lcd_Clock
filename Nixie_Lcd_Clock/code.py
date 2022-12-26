import board,busio
import digitalio
from time import sleep
from adafruit_st7735r import ST7735R
import displayio

import neopixel
import adafruit_ds3231

SDA = board.GP20
SCL = board.GP21
i2c = busio.I2C(SCL, SDA)
rtc = adafruit_ds3231.DS3231(i2c)

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
#----WS2812B
# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 17
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = 0.06

#----ST7735
mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin_FAKE = board.GP19

cs1 = digitalio.DigitalInOut(board.GP1)
cs1.direction = digitalio.Direction.OUTPUT
cs2 = digitalio.DigitalInOut(board.GP2)
cs2.direction = digitalio.Direction.OUTPUT
cs3 = digitalio.DigitalInOut(board.GP3)
cs3.direction = digitalio.Direction.OUTPUT
cs4 = digitalio.DigitalInOut(board.GP4)
cs4.direction = digitalio.Direction.OUTPUT

dc_pin = board.GP16
cs1.value = False
cs2.value = False
cs3.value = False
cs4.value = False

displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin_FAKE, reset=reset_pin)
display = ST7735R(display_bus, width=128, height=160, bgr = True)

Nixie_0 = displayio.OnDiskBitmap("/b00.bmp")
Nixie_1 = displayio.OnDiskBitmap("/b01.bmp")
Nixie_2 = displayio.OnDiskBitmap("/b02.bmp")
Nixie_3 = displayio.OnDiskBitmap("/b03.bmp")
Nixie_4 = displayio.OnDiskBitmap("/b04.bmp")
Nixie_5 = displayio.OnDiskBitmap("/b05.bmp")
Nixie_6 = displayio.OnDiskBitmap("/b06.bmp")
Nixie_7 = displayio.OnDiskBitmap("/b07.bmp")
Nixie_8 = displayio.OnDiskBitmap("/b08.bmp")
Nixie_9 = displayio.OnDiskBitmap("/b09.bmp")

#Enable
cs1.value = True
cs2.value = True
cs3.value = True
cs4.value = True
group = displayio.Group()
display.show(group)
COLOR = (0, 0, 0) 
RR = (250, 0, 0)  # color to blink
GG = (0, 250, 0)
BB = (0, 0, 250) 
pixels.fill((0, 0, 250))
pixels[9] = COLOR
pixels[10] = COLOR
pixels[11] = COLOR
pixels[12] = COLOR
pixels[14] = COLOR
pixels[15] = COLOR
pixels.show()
cntled = 0
def WsR(n):
    pixels[0] = RR
    pixels[1] = RR
    pixels[2] = RR
    pixels[3] = RR
    pixels[4] = RR
    pixels[5] = RR    
    pixels[6] = RR
    pixels[7] = RR
    pixels[8] = RR
    pixels[13] = RR
    pixels[16] = RR
    
def WsG(n):
    pixels[0] = GG
    pixels[1] = GG
    pixels[2] = GG
    pixels[3] = GG
    pixels[4] = GG
    pixels[5] = GG    
    pixels[6] = GG
    pixels[7] = GG
    pixels[8] = GG
    pixels[13] = GG
    pixels[16] = GG    

def WsB(n):
    pixels[0] = BB
    pixels[1] = BB
    pixels[2] = BB
    pixels[3] = BB
    pixels[4] = BB
    pixels[5] = BB    
    pixels[6] = BB
    pixels[7] = BB
    pixels[8] = BB
    pixels[13] = BB
    pixels[16] = BB
    
def digit(n):
    if n == 0:
        tile_grid = displayio.TileGrid(Nixie_0, pixel_shader=Nixie_0.pixel_shader)
    if n == 1:
        tile_grid = displayio.TileGrid(Nixie_1, pixel_shader=Nixie_0.pixel_shader)
    if n == 2:
        tile_grid = displayio.TileGrid(Nixie_2, pixel_shader=Nixie_0.pixel_shader)
    if n == 3:
        tile_grid = displayio.TileGrid(Nixie_3, pixel_shader=Nixie_0.pixel_shader)
    if n == 4:
        tile_grid = displayio.TileGrid(Nixie_4, pixel_shader=Nixie_0.pixel_shader)
    if n == 5:
        tile_grid = displayio.TileGrid(Nixie_5, pixel_shader=Nixie_0.pixel_shader)
    if n == 6:
        tile_grid = displayio.TileGrid(Nixie_6, pixel_shader=Nixie_0.pixel_shader)
    if n == 7:
        tile_grid = displayio.TileGrid(Nixie_7, pixel_shader=Nixie_0.pixel_shader)
    if n == 8:
        tile_grid = displayio.TileGrid(Nixie_8, pixel_shader=Nixie_0.pixel_shader)
    if n == 9:
        tile_grid = displayio.TileGrid(Nixie_9, pixel_shader=Nixie_0.pixel_shader)
        
    group.append(tile_grid)
    display.show(group)
    sleep(.2)
    group.remove(tile_grid)

# change to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
#    t = time.struct_time((2022, 12 , 26  , 10  , 48 , 20 , 0   , -1  , -1))
#    print("Setting time to:", t)  
#    rtc.datetime = t
#    print()
    
while True:
    t = rtc.datetime
    print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))

    Hmax = t.tm_hour / 10
    Hmin = t.tm_hour % 10
    MinH = t.tm_min / 10
    MinL = t.tm_min % 10
    
    cs1.value = False
    digit(int(Hmax)) 
    cs1.value = True
    sleep(.1)
    
    cs2.value = False
    digit(int(Hmin)) 
    cs2.value = True
    sleep(.1)
    
    cs3.value = False
    digit(int(MinH))
    cs3.value = True
    sleep(.1)
    
    cs4.value = False
    digit(int(MinL)) 
    cs4.value = True
    sleep(.2)    

    cntled=cntled+1
    if(cntled==1):
        WsR(0)
    if(cntled==2):
        WsG(0)
    if(cntled==3):
        WsB(0)
        cntled=0

    pixels[9] = COLOR
    pixels[10] = COLOR
    pixels[11] = COLOR
    pixels[12] = COLOR
    pixels[14] = COLOR
    pixels[15] = COLOR
    pixels.show()  
sleep(.2) 






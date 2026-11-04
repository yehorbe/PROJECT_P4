from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from filefifo import Filefifo
from led import Led
import micropython

micropython.alloc_emergency_exception_buf(200)

class Encoder:
    def __init__ (self, rot_A, rot_B):
        self.a = Pin(rot_A, Pin.IN)
        self.b = Pin(rot_B, Pin.IN)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler (self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
            
file = 'week3_data.txt'

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

samples_to_read = 1000
data = Filefifo(10, name=file)

oled.fill(0)
oled.show()

signal = Encoder(10,11)

x=0
y=0

min_val = None
max_val = None
samples =[]
start_index = 0

for i in range(samples_to_read):
    v = data.get()
    samples.append(v)

    if min_val is None or v < min_val:
        min_val = v
    if max_val is None or v > max_val:
        max_val = v

while True:
    while signal.fifo.has_data():
        value = signal.fifo.get()
        start_index += value
        if start_index < 0:
            start_index = 0
        if start_index > 1000 - 128:
            start_index = 872
    
    while signal.b.value() == 0:
        oled.fill(0)
        for x in range (128):
            v = samples[start_index + x]
            y = 63 - int (((v-min_val)/(max_val-min_val))*63)
            oled.pixel(x, int(y), 1)
            
        oled.show()


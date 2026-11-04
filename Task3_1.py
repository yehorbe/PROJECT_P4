from machine import Pin
from fifo import Fifo
from led import Led
import micropython 

micropython.alloc_emergency_exception_buf(200)

class Encoder:
    def __init__(self, rot_A, rot_B, rot_push):
        self.a = Pin(rot_A, Pin.IN)
        self.b = Pin(rot_B, Pin.IN)
        self.push = Pin(rot_push, Pin.IN, Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        
    def handler (self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

led = Led(22)
brightness = 50
last_push_state = 1
led_is_on = False
led.brightness(brightness)

signal = Encoder (10,11,12)

while True:
    if signal.push.value() == 0 and last_push_state == 1:
        last_push_state = signal.push.value()
        led_is_on = not led_is_on
        if led_is_on == True:
            led.on()
        if led_is_on == False:
            led.off()
    if signal.push.value() == 1 and last_push_state == 0:
        last_push_state = signal.push.value()
    while signal.fifo.has_data():
        value = signal.fifo.get()
        brightness += value * 5
        if brightness < 0:
            brightness = 0
        if brightness > 100:
            brightness = 100
        if led_is_on == True:
            led.brightness(brightness)

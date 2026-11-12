from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo
from piotimer import Piotimer

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

file = 'hr_capture01_250Hz.txt'        
data_fifo = Filefifo(10, name=file)
sample_flag = False

def timer_callback(t):
    global sample_flag
    sample_flag = True

timer = Piotimer(freq=250, callback=timer_callback)

scaling_window = []
scaling_min = None
scaling_max = None

pixel_batch = []
x = 0
prev_x = None
prev_y = None

oled.fill(0)
oled.show()

def scaler(val, min_v, max_v):
    if max_v == min_v:
        scaled = 0
    else:
        scaled = int((val - min_v) / (max_v - min_v) * 63)
    
    if scaled < 0:
        scaled = 0
    elif scaled > 63:
        scaled = 63
        
    return 63 - scaled

while True:
    if sample_flag:
        sample_flag = False
        
        raw_sample = data_fifo.get()
        
        scaling_window.append(raw_sample)
        if len(scaling_window) == 250:
            scaling_min = min(scaling_window)
            scaling_max = max(scaling_window)
            scaling_window.clear()
            
        curr_min = scaling_min
        curr_max = scaling_max
        
        pixel_batch.append(raw_sample)
        if len(pixel_batch) == 5:
            avg_val = sum(pixel_batch) / 5
            pixel_batch.clear()
            
            y = scaler(avg_val, curr_min, curr_max)
            
            if prev_x is not None and prev_y is not None:
                oled.line(prev_x, prev_y, x, y, 1)
            else:
                oled.pixel(x, y, 1)
                
            oled.show()
            
            prev_x = x
            prev_y = y
            x += 1
            
            if x >= 128:
                oled.fill(0)
                x = 0
                prev_x = None
                prev_y = None



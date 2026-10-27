from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo

def execute():
    SW_0 = Pin(9, Pin.IN, Pin.PULL_UP)
    SW_1 = Pin(8, Pin.IN, Pin.PULL_UP)
    SW_2 = Pin(7, Pin.IN, Pin.PULL_UP)

    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)

    file_name = ['sinewave_250Hz_01.txt', 'sinewave_250Hz_02.txt', 'sinewave_250Hz_03.txt']

    oled.fill(0)
    oled.text("Select file:", 0, 0)
    oled.text("SW0: File 1", 0, 9)
    oled.text("SW1: File 2", 0, 18)
    oled.text("SW2: File 3", 0, 27)
    oled.show()

    file_num = None

    while file_num is None:
        if SW_0.value() == 0:
            while SW_0.value() == 0:
                pass
            file_num = 0
        elif SW_1.value() == 0:
            while SW_1.value() == 0:
                pass
            file_num = 1
        elif SW_2.value() == 0:
            while SW_2.value() == 0:
                pass
            file_num = 2

    samples_to_read = 500
    data = Filefifo(10, name=file_name[file_num])

    min_val = None
    max_val = None

    for i in range(samples_to_read):
        v = data.get()

        if min_val is None or v < min_val:
            min_val = v
        if max_val is None or v > max_val:
            max_val = v

    threshold = min_val + ((max_val - min_val) / 2)

    below_threshold = True
    last_index = None
    counter = 0
    interval_periods = []

    oled.fill(0)
    oled.text("Calculating...", 0, 0)
    oled.show()

    while len(interval_periods) < 4:
        v = data.get()
        counter += 1

        if v < threshold:
            below_threshold = True

        if v >= threshold and below_threshold:
            below_threshold = False
            if last_index is not None:
                wave_period = counter - last_index
                interval_periods.append(wave_period)
            last_index = counter

    period_avg = sum(interval_periods) / float(len(interval_periods))
    freq = 250 / period_avg

    oled.fill(0)

    for i in range(4):
        per = interval_periods[i]
        ms = per * 4
        text_line = f"{i+1})int:{per}-{ms}ms"
        oled.text(text_line, 0, i * 9)

    oled.text(f"freq {freq:.4f}Hz", 0, 45)
    oled.show()

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo

SW_0 = Pin(9, Pin.IN, Pin.PULL_UP)
SW_1 = Pin(8, Pin.IN, Pin.PULL_UP)
SW_2 = Pin(7, Pin.IN, Pin.PULL_UP)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
a
oled.fill(0)
oled.text("-----SELECT-----:", 0, 0)
oled.text("SW0: Task 1", 0, 12)
oled.text("SW1: Task 2", 0, 21)
oled.text("SW2: Task 3", 0, 30)
oled.show()

while True:
    if SW_0.value() == 0:
        while SW_0.value() == 0:
            pass
        import Task2_1
        Task2_1.execute()
        break

    elif SW_1.value() == 0:
        while SW_1.value() == 0:
            pass
        import Task2_2
        Task2_2.execute()
        break

    elif SW_2.value() == 0:
        while SW_2.value() == 0:
            pass
        import Task2_3
        Task2_3.execute()
        break


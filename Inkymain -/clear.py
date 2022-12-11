#!/usr/bin/env python3
#Program to clear the screen

import time
from PIL import Image
from inky.inky_uc8159 import Inky
inky = Inky()

for _ in range(2):
    inky.set_border(1)
    img = Image.open("/home/pi/InkyGiftbytim/img/whiteC.jpg")
    inky.set_image(img)
    inky.show()
    time.sleep(2)

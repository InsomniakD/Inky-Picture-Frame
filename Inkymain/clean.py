#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Program to clean the screen if there is ghost


import time

from PIL import Image
from inky.inky_uc8159 import Inky

inky = Inky()

for i in range(2):
        inky.set_border(4)
        img = Image.open("/home/pi/InkyGiftbytim/img/redC.jpg")
        inky.set_image(img)
        inky.show()
        time.sleep(3)
        inky.set_border(0)
        img = Image.open("/home/pi/InkyGiftbytim/img/blackC.jpg")
        inky.set_image(img)
        inky.show()
        time.sleep(3)
        inky.set_border(1)
        img = Image.open("/home/pi/InkyGiftbytim/img/whiteC.jpg")
        inky.set_image(img)
        inky.show()
        time.sleep(2)
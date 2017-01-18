#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import nfc
import time
import led
colors = [0x4CE187, 0xF52832]
R = 17
G = 18
B = 27

def read():
    led.setColor(col[0])
    cardId=nfc.readNfc()
    led.setColor(col[1])
    return cardId
  
if __name__ == "__main__":
	try:
		led.setup(R, G, B)
    		print(led.read())
	except KeyboardInterrupt:
		destroy()

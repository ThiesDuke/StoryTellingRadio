#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import nfc
import time
import led
import pygame
import os
colors = [0x4CE187, 0xF52832]
R = 17
G = 18
B = 27
global cardId
global BackGroundMusicArray

def read():
    led.setColor(colors[0])
    cardId=nfc.readNfc()
    led.setColor(colors[1])
    return cardId

def setup():
	pygame.mixer.pre_init(44100, -16, 2, 512)
    	pygame.mixer.init()
    	pygame.mixer.music.set_volume(0.5)
    	filepath_music = "/home/pi/share/StoryTellingRadio2/content/"
	BackGroundMusicArray=[]
    	BackGroundMusicArrayCount=0
    	for filename in sorted(os.listdir(filepath_music)):
        	BackGroundMusicArray.append(filepath_music + filename)
	print("Setup done")

def run():
	while True:
	       CardIdentification= str(read())
            #if (cardId == "616630126192"):
            #   pygame.mixer.music.load(BackGroundMusicArray[0])
            #   print("CardOne")
            #if (cardId != "616630126192"):
            #    pygame.mixer.music.load(BackGroundMusicArray[1])
            #    print("CardTwo")
        print("something")
        pygame.mixer.music.play()
        time.sleep(3)
        led.setColor(colors[0])


if __name__ == "__main__":
    try:
        led.setup(R, G, B)
        setup()
	run()
    except KeyboardInterrupt:
        destroy()

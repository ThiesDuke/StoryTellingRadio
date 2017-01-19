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

def read():
    led.setColor(col[0])
    cardId=nfc.readNfc()
    led.setColor(col[1])
    return cardId

def run():
	pygame.mixer.pre_init(44100, -16, 2, 512)
	pygame.mixer.init()
	pygame.mixer.music.set_volume(0.5)
	filepath_music = "/home/pi/share/StoryTellingRadio/audio/"
	for filename in sorted(os.listdir(filepath_music)):
		BackGroundMusicArray.append(filepath_music + filename)
	BackGroundMusicArrayCount = 0
	pygame.mixer.music.load(BackGroundMusicArray[BackGroundMusicArrayCount])
	pygame.mixer.music.set_volume(0.7)
	pygame.mixer.music.play()
	time.sleep(3)
	while TRUE:
		nfc.read()
		pygame.mixer.music.stop()
		pygame.mixer.music.load(BackGroundMusicArray[CardId])
		pygame.mixer.music.play()
		time.sleep(1800)
		led.setColor(col[0])
  
if __name__ == "__main__":
	try:
		led.setup(R, G, B)
    		run()
	except KeyboardInterrupt:
		destroy()

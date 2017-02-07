#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
import led
import pygame
import os
import signal
import MFRC522

colors = [0x0000FF, 0xFF0000]
R = 17
G = 18
B = 27
global cardId
global BackGroundMusicArray
global reading

def read():
    global reading
    led.setColor(colors[0])
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status,backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        MIFAREReader.AntennaOff()
        led.setColor(colors[1])
        reading = False
        return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])

def setup():
    global BackGroundMusicArray
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    filepath_music = "/home/pi/share/StoryTellingRadio2/content/"
    BackGroundMusicArray=[]
    BackGroundMusicArrayCount=0
    for filename in sorted(os.listdir(filepath_music)):
        BackGroundMusicArray.append(filepath_music + filename)    

def run():
    global BackGroundMusicArray
    global reading
    music_list = {
        "136419912051": BackGroundMusicArray[0],
        "136416012084": BackGroundMusicArray[1],        
        "1364152120108": BackGroundMusicArray[0],
        "136419812050": BackGroundMusicArray[1],
        "1364159120107": BackGroundMusicArray[0],
        "616630126192": BackGroundMusicArray[1]
        }
    reading = True
    lastcardId = "initialized"
    while reading==True:
        cardId= read()
        if cardId != None and cardId != lastcardId:
            pygame.mixer.music.load(music_list[cardId])
            pygame.mixer.music.play()
            #print("music plays")
            time.sleep(10)
            led.setColor(colors[0])
            reading = True
            lastcardId = cardId
        elif cardId == lastcardId:
            pygame.mixer.music.stop()
            #print("music stopped")
            led.setColor(colors[1])
            time.sleep(1)
            led.setColor(colors[0])
            reading = True

def destroy():
    global BackGroundMusicArray
    BackGroundMusicArray = []
    GPIO.cleanup()                     # Release resource

if __name__ == "__main__":
    try:
        led.setup(R, G, B)
        setup()
        run()
    except KeyboardInterrupt:
        destroy()
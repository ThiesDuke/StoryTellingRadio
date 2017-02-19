#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
import led
#import led as led2
import pygame
import os
import signal
import MFRC522
from rotary_encoder import RotaryEncoder
import multiprocessing as mp
from multiprocessing import Process
from threading import Thread

pin_a = 22
pin_b = 23
colors = [0x0000FF, 0xFF0000]
R = 17
G = 18
B = 27
GPIO_Button = 12
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

def rfid_chip():
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
            lastcardId = cardId
        elif cardId == lastcardId:
            pygame.mixer.music.stop()
            #print("music stopped")
            led.setColor(colors[1])
            time.sleep(1)
            led.setColor(colors[0])

def encoder():
    encoder = RotaryEncoder(pin_a, pin_b)
    ts = time.time()
    i = 0
    last_position = 1
    led.setup(R, G, B)
    led.setColor(colors[0])
    redPart = 1
    greenPart = 1
    bluePart = 255

    while True:
        encoder.update()
        if encoder.check_state_change():
            if encoder.at_rest:
                speed = time.time() - ts
                ts = time.time()
                print 'speed:', speed, i
                direction = 10
                if encoder.current_rotation > last_position:
                    i += 1
                    colorchanger = i*-1
                    direction = 1
                    redPart = redPart+20
                    greenPart = greenPart+20
                elif encoder.current_rotation < last_position:
                    colorchanger = i*-1
                    i -= 1
                    direction = 0
                    redPart = redPart-20
                    greenPart = greenPart-20
                redPart = clamp(redPart)
                greenPart = clamp(greenPart)
                bluePart= clamp(bluePart)
                Multicolor1 = int('%02x%02x%02x' % (redPart,greenPart,bluePart),16)
                led.setColor(Multicolor1)  
                last_position = encoder.current_rotation

def clamp(x):
    return max(0, min(x, 255))

def destroy():
    global BackGroundMusicArray
    BackGroundMusicArray = []
    GPIO.cleanup()                     # Release resource

if __name__ == "__main__":
    try:
        led.setup(R, G, B)
        setup()
        #run()
        #ThreadA = Thread(target= encoder)
        #ThreadB = Thread(target= rfid_chip)
        #ThreadB.run()
        #time.sleep(5)
        #ThreadA.run()
        #ThreadA.join()
        #ThreadB.join()
        mp.set_start_method('fork')
        p = mp.Process(target=encoder)
        p2= mp.Process(target=rfid_chip)
        p.start()
        p2.start()
        #p.join()
        #Process(target=main).start()
    except KeyboardInterrupt:
        destroy()
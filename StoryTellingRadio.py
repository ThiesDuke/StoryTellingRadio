#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
import led
#import pygame
import os
import signal
import MFRC522
from rotary_encoder import RotaryEncoder

pin_a = 22
pin_b = 23
R = 17
G = 18
B = 27
GPIO_Button = 12
global reading
global lockstate
global last_position
last_position = 1

def read():
    global reading
    global lockstate
    #print("called read")
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status,backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        MIFAREReader.AntennaOff()
        return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])

def led_control(playerstate):
    global lockstate
    lockstate = True
    print("called led_control")
    led_colors = [0x00FF00, 0xFF0000]
    led.setup(R, G, B)
    redPart = 1
    greenPart = 1
    bluePart = 255
    if playerstate == "rfid_ready":
        show_led = led_colors[0]
    elif playerstate == "rfid_busy":
        show_led = led_colors[1]
    elif playerstate == "encoder_up":
        redPart = redPart+20
        greenPart = greenPart+20
        redPart = clamp(redPart)
        greenPart = clamp(greenPart)
        bluePart= clamp(bluePart)
        Multicolor1 = int('%02x%02x%02x' % (redPart,greenPart,bluePart),16)
        show_led = Multicolor1
    elif playerstate == "encoder_down":
        redPart = redPart-20
        greenPart = greenPart-20
        redPart = clamp(redPart)
        greenPart = clamp(greenPart)
        bluePart= clamp(bluePart)
        Multicolor1 = int('%02x%02x%02x' % (redPart,greenPart,bluePart),16)
        show_led = Multicolor1
    led.setColor(show_led)
    lockstate = False

def rfid_chip():
    global reading
    global lockstate
    print("called rfid_chip")
    led_control("rfid_ready")
    #pygame.mixer.pre_init(44100, -16, 2, 512)
    #pygame.mixer.init()
    #pygame.mixer.music.set_volume(0.5)
    filepath_music = "/home/pi/share/StoryTellingRadio2/content/"
    BackGroundMusicArray=[]
    BackGroundMusicArrayCount=0
    for filename in sorted(os.listdir(filepath_music)):
        BackGroundMusicArray.append(filepath_music + filename)
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
            print("reading successful")
            #pygame.mixer.music.stop()
            #pygame.mixer.music.load(music_list[cardId])
            #pygame.mixer.music.play()
            print("music plays")
            if lockstate == False:
                led_control("rfid_busy")
            time.sleep(10)
            lastcardId = cardId
            if lockstate == False:
                led_control("rfid_ready")

def setup_rotary_encoder():
    global encoder
    encoder = RotaryEncoder(pin_a, pin_b)
    

def detect(chn):
    global lockstate
    global last_position
    global encoder
    print("called detect")
    ts = time.time()
    i = 0
    #while True:
    encoder.update()
    if encoder.check_state_change():
        print("state_change")
        if encoder.at_rest:
            print("at_rest")
            speed = time.time() - ts
            ts = time.time()
            direction = 10
            if encoder.current_rotation > last_position:
                i += 1
                direction = 1
                print("louder")
            elif encoder.current_rotation < last_position:
                i -= 1
                direction = 0
                print("lower")
            last_position = encoder.current_rotation

def detect_btn(chn):
    print("music mute/unmute")

def clamp(x):
    return max(0, min(x, 255))

def destroy():
    global BackGroundMusicArray
    BackGroundMusicArray = []
    GPIO.cleanup()                     # Release resource

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
        GPIO.add_event_detect(pin_a, GPIO.FALLING, callback=detect, bouncetime=1) 
        GPIO.setup(pin_b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
        GPIO.add_event_detect(pin_b, GPIO.RISING, callback=detect, bouncetime=1)
        GPIO.setup(GPIO_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
        GPIO.add_event_detect(GPIO_Button, GPIO.FALLING, callback=detect_btn, bouncetime=300) 
        setup_rotary_encoder()
        rfid_chip()
    except KeyboardInterrupt:
        destroy()
#!/usr/bin/env python

"""Example on how to use RotaryEncoder lib"""

from pprint import pprint
import time
import led
from rotary_encoder import RotaryEncoder


# physical pin numbers
pin_a = 22
pin_b = 23
colors = [0x0000FF, 0xFF0000]
R = 17
G = 18
B = 27

def main(encoder):
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
    main(encoder)

def clamp(x):
    return max(0, min(x, 255))

if __name__ == '__main__':
    encoder = RotaryEncoder(pin_a, pin_b)

    try:
        main(encoder)
    except KeyboardInterrupt:
        encoder.cleanup()
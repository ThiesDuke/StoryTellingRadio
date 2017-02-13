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
Multicolor = None

#test
# delay in seconds before stopping playback
crank_delay = 3


def main(encoder):
    global Multicolor
    ts = time.time()
    i = 0
    last_position = 1
    led.setup(R, G, B)
    led.setColor(colors[0])

    while True:
        encoder.update()
        if encoder.check_state_change():
            # encoder state changed

            # only take action once per full click advance
            if encoder.at_rest:
                # update timestamp, continue playback
                # speed is seconds since last click
                speed = time.time() - ts
                ts = time.time()
                #i += 1
                print 'speed:', speed, i

                # check rotation direction
                bluePart = int(i)*10
                if bluePart <1:
                    bluePart = 1
                elif bluePart >255:
                    bluePart = 254
                if encoder.current_rotation > last_position:
                    i += 1
                    direction = 1
                    Multicolor = int(str(bluePart),16)
                elif encoder.current_rotation < last_position:
                    i -= 1
                    direction = 0
                    bluePart = i*16
                    Multicolor = int(str(bluePart),16)
                print(bluePart)
                print(Multicolor)
                led.setColor(Multicolor)


                last_position = encoder.current_rotation
                Multicolor = int("FFFFFF",16)

                # put playback code here
                if i % 3 == 0 and direction == 1:
                    # one frame every 3 clicks
                    print 'play next frame'
                elif i % 3 == 0 and direction == 0:
                    # one frame backward
                    print 'play previous frame'

        else:
            # encoder state not changed, check timeout value
            if time.time() - ts >= crank_delay:
                # timeout value reached, stop playback
                break

    print '3 sec pause detected'

    # put playback stop code here
    print 'playback stopped'

    # this will start the loop over
    main(encoder)


if __name__ == '__main__':
    encoder = RotaryEncoder(pin_a, pin_b)

    try:
        main(encoder)
    except KeyboardInterrupt:
        encoder.cleanup()
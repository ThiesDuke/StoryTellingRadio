#!/usr/bin/env python

"""Example on how to use RotaryEncoder lib"""

from pprint import pprint
import time
from rotary_encoder import RotaryEncoder


# physical pin numbers
pin_a = 22
pin_b = 23

# delay in seconds before stopping playback
crank_delay = 3


def main(encoder):
    ts = time.time()
    i = 0
    last_position = 1

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
                i += 1
                print 'speed:', speed, i

                # check rotation direction
                if encoder.current_rotation > last_position:
                    i += 1
                    direction = 1
                elif encoder.current_rotation < last_position:
                    i -= 1
                    direction = 0

                last_position = encoder.current_rotation

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
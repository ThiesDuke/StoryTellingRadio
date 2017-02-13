#!/bin/env python

import RPi.GPIO as gpio

class RotaryEncoder(object):
    def __init__(self, pin_a, pin_b):
        '''Provide the GPIO pins as integers that
        correspond to the physical location on board.'''
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.global_counter = int()
        self.resting_state = True
        self.last_state_a = 1
        self.last_state_b = 1
        self.current_state_a = 1
        self.current_state_b = 1
        self._leading_lagging_state = ((1, 0), (0, 1))
        self._mid_rotation_state = (0, 0)
        self._resting_state = (1, 1)
        self.current_rotation = 0
        self._setup()
        self.get_current_state()
        print 'Rotary Encoder loaded'

    def update(self):
        # helper function for updating state
        self.get_current_state()
        self.check_last_state()

    def cleanup(self):
        gpio.cleanup()


    def get_current_state(self):
        '''Rotate last pin state and get current pin state.'''
        self.last_state_a = self.current_state_a
        self.last_state_b = self.current_state_b
        self.current_state_a = gpio.input(self.pin_a)
        self.current_state_b = gpio.input(self.pin_b)

    def check_last_state(self):
        '''Check for state change and update state variables'''
        if self.check_state_change():
            self._handle_state_change()

    def check_state_change(self):
        '''return true if state has changed, false if state is same'''
        if self.current_state == self.last_state:
            return False
        elif self.current_state != self.last_state:
            return True

    def _handle_state_change(self):
        if self.current_state == self._resting_state:
            self._handle_rotation_end()

        elif self.last_state == self._resting_state:
            self._handle_rotation_init()

    def _handle_rotation_init(self):
        if self.current_state == (1, 0):
            print 'anti-clockwise rotation started'

        elif self.current_state == (0, 1):
            print 'clockwise rotation started'

    def _handle_rotation_end(self):
        if self.last_state == (0, 1):
            print 'anti-clockwise rotation ended'
            self.current_rotation -= 1

        elif self.last_state == (1, 0):
            print 'clockwise rotation ended'
            self.current_rotation += 1


    def _setup(self):
        '''Initialize GPIO pins and settings'''
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin_a, gpio.IN)
        gpio.setup(self.pin_b, gpio.IN)

    @property
    def current_state(self):
        return (self.current_state_a, self.current_state_b)

    @property
    def last_state(self):
        return (self.last_state_a, self.last_state_b)

    @property
    def at_rest(self):
        if self.current_state == self._resting_state:
            return True
        else:
            return False
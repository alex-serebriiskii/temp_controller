#/usr/bin/python

import RPi.GPIO as GPIO
class breadboard(object):
    ''' 
    Breadboard driver class for setting up multiple thermocouples on a breadboard
    '''
    def __init__(self, cs_pin, clock_pin, board = GPIO.BOARD):
        '''Initialize shared pins
        Parameters:
        - cs_pin:    Chip Select (CS) / Slave Select (SS) pin (Any GPIO)(sleep/wake sensors)  
        - clock_pin: Clock (SCLK / SCK) pin (Any GPIO)
        Note: 3.3v and ground are also shared pins across the breadboard
        '''
        self.cs_pin = cs_pin
        self.clock_pin = clock_pin
        self.board = board

        #Initialize board-specific GPIO
        GPIO.setmode(self.board)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)

        # Pull chip select high to make chip inactive
        GPIO.output(self.cs_pin, GPIO.HIGH)

    def wake(self):
        # Toggle the chip to low for active
        GPIO.output(self.cs_pin, GPIO.LOW)

    def sleep(self):
        # Toggle the chip to high for inactive
        GPIO.output(self.cs_pin, GPIO.HIGH)
        
    def cleanup(self):
        '''Selective GPIO cleanup'''
        GPIO.setup(self.cs_pin, GPIO.IN)
        GPIO.setup(self.clock_pin, GPIO.IN)

class breadboardError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

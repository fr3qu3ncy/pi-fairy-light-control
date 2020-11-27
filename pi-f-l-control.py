#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LedPin_1 = 18   # pin12 --- led fairy lights 1
LedPin_2 = 19   # pin35 --- led fairy lights 2
LedPin_3 = 20   # pin38 --- led fairy lights 1

BtnPin = 2     # pin12 --- button

Led_status = 1

def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by Broadcom numbering. (GPIO.Board) would nubmer by physical location.
    GPIO.setup(LedPin_1,GPIO.OUT)   # Set LedPin_1's mode is output
    GPIO.setup(LedPin_2,GPIO.OUT)   # Set LedPin_2's mode is output
    GPIO.setup(LedPin_3,GPIO.OUT)   # Set LedPin_3's mode is output
    GPIO.setup(BtnPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    
    GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) to off led
    time.sleep(1)
    GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) to off led
    time.sleep(1)
    GPIO.output(LedPin_3,GPIO.HIGH) # Set LedPin_3 high(+3.3V) to off led
    GPIO.output(LedPin_1,GPIO.LOW)
    time.sleep(1)
    GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) to off led
    GPIO.output(LedPin_2,GPIO.LOW)
    time.sleep(1)
    GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) to off led
    GPIO.output(LedPin_3,GPIO.LOW)
    time.sleep(2)
    GPIO.output(LedPin_1,GPIO.LOW)
    GPIO.output(LedPin_2,GPIO.LOW)

def swLed(ev=None):
	global Led_status
	Led_status = not Led_status
	GPIO.output(LedPin_1, Led_status)  # switch led status(on-->off; off-->on)
	if Led_status == 1:
		print('led off...')
	else:
		print('...led on')

def loop():
	GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=swLed, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		time.sleep(1)   # Don't do anything

def destroy():
	GPIO.output(LedPin_1, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

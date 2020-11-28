#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import threading

LedPin_1 = 18   # pin12 --- led fairy lights 1
LedPin_2 = 19   # pin35 --- led fairy lights 2
LedPin_3 = 20   # pin38 --- led fairy lights 1
BtnPin = 2     # pin12 --- button
Led_status = 1
led_thread_type = "none"         #Type of lighting thread to run. [none, all, rotate, twinkle] This is to controll stopping thread

def testCode():
    global led_thread_type
    on_rotate()
    time.sleep(5)
    on_rotate()
    time.sleep(5)
    off_all()
    time.sleep(5)
    on_rotate()
    time.sleep(5)
    on_all()
    time.sleep(5)
    off_all()
    time.sleep(1)
    #destroy()

def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by Broadcom numbering. (GPIO.Board) would nubmer by physical location.
    GPIO.setup(LedPin_1,GPIO.OUT)   # Set LedPin_1's mode is output
    GPIO.setup(LedPin_2,GPIO.OUT)   # Set LedPin_2's mode is output
    GPIO.setup(LedPin_3,GPIO.OUT)   # Set LedPin_3's mode is output
    GPIO.setup(BtnPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    
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
    GPIO.output(LedPin_1, GPIO.LOW)     # led_1 off
    GPIO.output(LedPin_2, GPIO.LOW)     # led_2 off
    GPIO.output(LedPin_3, GPIO.LOW)     # led_3 off
    GPIO.cleanup()                     # Release resource

def off_all():
    global led_thread_type
    led_thread_type = "none"
    GPIO.output(LedPin_1,GPIO.LOW)
    GPIO.output(LedPin_2,GPIO.LOW)
    GPIO.output(LedPin_3,GPIO.LOW)
    print("Led Thread none (no thread started)")

def on_all():
    global led_thread_type
    global led_thread
    if led_thread_type!="all":
        led_thread_type = "all"
        try:                        # If led thread is runing then stop it.
            led_thread.isAlive()
            time.sleep(1)
            print("Thread was running.. but should stop???")
            led_thread.join()
        except NameError:
            print("Thread not running")
        
        led_thread = threading.Thread(target=start_thread_all) # Start new led thread
        led_thread.start()
        print("Led Thread All STARTED")
    else:
        print("Led Thread All alreaday running")
    time.sleep(1)
    print("Led Thread All (no thread started)")

def on_rotate():
    global led_thread_type
    global led_thread
    if led_thread_type!="rotate":
        led_thread_type = "rotate"
        try:                        # If led thread is runing then stop it.
            led_thread.isAlive()
            time.sleep(1)
            print("Thread was running.. but should stop???")
            led_thread.join()
        except NameError:
            print("Thread not running")
        
        led_thread = threading.Thread(target=start_thread_rotate) # Start new led thread
        led_thread.start()
        print("Led Thread Rotate STARTED")
    else:
        print("Led Thread Rotate alreaday running")

def start_thread_rotate():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "rotate":
            time.sleep(thread_sleep)
            print(led_thread_type)
            # break

    while led_thread_type == "rotate":
        GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) to off led
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) to off led
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_3,GPIO.HIGH) # Set LedPin_3 high(+3.3V) to off led
        GPIO.output(LedPin_1,GPIO.LOW)
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) to off led
        GPIO.output(LedPin_2,GPIO.LOW)
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) to off led
        GPIO.output(LedPin_3,GPIO.LOW)
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_3,GPIO.HIGH) # Set LedPin_2 high(+3.3V) to off led
        check_thread_type_and_sleep(1)
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_1,GPIO.LOW)
        GPIO.output(LedPin_2,GPIO.LOW)
        GPIO.output(LedPin_3,GPIO.LOW)
        check_thread_type_and_sleep(1)

def start_thread_all():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "all":
            time.sleep(thread_sleep)
            print(led_thread_type)
            # break

    while led_thread_type == "all":
        GPIO.output(LedPin_1,GPIO.HIGH)
        GPIO.output(LedPin_2,GPIO.HIGH)
        GPIO.output(LedPin_3,GPIO.HIGH)
        check_thread_type_and_sleep(1)

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        testCode()
        loop()
    except KeyboardInterrupt:
        destroy()
    finally:
        destroy()
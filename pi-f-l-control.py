#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import threading
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import errno

version = "0.1"

LedPin_1 = 18       # pin12 --- led fairy lights 1
LedPin_2 = 19       # pin35 --- led fairy lights 2
LedPin_3 = 20       # pin38 --- led fairy lights 1
BtnPin_cycle = 23   # pin16 --- button

led_thread_type = "none"    # Type of lighting thread to run. [none, all, rotate, twinkle] This is to controll stopping thread
led_cycle_type = 0          # Index of the LED patten to be showing. 0=none, 1=all, 2=rotate, 3=twinkle    

logging
log_path = "/var/log/pi-fairy-light-control/"
log_file = "pi-f-l-control.log"

## Test code, not to be using in a release.
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

## Set up the GPIO Pins
def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by Broadcom numbering. (GPIO.Board) would nubmer by physical location.
    GPIO.setup(LedPin_1,GPIO.OUT)   # Set LedPin_1's mode is output
    GPIO.setup(LedPin_2,GPIO.OUT)   # Set LedPin_2's mode is output
    GPIO.setup(LedPin_3,GPIO.OUT)   # Set LedPin_3's mode is output
    GPIO.setup(BtnPin_cycle,GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin_cycle's mode is input, and pull up to high level (3.3v)

## Handler for button presssed.
def cycle_btn_pressed(ev=None):
    global led_cycle_type
    global led_thread_type
    if led_cycle_type == 0:
        led_cycle_type = 1
        on_all()
    elif led_cycle_type == 1:
        led_cycle_type = 2
        on_rotate()
    elif led_cycle_type == 2:
        led_cycle_type = 0
        off_all()
    else:
        logging.info("Some issue with led_cycle_type")
        pass
    # to-do add led_cycle_type = 3,4,5,6,erc...
	logging.info("button pressed")

## Main loop, adds event handler for button press.
def loop():
	GPIO.add_event_detect(BtnPin_cycle, GPIO.FALLING, callback=cycle_btn_pressed, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		time.sleep(1)   # Don't do anything

## clean up GPIO pins
def destroy():
    GPIO.output(LedPin_1, GPIO.LOW)     # led_1 off
    GPIO.output(LedPin_2, GPIO.LOW)     # led_2 off
    GPIO.output(LedPin_3, GPIO.LOW)     # led_3 off
    GPIO.cleanup()                     # Release resource

##
## Functions to handle diffferent lighting effects
##

def off_all():
    global led_thread_type
    led_thread_type = "none"
    GPIO.output(LedPin_1,GPIO.LOW)
    GPIO.output(LedPin_2,GPIO.LOW)
    GPIO.output(LedPin_3,GPIO.LOW)
    logger.info("Led Thread: none - (no thread started)")

def on_all():
    global led_thread_type
    global led_thread
    if led_thread_type!="all":
        led_thread_type = "all"
        try:                        # If led thread is runing then stop it.
            led_thread.isAlive()
            time.sleep(0.05)
            logger.info("Thread was running.. but should stop???")
            led_thread.join()
        except NameError:
            logger.info("Thread not running")
        
        led_thread = threading.Thread(target=start_thread_all) # Start new led thread
        led_thread.start()
    else:
        logger.info("Led Thread: All - alreaday running")
    time.sleep(1)

def on_rotate():
    global led_thread_type
    global led_thread
    if led_thread_type!="rotate":
        led_thread_type = "rotate"
        try:                        # If led thread is runing then stop it.
            led_thread.isAlive()
            time.sleep(0.05)
            logger.debug("Thread was running.. but should stop???")
            led_thread.join()
        except NameError:
            logger.info("Thread not running")
        
        led_thread = threading.Thread(target=start_thread_rotate) # Start new led thread
        led_thread.start()
    else:
        logger.info("Led Thread: Rotate - alreaday running")

## Functions for light pattern threads
def start_thread_rotate():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "rotate":
            time.sleep(thread_sleep)
            logger.debug(led_thread_type)
            # break
    logger.info("Led Thread: Rotate - STARTED")
    while led_thread_type == "rotate":
        GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) to off led
        GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) to off led
        GPIO.output(LedPin_3,GPIO.LOW)
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
        GPIO.output(LedPin_1,GPIO.LOW)
        GPIO.output(LedPin_2,GPIO.LOW)
        GPIO.output(LedPin_3,GPIO.LOW)
        check_thread_type_and_sleep(1)
    logger.info("Led Thread: Rotate - STOP")

def start_thread_all():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "all":
            time.sleep(thread_sleep)
            logger.debug(led_thread_type)
            # break
    logger.info("Led Thread: All - STARTED")
    while led_thread_type == "all":
        GPIO.output(LedPin_1,GPIO.HIGH)
        GPIO.output(LedPin_2,GPIO.HIGH)
        GPIO.output(LedPin_3,GPIO.HIGH)
        check_thread_type_and_sleep(1)
    logger.info("Led Thread: All - STOP")
##
## Logging
##
def log_create():
    global logger
    mkdir_p(log_path)
    format = "%(asctime)s.%(msecs)03d %(levelname)s %(process)d (%(name)s-%(threadName)s) %(message)s (linuxThread-%(thread)d)"
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    log_handler = TimedRotatingFileHandler(log_path + log_file, when="midnight", interval=1, backupCount=30)
    log_handler.setFormatter(logging.Formatter(format))
    #logger.setFormatter(format)
    logger.addHandler(log_handler)
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%m/%d/%Y %H:%M:%S")

def log_create_stdout():
    format = "%(asctime)s.%(msecs)03d %(levelname)s %(process)d (%(name)s-%(threadName)s) %(message)s (linuxThread-%(thread)d)"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%m/%d/%Y %H:%M:%S")

def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

if __name__ == '__main__':     # Program start from here
    log_create()
    #log_create_stdout()
    logger.info("Start up...")
    logger.info("pi-fairy-lights : version v%s : STARTED", version)
    setup()
    try:
        #testCode()
        loop()
    except KeyboardInterrupt:
        destroy()
    finally:
        logger.info("pi-fairy-lights : version v%s : EXIT", version)
        destroy()
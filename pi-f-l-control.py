#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import threading
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import errno

version = "v1.0.0"

LedPin_1 = 18       # pin12 --- led fairy lights 1
LedPin_2 = 19       # pin35 --- led fairy lights 2
LedPin_3 = 20       # pin38 --- led fairy lights 1
BtnPin_cycle = 23   # pin16 --- button

led_thread_type = "none"    # Type of lighting thread to run. [none, all, rotate, twinkle fast, twinkle medium, twinkle slow, sparkle fast, sparkle medium, sparkle slow] This is to controll stopping thread
led_cycle_type = 0          # Index of the LED patten to be showing. 0=none, 1=all, 2=rotate, 3=twinkle fast, 4=twinkle medium, 5=twinkle slow, 6=sparkle fast, 7=sparkle medium, 8=sparkle slow.

logging
log_path = "/var/log/pi-fairy-light-control/"
log_file = "pi-f-l-control.log"

## Set up the GPIO Pins
def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by Broadcom numbering. (GPIO.Board) would nubmer by physical location.
    GPIO.setup(LedPin_1,GPIO.OUT)   # Set LedPin_1's mode is output
    GPIO.setup(LedPin_2,GPIO.OUT)   # Set LedPin_2's mode is output
    GPIO.setup(LedPin_3,GPIO.OUT)   # Set LedPin_3's mode is output
    GPIO.setup(BtnPin_cycle,GPIO.IN)    # Set BtnPin_cycle's mode is input.

## Handler for button presssed.
def btn_pressed_cycle(ev=None):
    global led_cycle_type
    global led_thread_type
    logger.info("Button pressed - cycle pattern")
    if led_cycle_type == 0:
        led_cycle_type = 1
        on_all()
    elif led_cycle_type == 1:
        led_cycle_type = 2
        on_rotate()
    elif led_cycle_type == 2:
        led_cycle_type = 3
        on_twinkle(0.5) # twinkle fast 0.5 second
    elif led_cycle_type == 3:
        led_cycle_type = 4
        on_twinkle(1) # twinkle medium 1 seconds
    elif led_cycle_type == 4:
        led_cycle_type = 5
        on_twinkle(2) # twinkle slow 2 seconds
    elif led_cycle_type == 5:
        led_cycle_type = 6
        on_sparkle(1) # sparkle 1 seconds
    elif led_cycle_type == 6:
        led_cycle_type = 7
        on_sparkle(2.5) # sparkle 2.5 seconds
    elif led_cycle_type == 7:
        led_cycle_type = 8
        on_sparkle(4) # sparkle 4 seconds
    elif led_cycle_type == 8:
        led_cycle_type = 0
        off_all()
    else:
        logger.info("Some issue with led_cycle_type")
        pass
    # to-do add led_cycle_type = 3,4,5,6,etc... as new patterns are added

## Main loop, adds event handler for button press.
def loop():
    GPIO.add_event_detect(BtnPin_cycle, GPIO.FALLING, callback=btn_pressed_cycle, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
    while True:
        time.sleep(1) # Don't do anything

## clean up GPIO pins
def destroy(): # Not woking! 
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

def on_twinkle(speed):
    global led_thread_type
    global led_thread
    global twinkle_speed
    twinkle_speed = speed # Update global variable to fast (0.5 sec) or slow (1 sec). Could be any number of seconds.
    if led_thread_type!="twinkle":
        led_thread_type = "twinkle"
        try:                        # If led thread is runing and not 'twinkle' then stop it.
            led_thread.isAlive()
            time.sleep(0.05)
            logger.debug("Thread was running.. but should stop???")
            led_thread.join()
        except NameError:
            logger.info("Thread not running")
        
        led_thread = threading.Thread(target=start_thread_twinkle) # Start new led thread
        led_thread.start()
    else:
        logger.info("Led Thread: Twinkle - alreaday running - Twinkle Speed %s secs", twinkle_speed) # If just updating twinkle_speed then we keep the twinkle thread running

def on_sparkle(speed):
    global led_thread_type
    global led_thread
    global sparkle_speed
    sparkle_speed = speed # Update global variable to fast (0.5 sec) or slow (1 sec). Could be any number of seconds.
    if led_thread_type!="sparkle":
        led_thread_type = "sparkle"
        try:                        # If led thread is runing and not 'sparkle' then stop it.
            led_thread.isAlive()
            time.sleep(0.05)
            logger.debug("Thread was running.. but should stop???")
            led_thread.join()
        except NameError:
            logger.info("Thread not running")
        
        led_thread = threading.Thread(target=start_thread_sparkle) # Start new led thread
        led_thread.start()
    else:
        logger.info("Led Thread: Sparkle - alreaday running - sparkle Speed %s secs", sparkle_speed) # If just updating sparkle_speed then we keep the sparkle thread running

## Functions for light pattern threads
def start_thread_rotate():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "rotate":
            time.sleep(thread_sleep)
            logger.debug(led_thread_type)
            # break
    logger.info("Led Thread: Rotate - STARTED")
    while led_thread_type == "rotate":
        # Turn on Light strings 1 and 2
        GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) turn on leds
        GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) turn on leds
        GPIO.output(LedPin_3,GPIO.LOW)
        check_thread_type_and_sleep(1)
        # Main rotate loop
        for n in range(0,13,1): 
            GPIO.output(LedPin_3,GPIO.HIGH) # Set LedPin_3 high(+3.3V) turn on leds
            GPIO.output(LedPin_1,GPIO.LOW)
            check_thread_type_and_sleep(1)
            GPIO.output(LedPin_1,GPIO.HIGH) # Set LedPin_1 high(+3.3V) turn on leds
            GPIO.output(LedPin_2,GPIO.LOW)
            check_thread_type_and_sleep(1)
            GPIO.output(LedPin_2,GPIO.HIGH) # Set LedPin_2 high(+3.3V) turn on leds
            GPIO.output(LedPin_3,GPIO.LOW)
            check_thread_type_and_sleep(1)
        # This section turns all light strings on, and then off, then the loop restarts
        GPIO.output(LedPin_3,GPIO.HIGH) # Set LedPin_2 high(+3.3V) turn on leds
        check_thread_type_and_sleep(1)
        GPIO.output(LedPin_1,GPIO.LOW)
        GPIO.output(LedPin_2,GPIO.LOW)
        GPIO.output(LedPin_3,GPIO.LOW)
        check_thread_type_and_sleep(1)
    logger.info("Led Thread: Rotate - STOP")

def start_thread_twinkle():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "twinkle":
            time.sleep(thread_sleep)
            logger.debug(led_thread_type)
            # break
    # Set up LED pins to be PWM so we can change the brightness
    led_pwm_1 = GPIO.PWM(LedPin_1,1000)
    led_pwm_1.start(0)
    led_pwm_2 = GPIO.PWM(LedPin_2,1000)
    led_pwm_2.start(0)
    led_pwm_3 = GPIO.PWM(LedPin_3,1000)
    led_pwm_3.start(0)
    logger.info("Led Thread: Twinkle - STARTED - Twinkle Speed %s secs", twinkle_speed)
    while led_thread_type == "twinkle":
        # led_value 0 to 100 (brighten)
        for pwm_value in range(0,101,1):
            pwm_value_2 = pwm_value + 49
            pwm_value_3 = pwm_value + 99
            if pwm_value_2 > 100: # vlaues over 100 decrease value
                pwm_value_2 = pwm_value_2 - ((pwm_value_2 - 100) * 2)
            if pwm_value_3 > 100: # values over 100 decrease value
                pwm_value_3 = pwm_value_3 - ((pwm_value_3 - 100) * 2)
            led_pwm_1.ChangeDutyCycle(pwm_value)
            led_pwm_2.ChangeDutyCycle(pwm_value_2)
            led_pwm_3.ChangeDutyCycle(pwm_value_3)
            check_thread_type_and_sleep(twinkle_speed / 100)
        # led_value 100 to 0 (dimm)
        for pwm_value in range(100,0,-1):
            pwm_value_2 = pwm_value - 49
            pwm_value_3 = pwm_value - 99
            if pwm_value_2 < 0: # values under 0, increase vlaue
                pwm_value_2 = abs(pwm_value_2)
            if pwm_value_3 < 0: # values under 0, increase vlaue
                pwm_value_3 = abs(pwm_value_3)
            led_pwm_1.ChangeDutyCycle(pwm_value)
            led_pwm_2.ChangeDutyCycle(pwm_value_2)
            led_pwm_3.ChangeDutyCycle(pwm_value_3)
            check_thread_type_and_sleep(twinkle_speed / 100)
    led_pwm_1.stop()
    led_pwm_2.stop()
    led_pwm_3.stop()
    logger.info("Led Thread: Twinkle - STOP")

def start_thread_sparkle():
    def check_thread_type_and_sleep(thread_sleep):
        if led_thread_type == "sparkle":
            time.sleep(thread_sleep)
            logger.debug(led_thread_type)
            # break
    # Set up LED pins to be PWM so we can change the brightness
    led_pwm_1 = GPIO.PWM(LedPin_1,1000)
    led_pwm_1.start(0)
    led_pwm_2 = GPIO.PWM(LedPin_2,1000)
    led_pwm_2.start(0)
    led_pwm_3 = GPIO.PWM(LedPin_3,1000)
    led_pwm_3.start(0)
    logger.info("Led Thread: Sparkle - STARTED - Sparkle Speed %s secs", sparkle_speed)
    # Set all LED strings to 50% brightness
    led_pwm_1.ChangeDutyCycle(50)
    led_pwm_2.ChangeDutyCycle(50)
    led_pwm_3.ChangeDutyCycle(50)
    # MAke the LED strings 'sparkle'
    while led_thread_type == "sparkle":
        for pwm_value in range(50,30,-1):               # LED string 2 dimmer
            led_pwm_2.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0003)
        for pwm_value in range(31,101,1):               # LED string 1 brighter
            led_pwm_1.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0033)
        for pwm_value in range(100,50,-1):              # LED string 1 dimmer
            led_pwm_1.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0033)
        check_thread_type_and_sleep(sparkle_speed / 6)  # Wait
        
        for pwm_value in range(50,30,-1):               # LED string 3 dimmer
            led_pwm_3.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0003)
        for pwm_value in range(31,101,1):               # LED string 2 brighter
            led_pwm_2.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0033)
        for pwm_value in range(100,50,-1):              # LED string 2 dimmer
            led_pwm_2.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0033)
        check_thread_type_and_sleep(sparkle_speed / 6)  # Wait
        
        for pwm_value in range(50,30,-1):               # LED string 1 dimmer
            led_pwm_1.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0003)
        for pwm_value in range(31,101,1):               # LED string 3 brighter
            led_pwm_3.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0033)
        for pwm_value in range(100,50,-1):              # LED string 3 dimmer
            led_pwm_3.ChangeDutyCycle(pwm_value)
            check_thread_type_and_sleep(0.0033)
        check_thread_type_and_sleep(sparkle_speed / 6)  # Wait

    led_pwm_1.stop()
    led_pwm_2.stop()
    led_pwm_3.stop()
    logger.info("Led Thread: Sparkle - STOP")

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
    #logger.setLevel(logging.INFO)
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
    logger.info("Starting up...")
    logger.info("pi-fairy-lights : version %s : STARTED", version)
    setup()
    try:
        #testCode()
        loop()
    except KeyboardInterrupt:
        logger.info("pi-fairy-lights : version %s : EXIT", version)
        destroy()
    finally:
        logger.info("pi-fairy-lights : version %s : EXIT", version)
        destroy()
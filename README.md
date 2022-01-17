# pi-fairy-light-control
Control low power 3v LED fairy lights / Christmas tree lights from a Raspberry Pi
Allows patten to be changed from a hardware button, and now also a web interface.

## About
This code requires 3 low power LED fairly light strings/strips that run at around 3v. Or to simply test or develop with this code 3 LEDs would work.

The [hardware list and circuit diagrams](https://github.com/fr3qu3ncy/pi-fairy-light-control#hardware) are both below

### Version
v2.0.1
### Features working:
* Control multiple light strings of fairy light connected to the GPIO pins.
* Threading of LED control.
* Patterns/effect - All on, Rotate, Twinkle (slow/medium/fast), Sparkle (slow/mediuam/fast), All off.
* Software PWM to allow fading in and out of light.
* Hardware button for on off / cycle through patterns
* Logging - rotating log to /var/logs/pi-fairy-light-control/pi-f-l-control.log
* Web interface to control light patterns (http://*hostname*:5000/)
### Features in progress
* none
### Features in to-do
* More differnt patterns and effects
* Smart Home Integration
    * Apple HomeKit intergration (can be controled on local network, **prefered**)
    * Alexa Skill for ccontrol from Echo devices (needs an **endpoint viable in the internet**, would want to run in IoT LAN or DMZ)
    * Philips Hue with a Zigby Hat/dongle. (Should then intergrate to Alexa/Apple/Google etc)
* Run as Daemon
* Install scripts
* BPM detaction options
* Photorisistor to control light strings at differnt light levels.

## Install Instructions
### Download and unzip latest release code
```
wget https://github.com/fr3qu3ncy/pi-fairy-light-control/archive/v2.0.1.tar.gz
tar -zxvf v2.0.1.tar.gz
rm v2.0.1.tar.gz
```

### Install Prerequisites (for python3)
```
sudo apt-get update
sudo apt-get -y install python3-rpi.gpio
sudo apt-get -y install python-pip
python3 -m pip install --upgrade pip
sudo pip3 install flask
```

### Run Code
```
cd pi-fairy-light-control-2.0.1/
python3 pi-f-l-control.py
```
You can run under python2.7 if you wish.

## Instructions
When you start the code `python3 pi-f-l-control.py` the LED lights will all be off, or lit in their last static state.

Pressing the button will cycle through the available patterns in the following order:
1. All On
1. Rotate
1. Twinkle Fast
1. Twinkle Medium
1. Twinkle Slow
1. Sparkle Fast
1. Sparkle Medium
1. Sparkle Slow
1. All Off

### Web Interfaace
New in **v2.0.0** and above there is a web interface to control the pattern running, and display the curently running pattern.

In a web browser, go to `http://hostname:5000/` replacing **hostname** with the hostname of your Raspberry Pi

<img alt="Pi Fairy Light Control Web Interface" src="https://user-images.githubusercontent.com/33297343/102696422-0c733780-4226-11eb-88a4-9ad3f81dfe27.png" width="50%">


To add the web interface as a web app to an iPhone or other iOS device, click the share button at the bottom, and select **Add to Home Screen**

<img alt="Pi Fairy Light Control Web Interface" src="https://user-images.githubusercontent.com/33297343/102696405-ea79b500-4225-11eb-80b1-6536186df2a4.png" width="50%">


## Hardware
### Parts List
* LED - Fairy Lights **x3** - Low voltage 3.3v fairly lights.
    * I used these [battery powered lights from Amazon UK](https://www.amazon.co.uk/gp/product/B08FSQDRJX/ref=ppx_yo_dt_b_asin_image_o04_s00?ie=UTF8&psc=1). I cut of the battery pack, and **crimped on Dupoint conenctors**.
* S - Push button
    * Any push button switch
* R 1-3 - 330 Ohms resistors **x3**
* R 4 - 1K Ohm resister **x1** - _Ptotect GPIO pin incase accidently set to output._
* R 5 - 10K Ohms resistor **x1** - _Pull up the state of the GPIO pin._
* Raspberry Pi
* Breadboard
* Dupoint connection cables (various)

### Circuit Diagram
![Pi Fairy Light Control Circuit diagram](https://user-images.githubusercontent.com/33297343/102684505-19197080-41d1-11eb-9976-910c02450e79.png)


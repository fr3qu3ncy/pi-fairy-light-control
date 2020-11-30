# pi-fairy-light-control
Control low power 3v fairy lights / Christmas tree lights from a Raspberry Pi

## About
This is still a work in proress, and in an Alpha state. the features listed as working below do work.
### Version
v0.2.1
### Features working:
* Control multiple light strings of fairy light connected to the GPIO pins
* Threading of LED control
* Some patterns/effect
* Hardware button for on off / cycle through patterns
* Logging
### Features in progress
* Software/hardware PWM to allow fading in and out of light (If the LED light strings suport this!)
### Features in to-do
* More differnt patterns and effects
* Software PWM to allow fading in and out of light (If the LED light strings suport this!)
* Smart Home Integration
    * Apple HomeKit intergration (can be controled on local network, **prefered**)
    * Alexa Skill for ccontrol from Echo devices (needs an **endpoint viable in the internet**, would want to run in IoT LAN or DMZ)
    * Philips hue with a Zigby Hat/dongle.
* Run as Daemon
* Install scripts
* Photorisistor to control light strings at differnt light levels.

## Install Instructions
### Download and unzip latest release code
```
wget https://github.com/fr3qu3ncy/pi-fairy-light-control/archive/v0.2.1.tar.gz
tar -zxvf v0.2.1.tar.gz
rm v0.2.1.tar.gz
```

### Install Prerequisites (for python3)
```
sudo apt-get update
sudo apt-get -y install python3-rpi.gpio
```

### Run Code
```
cd pi-fairy-light-control-0.2.1/
python3 pi-f-l-control.py
```
You can run under python2.7 if you wish.

## Hardware
### Parts List
* LED - Fairy Lights **x3** - Low voltage 3.3v fairly lights.
    * I used these [battery powered lights from Amazon UK](https://www.amazon.co.uk/gp/product/B08FSQDRJX/ref=ppx_yo_dt_b_asin_image_o04_s00?ie=UTF8&psc=1). I cut of the battery pack, and **crimped on Dupoint conenctors**.
* S - Push button
    * Any push button switch
* R - 330 Ohms resistors **x3**
* Raspberry Pi
* Breadboard
* Dupoint connection cables (various)

### Circuit Diagram
![Pi Fairy Light Control Circuit diagram](https://user-images.githubusercontent.com/33297343/100523077-6cd20480-31a5-11eb-9c0d-f8271f841109.png)


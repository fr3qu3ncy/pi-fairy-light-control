# pi-fairy-light-control
Control low power 3v fairy lights / Christmas tree lights from a Raspberry Pi

## About
This is still a work in proress, and in an Alpha state. the features listed as working below do work.
### Version
0.1
### Features working:
* Control multiple light strings of fairy light connected to the GPIO pins
* Threading of LED control
* Some patterns/effect
* Hardware button for on off / cycle through patterns
* Logging
### Features in progress
* none
### Features in to-do
* More differnt patterns and efects
* Software PWN to allow fading in and out of light (If the LED light strings suport this!)
* Apple HomeKit intergration (can be controled on local network, **prefered**)
* Alexa Skill for ccontrol from Echo devices (needs an **endpoint viable in the internet**, would want to run in IoT LAN or DMZ)
* Run as Daemon
* Install scripts
* Photorisistor to control light strings at differnt light levels.

## Hardware
### Parts List
* LED - Fairy Lights **x3** - Low voltage 3.3v fairly lights.
    * I used these [battery powered lights from Amazon UK](https://www.amazon.co.uk/gp/product/B08FSQDRJX/ref=ppx_yo_dt_b_asin_image_o04_s00?ie=UTF8&psc=1). I cut of the battery pack, and **crimped on Dupoint conenctors**.
* S - Push button
    * Any push botton switch
* R - 330 Ohms resisttors **x3**
* Raspberry Pi
* Breadboard
* Dupoint conenction cables (various)

### Circuit Diagram
![Pi Fairy Light Control Circuit diagram](https://user-images.githubusercontent.com/33297343/100523077-6cd20480-31a5-11eb-9c0d-f8271f841109.png)


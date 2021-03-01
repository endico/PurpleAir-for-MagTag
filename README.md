# A PurpleAir Dashboard For MagTag
![MagTag Display](/IMG_2638.jpeg)

[PurpleAir](https://www.purpleair.com/) air quality sensors are great but their readings aren't as accessible as they could be. The [MagTag](https://www.adafruit.com/product/4819) is a battery powered E-Ink display with magnetic feet that sticks to your fridge and talks to purpleair.com over WiFI so it can display your sensor's current air quality reading. Its a complete package so you don't need to do any soldering. You just need to install software and edit a text file.

The dashboard shows the current AQI, the name of the sensor, a low battery warning as well as the date stamp of the sensor reading. The E-Ink display will remain readable even after the battery dies so if the time stamp is ever more than 15 minutes old then either the sensor or the MagTag stopped updating.

## Install the Code

If you're not a `git` user, you can download the dashboard code by clicking on the green `Code` button above and choose `Download ZIP`.

Plug the MagTag into your computer and it will show up as a USB drive called `CIRCUITPY`. Copy the file `code.py` and the `fonts` folder to the drive. If the battery is plugged in you may need to hit the reset button first.

Follow the directions in this tutorial to install the necessary libraries from the latest bundle. You need a version of the library dated February 27, 2021 or later.
https://learn.adafruit.com/creating-magtag-projects-with-circuitpython/magtag-specific-circuitpython-libraries

If things aren't working you might also need to install a new version of CircuitPython. If the face of your MagTag is black then its a newer version and you can do the UF2 installation and ignore the part about bin files.
https://learn.adafruit.com/creating-magtag-projects-with-circuitpython/install-circuitpython

For further information see the Adafruit's MagTag learning guide.
https://learn.adafruit.com/adafruit-magtag

## Secrets File

```
secrets = {
    'ssid' : 'Your WiFi Network Name',
    'password' : 'Your WiFI Password',
    'sensor_id' : "Your PurpleAir Sensor's ID",
    'thingspeak_key': "Your Sensor's Key",
    'timezone_offset' : "-8",
}
```
Create a file called `secrets.py` in the top level of your `CIRCUITPY` drive containing your WiFi credentials and information about your sensor.

1. Find your sensor on the PurpleAir map https://www.purpleair.com/map
1. Click on the marker and when you mouse over `Get This Widget` another layer pops up. Click the link to the JSON file.
1. The `ID` field is your ``sensor_id`` and if your sensor is private you'll need the `THINGSPEAK_PRIMARY_ID_READ_KEY` too.

```
'timezone_offset' : "-8",
```
Add a time zone offset for your location. In the US, Eastern Standard time has an offset of -5, Central is -6, Mountain is -7 and Pacific Standard time is -8. Other offsets can be found at  
https://en.wikipedia.org/wiki/List_of_UTC_time_offsets

```
'sensor_alias' : "PurpleAir",
```
When you registered your sensor you gave it a name and that name will be shown on the display. You can make it say something else by adding an entry for _sensor_alias_, which can be up to 25 characters.

```
'update_frequency': '20'
```
This is the number of minutes between updates. When my MagTag sleeps 10 minutes between updates a battery charge me about a week. The battery lasts considerably longer if you only update once per hour. Be kind to the PurpleAir site and don't update more often than every ten minutes.

## Finally

As you make changes to things on your `CIRCUITPY` drive, the MagTag will restart automatically. You can force it by pressing the reset button above the USB port. After resetting, it will take several seconds for the screen to update. After that it should update every 10 minutes.

If you have trouble getting it to update, it may be having trouble connecting to the network so try moving it closer to your WiFI router. Also, make sure that the power switch on the top left corner is in the on position to the right.

## See Also

MagTag product page  
https://www.adafruit.com/product/4819

Adabox 17 Unboxing showing assembly and other projects  
https://www.youtube.com/watch?v=_YfmqJiznDY

Getting started with the MagTag  
https://learn.adafruit.com/adafruit-magtag

Creating Projects with the MagTag  
https://learn.adafruit.com/creating-magtag-projects-with-circuitpython

Deep Sleep and Battery Usage  
https://learn.adafruit.com/deep-sleep-with-circuitpython

CircuitPython Display Support Using displayio  
https://learn.adafruit.com/circuitpython-display-support-using-displayio

Getting Started With CircuitPython  
https://learn.adafruit.com/welcome-to-circuitpython

Source Sans Pro font family  
https://fonts.google.com/specimen/Source+Sans+Pro?query=source+sa

Creating custom fonts for CircuitPython  
https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display

PurpleAir PM2.5 performance across the U.S.#2  
https://cfpub.epa.gov/si/si_public_record_report.cfm?Lab=CEMM&dirEntryId=348236

PurpleAir PM2.5 U.S. Correction and Performance During Smoke Events 4/2020  
https://cfpub.epa.gov/si/si_public_record_report.cfm?Lab=CEMM&dirEntryId=349513

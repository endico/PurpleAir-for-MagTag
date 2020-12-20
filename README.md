# A PurpleAir Dashboard For MagTag
![MagTag Display](/IMG_2638.jpeg)

PurpleAir air quality sensors are great but their readings aren't as accessible as they could be. The MagTag is a battery powered E-Ink display with magnetic feet that sticks to your fridge and talks to purpleair.com over WiFI so it can display your sensor's current air quality reading.

This code shows the current AQI, the name of the sensor, a low battery warning as well as the date stamp of the sensor reading. The E-Ink display will remain readable even after the battery dies so if the time stamp is ever more than 15 minutes old then either the sensor or the MagTag stopped updating.

# Install the Code

Plug the MagTag into your computer and it will show up as a USB drive called `CIRCUITPY`. Copy the file `code.py` and the `fonts` folder to the drive. If the battery is plugged in you may need to hit the reset button first.

Follow the directions in this tutorial to install the necessary libraries from the latest bundle.
https://learn.adafruit.com/creating-magtag-projects-with-circuitpython/magtag-specific-circuitpython-libraries

If things aren't working you might also need to install a new version of CircuitPython. If the face of your MagTag is black then you can do the u2f installation and ignore the part about bin files.
https://learn.adafruit.com/creating-magtag-projects-with-circuitpython/install-circuitpython

# Secrets File

```
secrets = {
    'ssid' : 'Your WiFi Network Name',
    'password' : 'Your WiFI Password',
    'sensor_id' : "Your PurpleAir Sensor's ID",
    'thingspeak_key': "Your Sensor's Key",
}
```
Create a file in the top level of your CIRCUITPY drive containing your WiFi credentials and information about your sensor.

1. Find your sensor on the PurpleAir map https://www.purpleair.com/map
1. Click on the marker and when you mouse over _'Get This Widget'_ another layer pops up. Click the link to the JSON file.
1. The `ID` field is your sensor_id and if your sensor is private you'll need the `THINGSPEAK_PRIMARY_ID_READ_KEY` too.

```
'timezone_offset' : "-8",
```
Add a time zone offset for your location. In the US, Eastern Standard time has an offset of -5, Central is -6, Mountain is -7 and Pacific Standard time is -8. Other offsets can be found at https://en.wikipedia.org/wiki/List_of_UTC_time_offsets

```
'sensor_alias' : "PurpleAir",
```
When you registered your sensor you gave it a name and that name will be shown on the display. You can make it say something else by adding an entry for _sensor_alias_, which can be up to 25 characters.

# See Also

MagTag product page
https://www.adafruit.com/product/4819

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

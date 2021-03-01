# Purple Air AQI Display for the Adafruit MagTag
# https://www.adafruit.com/product/4819

# Port of John Park's Purple Air AQI Display for
# the Matrix Portal
# https://learn.adafruit.com/purple-air-aqi-display/

import time
import json
import board
import displayio
from secrets import secrets
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_magtag.magtag import MagTag
display = board.DISPLAY

#
# PurpleAir AQI Helper functions
#
def aqi_transform(val):
    # derive Air Quality Index from Particulate Matter 2.5 value
    aqi = pm_to_aqi(val)
    return "%d" % aqi

def message_transform(val):  # picks message based on thresholds
    index = aqi_to_list_index(pm_to_aqi(val))
    messages = (
        "Hazardous",
        "Very Unhealthy",
        "Unhealthy",
        "Unhealthy for Sensitive Groups",
        "Moderate",
        "Good",
    )
    if index is not None:
        return messages[index]
    return "Unknown"

def aqi_to_list_index(aqi):
    aqi_groups = (301, 201, 151, 101, 51, 0)
    for index, group in enumerate(aqi_groups):
        if aqi >= group:
            return index
    return None

# wikipedia.org/wiki/Air_quality_index#Computing_the_AQI
def calculate_aqi(Cp, Ih, Il, BPh, BPl):
    return round(((Ih - Il)/(BPh - BPl)) * (Cp - BPl) + Il)

def pm_to_aqi(pm):
    pm = float(pm)
    if pm < 0:
        return pm
    if pm > 1000:
        return 1000
    if pm > 350.5:
        return calculate_aqi(pm, 500, 401, 500, 350.5)
    elif pm > 250.5:
        return calculate_aqi(pm, 400, 301, 350.4, 250.5)
    elif pm > 150.5:
        return calculate_aqi(pm, 300, 201, 250.4, 150.5)
    elif pm > 55.5:
        return calculate_aqi(pm, 200, 151, 150.4, 55.5)
    elif pm > 35.5:
        return calculate_aqi(pm, 150, 101, 55.4, 35.5)
    elif pm > 12.1:
        return calculate_aqi(pm, 100, 51, 35.4, 12.1)
    elif pm >= 0:
        return calculate_aqi(pm, 50, 0, 12, 0)
    else:
        return None

if 'sensor_id' in secrets:
    sensor_id = secrets['sensor_id']
else:
    sensor_id = 21441  # New York City

if 'thingspeak_key' in secrets:
    key = secrets['thingspeak_key']
    data_source = f'https://www.purpleair.com/json?show={sensor_id}&key={key}'
else:
    data_source = f'https://www.purpleair.com/json?show={sensor_id}'

big_font = bitmap_font.load_font("/fonts/SourceSansPro-Black-70.bdf")
medium_font = bitmap_font.load_font("/fonts/SourceSansPro-Bold-20.bdf")
small_font = bitmap_font.load_font("/fonts/SourceSansPro-SemiBold-18.bdf")
main_group = displayio.Group(max_size=7)
margin = 10

# white background. Scaled to save RAM
bg_bitmap = displayio.Bitmap(display.width // 8, display.height // 8, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
bg_group = displayio.Group(scale=8)
bg_group.append(bg_sprite)
main_group.append(bg_group)

current_aqi_text = label.Label(
    big_font,
    max_glyphs=6,
    text="...",
    color=0x000000,
    background_color=0xFFFFFF,
    anchor_point=(0.0, 0.0),
    anchored_position=(margin, margin),
    base_alignment=True,
)
main_group.append(current_aqi_text)

aqi_label_text = label.Label(
    medium_font,
    text="AQI",
    color=0x000000,
    background_color=0xFFFFFF,
    base_alignment=True,
)
main_group.append(aqi_label_text)

hazard_aqi_text = label.Label(
    medium_font,
    max_glyphs=31,
    text=".",
    color=0x000000,
    background_color=0xFFFFFF,
    x=margin,
    base_alignment=True,
)
main_group.append(hazard_aqi_text)

sensor_max_glyphs = 25
sensor_text = label.Label(
    small_font,
    max_glyphs=sensor_max_glyphs,
    text="...",
    color=0x000000,
    background_color=0xFFFFFF,
    anchor_point=(1.0, 1.0),
    anchored_position=(display.width - margin, display.height - margin),
    base_alignment=True,
)
main_group.append(sensor_text)

last_modified_text = label.Label(
    small_font,
    max_glyphs=12,
    text="11:00am",
    color=0x000000,
    background_color=0xFFFFFF,
    anchor_point=(0.0, 1.0),
    anchored_position=(margin, display.height - margin),
    base_alignment=True,
)
main_group.append(last_modified_text)

voltage_text = label.Label(
    small_font,
    max_glyphs=13,
    text="...",
    color=0x000000,
    background_color=0xFFFFFF,
    anchor_point=(1.0, 0.0),
    anchored_position=(display.width - margin, margin)
)
main_group.append(voltage_text)

magtag = MagTag()

# What is the right voltage to start warning about the battery being low?
# A full battery has 4 volts. It supplies 3.7V to the board so I decided
# to start warning at 3.8v but maybe there's a better number
if (magtag.peripherals.battery > 3.3):
    voltage_text.text = ' '
else:
    voltage_text.text = 'Battery Low'
print(f'battery: {magtag.peripherals.battery} V')

try:
    magtag.network.connect()
    response = magtag.network.requests.get(data_source)
    value = response.json()
    results = value['results'][0]
except (ConnectionError, ValueError, RuntimeError) as e:
    print("Some error occured, retrying in 10 seconds -", e)
    magtag.exit_and_deep_sleep(10)

# Default time zone is Pacific Standard
timezone_offset = secrets['timezone_offset']
valid_offsets = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                 "10", "11", "12", "-1", "-2", "-3", "-4", "-5",
                 "-6", "-7", "-8", "-9", "-10", "-11", "-12"]
if (timezone_offset not in valid_offsets):
    print("timezone_offset must be one of the following values", valid_offsets)
    print("Using default offset -8 for Pacific Standard Time")
    timezone_offset = -8  # Pacific Standard Time
last_seen = results['LastSeen'] + (int(timezone_offset)*60*60)
last_modified = time.localtime(last_seen)
hour = int(last_modified[3])
min = int(last_modified[4])
last_modified_text.text = f'At {hour:02}:{min:02}'

# Instead of using PM2_5Value, use the 10 minute average
# in Stats['v1'] since this is what the purpleair map uses.
stats = json.loads(results['Stats'])
avg_pm2_5 = stats['v1']
current_aqi_text.text = aqi_transform(avg_pm2_5)
hazard_aqi_text.text = message_transform(avg_pm2_5)

# Truncate sensor name to 25 characters. If it
# exceeds max_glyphs then it crashes
if 'sensor_alias' in secrets:
    sensor_text.text = secrets['sensor_alias'][0:sensor_max_glyphs]
else:
    sensor_text.text = results['Label'][0:sensor_max_glyphs]

aqi_label_text.x = \
    current_aqi_text.x + current_aqi_text.bounding_box[2] + margin
aqi_label_text.y = current_aqi_text.y
hazard_aqi_text.y = \
    current_aqi_text.y + hazard_aqi_text.bounding_box[3] + margin
last_modified_text.y = display.height - margin
sensor_text.y = display.height - margin

display.show(main_group)
display.refresh()

# wait for the screen to finish refreshing then deep sleep for 10 minutes
while display.busy:
    pass

# Set the frequency of updates, in minutes. Be kind to the server and
# don't check more often that 10 minutes. At 10 minutes the battery
# lasts about a week.
if 'update_frequency' in secrets:
    update_frequency = secrets['update_frequency'] * 60
else:
    update_frequency = 1200
magtag.exit_and_deep_sleep(update_frequency)

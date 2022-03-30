import argparse
import distutils.util
import json
import os
import pytz
from datetime import datetime
from urllib.request import urlopen
from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto
# from gpiozero import CPUTemperature

# Set current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Command Line parser
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--apihosts', help='List of comma separated API host names')
parser.add_argument('-r', '--rotate', action='store_true', help='Rotate display 180 deg')
parser.add_argument('-s', '--simple', action='store_true', help='Simple Statistics Display')
parser.add_argument('--lcars', action='store_true', help='Use LCARS style display')
parser.add_argument('--tz', help='Timezone (default: UTC)')
# Helpers
parser.add_argument('--timezones', action='store_true', help='Show all available TimeZone values')

args = parser.parse_args()
#print('Args:', args)

if (args.timezones):
    for tz in pytz.all_timezones:
        print(tz)
    exit()

# Initialize Inky pHAT Display
display = auto()

# Colours depend on background image selected - RED doesn't show up wel on black BG.
WHITE = display.WHITE
BLACK = display.WHITE if args.lcars else display.BLACK
RED = display.WHITE if args.lcars else display.RED

# Get the current date/time based on TimeZone (if specified)
tzLocal = pytz.timezone(args.tz or 'UTC')
now = datetime.now(tzLocal)

# Load True Type Fonts...
font = ImageFont.truetype('./Signika-Bold.ttf', 22)
smallfont = ImageFont.truetype('./Signika-Light.ttf', 14)

# Initialize Data Object
data = {'unique_clients': 0, 'domains_being_blocked': 0,
        'dns_queries_today': 0, 'ads_blocked_today': 0}

# Get Pi-Hole API data
def get_data(host, combine=False):
    try:
        f = urlopen('http://' + host + '/admin/api.php')  # open API connection
        json_data_string = f.read()                   # Read data
        f.close()                                     # close connection

        # print(json_data_string)
        # Deserialize JSON to Python Object
        tmp_data = json.loads(json_data_string)

        # extract data
        data['unique_clients'] = data['unique_clients'] + \
            tmp_data['unique_clients'] if combine else max(
                data['unique_clients'], tmp_data['unique_clients'])
        data['domains_being_blocked'] = max(
            tmp_data['domains_being_blocked'], data['domains_being_blocked'])
        data['dns_queries_today'] += tmp_data['dns_queries_today']
        data['ads_blocked_today'] += tmp_data['ads_blocked_today']

    except Exception as ex:
        print(ex)
# end get_data()

# Draw large text, with small prefix and suffix
def draw_text(position, prefix, text, suffix, colour):
    bg_colour = display.WHITE if args.lcars else display.BLACK
    pw = smallfont.getlength(prefix)
    tw = font.getlength(text)
    w, h = position

    if prefix:
        draw.text((w, h+6), prefix, bg_colour, smallfont)
        w += pw + 4

    if text:
        draw.text((w, h), text, colour, font)
        w += tw + 4

    if suffix:
        draw.text((w, h+6), suffix, bg_colour, smallfont)
# end draw_text()

# Get X Position of text
def get_x(text_width, margin):
    RIGHT = 1; LEFT = 3;
    dw = round(display.WIDTH - margin[LEFT] - margin[RIGHT])
    x = round((dw - text_width) / 2) + margin[LEFT]
    return x
# end get_x()

# Get Y Position of text
def get_y(text_height, section, number_of_sections, margin):
    TOP = 0; BOTTOM = 2;
    dh = (display.HEIGHT - margin[TOP] - margin[BOTTOM]) / number_of_sections
    y = round(dh * section) - text_height + margin[TOP]
    return y
# end get_y()

# Get text position when "==simple" switch is used.
def get_simple_position(text, font, row = 1, rows = 1):
    # (top, right, bottom, left)
    margin = (10,10,10,60) if args.lcars else (10,100,10,10)
    w,h = font.getsize(text)
    x = get_x(w, margin)
    y = get_y(h, row, rows, margin)
    return (x, y)

# Get DATA and parse to strings
api_host_names = (args.apihosts or "127.0.0.1").split(",")
for host_item in api_host_names:
    parts = host_item.split(":")
    host = parts[0]
    combine = bool(distutils.util.strtobool((parts[1] if len(parts) > 1 else "False") or "False"))
    get_data(host, combine)  # primary
# end for...

fRatio = (data['ads_blocked_today'] / data['dns_queries_today']) * 100
ratio = "{:.1f}".format(round(fRatio, 2))
clients = "{:,}".format(data['unique_clients'])
domains = "{:,}".format(data['domains_being_blocked'])
queries = "{:,}".format(data['dns_queries_today'])
blocked = "{:,}".format(data['ads_blocked_today'])
blocked_full = blocked + " (" + ratio + "%)"

# Load graphic
if (args.lcars):
    display.set_border(display.BLACK)
    img = Image.open("./lcars_black_red.png")
else:
    display.set_border(display.WHITE)
    img = Image.open("./logo.png")

# Create canvas on the image we just loaded
draw = ImageDraw.Draw(img)

# Render the display text...
if (args.simple):
    font = ImageFont.truetype('./Signika-Bold.ttf', 34)

    pos = get_simple_position(queries, font, 1, 3)
    draw.text(pos, queries, BLACK, font)

    pos = get_simple_position('-'+blocked, font, 2, 3)
    draw.text(pos, '-'+blocked, RED, font)

    pos = get_simple_position(ratio + '%', font, 3, 3)
    draw.text((pos[0], pos[1]-5), ratio+'%', RED, font) # y-5 as '%' causes extra height

    if (args.lcars): #lcars+simple
        draw.text((2,45), now.strftime("%m.%d"), display.BLACK, smallfont)
        draw.text((2,60), now.strftime("%H.%M"), display.BLACK, smallfont)
        draw.text((15,100), clients, display.BLACK, smallfont)

else:
    if (args.lcars):
        x = 60
        draw_text((x, 5), now.strftime("%b-%d %H:%M"), "", "- blocked:", WHITE)
        draw_text((x, 24), "", blocked_full, "", WHITE)
        draw_text((x, 46), "of", queries, "requests", WHITE)
        draw_text((x, 68), "protecting", clients, "clients", WHITE)
        draw_text((x, 88), "@", domains, "domains", WHITE)
    else:
        x = 10
        draw_text((x, -3), now.strftime("%b-%d %H:%M"), "", "- blocked:", BLACK)
        draw_text((x, 19), "", blocked_full, "", RED)
        draw_text((x, 42), "of", queries, "requests", BLACK)
        draw_text((x, 75), "protecting", clients, "clients", BLACK)
        draw_text((x, 95), "@", domains, "domains", BLACK)

# CPU Temprature - Work in progress...
try:
    # Try getting CPU Temperature - FAILS ON "Pi Zero 2 W"
    cputemp = 0.0
    # cputemp = CPUTemperature().temperature # << THIS CRASHES INKYPHAT
    # print(cputemp, type(cputemp))
    # draw.text((10, 105), "core temp:", display.BLACK, smallfont)
    # draw_text((90,101), "core temp:", "{:.1f}".format(cputemp) + "°c", "", display.RED)
except Exception as ex:
    print(ex)

# RENDER!
if (args.rotate): img = img.rotate(180) # image rotation switch - must happen after all text drawing.
display.set_image(img)
display.show()

import os
import json
from urllib.request import urlopen
from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto
# from gpiozero import CPUTemperature
# from font_fredoka_one import FredokaOne

# Set current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    cputemp = 0.0
    # cputemp = CPUTemperature().temperature # THIS CRASHES INKYPHAT
    # print(cputemp, type(cputemp))
except Exception as ex:
    print(ex)

# get api data
try:
    f = urlopen('http://127.0.0.1/admin/api.php')
    json_data_string = f.read()
    pihole = json.loads(json_data_string)

    # read JSON contents
    clients = "{:,}".format(pihole['unique_clients'])
    domains = "{:,}".format(pihole['domains_being_blocked'])
    queries = "{:,}".format(pihole['dns_queries_today'])
    blocked = "{:,}".format(pihole['ads_blocked_today'])
    ratio = "{:.1f}".format(round(pihole['ads_percentage_today'], 2))
    blocked_full = blocked + " (" + ratio + "%)"

    f.close()

except Exception as ex:
    print(ex)
    clients = '--'
    domains = '--'
    queries = '--'
    blocked = '--'
    ratio = '0.0'

display = auto()

font = ImageFont.truetype('./Signika-Bold.ttf', 22)
smallfont = ImageFont.truetype('./Signika-Light.ttf', 14)

# Load graphic
img = Image.open("./lcars_black_red.png")
# Create canvas on the image we just loaded
draw = ImageDraw.Draw(img)

# Draw all text output


def draw_text(position, prefix, text, suffix, colour):
    # pW,pH = smallfont.getsize(prefix)
    pW = smallfont.getlength(prefix)
    # tW,tH = font.getsize(text)
    tW = font.getlength(text)
    w, h = position

    if prefix:
        draw.text((w, h+6), prefix, display.WHITE, smallfont)
        w += pW + 5

    if text:
        draw.text((w, h), text, colour, font)
        w += tW + 5

    if suffix:
        draw.text((w, h+6), suffix, display.WHITE, smallfont)
# end draw_text

draw.text((55,10), "blocked", display.WHITE, smallfont)
draw_text((55,24), "", blocked_full, "", display.WHITE)
draw_text((55,46), "of", queries, "requests", display.WHITE)

draw_text((55, 68), "protecting", clients, "clients", display.WHITE)
draw_text((55, 88), "@", domains, "domains", display.WHITE)

# draw.text((10, 105), "core temp:", display.BLACK, smallfont)
# draw_text((90,101), "core temp:", "{:.1f}".format(cputemp) + "°c", "", display.RED)

# img = img.rotate(180)

display.set_border(display.BLACK)
display.set_image(img)
display.show()

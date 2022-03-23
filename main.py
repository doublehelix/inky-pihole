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
  ratio   = "{:.1f}".format(round(pihole['ads_percentage_today'], 2))
  blocked_full = blocked + " (" + ratio + "%)"

  f.close()

except Exception as ex:
  print(ex)
  clients = '--'
  domains = '--'
  queries = '--'
  blocked = '--'
  ratio   = '0.0'

display = auto()
# font = ImageFont.truetype(FredokaOne, 20)
# ttf_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = ImageFont.truetype('./Signika-Bold.ttf', 22)
# font.set_variation_by_name('Bold')
# print(font.get_variation_names())

# smallfont = ImageFont.truetype('./Signika-Medium.ttf', 14)
smallfont = ImageFont.truetype('./Signika-Light.ttf', 14)

# Load graphic
img = Image.open("./logo.png")
# Create canvas on the image we just loaded
draw = ImageDraw.Draw(img)

# Draw all text output
def draw_text(position, prefix, text, suffix, colour):
  # pW,pH = smallfont.getsize(prefix)
  pW = smallfont.getlength(prefix)
  # tW,tH = font.getsize(text)
  tW = font.getlength(text)
  w,h = position

  if prefix:
    draw.text((w, h+6), prefix, display.BLACK, smallfont)
    w += pW + 5

  if text:
    draw.text((w, h), text, colour, font)
    w += tW + 5

  if suffix:
    draw.text((w, h+6), suffix, display.BLACK, smallfont)
# end draw_text

draw.text((10,4), "blocked", display.BLACK, smallfont)
draw_text((10,19), "", blocked_full, "", display.RED)
draw_text((10,42), "of", queries, "requests", display.BLACK)

draw_text((10, 75), "protecting", clients, "clients", display.BLACK)
draw_text((10, 95), "@", domains, "domains", display.BLACK)

# draw.text((10, 105), "core temp:", display.BLACK, smallfont)
# draw_text((90,101), "core temp:", "{:.1f}".format(cputemp) + "°c", "", display.RED)

# img = img.rotate(180)

display.set_border(display.WHITE)
display.set_image(img)
display.show()

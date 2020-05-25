import time
from datetime import datetime
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess
import requests

from coinbase.wallet.client import Client

# The client requires non-empty values for authentication, even though the call
# we're making does not require it.
client = Client("a", "1")

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# flip the display upside down because that's how I mounted it
disp.rotation = 2

height = disp.height
width = disp.width
padding = -2
top = padding
bottom = height-padding
x = 0

# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font
# font = ImageFont.load_default()

# load a TTF fonts
font = ImageFont.truetype('fonts/UbuntuMono-B.ttf', 16)
alt_font = ImageFont.truetype('fonts/UbuntuMono-R.ttf', 16)
small_font = ImageFont.truetype('fonts/Ubuntu-C.ttf', 13)

# Draw a black filled box to clear the image.
def draw_reset():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.image(image)

def draw_text_lines(line_one, line_two, line_three, line_four):
    draw.text((x, top), str(line_one), font=alt_font, fill=255)
    draw.text((x, top+16), str(line_two), font=small_font, fill=255)
    draw.text((x, top+16+13+2), str(line_three), font=font, fill=255)
    draw.text((x, top+16+13+16+2), str(line_four), font=small_font, fill=255)

try:
    while True:
        try:
            bitcoin_price = client.get_spot_price(currency_pair = 'BTC-USD')
            BTC_USD_PRICE = 'BTC: ' + f'{float(bitcoin_price.amount):,.0f}' + ' USD'
        except:
            BTC_USD_PRICE = 'BTC: Error'

        IP = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip(' \n')

        space_people = requests.get('https://www.howmanypeopleareinspacerightnow.com/peopleinspace.json', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'})

        TIME_OF_DAY = subprocess.run(['date', '+%I:%M:%S%p'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip(' \n')

        DATE_TODAY = subprocess.run(['date', '+%b %d, %Y'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip(' \n')

        PEOPLE_IN_SPACE = 'Humans in Space: ' + str(space_people.json()['number'])

        draw_reset()
        draw_text_lines(IP, DATE_TODAY + ' / ' + TIME_OF_DAY, BTC_USD_PRICE, PEOPLE_IN_SPACE)

        # Update and display image
        disp.image(image)
        disp.show()
        time.sleep(60) # TODO: make this value a constant or environment variable

except:
    draw_reset()
    draw.text((x, top+16), 'Closing...',  font=font, fill=255)
    disp.image(image)
    disp.show()
    time.sleep(2)
    draw_reset()
    disp.show()

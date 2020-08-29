import adafruit_ssd1306
import busio
import time
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont
import actions

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# flip the display 180º if needed
# display.rotation = 2

height = display.height
width = display.width
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

# Load TTF fonts
font = ImageFont.truetype('./fonts/UbuntuMono-B.ttf', 16)
alt_font = ImageFont.truetype('./fonts/UbuntuMono-R.ttf', 14)
small_font = ImageFont.truetype('./fonts/Ubuntu-C.ttf', 13)

IP = actions.get_device_ip_address()

# Draw a black filled box to clear the image.
def draw_reset():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    display.image(image)

def draw_text_lines(line_one, line_two, line_three, line_four):
    draw.text((x, top), str(line_one), font=alt_font, fill=255)
    draw.text((x, top+14), str(line_two), font=small_font, fill=255)
    draw.text((x, top+14+13+2), str(line_three), font=font, fill=255)
    draw.text((x, top+14+13+16+2), str(line_four), font=small_font, fill=255)

def update_display():
    DATETIME = actions.get_current_datetime()
    BTC_USD_PRICE = actions.get_bitcoin_usd_price()
    PEOPLE_IN_SPACE = actions.get_people_in_space()

    draw_reset()
    draw_text_lines(IP, DATETIME, BTC_USD_PRICE, PEOPLE_IN_SPACE)

    # Update and display image
    display.image(image)
    display.show()

def shutdown():
    draw_reset()
    draw.text((x, top+16), 'Closing...',  font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(2)
    draw_reset()
    display.show()

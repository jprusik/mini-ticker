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
font_height = 16
alt_font_height = 14
small_font_height = 13

font = ImageFont.truetype('./fonts/UbuntuMono-B.ttf', font_height)
alt_font = ImageFont.truetype('./fonts/UbuntuMono-R.ttf', alt_font_height)
small_font = ImageFont.truetype('./fonts/Ubuntu-C.ttf', small_font_height)

IP = actions.get_device_ip_address()

# Draw a black filled box to clear the image.
def draw_reset():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    display.image(image)

def draw_text_lines(line_one, line_two, line_three, line_four):
    draw.text(
        (x, top),
        str(line_one),
        font=alt_font,
        fill=255
    )
    draw.text(
        (x, top+alt_font_height),
        str(line_two),
        font=small_font,
        fill=255
    )
    draw.text(
        (x, top+alt_font_height+small_font_height+2),
        str(line_three),
        font=font,
        fill=255
    )
    draw.text(
        (x, top+alt_font_height+small_font_height+font_height+2),
        str(line_four),
        font=small_font,
        fill=255
    )

def update_display():
    DATETIME = actions.get_current_datetime()
    BTC_USD_PRICE = actions.get_bitcoin_usd_price()
    PEOPLE_IN_SPACE = actions.get_people_in_space()
    TEMP_HUMIDITY = actions.get_temp_and_humidity()

    draw_reset()
    draw_text_lines(IP, DATETIME + ' | ' + PEOPLE_IN_SPACE, BTC_USD_PRICE, TEMP_HUMIDITY)

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

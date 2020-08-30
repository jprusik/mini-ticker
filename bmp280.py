import time
import board
import digitalio # For use with SPI
import busio
import adafruit_bmp280

# Create library object using our Bus I2C port
# i2c = busio.I2C(board.SCL, board.SDA)
# bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# OR create library object using our Bus SPI port
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
bmp_cs = digitalio.DigitalInOut(board.D5)
bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)

# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25

def get_measurements():
    try:
        temperature = bmp280.temperature

        return {
            'altitude': bmp280.altitude, # meters
            'pressure': bmp280.pressure, # hPa
            'temperature_c': temperature,
            'temperature_f': temperature * (9 / 5) + 32
        }

    except Exception as error:
        print(error)
        return None

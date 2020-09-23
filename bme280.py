import board
import busio
import digitalio
import adafruit_bme280
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

def get_measurements():
    try:
        temperature = bme280.temperature

        return {
            'altitude': bme280.altitude, # meters
            'humidity': bme280.humidity, # relative humidity
            'pressure': bme280.pressure, # hPa
            'temperature_c': temperature,
            'temperature_f': temperature * (9 / 5) + 32
        }

    except Exception as error:
        print(error)
        return None

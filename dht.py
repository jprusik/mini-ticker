import adafruit_dht
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

DHT11_PIN = os.getenv('DHT11_PIN')

# Initialize the dht device, with data pin connected to:
# Use a DHT11 sensor
dhtDevice = adafruit_dht.DHT11(int(DHT11_PIN))
# Use a DHT22 sensor
# dhtDevice = adafruit_dht.DHT22(int(DHT11_PIN))

def get_measurements():
    try:
        temperature = dhtDevice.temperature

        return {
            'humidity': dhtDevice.humidity,
            'temperature_c': temperature,
            'temperature_f': temperature * (9 / 5) + 32
        }

    except RuntimeError as error:
        # Errors happen fairly often, DHTs are hard to read, just keep going
        print(error.args[0])
        return None

    except Exception as error:
        dhtDevice.exit()
        print(error)
        return None

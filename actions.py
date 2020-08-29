import subprocess
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
from coinbase.wallet.client import Client

# The client requires non-empty values for authentication, even though the call
# we're making does not require it.
coinbase_client = Client("a", "1")

# Create .env file path.
dotenv_path = '.env'

# Load file from the path.
load_dotenv(dotenv_path)

PC_MAC_ADDRESS = os.getenv('PC_MAC_ADDRESS')

def wake_pc(channel):
    subprocess.run('wakeonlan ${PC_MAC_ADDRESS}', shell=True)

def get_people_in_space():
    space_people = requests.get('https://www.howmanypeopleareinspacerightnow.com/peopleinspace.json', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'})

    return 'Humans in Space: ' + str(space_people.json()['number'])

def get_bitcoin_usd_price():
    try:
        bitcoin_price = coinbase_client.get_spot_price(currency_pair = 'BTC-USD')

        return 'BTC: ' + f'{float(bitcoin_price.amount):,.0f}' + ' USD'
    except:
        return 'BTC: Error'

def get_current_datetime():
    now = datetime.now().astimezone().replace(microsecond=0)
    return now.strftime('%d/%m/%y %I:%M%P')

def get_device_ip_address():
    return subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip(' \n')

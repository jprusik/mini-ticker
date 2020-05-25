import subprocess
import os
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = '.env'

# Load file from the path.
load_dotenv(dotenv_path)

PC_MAC_ADDRESS = os.getenv('PC_MAC_ADDRESS')

def wake_pc(channel):
    subprocess.run('wakeonlan ${PC_MAC_ADDRESS}', shell=True)

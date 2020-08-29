# Mini Ticker

This project is a purpose-built solution for retrieving and displaying various information that is important to the author.

Additionally, it has configured interfaces (button presses, NFC/RFID card/tag scan) which can trigger arbitrary actions (e.g. send magic packet). It aims to have a small footprint, with minimal maintenance.

The code provided here is based on examples ([1](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/tree/master/examples), [2](https://github.com/ondryaso/pi-rc522/tree/master/examples)) from the [pi-rc522](https://github.com/ondryaso/pi-rc522) and [adafruit-circuitpython-ssd1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306) projects.

## Requirements

- Raspberry Pi computer with installed header pins and power source
- [compatible](https://www.raspberrypi.org/documentation/installation/sd-cards.md) microSD/SD card
- SSD1306-based 128x64 or 128x32 pixel OLED display (I2C)
- (Optional) RC522 module (for RFID/NFC communication)

## Setup

- [Install Raspbian (Lite)](https://www.raspberrypi.org/downloads/raspbian/) on a microSD/SD card
- Set up the Raspberry Pi to run headless and connect it to your network ([guide](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md))
- [ssh into the Raspberry Pi](https://www.raspberrypi.org/documentation/remote-access/ssh/):
- Do `sudo raspi-config` and set up:
  - "Interfacing Options" > "Interfacing Options" > "I2C" > select "Yes"
  - (Optional) "Localisation Options"
  - (Optional) "Change User Password"
    **Important!** Because we're using a Raspberry Pi, the default user is `pi` with a password of `raspberry` - it is strongly advised to change the password, at minimum.
- Install dependencies:

  ```shell
  sudo apt update && sudo apt-get install git python3-pip python3-dev libtiff5-dev libopenjp2-7-dev
  ```

- (Optional) Enable Wake-on-LAN packet sending `sudo apt-get install etherwake`
- Clone this repo and `cd mini-ticker`
- Install required packages with `pip3 install -r requirements.txt`
- (Optional) Edit `/boot/config.txt` at the line `dtparam=i2c_arm=on` and replace it with:

  ```shell
  dtparam=i2c_arm=on,i2c_arm_baudrate=400000
  ```

- (Optional) If using an RC522 module for RFID/NFC communication, edit `/boot/config.txt` to include the following settings:

  ```settings
  device_tree_param=spi=on
  dtoverlay=spi-bcm2708
  dtparam=spi=on
  ```

## Running the code

Once the `ticker.py` script is executed, it will continue to run until the process is terminated. You can manually execute the script on demand, or automatically execute on shell start by editing `/etc/profile` and appending the following to the end of the file (update the file path as needed):

```shell
python3 /home/pi/mini-ticker
```

Alternatively, run any given script as a service:

- Run `sudo systemctl --force --full edit mini-ticker.service` and enter the config:

  ```config
  [Unit]
  Description=Mini Ticker
  Requires=network.target
  After=multi-user.target

  [Service]
  WorkingDirectory=/home/pi/mini-ticker
  User=pi
  ExecStart=python3 .
  ExecStopPost=python3 -c 'import ticker; ticker.shutdown()'

  [Install]
  WantedBy=multi-user.target
  ```

- Enable the service with `sudo systemctl enable --now mini-ticker.service`, and start it with `sudo systemctl start mini-ticker.service`

Other scripts that listen for triggers (e.g. card scan, button press) can be executed in the same way.

## Notes

- This build assumes Raspberry Pi Zero hardware - no other Raspberry Pi hardware has been tested with this code.
- [Ubuntu Font Family](https://design.ubuntu.com/font/) is included in `/fonts` by default. If you wish to use a different font, add them to the `/fonts` directory and update the import references in `ticker.py` (note, line spacing currently presumes Ubuntu fonts and may require adjustments when using other fonts).
- Tip: You can access the the target pi on your network using the pi's network DNS reference (`raspberrypi` by default). This is particularly useful if your network has dynamic IP address assignment; you can simply `ssh pi@raspberrypi.local`)

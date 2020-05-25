# Mini Ticker

This project is a purpose-built solution for retrieving and displaying various information that is important to the author.

Additionally, it has configured interfaces (button presses, NFC/RFID card/tag scan) which can trigger arbitrary actions (e.g. send magic packet). It aims to have a small footprint, with minimal maintenance.

The code provided here is based on examples[^1][^2] from the [pi-rc522](https://github.com/ondryaso/pi-rc522) and [adafruit-circuitpython-ssd1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306) projects.

## Requirements

- Raspberry Pi computer with installed header pins and power source
- [compatible](https://www.raspberrypi.org/documentation/installation/sd-cards.md) microSD/SD card
- SSD1306-based 128x64 or 128x32 pixel OLED display (I2C)
- (optional) RC522 module (for RFID/NFC communication)

## Setup

- [Install Raspbian (Lite)](https://www.raspberrypi.org/downloads/raspbian/) on a microSD/SD card
- Set up the Raspberry Pi to run headless and connect it to your network ([guide](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md))
- [ssh into the Raspberry Pi](https://www.raspberrypi.org/documentation/remote-access/ssh/):
  - Do `sudo raspi-config` and set up:
    - "Interfacing Options" > "Interfacing Options" > "I2C" > select "Enable"
    - "Network Options"
    - (Optional) "Localisation Options"
    - (Optional) "Change User Password"
      **Important!** Because we're using a Raspberry Pi, the default user is `pi` with a password of `raspberry` - it is strongly advised to change the password, at minimum.
  - Install [pip3](https://www.raspberrypi.org/documentation/linux/software/python.md) with `sudo apt update && sudo apt install python3-pip`
  - Clone this repo and `cd mini-ticker`
  - Install dependencies:
  
    ```shell
    sudo apt-get install python3-dev libtiff5-dev libopenjp2-7-dev
    ```

  - Install required packages with `pip3 install -r requirements.txt`
  - (Optional) Edit `/boot/config.txt` at the line `dtparam=i2c_arm=on` and replace it with:

    ```shell
    dtparam=i2c_arm=on,i2c_arm_baudrate=400000
    ```
  
  - (Optional) Enable Wake-on-LAN packet sending `sudo apt-get install etherwake`

### (Optional) If using an RC522 module for RFID/NFC communication

- Install [pi-rc522](https://github.com/ondryaso/pi-rc522) (don't use `pip3 install`; as of this writing, [the version on pypi](https://pypi.org/project/pi-rc522/#history) is out of date):

  ```shell
  git clone https://github.com/ondryaso/pi-rc522.git
  cd pi-rc522
  python setup.py install
  ```

- Edit `/boot/config.txt` to include the following settings:

  ```settings
  device_tree_param=spi=on
  dtoverlay=spi-bcm2708
  dtparam=spi=on
  ```

## Running the code

Once the `ticker.py` script is executed, it will continue to run until the process is terminated. You can manually execute the script on demand, or automatically execute on shell start by editing `/etc/profile` and appending the following to the end of the file:

```shell
sudo python3 /home/pi/ticker.py
```

Other scripts that listen for triggers (e.g. card scan, button press) can be executed in the same way.

## Notes

- This build assumes Raspberry Pi Zero hardware - no other Raspberry Pi hardware has been tested with this code.
- [Ubuntu Font Family](https://design.ubuntu.com/font/) is included in `/fonts` by default. If you wish to use a different font, add them to the `/fonts` directory and update the import references in `ticker.py` (note, line spacing currently presumes Ubuntu fonts and may require adjustments when using other fonts).
- Tip: You can access the the target pi on your network using the pi's network DNS reference (`raspberrypi` by default). This is particularly useful if your network has dynamic IP address assignment; you can simply `ssh pi@raspberrypi.local`)

[^1]: https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/tree/master/examples
[^2]: https://github.com/ondryaso/pi-rc522/tree/master/examples

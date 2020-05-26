import RPi.GPIO as GPIO
from pirc522 import RFID
import actions

rdr = RFID(pin_rst=25, pin_irq=24, pin_mode=GPIO.BCM)

util = rdr.util()

try:
  while True:
    print('Waiting for tag')
    rdr.wait_for_tag()
    (request_error, tag_type) = rdr.request()

    if not request_error:
      print('Tag detected')
      (col_error, uid) = rdr.anticoll()

      if not col_error:
        print('Tag id: ', uid)

except KeyboardInterrupt:
    print("\nExit")
    # Calls GPIO cleanup
    rdr.cleanup()

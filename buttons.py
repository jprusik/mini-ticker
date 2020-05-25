import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import actions

# GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup event on pin 10 rising edge
GPIO.add_event_detect(10, GPIO.RISING, callback=actions.wake_pc, bouncetime=500)

while True:
    pass

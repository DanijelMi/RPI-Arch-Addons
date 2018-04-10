import RPi.GPIO as GPIO
from time import sleep

# ##############CONFIG###############
# GPIO.BOARD/GPIO.BCM - Configures how numbers represent which GPIO
GPIO.setmode(GPIO.BOARD)
pins = [15, 16, 18]			# Red, green, and blue pins, respectively
freq = 100                  # Square wave frequency. Used for all 3 channels
# ###################################
GPIO.setup(pins, GPIO.OUT)  # Sets configured pins as outputs
GPIO.output(pins, 1)  # Sets pins to HIGH. This turns the common-anode LED off.
# Initialize PWM for each channel
Red = GPIO.PWM(pins[0], freq)
Green = GPIO.PWM(pins[1], freq)
Blue = GPIO.PWM(pins[2], freq)
offFlag = 0


def ON(r, g, b):
    GPIO.setup(pins, GPIO.OUT)  # Sets configured pins as outputs
    # Start each channel. The values are inverted due to the LED being common-anode.
    # Common anode LEDs have 3.3V on the anode and 3 GPIO pins to sink the current.
    # Therefore, the most possible current passes when the duty cycle is 0.
    Red.start(100 - r)
    Green.start(100 - g)
    Blue.start(100 - b)


def OFF():
    Red.stop()
    Green.stop()
    Blue.stop()
    GPIO.setup(pins, GPIO.IN)


def Duration(r, g, b, duration):
    ON(r, g, b)
    # Sleep stops the LED from turning off instantly
    sleep(duration / 1000)
    OFF()


def Blink(r, g, b, rf, gf, bf, duration):
    GPIO.setup(pins, GPIO.OUT)  # Sets configured pins as outputs
    Red = GPIO.PWM(pins[0], rf)
    Green = GPIO.PWM(pins[1], gf)
    Blue = GPIO.PWM(pins[2], bf)
    Red.start(100 - r)
    Green.start(100 - g)
    Blue.start(100 - b)
    sleep(duration / 1000)
    OFF()

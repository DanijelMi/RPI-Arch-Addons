# Small script that safely shuts the system down if a certain pin is pulled LOW.
# Tested on Arch Linux (RPI3)
# Needs to have the ledControl.py for the LED indication to work
from os import system
import RPi.GPIO as GPIO
from time import sleep
import LED

# ###### CONFIG #########
pin = 5     # GPIO pin which will check the voltage state for shutdown
confirmTimeout = 1800  # How much time spent on any stage.
# Time of input unresponsiveness between presses. Adjust if signal bounces
softDebounce = 0.2

# Sets up which way we address the pins:
# GPIO.BOARD = Pins are addressed 1 to 40, from the top left to bottom right
# pin on the physical PCB. Some are unusuable since they are not GPIO (ex.GND).
# GPIO.BCM = Address pins by their real GPIO numbers (ex. GPIO0, GPIO7).
GPIO.setmode(GPIO.BOARD)
# Sets the pin as INPUT with internal PULL_UP enabled.
GPIO.setup(pin, GPIO.IN)

askLED = [40, 0, 40]
shutdownLED = [80, 0, 0]
restartLED = [50, 35, 0]
ledMatrix = [askLED, shutdownLED, restartLED]


def action(selection):
    if (selection == 1):
        system("echo Shutdown selected!")
        LED.ON(10, 0, 0)
        system("shutdown now")
    elif(selection == 2):
        system("echo Restart selected!")
        LED.ON(10, 8, 0)
        system("reboot now")


def mainLogic():
    LED.Blink(5, 5, 5, 1, 2, 3, 1100)
    while(True):
        GPIO.wait_for_edge(pin, GPIO.FALLING)
        sleep(softDebounce)             # Software button debounce
        count = 0
        while(True):
            LED.ON(ledMatrix[count][0], ledMatrix[count]
                   [1], ledMatrix[count][2])
            isPressed = GPIO.wait_for_edge(
                pin, GPIO.FALLING, timeout=confirmTimeout)
            sleep(softDebounce)         # Software button debounce
            if(isPressed):
                count = (count + 1) % 3     # Makes sure the selection is 0-2
                if(count == 0):     # Goes back to start if all options got scrolled through
                    LED.OFF()
                    break
            else:                   # Acts when a timeout occurs on non-zero selection
                LED.OFF()
                action(count)
                break


mainLogic()

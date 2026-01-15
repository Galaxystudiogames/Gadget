import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def read():
    reader = SimpleMFRC522()
    try:
        text = input('Enter tag data:')
        print("Hold tag to module")
        reader.write(text)
        print("Done...")
    finally:
        GPIO.cleanup()

def emulate():
    pass

def write():
    pass
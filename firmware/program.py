# lala libaries 
from time import sleep
import vlc
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import threading

# implement these later!
startButton = Pin(4, Pin.IN)
stopButton = Pin(5, Pin.IN)

GPIO.setmode(GPIO.BCM)
control_pins = [22, 23, 24, 25]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

WIDTH = 128
HEIGHT = 32
i2c = I2C(0, scl=Pin(2), sda=Pin(3), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

needle = SimpleMFRC522()

# songs... only two for now
spiderdance = vlc.MediaPlayer("spiderdance.mp3")
asgore = vlc.MediaPlayer("asgore.mp3")


def spinning():
    for i in range(512):  # number of steps
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            sleep(0.001)

def display_song(text):
    oled.fill(0)
    oled.text(text, 0, 0)
    oled.show()


while True:
    try:
        id, text = needle.read_no_block()
        # whatever the nfc code is for spiderdance
        if id == 12345678:
            display_song("Now playing:\nSpiderdance")
            spiderdance.play()
            threading.Thread(target=spinning).start()
            
        # whatever the nfc code is for asgore
        elif id == 98765432:
            display_song("Now playing:\nAsgore")
            asgore.play()
            threading.Thread(target=spinning).start()

    except KeyboardInterrupt:
        GPIO.cleanup()
        break

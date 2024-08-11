import RPi.GPIO as GPIO
import time

# // 
# // 
# // 
# // 
# // P0.09 LED2
# // P0.29 LED1
# // P0.13 RX
# // P0.14 TX

p_0_0 = 2 # P0.0   - Source switch / pairing
p_0_4 = 3 # P0.04  - Power/Mute/Encoder C
p_0_1 = 4 # P0.01  - Encoder A
p_0_3 = 5 # P0.03  - Encoder B
p_0_9 = 17 # P0.09 - LED2


GPIO.setmode(GPIO.BCM)
GPIO.setup(p_0_0, GPIO.OUT)
GPIO.setup(p_0_4, GPIO.OUT)
GPIO.setup(p_0_1, GPIO.OUT)
GPIO.setup(p_0_3, GPIO.OUT)

def switch_source():
    GPIO.output(p_0_0, False)
    time.sleep(0.1)
    GPIO.output(p_0_0, True)


def pair():
    GPIO.output(p_0_0, False)
    time.sleep(16)
    GPIO.output(p_0_0, True)


def switch_power():
    # detect if it is on by adjusting volume and detecting led blink or not
    GPIO.output(p_0_4, False)
    time.sleep(2)
    GPIO.output(p_0_4, True)

def mute():
    GPIO.output(p_0_4, False)
    time.sleep(0.1)
    GPIO.output(p_0_4, True)


def volume_down():
    # Emulate the hardware encoder by "rotating" it
    GPIO.output(p_0_1, False)
    time.sleep(0.1)
    GPIO.output(p_0_3, False)
    time.sleep(0.1)
    GPIO.output(p_0_1, True)
    time.sleep(0.1)
    GPIO.output(p_0_3, True)


def volume_down():
    # Emulate the hardware encoder by "rotating" it
    GPIO.output(p_0_3, False)
    time.sleep(0.1)
    GPIO.output(p_0_1, False)
    time.sleep(0.1)
    GPIO.output(p_0_3, True)
    time.sleep(0.1)
    GPIO.output(p_0_1, True)



try:
    print("switch")
    switch_power()
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 

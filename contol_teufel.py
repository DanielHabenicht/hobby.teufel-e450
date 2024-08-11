import RPi.GPIO as GPIO
import time

# Unused pins
# P0.29 LED1
# P0.13 RX
# P0.14 TX

GPIO.setmode(GPIO.BCM)


p_0_9 = 17 # P0.09 - LED2
GPIO.setup(p_0_9, GPIO.IN)

# Always HIGH as the button press disconnects the power
p_0_0 = 2 # P0.0   - Source switch / pairing
GPIO.setup(p_0_0, GPIO.OUT, initial=GPIO.HIGH)
# Always HIGH as the button press disconnects the power
p_0_4 = 3 # P0.04  - Power/Mute/Encoder C
GPIO.setup(p_0_4, GPIO.OUT, initial=GPIO.HIGH)

# Always Low as encoder only sets those to HIGH on rotation
p_0_1 = 4 # P0.01  - Encoder A
p_0_3 = 5 # P0.03  - Encoder B
GPIO.setup(p_0_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(p_0_3, GPIO.OUT, initial=GPIO.LOW)

print("p_0_0:" + str(GPIO.input(p_0_0)))
print("p_0_4:" + str(GPIO.input(p_0_4)))
print("p_0_1:" + str(GPIO.input(p_0_1)))
print("p_0_3:" + str(GPIO.input(p_0_3)))


time.sleep(2)

def switch_source():
    print("switch source")
    GPIO.output(p_0_0, False)
    time.sleep(0.1)
    GPIO.output(p_0_0, True)
    time.sleep(0.1)


def pair():
    print("pair")
    GPIO.output(p_0_0, False)
    time.sleep(16)
    GPIO.output(p_0_0, True)


def turn_on():
    print("turn on")
    # detect if it is on by adjusting volume and detecting led blink or not
    GPIO.output(p_0_4, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(p_0_4, GPIO.HIGH)

def turn_off():
    print("turn off")
    # detect if it is on by adjusting volume and detecting led blink or not
    GPIO.output(p_0_4, GPIO.LOW)
    time.sleep(5)
    GPIO.output(p_0_4, GPIO.HIGH)

def mute():
    print("mute")
    GPIO.output(p_0_4, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(p_0_4, GPIO.HIGH)
    time.sleep(0.1)

def volume_up():
    print("volume up")
    # Emulate the hardware encoder by "rotating" it
    GPIO.output(p_0_1, False)
    time.sleep(0.1)
    GPIO.output(p_0_3, False)
    time.sleep(0.1)
    GPIO.output(p_0_1, True)
    time.sleep(0.1)
    GPIO.output(p_0_3, True)
    time.sleep(0.1)


def volume_down():
    print("volume down")
    # Emulate the hardware encoder by "rotating" it
    GPIO.output(p_0_3, False)
    time.sleep(0.1)
    GPIO.output(p_0_1, False)
    time.sleep(0.1)
    GPIO.output(p_0_3, True)
    time.sleep(0.1)
    GPIO.output(p_0_1, True)
    time.sleep(0.1)


try:
   turn_on()
   volume_up()
   volume_up()
   volume_up()
   volume_up()
   volume_up()
   volume_up()
   volume_up()
   volume_up()
   volume_down()
   volume_down()
   volume_down()
   volume_down()
   volume_down()
   volume_down()
   volume_down()
   volume_down()
   volume_down()
   switch_source()
   mute()
   turn_off()
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Keyboard interrupt")

except:
    print("some error")

finally:
    print("clean up")
    GPIO.cleanup() # cleanup all GPIO
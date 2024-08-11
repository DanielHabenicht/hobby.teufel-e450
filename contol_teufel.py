import RPi.GPIO as GPIO
import time
import datetime

# Unused pins
# P0.29 LED1
# P0.13 RX
# P0.14 TX

GPIO.setmode(GPIO.BCM)


p_0_9 = 25 # P0.09 - LED2
GPIO.setup(p_0_9, GPIO.IN)


prev = 0
def buttonPress(channel):
    current = GPIO.input(p_0_9)
    global prev
#    if prev is not current:
    print("Button pressed:" + str(prev) + " - " + str(current))
    prev = current

GPIO.add_event_detect(p_0_9, GPIO.BOTH, callback=buttonPress) #, bouncetime=6)

# Always HIGH as the button press disconnects the power
p_0_0 = 7 # P0.0   - Source switch / pairing
GPIO.setup(p_0_0, GPIO.OUT, initial=GPIO.HIGH)
# Always HIGH as the button press disconnects the power
p_0_4 = 8 # P0.04  - Power/Mute/Encoder C
GPIO.setup(p_0_4, GPIO.OUT, initial=GPIO.HIGH)

# Always Low as encoder only sets those to HIGH on rotation
p_0_1 = 23 # P0.01  - Encoder A
p_0_3 = 24 # P0.03  - Encoder B
GPIO.setup(p_0_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(p_0_3, GPIO.OUT, initial=GPIO.LOW)

#print("p_0_0:" + str(GPIO.input(p_0_0)))
#print("p_0_4:" + str(GPIO.input(p_0_4)))
#print("p_0_1:" + str(GPIO.input(p_0_1)))
#print("p_0_3:" + str(GPIO.input(p_0_3)))

def switch_source():
    print("switch source")
    GPIO.output(p_0_0, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(p_0_0, GPIO.HIGH)
    time.sleep(0.1)


def pair():
    print("pair")
    GPIO.output(p_0_0, False)
    time.sleep(16)
    GPIO.output(p_0_0, True)


def check_if_on():
    print("check state")
    GPIO.output(p_0_3, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(p_0_1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(p_0_3, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(p_0_1, GPIO.LOW)
#    channel = GPIO.wait_for_edge(p_0_9, GPIO.RISING, timeout=2000)
 #   if channel is None:
  #      print('off')
   # else:
    #    print('on')



def turn_on():
    print("turn on")
    # detect if it is on by adjusting volume and detecting led blink or not
    GPIO.output(p_0_4, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(p_0_4, GPIO.HIGH)
    channel = GPIO.wait_for_edge(p_0_9, GPIO.RISING, timeout=2000)
    if channel is None:
        print('Timeout occurred')
    else:
        print('Edge detected on channel', channel)

    print("continue")
   # wait for device to turn on
    time.sleep(2)

def turn_off():
    print("turn off")
    # detect if it is on by adjusting volume and detecting led blink or not
    GPIO.output(p_0_4, GPIO.LOW)
    time.sleep(4)
    GPIO.output(p_0_4, GPIO.HIGH)

def mute():
    print("mute")
    GPIO.output(p_0_4, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(p_0_4, GPIO.HIGH)
    time.sleep(0.1)

system_volume = 0
""" volume range of the system (13 * 3 = 39)

13 LED Units System, each with 3 steps (dim, brighter, bright)
"""

def reset_volume():
    
    for i in range(13 * 3):
        volume_down()
    global system_volume
    system_volume = 0



def adjust_volume(volume):
    """ adjust volume (0-100) to the system volume """
    
    print("adjust volume")
    global system_volume
    # convert volume to system volume
    new_system_volume = int(volume / 100 * 39) 

    print("system_volume: " + str(system_volume))
    print("new volume: " + str(new_system_volume))
    diff = new_system_volume - system_volume
    print("diff: " + str(diff))
    if diff == 0:
        return
    if diff < 0:
        for i in range(abs(diff)):
            print("decrease")
            pass
            # volume_down()
    else:
        for i in range(abs(diff)):
            print("increase")
            pass
            # volume_up()
    system_volume = new_system_volume



def volume_up():
    print("volume up")
    # Emulate the hardware encoder by "rotating" it
    GPIO.output(p_0_1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(p_0_3, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(p_0_1, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(p_0_3, GPIO.LOW)
    time.sleep(0.1)


def volume_down():
    print("volume down")
    # Emulate the hardware encoder by "rotating" it
    GPIO.output(p_0_3, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(p_0_1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(p_0_3, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(p_0_1, GPIO.LOW)
    time.sleep(0.1)


def test_functionality():
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

try:
   reset_volume()
   adjust_volume(50)
#   check_if_on()
#   turn_on()
#   test_functionality()
#   time.sleep(1)
#   switch_source()
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Keyboard interrupt")


finally:
    print("clean up")
    #GPIO.output(p_0_0, GPIO.HIGH)
    #GPIO.output(p_0_4, GPIO.HIGH)
    #GPIO.output(p_0_1, GPIO.LOW)
    #GPIO.output(p_0_3, GPIO.LOW)
#    GPIO.cleanup() # cleanup all GPIO
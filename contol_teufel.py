import RPi.GPIO as GPIO
import time
import datetime
from pyalsa import alsamixer, alsacard
import math


mixer = alsamixer.Mixer()
mixer.attach("default:CARD=Dummy")
mixer.load()

alsa = alsamixer.Element(mixer, 'Master')
(min, max) = alsa.get_volume_range()  # shows e.g., 15729 (max 65536)
volume_range = max - min

# Unused pins
# P0.29 LED1
# P0.13 RX
# P0.14 TX

GPIO.setmode(GPIO.BCM)


p_0_9 = 25  # P0.09 - LED2
GPIO.setup(p_0_9, GPIO.IN)


prev = 0


def buttonPress(channel):
    current = GPIO.input(p_0_9)
    global prev
    #    if prev is not current:
    print("Button pressed:" + str(prev) + " - " + str(current))
    prev = current


# GPIO.add_event_detect(p_0_9, GPIO.BOTH, callback=buttonPress) #, bouncetime=6)

# Always HIGH as the button press disconnects the power
p_0_0 = 7  # P0.0   - Source switch / pairing
GPIO.setup(p_0_0, GPIO.OUT, initial=GPIO.HIGH)
# Always HIGH as the button press disconnects the power
p_0_4 = 8  # P0.04  - Power/Mute/Encoder C
GPIO.setup(p_0_4, GPIO.OUT, initial=GPIO.HIGH)

# Always Low as encoder only sets those to HIGH on rotation
p_0_1_A = 23  # P0.01  - Encoder A
p_0_3_B = 24  # P0.03  - Encoder B
GPIO.setup(p_0_1_A, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(p_0_3_B, GPIO.OUT, initial=GPIO.LOW)

# print("p_0_0:" + str(GPIO.input(p_0_0)))
# print("p_0_4:" + str(GPIO.input(p_0_4)))
# print("p_0_1:" + str(GPIO.input(p_0_1)))
# print("p_0_3:" + str(GPIO.input(p_0_3)))


class TeufelControl:

    system_volume = 0
    """ volume range of the system (13 * 3 = 39)

    13 LED Units System, each with 3 steps (dim, brighter, bright)
    """

    encoder_state = (False, False)
    """ virtual encoder state (A, B) """

    def switch_source(self):
        print("switch source")
        GPIO.output(p_0_0, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(p_0_0, GPIO.HIGH)
        time.sleep(0.1)

    def pair(self):
        print("pair")
        GPIO.output(p_0_0, False)
        time.sleep(16)
        GPIO.output(p_0_0, True)

    def check_if_on(self):
        print("check state")
        GPIO.output(p_0_3_B, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(p_0_1_A, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(p_0_3_B, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(p_0_1_A, GPIO.LOW)

    #    channel = GPIO.wait_for_edge(p_0_9, GPIO.RISING, timeout=2000)
    #   if channel is None:
    #      print('off')
    # else:
    #    print('on')

    def turn_on(self):
        print("turn on")
        # detect if it is on by adjusting volume and detecting led blink or not
        GPIO.output(p_0_4, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(p_0_4, GPIO.HIGH)
        channel = GPIO.wait_for_edge(p_0_9, GPIO.RISING, timeout=2000)
        if channel is None:
            print("Timeout occurred")
        else:
            print("Edge detected on channel", channel)

        print("continue")
        # wait for device to turn on
        time.sleep(3)

    def turn_off(self):
        print("turn off")
        # detect if it is on by adjusting volume and detecting led blink or not
        GPIO.output(p_0_4, GPIO.LOW)
        time.sleep(4)
        GPIO.output(p_0_4, GPIO.HIGH)

    def mute(self):
        print("mute")
        GPIO.output(p_0_4, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(p_0_4, GPIO.HIGH)
        time.sleep(0.1)

    def reset_volume(self):

        for i in range(13 * 3):
            self.volume_down()
        self.system_volume
        system_volume = 0

    def adjust_volume(self, volume: int):
        """adjust volume (0-100) to the system volume"""

        print("adjust volume:" + str(volume))
        # convert volume to system volume
        new_system_volume = int(volume / 100 * 39)

        print("system_volume: " + str(self.system_volume))
        print("new volume: " + str(new_system_volume))
        diff = new_system_volume - self.system_volume
        print("diff: " + str(diff))
        print("diff percentage:" + str(diff / 39))
        if diff == 0:
            return
        if diff < 0:
            for i in range(abs(diff)):
                print("decrease")
                self.volume_down()
        else:
            for i in range(abs(diff)):
                print("increase")
                self.volume_up()
        self.system_volume = new_system_volume

    def volume_up(self):
        print("volume up")
        # Emulate the hardware encoder by "rotating" it
        # meaning setting the pins to HIGH and LOW in the right order
        (a, b) = self.encoder_state

        if a:
            GPIO.output(p_0_1_A, GPIO.LOW)
        else:
            GPIO.output(p_0_1_A, GPIO.HIGH)
        time.sleep(0.005)

        if b:
            GPIO.output(p_0_3_B, GPIO.LOW)
        else:
            GPIO.output(p_0_3_B, GPIO.HIGH)
        self.encoder_state = (not a, not b)
        time.sleep(0.005)

    def volume_down(self):
        print("volume down")
        # Emulate the hardware encoder by "rotating" it
        (a, b) = self.encoder_state

        if b:
            GPIO.output(p_0_3_B, GPIO.LOW)
        else:
            GPIO.output(p_0_3_B, GPIO.HIGH)
        time.sleep(0.005)
        if a:
            GPIO.output(p_0_1_A, GPIO.LOW)
        else:
            GPIO.output(p_0_1_A, GPIO.HIGH)
        self.encoder_state = (not a, not b)
        time.sleep(0.005)


def test_functionality(control: TeufelControl):
    #control.turn_on()
    control.volume_up()
    #control.volume_up()
    #control.volume_up()
    #control.volume_up()
    #control.volume_up()
    #control.volume_up()
    #control.volume_up()
    #control.volume_up()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.volume_down()
    #control.switch_source()
    #control.mute()
    #control.turn_off()


try:
    control = TeufelControl()
    control.reset_volume()
    while True:
        mixer.handle_events()
        volume = alsa.get_volume()
        percentage = (volume - min) / volume_range
        print(percentage)
        time.sleep(1)
        control.adjust_volume(percentage)
#   check_if_on()
#   turn_on()
#    test_functionality(control)
#   time.sleep(1)
#   switch_source()
except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print("Keyboard interrupt")


finally:
    print("clean up")
    # GPIO.output(p_0_0, GPIO.HIGH)
    # GPIO.output(p_0_4, GPIO.HIGH)
    # GPIO.output(p_0_1, GPIO.LOW)
    # GPIO.output(p_0_3, GPIO.LOW)
#    GPIO.cleanup() # cleanup all GPIO
from pyalsa import alsamixer, alsacard
import time
import math

print(alsacard.card_get_name(2))
#print(alsacard.card_list())
#card = alsacard.card_load(2)
#print(card)

mixer = alsamixer.Mixer()
mixer.attach("default:CARD=Dummy")
mixer.load()

alsa = alsamixer.Element(mixer, 'Master')
(min, max) = alsa.get_volume_range()  # shows e.g., 15729 (max 65536)

range = max - min


while True:
  mixer.handle_events()
  print("read")
  volume = alsa.get_volume()
  percentage = (volume - min) / range
  print(percentage)
  time.sleep(1)
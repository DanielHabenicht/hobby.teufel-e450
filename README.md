From: https://hackaday.io/project/184708-make-teufel-smart-home-capable-with-mqtt

# Guide

> Example Video [Example Video](./VID_20240811_224344.mp4)

## Flash nrf51822

### Prerequisites

- [OpenOCD](https://github.com/xpack-dev-tools/openocd-xpack/releases)
- ST-Link V2 and [Driver](https://www.st.com/en/development-tools/stsw-link009.html)
- nrf51822
- https://shop.pimoroni.com/products/audio-dac-shim-line-out?variant=32343184965715

### Flashing

1. Connect the ST-Link V2 to the nrf51822

   | NRF51822 | STLINK V2 |
   | -------- | --------- |
   | GND      | GND       |
   | VDD      | 3.3V      |
   | SDO      | SWDIO     |
   | SCL      | SWCLK     |

2. Connect the ST-Link V2 to the computer

Flash:

```
xpack-openocd-0.12.0-4/bin/openocd.exe -f xpack-openocd-0.12.0-4/openocd/scripts/interface/stlink.cfg -f xpack-openocd-0.12.0-4/openocd/scripts/target/nrf51.cfg  -c "init; halt; nrf51 mass_erase; program firmware/teufel.hex; reset; exit;"
```

Used:

- https://www.jentsch.io/nrf51822-flashen-mit-st-link-v2-und-openocd/

Raspberry Pi Zero W
with Pimoroni Audio DAC SHIM (uses GPIO 18, 19, and 21)
and PiCorePlayer OS

- Select Audio Output "HifiBerry DAC Zero/MiniAMP" in PiCorePlayer settings.

But this lacks board support for tinkering with the GPIO pins.
So I installed Raspberry Lite OS and installed squeezelite manually.

```
#dtparam=audio=on
# Enable Audio DAC
dtoverlay=hifiberry-dac
```

```bash
sudo apt install squeezelite
# Change Name:
sudo nano /etc/default/squeezelite
```

If the service is not working provide your own service file:

```toml
[Unit]
Requires=bluetooth.service
After=network.target bluetooth.service
Description=Squeezelite Client

[Service]
ExecStart=runuser -l pi -c '/usr/bin/squeezelite -o default -n "Kitchen"'

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl enable squeezelite.service
sudo systemctl start squeezelite.service
```


```
# Control
sudo apt remove python3-rpi.gpio
sudo apt install python3-rpi-lgpio

# Custom controls
sudo apt-get install python3-pyalsa

# Add Dummy Soundcard for alsa controls
https://superuser.com/questions/344760/how-to-create-a-dummy-sound-card-device-in-linux-server


squeezelite -o 'default:CARD=sndrpihifiberry' -n 'Living Room' -O 'default:CARD=Dummy' -V 'Master' 
```

https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-reduced-schematics.pdf


Raspberry Pi GPIO 0-8 default to HIGH which is what we need in order to not trigger any buttons on raspberry pi start. (https://www.raspberrypi.org/app/uploads/2012/02/BCM2835-ARM-Peripherals.pdf#page=102)

| NRF51822 | Default | Raspberry Pi Zero W | Description             |
| -------- | ------- | ------------------- | ----------------------- |
| P0.0     | HIGH    | GPIO 7              | Source switch / pairing |
| P0.04    | HIGH    | GPIO 8              | Power/Mute/Encoder C    |
| P0.01    | LOW     | GPIO 23             | Encoder A               |
| P0.03    | LOW     | GPIO 24             | Encoder B               |
| P0.09    | LOW     | GPIO 25             | LED2                    |
| P0.29    | LOW     | --                  | LED1                    |
| P0.13    | HIGH    | --                  | RX                      |
| P0.14    | HIGH    | --                  | TX                      |
| --       | --      | GPIO 18             | Audio DAC SHIM          |
| --       | --      | GPIO 19             | Audio DAC SHIM          |
| --       | --      | GPIO 21             | Audio DAC SHIM          |



Commands

```
aplay -l
amixer -c 0 get Master
```
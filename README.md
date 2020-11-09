# What's this?

I thought to purchase some Arduino stuff, but then I looked at a calendar.
Man, there was 2020 already, I supposed that it's better to pay extra $2 for one-time purchase 
and get even more fun.
So I got my new `ESP-WROOM-32` with 38 contacts onboard. 
And then it filled up my breadboard, leaving only a single row of contacts.
Was I mocked? Probably, yet let'start this.

# Installation
I've just plugged in micro USB and the ESP32 ready on the COM5 port. 
No external power source was attached, I mean, excepting the one leading to my USB3 hub where the 
ESP32 was connected to.
It was simple.

## Install `esptool`

```shell script
curl -fsSL https://github.com/espressif/esptool/archive/v3.0.zip -o esptool.zip
unzip esptool.zip
rm esptool.zip
cd esptool-3.0
python3 setup.py install

pip install --upgrade esptool
```

## Erase the ESP32 factory firmware

```shell script
python esptool.py --port COM5 erase_flash
```
```text
esptool.py v3.0
Serial port COM5
Connecting....
Detecting chip type... ESP32
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 10:52:1c:5e:64:48
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 3.2s
Hard resetting via RTS pin...
```
## Get & flash the ESP32 no-SPIRAM MicroPython firmware

```shell script
curl -fsSL https://micropython.org/resources/firmware/esp32-idf3-20200902-v1.13.bin -o ../esp32.bin

python esptool.py --chip esp32 --port COM5 --baud 460800 write_flash --flash_size=detect -z 0x1000 ../esp32.bin
```
```text
esptool.py v3.0
Serial port COM5
Connecting....
Chip is ESP32-D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 10:52:1c:5e:64:48
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Compressed 1448768 bytes to 926007...
Wrote 1448768 bytes (926007 compressed) at 0x00001000 in 21.3 seconds (effective 545.4 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```


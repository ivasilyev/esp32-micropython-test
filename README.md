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

# Try to upgrade esptool & necessary tools
pip install --upgrade esptool docopt adafruit-ampy
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
curl -fsSL https://micropython.org/resources/firmware/esp32-idf3-20200902-v1.13.bin -o ../micropython.bin

python esptool.py --chip esp32 --port COM5 --baud 460800 write_flash --flash_size=detect -z 0x1000 ../micropython.bin
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

# Connection

The easiest method is doing this via PUTTY. I've just set:
* Protocol: Serial
* Serial line: COM5
* Baud: 115200

And then I was able to see the CLI working. 
If we're calling REPL CLI, of course.

```text
ets Jun  8 2016 00:22:57

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0018,len:4
load:0x3fff001c,len:5008
ho 0 tail 12 room 4
load:0x40078000,len:10600
ho 0 tail 12 room 4
load:0x40080400,len:5684
entry 0x400806bc
I (539) cpu_start: Pro cpu up.
I (539) cpu_start: Application information:
I (539) cpu_start: Compile time:     Sep  2 2020 03:00:08
I (543) cpu_start: ELF file SHA256:  0000000000000000...
I (549) cpu_start: ESP-IDF:          v3.3.2
I (553) cpu_start: Starting app cpu, entry point is 0x40082f30
I (0) cpu_start: App cpu up.
I (564) heap_init: Initializing. RAM available for dynamic allocation:
I (571) heap_init: At 3FFAFF10 len 000000F0 (0 KiB): DRAM
I (577) heap_init: At 3FFB6388 len 00001C78 (7 KiB): DRAM
I (583) heap_init: At 3FFB9A20 len 00004108 (16 KiB): DRAM
I (589) heap_init: At 3FFBDB5C len 00000004 (0 KiB): DRAM
I (595) heap_init: At 3FFCA9E8 len 00015618 (85 KiB): DRAM
I (601) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (608) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (614) heap_init: At 4009DE28 len 000021D8 (8 KiB): IRAM
I (620) cpu_start: Pro cpu start user code
I (303) cpu_start: Starting scheduler on PRO CPU.
I (0) cpu_start: Starting scheduler on APP CPU.
MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
Type "help()" for more information.
I (946560) modsocket: Initializing
>>>
```

# Why `MicroPython`, not `CircuitPython`?

Ayy LMAO, I can't even install it on my ESP32.
Wanna try?

```shell script
curl -fsSL https://downloads.circuitpython.org/bin/espressif_saola_1_wroom/en_US/adafruit-circuitpython-espressif_saola_1_wroom-en_US-6.0.0-rc.1.bin -o ../circuitpython.bin
python esptool.py --port COM5 erase_flash
python esptool.py --chip esp32 --port COM5 --baud 460800 write_flash --flash_size=detect 0 ../circuitpython.bin
```

At `SERIAL`, you'll probably get something like this:
```text
rst:0x10 (RTCWDT_RTC_RESET),boot:0x12 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3ffe6100,len:8
load:0x3ffe6108,len:6304
load:0x4004c000,len:2352
load:0x40050000,len:11464
entry 0x4004c1b4
Fatal exception (9): LoadStoreAlignment
epc1=0x4005919c, epc2=0x00000000, epc3=0x00000000, excvaddr=0x4004c247, depc=0x00000000
```
It means that the firmware is not working.


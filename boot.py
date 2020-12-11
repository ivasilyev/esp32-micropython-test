# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from utils import Utils

cfg_dict = Utils.read_json("config.json")
Utils.wlan_connect(wlan_essid=cfg_dict["network"]["wlan"]["ssid"],
                   wlan_password=cfg_dict["network"]["wlan"]["password"],
                   hostname="esp32")

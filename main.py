#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import Utils

cfg_dict = Utils.read_json("config.json")
Utils.wlan_connect(wlan_essid=cfg_dict["network"]["wlan"]["ssid"],
                   wlan_password=cfg_dict["network"]["wlan"]["password"],
                   hostname="esp32")

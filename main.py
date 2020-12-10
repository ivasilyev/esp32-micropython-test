#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import Utils
import _thread
from http_server import HTTPServer
from demo import Strip, Animations, AnimationController

cfg_dict = Utils.read_json("config.json")
Utils.wlan_connect(wlan_essid=cfg_dict["network"]["wlan"]["ssid"],
                   wlan_password=cfg_dict["network"]["wlan"]["password"],
                   hostname="esp32")

strip = Strip(17, 16, brightness=1)

animations = Animations(strip)
controller = AnimationController(animations)
_thread.start_new_thread(controller.run, ())

server = HTTPServer(controller)
_thread.start_new_thread(server.run, ())

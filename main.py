#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import Utils

cfg_dict = Utils.read_cfg("config.json")
Utils.do_connect(cfg_dict["network"]["wlan"]["ssid"], cfg_dict["network"]["wlan"]["password"])



#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Utils:
    @staticmethod
    def load_string(file: str):
        with open(file=file, mode="r", encoding="utf-8") as f:
            s = f.read()
            f.close()
        return s

    @staticmethod
    def read_json(file: str):
        from json import load
        with open(file=file, mode="r", encoding="utf-8") as f:
            out = load(f)
            f.close()
        return out

    @staticmethod
    def wlan_connect(wlan_essid, wlan_password, hostname: str = ""):
        from network import WLAN, STA_IF
        from utime import sleep
        controller = WLAN(STA_IF)
        if not controller.isconnected():
            print("Connecting to network: ...")
            controller.active(True)
            if len(hostname) > 0:
                controller.config(dhcp_hostname=hostname)
            controller.connect(wlan_essid, wlan_password)
            while not controller.isconnected():
                sleep(1)
        print("Network connected, the config: {}".format(controller.ifconfig()))

    @staticmethod
    def rm(s):
        import uos as os
        try:
            _ = os.stat(s)[0]
            try:
                os.remove(s)  # A file
            except OSError:  # A folder
                for i in os.listdir(s):
                    s_ = "{}/{}".format(s, i)
                    Utils.rm(s_)
                os.rmdir(s)
        except OSError:
            print("Not found: '{}'".format(s))

    @staticmethod
    def clean_lib():
        _JUNK = ['.github', '.gitignore', '.pre-commit-config.yaml', '.pylintrc', '.readthedocs.yml',
                 '@PaxHeader', 'CODE_OF_CONDUCT.md', 'LICENSES', 'LICENSE', 'docs', 'examples',
                 'pyproject.toml', 'requirements.txt']
        for j in _JUNK:
            Utils.rm("/lib/{}".format(j))

    @staticmethod
    def timeit(func, run_number: int = 1, *args, **kwargs):
        import utime as time
        start = time.ticks_us()
        for i in range(run_number):
            _ = func(*args, **kwargs)
        return time.ticks_diff(time.ticks_us(), start)

    @staticmethod
    def soft_reset():
        # From http://docs.micropython.org/en/v1.8.6/wipy/wipy/tutorial/reset.html
        import sys
        sys.exit()

    @staticmethod
    def hard_reset():
        import machine
        machine.reset()


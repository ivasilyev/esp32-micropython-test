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
        print("Network connected, the configuration: {}".format(controller.ifconfig()))

    @staticmethod
    def rm(s):
        try:
            import uos as os
        except ImportError:
            import os
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

    @staticmethod
    def parse_percent_encoding(s: str):
        # See https://en.wikipedia.org/wiki/Percent-encoding
        pasted_1 = """! 	# 	$ 	% 	& 	' 	( 	) 	* 	+ 	, 	/ 	: 	; 	= 	? 	@ 	[ 	]
        %21 	%23 	%24 	%25 	%26 	%27 	%28 	%29 	%2A 	%2B 	%2C 	%2F 	%3A 	%3B 	%3D 	%3F 	%40 	%5B 	%5D
        """
        pasted_2 = """" 	% 	- 	. 	< 	> 	\ 	^ 	_ 	` 	{ 	| 	} 	~ 	£ 	円
        %22 	%25 	%2D 	%2E 	%3C 	%3E 	%5C 	%5E 	%5F 	%60 	%7B 	%7C 	%7D 	%7E 	%C2%A3 	%E5%86%86
        """
        replacements = []
        for pasted in (pasted_1, pasted_2):
            chars, percents = [[l_ for l_ in [k.strip() for k in j.split(" ")] if len(l_) > 0] for j in [i.strip() for i in pasted.split("\n")] if len(j) > 0]
            for char, percent in zip(chars, percents):
                replacements.append((percent, char))
        replacements.extend([(i.strip(), "\r\n") for i in "%0A or %0D or %0D%0A".split("or")])
        replacements.append(("%20", " "))
        replacements.sort(key=lambda x: len(x[0]), reverse=True)
        for replacement in replacements:
            s = s.replace(*replacement)
        return s

    @staticmethod
    def convert_hex_to_rgb(s: str):
        return tuple(int(s.strip("#")[i:i+2], 16) for i in (0, 2, 4))

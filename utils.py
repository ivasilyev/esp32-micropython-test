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
    def read_cfg(cfg):
        from json import load
        with open(file=cfg, mode="r", encoding="utf-8") as f:
            out = load(f)
            f.close()
        return out

    @staticmethod
    def do_connect(wlan_essid, wlan_password):
        from network import WLAN, STA_IF
        sta_if = WLAN(STA_IF)
        if not sta_if.isconnected():
            print("Connecting to network: ...")
            sta_if.active(True)
            sta_if.connect(wlan_essid, wlan_password)
            while not sta_if.isconnected():
                pass
        print("Network connected, the config: {}".format(sta_if.ifconfig()))

    @staticmethod
    def rm(s):
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

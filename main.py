#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import _thread
from http_server import HTTPServer
from demo import Strip, Animations, AnimationController


def main():
    strip = Strip(17, 16, brightness=1)

    animations = Animations(strip)
    controller = AnimationController(animations)
    _thread.start_new_thread(controller.run, ())

    server = HTTPServer(controller)
    _thread.start_new_thread(server.run, ())

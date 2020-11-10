#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep_ms
from neopixel import NeoPixel
from machine import Pin
from random import randint


class Colors:
    # Inspired by https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation
    # and https://raw.githubusercontent.com/vaab/colour (see below)
    BLACK = (0, 0, 0)
    NAVYBLUE = (0, 0, 128)
    DARKBLUE = (0, 0, 139)
    MEDIUMBLUE = (0, 0, 205)
    BLUE = (0, 0, 255)
    DARKGREEN = (0, 100, 0)
    LIME = (0, 128, 0)
    DARKCYAN = (0, 139, 139)
    DEEPSKYBLUE = (0, 191, 255)
    DARKTURQUOISE = (0, 206, 209)
    MEDIUMSPRINGGREEN = (0, 250, 154)
    GREEN = (0, 255, 0)
    SPRINGGREEN = (0, 255, 127)
    AQUA = (0, 255, 255)
    MIDNIGHTBLUE = (25, 25, 112)
    DODGERBLUE = (30, 144, 255)
    LIGHTSEAGREEN = (32, 178, 170)
    FORESTGREEN = (34, 139, 34)
    SEAGREEN = (46, 139, 87)
    DARKSLATEGREY = (47, 79, 79)
    LIMEGREEN = (50, 205, 50)
    MEDIUMSEAGREEN = (60, 179, 113)
    TURQUOISE = (64, 224, 208)
    ROYALBLUE = (65, 105, 225)
    STEELBLUE = (70, 130, 180)
    DARKSLATEBLUE = (72, 61, 139)
    MEDIUMTURQUOISE = (72, 209, 204)
    INDIGO = (75, 0, 130)
    DARKOLIVEGREEN = (85, 107, 47)
    CADETBLUE = (95, 158, 160)
    CORNFLOWERBLUE = (100, 149, 237)
    MEDIUMAQUAMARINE = (102, 205, 170)
    DIMGREY = (105, 105, 105)
    SLATEBLUE = (106, 90, 205)
    OLIVEDRAB = (107, 142, 35)
    SLATEGREY = (112, 128, 144)
    LIGHTSLATEGREY = (119, 136, 153)
    MEDIUMSLATEBLUE = (123, 104, 238)
    LAWNGREEN = (124, 252, 0)
    CHARTREUSE = (127, 255, 0)
    AQUAMARINE = (127, 255, 212)
    MAROON = (128, 0, 0)
    PURPLE = (128, 0, 128)
    OLIVE = (128, 128, 0)
    GREY = (128, 128, 128)
    LIGHTSLATEBLUE = (132, 112, 255)
    SKYBLUE = (135, 206, 235)
    LIGHTSKYBLUE = (135, 206, 250)
    BLUEVIOLET = (138, 43, 226)
    DARKRED = (139, 0, 0)
    DARKMAGENTA = (139, 0, 139)
    SADDLEBROWN = (139, 69, 19)
    DARKSEAGREEN = (143, 188, 143)
    LIGHTGREEN = (144, 238, 144)
    MEDIUMPURPLE = (147, 112, 219)
    DARKVIOLET = (148, 0, 211)
    PALEGREEN = (152, 251, 152)
    DARKORCHID = (153, 50, 204)
    YELLOWGREEN = (154, 205, 50)
    SIENNA = (160, 82, 45)
    BROWN = (165, 42, 42)
    DARKGREY = (169, 169, 169)
    LIGHTBLUE = (173, 216, 230)
    GREENYELLOW = (173, 255, 47)
    PALETURQUOISE = (175, 238, 238)
    LIGHTSTEELBLUE = (176, 196, 222)
    POWDERBLUE = (176, 224, 230)
    FIREBRICK = (178, 34, 34)
    DARKGOLDENROD = (184, 134, 11)
    MEDIUMORCHID = (186, 85, 211)
    ROSYBROWN = (188, 143, 143)
    DARKKHAKI = (189, 183, 107)
    SILVER = (192, 192, 192)
    MEDIUMVIOLETRED = (199, 21, 133)
    INDIANRED = (205, 92, 92)
    PERU = (205, 133, 63)
    VIOLETRED = (208, 32, 144)
    CHOCOLATE = (210, 105, 30)
    TAN = (210, 180, 140)
    LIGHTGREY = (211, 211, 211)
    THISTLE = (216, 191, 216)
    ORCHID = (218, 112, 214)
    GOLDENROD = (218, 165, 32)
    PALEVIOLETRED = (219, 112, 147)
    CRIMSON = (220, 20, 60)
    GAINSBORO = (220, 220, 220)
    PLUM = (221, 160, 221)
    BURLYWOOD = (222, 184, 135)
    LIGHTCYAN = (224, 255, 255)
    LAVENDER = (230, 230, 250)
    DARKSALMON = (233, 150, 122)
    VIOLET = (238, 130, 238)
    LIGHTGOLDENROD = (238, 221, 130)
    PALEGOLDENROD = (238, 232, 170)
    LIGHTCORAL = (240, 128, 128)
    KHAKI = (240, 230, 140)
    ALICEBLUE = (240, 248, 255)
    HONEYDEW = (240, 255, 240)
    AZURE = (240, 255, 255)
    SANDYBROWN = (244, 164, 96)
    WHEAT = (245, 222, 179)
    BEIGE = (245, 245, 220)
    WHITESMOKE = (245, 245, 245)
    MINTCREAM = (245, 255, 250)
    GHOSTWHITE = (248, 248, 255)
    SALMON = (250, 128, 114)
    ANTIQUEWHITE = (250, 235, 215)
    LINEN = (250, 240, 230)
    LIGHTGOLDENRODYELLOW = (250, 250, 210)
    OLDLACE = (253, 245, 230)
    RED = (255, 0, 0)
    FUCHSIA = (255, 0, 255)
    DEEPPINK = (255, 20, 147)
    ORANGERED = (255, 69, 0)
    TOMATO = (255, 99, 71)
    HOTPINK = (255, 105, 180)
    CORAL = (255, 127, 80)
    DARKORANGE = (255, 140, 0)
    LIGHTSALMON = (255, 160, 122)
    ORANGE = (255, 165, 0)
    LIGHTPINK = (255, 182, 193)
    PINK = (255, 192, 203)
    GOLD = (255, 215, 0)
    PEACHPUFF = (255, 218, 185)
    NAVAJOWHITE = (255, 222, 173)
    MOCCASIN = (255, 228, 181)
    BISQUE = (255, 228, 196)
    MISTYROSE = (255, 228, 225)
    BLANCHEDALMOND = (255, 235, 205)
    PAPAYAWHIP = (255, 239, 213)
    LAVENDERBLUSH = (255, 240, 245)
    SEASHELL = (255, 245, 238)
    CORNSILK = (255, 248, 220)
    LEMONCHIFFON = (255, 250, 205)
    FLORALWHITE = (255, 250, 240)
    SNOW = (255, 250, 250)
    YELLOW = (255, 255, 0)
    LIGHTYELLOW = (255, 255, 224)
    IVORY = (255, 255, 240)
    WHITE = (255, 255, 255)

    def __init__(self):
        self.colors = self.get_colors()

    def get_colors(self):
        return [i for i in dir(self) if i[0].isupper()]

    def randomize(self):
        return Colors.__getattribute__(self, self.colors[randint(0, len(self.colors) - 1)])


class Color:
    # BLACK = tuple([0, ] * 3)
    # WHITE = tuple([255, ] * 3)
    #
    # RED = (255, 0, 0)
    # GREEN = (0, 255, 0)
    # BLUE = (0, 0, 255)
    #
    # YELLOW = (255, 150, 0)
    # ORANGE = (255, 40, 0)
    # TEAL = (0, 255, 120)
    # CYAN = (0, 255, 255)
    # PURPLE = (180, 0, 255)
    # MAGENTA = (255, 0, 20)

    def __init__(self, red, green, blue):
        assert all(i < 256 for i in [red, green, blue])

    @staticmethod
    def randomize():
        dir(Color)

    @staticmethod
    def _convert_colors():
        # Only for use on the systems with `colour` package installed
        # Some color codes are doubtful. E.g. Lime is actually Green
        import colour
        d = colour.RGB_TO_COLOR_NAMES
        for k in d.keys():
            name = d.get(k)[-1].upper()
            print("{} = {}".format(name, k))


class Strip(NeoPixel):
    def __init__(self, pin: int, n: int, bpp=3, auto_write: bool = False):
        # View the super class source:
        # https://github.com/micropython/micropython/blob/master/ports/esp32/modules/neopixel.py
        super().__init__(pin=Pin(pin), n=n, bpp=bpp)
        self.LED_PIN = pin
        self.PIXEL_COUNT = n
        self._auto_write = auto_write

    def _apply(self):
        if self._auto_write:
            self.write()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._apply()

    def __len__(self):
        return self.PIXEL_COUNT

    def __repr__(self):
        return "LED Strip object with {} pixels on pin {}".format(self.PIXEL_COUNT, self.LED_PIN)

    def fill(self, color):
        # if not isinstance(color, Color):
        #     color = Color(*color)
        super().fill(color)
        self._apply()

    def shutdown(self):
        self.fill(Colors.BLACK)

    def fill_except(self, color, idx: int):
        if idx > len(self):
            return
        range_ = list(range(0, len(self)))
        range_.pop(idx)
        for i in range_:
            self[i] = color
        self._apply()


class Animations:
    def __init__(self, strip: Strip):
        self._strip = strip
        self.colors = Colors()

    def bounce(self, color, pause: int = 60):
        for i in range(4 * len(self._strip)):
            for j in range(len(self._strip)):
                self._strip[j] = color
            if (i // len(self._strip)) % 2 == 0:
                self._strip[i % len(self._strip)] = self.colors.BLACK
            else:
                self._strip[len(self._strip) - 1 - (i % len(self._strip))] = self.colors.BLACK
            self._strip.write()
            sleep_ms(pause)

    def bounce2(self, color, pause: int = 60):
        for i in range(4 * len(self._strip)):
            for j in range(len(self._strip)):
                self._strip[j] = color
            if (i // len(self._strip)) % 2 == 0:
                self._strip[i % len(self._strip)] = self.colors.BLACK
            else:
                self._strip[len(self._strip) - 1 - (i % len(self._strip))] = self.colors.BLACK
            self._strip.write()
            sleep_ms(pause)

    def cycle(self, color, reverse: bool = False, pause: int = 25):
        for i in range(4 * len(self._strip)):
            for j in range(len(self._strip)):
                self._strip[j] = self.colors.BLACK
            self._strip[i % len(self._strip)] = color
            self._strip.write()
            sleep_ms(pause)

    def fade(self):
        for i in range(0, 4 * 256, 8):
            for j in range(len(self._strip)):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self._strip[j] = (val, 0, 0)
            self._strip.write()

    def shutdown(self):
        self._strip.fill(self.colors.BLACK)
        self._strip.write()

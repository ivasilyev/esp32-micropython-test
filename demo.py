#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utime import sleep_ms
from neopixel import NeoPixel
from machine import Pin
from random import choice
from gc import collect
import _thread


BLK = (0, 0, 0)


class Color(tuple):
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


class ColorSet(set):
    KNOWN = [i for i in dir(Color) if i[0].isupper()]
    RAINBOW = (Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE)


class ColorIterator:
    def __init__(self, color_set):
        self._color_set = color_set
        self.current = 0

    def __len__(self):
        return len(self._color_set)

    def __iter__(self):
        return self._color_set[self.current]

    def __next__(self):
        out = self.current
        self.current += 1
        if self.current >= self.__len__():
            self.current = 0
        return self._color_set[out]

    def __getitem__(self, idx):
        return self._color_set[idx]


class ColorManager:
    # Inspired by https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation
    # and https://raw.githubusercontent.com/vaab/colour (see below)

    def __init__(self):
        pass

    @staticmethod
    def _convert_colors():
        # Only for use on the systems with `colour` package installed
        # Some color codes are doubtful. E.g. Lime is actually Green
        import colour
        d = colour.RGB_TO_COLOR_NAMES
        for k in d.keys():
            name = d.get(k)[-1].upper()
            print("{} = {}".format(name, k))

    @staticmethod
    def get_known_random_color():
        return getattr(ColorSet, ColorSet.KNOWN[choice(range(len(ColorSet.KNOWN)))])

    @staticmethod
    def get_random_color():
        return tuple([choice(range(256)) for _ in "rgb"])

    @staticmethod
    def count_linspace(start, stop, count: int = 10):
        if count == 2:
            return [start, stop]
        start = float(start)
        stop = float(stop)
        delta = stop - start
        step = delta / (count - 1)
        out = [start, ]
        for ex in range(1, count - 1):
            out.append(round(start + (ex * step), 2))
        out.append(stop)
        return out

    @staticmethod
    def mutate_color(start_color, stop_color, steps: int = 10):
        linspaces = [ColorManager.count_linspace(i, j, steps) for i, j in zip(start_color, stop_color)]
        return [tuple([i[j] for i in linspaces]) for j in range(steps)]

    @staticmethod
    def create_color_loop(color_2d_array, steps: int = 10):
        out = []
        previous = None
        for color in color_2d_array:
            if previous:
                out.extend(ColorManager.mutate_color(previous, color, steps)[:-1])
            previous = color
        out.extend(ColorManager.mutate_color(color_2d_array[-1], color_2d_array[0], steps))
        return out


class AnimationControllerThrowable(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class Strip(NeoPixel):
    def __init__(self, pin: int, n: int, bpp=3, brightness: float = 1., auto_write: bool = False):
        # View the super class source:
        # https://github.com/micropython/micropython/blob/master/ports/esp32/modules/neopixel.py
        super().__init__(pin=Pin(pin), n=n, bpp=bpp)
        self.is_enabled = True
        self.LED_PIN = pin
        self.PIXEL_COUNT = n
        self.range = list(range(len(self)))
        self._range_backup = self.range.copy()
        self.brightness = brightness
        self._auto_write = auto_write
        self.validate()
        self.reset()

    def validate(self):
        if self.brightness > 1.:
            raise ValueError("The brightness coefficient cannot be greater than 1!")

    def disable_auto_write(self):
        self._auto_write = False

    def _apply(self):
        if not self.is_enabled:
            raise AnimationControllerThrowable
        if self._auto_write:
            self.write()

    @staticmethod
    def validate_color(color):
        color = [i if i > 0 else 0 for i in color]
        color = [i if i < 256 else 255 for i in color]
        return color

    def _set_color(self, color):
        if color == "random":
            color = ColorManager.get_random_color()
        color = [round(i * self.brightness) for i in color]
        return self.validate_color(color)

    def __setitem__(self, key, value):
        super().__setitem__(key, self._set_color(value))
        self._apply()

    def __len__(self):
        return self.PIXEL_COUNT

    def __repr__(self):
        return "LED Strip object with {} pixels on pin {}".format(self.PIXEL_COUNT, self.LED_PIN)

    def fill(self, color, range_=()):
        if len(range_) == 0:
            range_ = self.range
        _ = list(map(lambda x: self.__setitem__(x, color), range_))
        self._apply()

    def reset(self):
        self.is_enabled = False
        sleep_ms(100)  # Otherwise the translator does not even notice that
        self.is_enabled = True
        self.fill(BLK, self._range_backup)
        self.write()
        collect()

    def fill_except(self, color, idx: int):
        if idx > len(self):
            return
        range_ = self.range.copy()
        range_.pop(idx)
        self.fill(color, range_)
        self._apply()

    def flip_order(self):
        self.range = self.range[::-1]
        collect()

    def loop_order(self):
        self.range = self.range + self.range[:-1][::-1]
        collect()

    def restore_order(self):
        self.range = self._range_backup.copy()
        collect()


class Animations:
    # Based on: https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
    def __init__(self, strip: Strip, clear: bool = True):
        self._strip = strip
        self._strip.disable_auto_write()
        self.is_clear = clear

    def get_strip(self):
        return self._strip

    @staticmethod
    def pause(ms: int):
        collect()
        sleep_ms(ms)

    def blink_single(self, colors, idx, background=Color.BLACK, pause: int = 15):
        """
        Blinks a certain LED with the given color
        """
        for color in colors:
            self._strip[idx] = color
            self._strip.write()
            self.pause(pause)
            self._strip[idx] = background

    def blink_all(self, colors, background=Color.BLACK, pause: int = 15):
        """
        Blinks the whole strip with the given colors
        """
        for color in colors:
            self._strip.fill(background)
            self._strip.fill(color)
            self._strip.write()
            self.pause(pause)

    def random_blink(self, colors, background=Color.BLACK, pause: int = 15):
        """
        Blinks a random LED with the given colors
        """
        idx = choice(self._strip.range)
        for color in colors:
            self._strip[idx] = color
            self._strip.write()
            self.pause(pause)
            self._strip[idx] = background

    def bounce(self, color, pause: int = 60):
        for i in range(4 * len(self._strip)):
            for j in self._strip.range:
                self._strip[j] = color
            if (i // len(self._strip)) % 2 == 0:
                self._strip[i % len(self._strip)] = Color.BLACK
            else:
                self._strip[len(self._strip) - 1 - (i % len(self._strip))] = Color.BLACK
            self._strip.write()
            self.pause(pause)

    def bounce2(self, colors, background=Color.BLACK, pause: int = 20, always_lit: bool = False):
        _range = self._strip.range + self._strip.range[:-1][::-1]
        for color in colors:
            for idx in _range:
                self._strip[idx] = color
                self._strip.write()
                if not always_lit:
                    self._strip[idx] = background
                self.pause(pause)

    def cycle(self, color, pause: int = 25):
        for i in range(4 * len(self._strip)):
            for j in self._strip.range:
                self._strip[j] = Color.BLACK
            self._strip[i % len(self._strip)] = color
            self._strip.write()
            self.pause(pause)

    def cycle2(self, colors, background=Color.BLACK, reverse: bool = False, pause: int = 20, always_lit: bool = False):
        if not reverse:
            _range = self._strip.range
        else:
            _range = self._strip.range[::-1]
        for color in colors:
            for idx in _range:
                self._strip[idx] = color
                self._strip.write()
                if not always_lit:
                    self._strip[idx] = background
                self.pause(pause)

    def fade(self):
        for i in range(0, 4 * 256, 8):
            for j in self._strip.range:
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self._strip[j] = (val, 0, 0)
            self._strip.write()

    def fade2(self, color, period: int = 500):
        brightest = max(color)
        darken_speed = brightest // period
        while period > 0 and sum(color) > 0:
            color = [i - 1 if i > 0 else 0 for i in color]
            self._strip.fill(color)
            self._strip.write()
            period -= 1

    def blacken(self):
        self._strip.fill(Color.BLACK)
        self._strip.write()

    def _clear(self):
        if self.is_clear:
            self.blacken()

    def animate(self, func, *args, **kwargs):
        self._clear()
        try:
            while True:
                func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self.blacken()


class AnimationController:
    def __init__(self, animations: Animations):
        self.is_running = False
        self._animations = animations
        self._strip = self._animations.get_strip()
        self._current_animation = None
        self._current_animation_args = ()
        self._current_animation_kwargs = dict()

    def restart(self):
        self.is_running = False
        try:
            self._strip.reset()
        except AnimationControllerThrowable:
            pass

    def set_animation(self, animation_name: str, *args, **kwargs):
        if animation_name not in dir(self._animations):
            print("No such animation: '{}'".format(animation_name))
            return
        self._current_animation = animation_name
        self._current_animation_args = args
        self._current_animation_kwargs = kwargs
        self.is_running = True
        sleep_ms(100)  # Same
        print("Change animation to:", animation_name, args, kwargs)

    def run(self):
        while True:
            while not self._current_animation or not self.is_running:
                sleep_ms(100)
            try:
                getattr(self._animations, self._current_animation)(
                    *self._current_animation_args, **self._current_animation_kwargs)
            except AnimationControllerThrowable:
                collect()
            except OSError:
                self.restart()

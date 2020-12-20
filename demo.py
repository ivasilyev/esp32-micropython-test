#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utime import sleep_ms
from neopixel import NeoPixel
from machine import Pin
from random import choice
from gc import collect

BLK = (0, 0, 0)


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
    @staticmethod
    def get_random_color():
        return tuple([choice(range(256)) for _ in "rgb"])

    @staticmethod
    def validate_color(color):
        return [j if j < 256 else 255 for j in [i if i > 0 else 0 for i in color]]

    @staticmethod
    def count_linspace(start, stop, count: int = 10):
        if count <= 2:
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

    @staticmethod
    def convert_hex_to_rgb(s: str):
        try:
            return tuple(int(s.strip("#")[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            print("Failed converting HEX to RGB:", s)
            raise

    @staticmethod
    def convert_rgb_to_hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)


class StripIsNotReadyThrowable(Exception):
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
        self.range = sorted(list(range(self.PIXEL_COUNT)))
        self._range_backup = self.range.copy()
        self.brightness = brightness
        self._auto_write = auto_write
        self._validate_args()
        self.reset()

    def _validate_args(self):
        if self.brightness > 1.:
            raise ValueError("The brightness coefficient cannot be greater than 1!")

    def disable_auto_write(self):
        self._auto_write = False

    def write(self):
        if not self.is_enabled:
            raise StripIsNotReadyThrowable
        super().write()

    def _apply(self):
        if self._auto_write:
            self.write()

    def _get_color(self, color):
        if color == "random":
            color = ColorManager.get_random_color()
        return ColorManager.validate_color([round(i * self.brightness) for i in color])

    def __setitem__(self, index, color):
        super().__setitem__(index, self._get_color(color))
        self._apply()

    def __len__(self):
        return self.PIXEL_COUNT

    def __repr__(self):
        return "LED Strip object with {} pixels on pin {}".format(self.PIXEL_COUNT, self.LED_PIN)

    def fill(self, color, range_=()):
        if len(range_) == 0:
            range_ = self.range
        for idx in range_:
            if not self.is_enabled:
                return
            self[idx] = color
        self._apply()

    def blacken(self):
        # An ultimate directive
        super().fill(BLK)
        super().write()

    def reset(self, pause: int = 100):
        self.is_enabled = False
        sleep_ms(pause)  # Otherwise the translator does not even notice that
        self.is_enabled = True
        self.blacken()
        collect()

    def fill_except(self, color, index: int):
        if index > len(self):
            return
        range_ = self.range.copy()
        range_.pop(index)
        self.fill(color, range_)
        self._apply()

    def flip_order(self):
        self.range = self.range[::-1]
        collect()

    def loop_order(self):
        self.range = self.range + self.range[1:-1][::-1]
        collect()

    def restore_order(self):
        self.range = self._range_backup.copy()
        collect()


class Animations:
    # Based on: https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
    def __init__(self, strip: Strip, clear: bool = True):
        self.is_enabled = True
        self._strip = strip
        self._strip.disable_auto_write()
        self.is_clear = clear
        self.state = dict()

    def stop(self):
        self.is_enabled = False
        sleep_ms(100)
        collect()
        self.is_enabled = True
        # self._strip.blacken()  # Throws `maximum recursion depth exceeded` when in separate thread

    def get_strip(self):
        return self._strip

    @staticmethod
    def pause(ms: int):
        collect()
        sleep_ms(ms)

    def blink_single(self, color, index, background=BLK, pause: int = 15):
        """
        Blinks a certain LED with the given color
        """
        if not self.is_enabled:
            return
        self._strip.fill(background)
        self._strip[index] = color
        self._strip.write()
        self.pause(pause)
        self._strip[index] = background

    def blink_all(self, colors, background=BLK, pause: int = 15):
        """
        Blinks the whole strip with the given colors
        """
        for color in colors:
            if not self.is_enabled:
                return
            self._strip.fill(background)
            self._strip.fill(color)
            self._strip.write()
            self.pause(pause)

    def random_blink(self, colors, background=BLK, pause: int = 15):
        """
        Blinks a random LED with the given colors
        """
        idx = choice(self._strip.range)
        while idx == self.state.get("random_blink_index"):
            idx = choice(self._strip.range)
        for color in colors:
            if not self.is_enabled:
                return
            self.blink_single(color, idx, background, pause)
        self.state["random_blink_index"] = idx

    def bounce(self, color, pause: int = 60):
        for i in range(4 * len(self._strip)):
            for j in self._strip.range:
                self._strip[j] = color
            if (i // len(self._strip)) % 2 == 0:
                self._strip[i % len(self._strip)] = BLK
            else:
                self._strip[len(self._strip) - 1 - (i % len(self._strip))] = BLK
            self._strip.write()
            self.pause(pause)

    def bounce2(self, colors, background=BLK, pause: int = 20, always_lit: bool = False):
        _range = self._strip.range + self._strip.range[1:-1][::-1]
        for color in colors:
            for idx in _range:
                if not self.is_enabled:
                    return
                self._strip[idx] = color
                self._strip.write()
                if not always_lit:
                    self._strip[idx] = background
                self.pause(pause)

    def cycle(self, color, pause: int = 25):
        for i in range(4 * len(self._strip)):
            for j in self._strip.range:
                self._strip[j] = BLK
            self._strip[i % len(self._strip)] = color
            self._strip.write()
            self.pause(pause)

    def cycle2(self, colors, background=BLK, reverse: bool = False, pause: int = 20,
               always_lit: bool = False):
        if not reverse:
            _range = self._strip.range
        else:
            _range = self._strip.range[::-1]
        for color in colors:
            for idx in _range:
                if not self.is_enabled:
                    return
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

    def _clear(self):
        if self.is_clear:
            self._strip.blacken()

    def animate(self, func, *args, **kwargs):
        self._clear()
        try:
            while True:
                func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self._strip.blacken()


class AnimationController:
    def __init__(self, animations: Animations):
        self.is_running = False
        self._animations = animations
        self._strip = self._animations.get_strip()
        self._current_animation = None
        self._current_animation_args = ()
        self._current_animation_kwargs = dict()

    def restart(self):
        pause = 100
        pause_ = self._current_animation_kwargs.get("pause")
        if pause_ is not None and pause_ > pause:
            pause = pause_
        try:
            self._strip.reset(pause)
        except StripIsNotReadyThrowable:
            pass
        except Exception as e:
            print("Animation restart problem:", e)
        sleep_ms(pause)

    def set_animation(self, animation_name: str, *args, **kwargs):
        if animation_name not in dir(self._animations):
            print("No such animation:", animation_name)
            return
        self._current_animation = animation_name
        self._current_animation_args = args
        self._current_animation_kwargs = kwargs
        args_string = ", ".join(str(i) for i in [animation_name, args, kwargs])
        if args_string == self._animations.state.get("current_animation_args"):
            print("The animation parameters were already set")
            return
        print("Change animation to:", animation_name, args, kwargs)
        self._animations.state["current_animation_args"] = args_string
        self.is_running = True
        self._animations.stop()
        self.restart()

    def run(self):
        while True:
            while not self._current_animation or not self.is_running:
                sleep_ms(100)
            try:
                getattr(self._animations, self._current_animation)(
                    *self._current_animation_args, **self._current_animation_kwargs)
            except StripIsNotReadyThrowable:
                collect()

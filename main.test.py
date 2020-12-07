from colors import BoilerPlate as Color
from demo import Strip, Animations, ColorManager

strip = Strip(17, 16, brightness=1, auto_write=True)
animations = Animations(strip)
# animations.animate(animations.cycle2, colors=ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 8), pause=10, always_lit=True)

import uasyncio as asyncio


async def coro_function1():
    animations.cycle2(colors=ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 8), pause=10, always_lit=True)
    return 1

async def coro_function2():
    animations.cycle2(colors=ColorManager.create_color_loop([Color.Red, Color.Aqua], 8), pause=10, always_lit=False)
    return 2

async def get():
    return await coro_function1() + await coro_function2()

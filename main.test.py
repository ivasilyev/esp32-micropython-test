from colors import BoilerPlate as Color
from demo import Strip, Animations, ColorManager

strip = Strip(17, 16, brightness=1, auto_write=True)
animations = Animations(strip)
animations.animate(animations.cycle2, colors=ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 8), pause=10, always_lit=True)

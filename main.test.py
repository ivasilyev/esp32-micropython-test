from color_maps import BoilerPlate as ColorMap
from demo import Strip, Animations, ColorManager

strip = Strip(17, 16, brightness=1, auto_write=True)
animations = Animations(strip)
animations.animate(animations.cycle2, colors=ColorManager.create_color_loop(ColorMap.gist_rainbow, 20), pause=50)

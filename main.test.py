from color_maps import BoilerPlate as ColorMap
from demo import Strip, Animations

strip = Strip(17, 16, brightness=1, auto_write=True)
animations = Animations(strip)
animations.animate(animations.cycle2, colors=ColorMap.jet, pause=100)

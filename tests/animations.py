from demo import Strip, Animations, ColorManager
strip = Strip(17, 16, brightness=1)
animations = Animations(strip)
colors = ColorManager.create_color_loop([(255, 0, 0), (0, 255, 0), (0, 0, 255)], steps=20)
animations.animate(animations.cycle2, colors=colors, pause=20, always_lit=True)

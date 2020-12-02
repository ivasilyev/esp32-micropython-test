from demo import Strip, Animations, ColorSet, ColorIterator
strip = Strip(17, 16, brightness=0.1, auto_write=True)
strip.fill([199,199,199])
strip.fill([0,0,0])

animations = Animations(strip)
animations.random_blink(colors=ColorSet.RAINBOW, pause=10)
animations.animate(animations.random_blink, colors=ColorSet.RAINBOW, pause=100)



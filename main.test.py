import _thread
from http_server import HTTPServer
from colors import BoilerPlate as Color
from demo import Strip, ColorManager, Animations, AnimationController

strip = Strip(17, 16, brightness=1)
animations = Animations(strip)
controller = AnimationController(animations)

server = HTTPServer()

_thread.start_new_thread(server.run, ())
_thread.start_new_thread(controller.run, ())

controller.set_animation("cycle2", colors=ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 30), pause=10, always_lit=False)
controller.set_animation("cycle2", colors=ColorManager.create_color_loop([Color.Green, Color.Red], 20), pause=30, always_lit=True)

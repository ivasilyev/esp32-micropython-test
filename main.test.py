import _thread
from http_server import HTTPServer
from colors import BoilerPlate as Color
from demo import Strip, ColorManager, Animations, AnimationController

strip = Strip(17, 16, brightness=1, auto_write=True)
controller = AnimationController(strip)

server = HTTPServer()
_thread.start_new_thread(server.run, ())
_thread.start_new_thread(controller.run, ())

controller.set_animation("cycle2", colors=ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 8), always_lit=False)
strip.switch()
strip.switch()
controller.set_animation("cycle2", colors=ColorManager.create_color_loop([Color.Green, Color.Red], 20), always_lit=True)

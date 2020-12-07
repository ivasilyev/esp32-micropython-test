import _thread
from http_server import HTTPServer
from colors import BoilerPlate as Color
from demo import Strip, Animations, ColorManager

strip = Strip(17, 16, brightness=1, auto_write=True)
animations = Animations(strip)
server = HTTPServer()

_thread.start_new_thread(server.run, ())
_thread.start_new_thread(animations.animate, (animations.cycle2, ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 8), Color.Black, False, 20, False))

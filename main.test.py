import _thread
from http_server import HTTPServer
from colors import BoilerPlate as Color
from demo import Strip, ColorManager, Animations, AnimationController

strip = Strip(17, 16, brightness=1)

animations = Animations(strip)
controller = AnimationController(animations)

server = HTTPServer(controller)

_thread.start_new_thread(controller.run, ())
_thread.start_new_thread(server.run, ())

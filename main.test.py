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

controller.set_animation("cycle2", colors=ColorManager.create_color_loop([(124, 196, 228), (0, 255, 17)]))



controller.set_animation("cycle2", colors=ColorManager.create_color_loop([(124, 196, 228), (245, 100, 127)]))

controller.set_animation("cycle2", colors=[[124.0, 196.0, 228.0], [137.44, 185.33, 216.78], [150.89, 174.67, 205.56], [164.33, 164.0, 194.33], [177.78, 153.33, 183.11], [191.22, 142.67, 171.89], [204.67, 132.0, 160.67], [218.11, 121.33, 149.44], [231.56, 110.67, 138.22], [245.0, 100.0, 127.0], [231.56, 110.67, 138.22], [218.11, 121.33, 149.44], [204.67, 132.0, 160.67], [191.22, 142.67, 171.89], [177.78, 153.33, 183.11], [164.33, 164.0, 194.33], [150.89, 174.67, 205.56], [137.44, 185.33, 216.78], [124.0, 196.0, 228.0]])

controller.set_animation("cycle2", colors=ColorManager.create_color_loop([Color.Red, Color.Orange, Color.Yellow, Color.Green, Color.Aqua, Color.Blue, Color.Purple], 30), pause=10, always_lit=False)
controller.set_animation("cycle2", colors=ColorManager.create_color_loop([Color.Green, Color.Red], 20), pause=30, always_lit=True)


getattr(controller._animations, "cycle2")()

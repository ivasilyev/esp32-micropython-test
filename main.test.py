from utils import Utils
from demo import Strip, Animations, Colors
strip = Strip(17, 500, brightness=0.1, auto_write=True)


Utils.timeit(strip.fill, color=[199, 199, 199])
# 8086769
Utils.timeit(strip.fill2, color=[199, 199, 199])
# 8084048
Utils.timeit(strip.fill3, color=[199, 199, 199])
# 8084196

Utils.timeit(strip.fill, run_number=10, color=[199, 199, 199])
# 80919121
Utils.timeit(strip.fill2, run_number=10, color=[199, 199, 199])
# 80874443
Utils.timeit(strip.fill3, run_number=10, color=[199, 199, 199])
# 80879480

# The list(map()) is faster

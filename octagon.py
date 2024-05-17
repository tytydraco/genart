from canvas import Canvas
from random import randint
import numpy as np


def lerp(x, start, end):
    return int((1 - x) * start + x * end)


c = Canvas(200, 200)

for x in range(0, c.width):
    for y in range(0, c.height):

        c1 = lerp(x / c.width, 0, 255)
        c2 = lerp(y / c.height, 0, 255)

        c.put(x, y, (c1, c2, c2))

    c.rotate(45)
    c.draw()

c.show('Example')
c.make_gif(30)

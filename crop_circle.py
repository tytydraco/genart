from canvas import Canvas
import random

c = Canvas(512, 512)
c.rotate(15)

for _ in range(0, 365 * 2):
    for y in range(0, c.height // 2):
        color = (random.randint(0, 255),
                 random.randint(0, 255), random.randint(0, 255))
        c.put(c.width // 2, y, color)

    c.rotate(7)
    c.imgDraw()

c.show('Example')

c.make_gif(20)

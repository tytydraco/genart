from canvas import Canvas
import random

c = Canvas(512, 512)

c.apply(lambda frame, x, y, px: (random.randint(0, 255),
        random.randint(0, 255), random.randint(0, 255)))

for _ in range(0, 24):
    for x in range(0, c.width):
        height = random.randint(32, 128)

        for y in range(0, height):
            c.put(x, y, (0, 0, 0))

        if x % 100 == 0:
            c.draw()

    for x in range(0, c.width):
        height = random.randint(32, 128)

        for y in range(c.height - 1, c.height - 1 - height, -1):
            c.put(x, y, (0, 0, 0))

        if x % 100 == 0:
            c.draw()

    c.rotate(15)

c.show('Example')
c.make_gif(20)

from canvas import Canvas
from random import randint

c = Canvas(500, 500)


for i in range(0, 5000):
    x = randint(0, c.width - 1)
    y = randint(0, c.height - 1)

    if i % 2 == 0:
        c.put(x, y, (255, 255, 255))

for _ in range(0, 300):
    c.rotate(1)
    c.draw()

c.show('Example')
c.make_gif(30)

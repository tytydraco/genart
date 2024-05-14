from canvas import Canvas
import random

c = Canvas(512, 512)

c.arc(200, 200, 300, 300, 0, 360, 10, (255, 0, 0))
c.line(200, 200, 300, 300, 10, (0, 255, 0))
c.rect(100, 100, 200, 200, 10, (0, 0, 255))
c.ellipse(300, 300, 400, 400, 20, (0, 255, 255))
c.draw()
c.show('Example')

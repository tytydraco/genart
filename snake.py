from canvas import Canvas
import random

c = Canvas(512, 512)


def xy(x: int, y: int):
    return (x % c.width, y % c.height)


def put_square(x: int, y: int, color: tuple[int, int, int]):
    c.rect(x - 1, y - 1, x + 1, y + 1, 1, color)


def make_snake(iters: int, color: tuple[int, int, int]):
    head_x = random.randint(0, c.width - 1)
    head_y = random.randint(0, c.height - 1)

    prev_d = -1
    for i in range(0, iters):
        travel = random.randint(5, 100)

        d = -1
        while True:
            d = random.randint(0, 3)

            if d == 0 and prev_d == 1 or d == 1 and prev_d == 0:
                continue
            if d == 2 and prev_d == 3 or d == 3 and prev_d == 2:
                continue

            prev_d = d
            break

        for _ in range(0, travel):
            if d == 0:
                head_x -= 1
            elif d == 1:
                head_x += 1
            elif d == 2:
                head_y += 1
            elif d == 3:
                head_y -= 1

            head_x = head_x % c.width
            head_y = head_y % c.height

            put_square(head_x, head_y, color)

        c.draw()


make_snake(255, (255, 0, 0))
make_snake(255, (0, 255, 0))
make_snake(255, (0, 0, 255))
make_snake(255, (0, 255, 255))
make_snake(255, (255, 255, 0))
make_snake(255, (255, 0, 255))
make_snake(255, (255, 255, 255))

c.draw()
c.show('Example')
c.make_gif()

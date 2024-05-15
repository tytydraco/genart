from PIL import Image, ImageDraw
import os
import shutil
import re


class Canvas:
    frame: int
    image: Image

    width: int
    height: int
    frames_dir: str

    def __init__(self, width: int, height: int, out_dir: str = './frames'):
        self.frame = 0
        self.width = width
        self.height = height
        self.frames_dir = out_dir

        self.image = Image.new('RGB', (width, height))

        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        os.mkdir(out_dir)

    def iter(self, func, frames: int, draw: bool = True):
        """
        Parameters
        ----------
        func: function
            Function that takes an argument `frame: int` and
            returns three arguments:
                x: int
                y: int
                color: tuple[int, int, int]
        frames: int
            Number of frames to run through.
        draw: bool = True
            Draw after every iteration.
        """
        for frame in range(0, frames):
            x, y, color = func(frame)

            if x is None or y is None or color is None:
                continue

            self.put(x, y, color)
            if draw:
                self.draw()

    def iters(self, funcs, frames: int, draw: bool = True):
        """
        Parameters
        ----------
        funcs: list[functions]
            A list of function that take an argument `frame: int` and
            returns three arguments:
                x: int
                y: int
                color: tuple[int, int, int]
        frames: int
            Number of frames to run through.
        draw: bool = True
            Draw after every iteration.
        """
        for frame in range(0, frames):
            for func in funcs:
                result = func(frame)

                if result is None:
                    continue

                x, y, color = result

                self.put(x, y, color)
                if draw:
                    self.draw()

    def rotate(self, degrees: float = 90, expand: bool = False, fill_color: tuple[int, int, int] = None, smooth: bool = False):
        """
        Parameters
        ----------
        degrees: float = 90
            Degrees to rotate counter-clockwise.
        expand: bool = False
            Expand the image size. May change dimensions.
        fill_color: tuple[int, int, int] = None
            Color to fill background with.
        smooth: bool = False
            Apply bicubic resampling.
        """
        resampling = Image.Resampling.BILINEAR if smooth else Image.Resampling.NEAREST
        self.image = self.image.rotate(
            degrees, expand=expand, fillcolor=fill_color, resample=resampling)
        self.width, self.height = self.image.size

    def show(self, title: str = None):
        self.image.show(title)

    def apply(self, func):
        """
        Parameters
        ----------
        func: function
            Function that takes arguments `frame: int, x: int, y: int,
            px: tuple[int, int, int]` and returns an argument:
                color: tuple[int, int, int]
        """

        data = self.image.getdata()
        new_data = list(data)
        for i in range(0, len(data)):
            x, y = divmod(i, self.width)
            px = self.get(x, y)
            result = func(self.frame, x, y, px)
            if result is None:
                continue
            new_data[i] = result
        self.image.putdata(new_data)

    def clear(self):
        pixel_cnt = len(self.image.getdata())
        self.image.putdata([(0, 0, 0)] * pixel_cnt)

    def put(self, x: int, y: int, color: tuple[int, int, int]):
        self.image.putpixel((x, y), color)

    def get(self, x: int, y: int) -> tuple[int, int, int]:
        return self.image.getpixel((x, y))

    def arc(self, x1: int, y1: int, x2: int, y2: int, start: int, end: int, width: int, color: tuple[int, int, int]):
        imgDraw = ImageDraw.Draw(self.image)
        imgDraw.arc([(x1, y1), (x2, y2)], start,
                    end, fill=color, width=width)

    def line(self, x1: int, y1: int, x2: int, y2: int, width: int, color: tuple[int, int, int]):
        imgDraw = ImageDraw.Draw(self.image)
        imgDraw.line([(x1, y1), (x2, y2)], fill=color, width=width)

    def rect(self, x1: int, y1: int, x2: int, y2: int, width: int, color: tuple[int, int, int], outline: bool = False):
        imgDraw = ImageDraw.Draw(self.image)

        fc = color
        oc = None
        if outline:
            oc = fc
            fc = None

        imgDraw.rectangle([(x1, y1), (x2, y2)], fill=fc,
                          outline=oc, width=width)

    def ellipse(self, x1: int, y1: int, x2: int, y2: int, width: int, color: tuple[int, int, int], outline: bool = False):
        imgDraw = ImageDraw.Draw(self.image)

        fc = color
        oc = None
        if outline:
            oc = fc
            fc = None

        imgDraw.ellipse([(x1, y1), (x2, y2)], fill=fc, outline=oc, width=width)

    def draw(self):
        output = os.path.join(self.frames_dir, f'{self.frame}.png')
        self.image.save(output, 'png')
        self.frame += 1

    def make_gif(self, fps: int = 30, loop: bool = False):
        def tryint(s):
            try:
                return int(s)
            except ValueError:
                return s

        def alphanum_key(s):
            return [tryint(c) for c in re.split('([0-9]+)', s)]

        def sort_nicely(l):
            return sorted(l, key=alphanum_key)

        frames = os.listdir(self.frames_dir)
        frames = sort_nicely(frames)

        imgs = [Image.open(os.path.join(self.frames_dir, frame))
                for frame in frames]
        output = os.path.join(self.frames_dir, 'out.gif')
        self.image.save(output, 'gif', append_images=imgs,
                        save_all=True, duration=fps, optimize=False, loop=loop)

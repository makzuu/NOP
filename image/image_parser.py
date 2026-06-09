from enum import Enum


class Color(Enum):
    BLACK = 0
    DARKGREY = 1
    BRIGHTGREY = 2
    WHITE = 3
    RED = 4

    @classmethod
    def get_color(cls, value):
        for color in cls:
            if value == color.value:
                return color
        return Color.BLACK


class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


class ImageParser:
    def __init__(self, source):
        self.source = source
        self.pixels = []

        self.cur = None
        self.pos = -1
        self.next()

    def next(self):
        self.pos += 1
        if self.pos >= len(self.source):
            self.cur = "\0"
        else:
            self.cur = self.source[self.pos]

    def add_pixel(self, x, y, color):
        self.pixels.append(Pixel(x, y, color))

    def get_pixels(self):
        x, y = None, None
        x_offset = 0
        while self.cur != "\0":
            if x == None:
                x = self.cur
            elif y == None:
                y = self.cur
            elif ImageParser.is_terminating_value(self.cur):
                x, y = None, None
                x_offset = 0
            else:
                self.add_pixel(x + x_offset, y, Color.get_color(self.cur))
                x_offset += 1

            self.next()

        return self.pixels

    @staticmethod
    def is_terminating_value(value):
        if value < 0:
            return True
        return False


def main():
    # image_parser = ImageParser([0, 0, 3, -1])
    # image_parser.get_pixels()
    # for pixel in image_parser.pixels:
    #     print(pixel.x, pixel.y, pixel.color)

    image_parser = ImageParser([0, 0, 4, 69, 4, 4, 4, -1, 4, 4, 3, 4, -1])
    pixels = image_parser.get_pixels()
    for pixel in pixels:
        print(pixel.x, pixel.y, pixel.color)


if __name__ == "__main__":
    main()

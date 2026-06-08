import pyray as rl
try:
    from .image_parser import ImageParser
except ImportError:
    # para poder ejecutar python screen.py
    from image_parser import ImageParser

class Screen:
    def __init__(self, image_data):
        self.pixel_size = 20
        self.window_width = 30 * self.pixel_size
        self.window_height = 18 * self.pixel_size
        self.colors = [rl.BLACK, rl.DARKGRAY, rl.LIGHTGRAY, rl.WHITE, rl.RED]

        self.init_window()

        self.pixels = ImageParser(image_data).get_pixels()
        self.pos = 0

        self.screen = []

    def init_window(self):
        rl.init_window(self.window_width, self.window_height, "")
        rl.set_target_fps(60)

    def add_pixel_to_screen(self):
        if self.pos < len(self.pixels):
            self.screen.append(self.pixels[self.pos])
            self.pos += 1

    def draw(self):
        while not rl.window_should_close():
            rl.begin_drawing()
            rl.clear_background(rl.BLACK)

            rl.wait_time(0.2)
            self.draw_screen()

            rl.end_drawing()
        rl.close_window()

    def draw_screen(self):
        self.add_pixel_to_screen()

        i = 0
        while i < len(self.screen):
            x = self.pixels[i].x * self.pixel_size
            y = self.pixels[i].y * self.pixel_size
            color = self.colors[self.pixels[i].color.value]

            rl.draw_rectangle(x, y, self.pixel_size, self.pixel_size, color)
            i += 1


def main():
    screen = Screen([0, 0, 3, 3, 3, -1, 5, 4, 8, 49, 1, 2, 3, 4, -1])
    screen.draw()


if __name__ == "__main__":
    main()

from time import sleep
from enum import Enum

class Color(Enum):
    BLACK           = 0
    DARK_GREY       = 1
    BRIGHT_GREY     = 2
    WHITE           = 3
    RED             = 4

class Img:
    def __init__(self):
        self.width = 30
        self.height = 18

        self.drawing_char_width = 3
        self.output_char_width = 8

        self.sleep_time = 0.3

        self.drawing_area = [[" " for _ in range(self.width)] for _ in range(self.height)]

        self.output = []

    def get_input(self):
        return input("< ")

    def write_output(self, n):
        self.output.append(n)
        self.render()

    def get_str_color(self, color):
        block = "\u2588"
        modesoff = "\033[0m"
        if color == Color.BLACK:
            r, g, b = 0, 0, 0
            color = f"\033[38;2;{r};{g};{b}m"
        elif color == Color.DARK_GREY:
            r, g, b = 32, 33, 36
            color = f"\033[38;2;{r};{g};{b}m"
        elif color == Color.BRIGHT_GREY:
            r, g, b = 172, 172, 172
            color = f"\033[38;2;{r};{g};{b}m"
        elif color == Color.WHITE:
            r, g, b = 255, 255, 255
            color = f"\033[38;2;{r};{g};{b}m"
        elif color == Color.RED:
            r, g, b = 255, 0, 0
            color = f"\033[38;2;{r};{g};{b}m"

        return color + block * self.drawing_char_width + modesoff

    def draw(self, draw_instruction):
        if len(draw_instruction) < 4:
            self.render()
            return
        if draw_instruction[-1] >= 0:
            self.render()
            return
        x, y = draw_instruction[:2]
        if x < 0 or x > self.width - 1:
            self.render()
            return
        if y < 0 or y > self.height - 1:
            self.render()
            return

        colors = draw_instruction[2:-1]
        null_character = draw_instruction[-1]

        for color in colors:
            if x < 0 or x > self.width - 1:
                break
            if color in Color:
                self.drawing_area[y][x] = self.get_str_color(Color(color))
            else:
                self.drawing_area[y][x] = self.get_str_color(Color(0))
            x += 1

        self.render()

    def clear_screen(self):
        print("\033[2J", end="")

    def mov_cursor_up(self):
        print("\033[H", end="")

    def render_output(self):
        if self.output_tail_index < len(self.output_tail):
            value = str(self.output_tail[self.output_tail_index])
            print(value + " " * (6 - len(value)), end="")
            self.output_tail_index += 1
        else:
            print(" " * self.output_char_width, end="")

    def render(self):
        self.clear_screen()
        self.mov_cursor_up()
        self.output_tail = self.output[-self.height:]
        self.output_tail_index = 0
        for rows in self.drawing_area:
            self.render_output()
            for cell in rows:
               print(cell, end="")
            print()
        sleep(self.sleep_time)


def main():
    img = Img()

    img.draw([0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])
    img.draw([0, 1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])
    img.draw([0, 2, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])
    img.draw([0, 3, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])
    img.draw([0, 4, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])
    img.draw([0, 5, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])
    img.draw([0, 6, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, -1])

if __name__ == "__main__":
    main()

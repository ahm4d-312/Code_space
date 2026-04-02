import pygame as visualizer
import random
from time import sleep

random.seed(77)
visualizer.init()

class DrawInformation:
    WHITE = 255, 255, 255
    BLACK = 25, 25, 25
    GREY = 107, 107, 107
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    PURPLE_1 = 88, 7, 98
    PURPLE_2 = 131, 11, 145
    CYAN_1= 33, 186, 222
    CYAN_2= 77, 200, 229
    BLUE = 0, 0, 255
    GOLD = 255, 215, 0
    BACKGROUND_COLOR = BLACK

    GRADIENTS = [
        (68, 69, 68),
        (45, 45, 45),
        (92, 92, 92)
    ]

    FONT = visualizer.font.SysFont('comicsans', 24)
    LARGE_FONT = visualizer.font.SysFont('comicsans', 36)

    SIDE_PAD = 20
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = visualizer.display.set_mode((width, height))
        visualizer.display.set_caption("Binary Search Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # width of each bar (at least 1 px)
        self.block_width = max(1, round((self.width - self.SIDE_PAD) / len(lst)))
        # height scaling
        self.block_height = (self.height - self.TOP_PAD) / max(1, self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

        # compute step for very large lists
        self.step = max(1, len(lst) // (self.width - self.SIDE_PAD))


def draw(draw_info: DrawInformation, title_text, target_input, status_text="", min_val=1, max_val=1):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # title
    title = draw_info.LARGE_FONT.render(title_text, 1, draw_info.GREY)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 20))

    # controls
    controls = draw_info.FONT.render(
        "R - Reset | SPACE - Start | Type number + ENTER", 1, draw_info.WHITE
    )
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 60))

    # target input
    input_text = draw_info.FONT.render(f"Target Input: {target_input}", 1, draw_info.GREEN)
    draw_info.window.blit(input_text, (draw_info.width/2 - controls.get_width()/2, 100))

    # status
    status = draw_info.FONT.render(status_text, 1, draw_info.GOLD)
    draw_info.window.blit(status, (draw_info.width/2 - controls.get_width()/2, 120))

    # min/max
    min_text = draw_info.FONT.render(f"Min value={min_val}", 1, draw_info.GREY)
    draw_info.window.blit(min_text, (20, 20))
    max_text = draw_info.FONT.render(f"Max value={max_val}", 1, draw_info.GREY)
    draw_info.window.blit(max_text, (20, 40))

    draw_list(draw_info)
    visualizer.display.update()


def draw_list(draw_info: DrawInformation, color_positions={}, clear_bg=False,
            target_index=None, left=None, right=None, mid=None):
    lst = draw_info.lst

    if clear_bg:
        # full clear of drawing area
        clear_rect = (
            draw_info.SIDE_PAD // 2,
            draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD
        )
        clear_corner=(
			20,
			60,
			100,
			100
		)
        visualizer.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
        visualizer.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_corner)

    # draw bars with step for large lists
    for i in range(0, len(lst), draw_info.step):
        val = lst[i]
        x = draw_info.start_x + (i // draw_info.step) * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val+20) * draw_info.block_height
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        visualizer.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

        # draw target above its bar
        if target_index == i:
            text = draw_info.FONT.render(str(val), 1, draw_info.GOLD)
            draw_info.window.blit(text, (x, y - 25))

    # low/mid/high text
    left_text = draw_info.FONT.render(f"low={left}", 1, draw_info.GREY)
    draw_info.window.blit(left_text, (20, 60))
    mid_text = draw_info.FONT.render(f"mid={mid}", 1, draw_info.GREY)
    draw_info.window.blit(mid_text, (20, 80))
    right_text = draw_info.FONT.render(f"top={right}", 1, draw_info.GREY)
    draw_info.window.blit(right_text, (20, 100))

    if clear_bg:
        visualizer.display.update()
        sleep(1)  # controlled slowdown


def generate_starting_list(n, min_val, max_val):
    return sorted(random.randint(min_val, max_val) for _ in range(n))


def binary_search(draw_info: DrawInformation, target):
    lst = draw_info.lst
    left = 0
    right = len(lst) - 1

    while left <= right:
        mid = (left + right) // 2
        status = f"L={left} ({lst[left]})  M={mid} ({lst[mid]})  R={right} ({lst[right]})"

        draw_list(draw_info, {
            left: draw_info.CYAN_1,
            right: draw_info.CYAN_2,
            mid: draw_info.GREEN
        }, True, left=left, mid=mid, right=right)

        yield status

        if lst[mid] == target:
            draw_list(draw_info, {mid: draw_info.GOLD}, True, target_index=mid)
            yield f"FOUND at index {mid}"
            return
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    yield "NOT FOUND"


def main():
    run = True
    clock = visualizer.time.Clock()

    n = 950
    min_val = 0
    max_val = n

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1920, 1080, lst)

    searching = False
    search_generator = None

    target_input = ""
    target = None
    status_text = ""

    while run:
        clock.tick(60)

        if searching:
            try:
                status_text = next(search_generator)
            except StopIteration:
                searching = False
        else:
            draw(draw_info, "Binary Search", target_input, status_text, min_val, max_val)

        for event in visualizer.event.get():
            if event.type == visualizer.QUIT:
                run = False
            if event.type == visualizer.KEYDOWN:
                if event.key == visualizer.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    target_input = ""
                    target = None
                    searching = False
                    status_text = ""
                elif (event.key == visualizer.K_RETURN or event.key == visualizer.K_SPACE) and target_input.isdigit():
                    target = int(target_input)
                    status_text = f"Target set to {target}"
                    searching = True
                    search_generator = binary_search(draw_info, target)
                elif event.key == visualizer.K_BACKSPACE:
                    target_input = target_input[:-1]
                else:
                    if event.unicode.isdigit():
                        target_input += event.unicode

    visualizer.quit()


if __name__ == "__main__":
    main()
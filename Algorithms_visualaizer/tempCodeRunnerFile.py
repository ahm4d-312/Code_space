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

    YELLOW_GRADIENTS=[
        (227,192,18),
        (227,217,18),
        (227,166,18)
    ]

    GREEN_GRADIENTS =[
        (7, 252, 0),
        (0,252,119),
        (133,252,0)
    ]
    BLUE= 0, 6, 219
    BLUE_GRADIENTS=[
        (0,6,219),
        (0,6,122),
        (0,139,193)
    ]
    CYAN= 77, 200, 229
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
            target_index=None, low=None, quarter_1=None,quarter_2=None,quarter_3=None, top=None,which_quarter=None,FLAG=False):
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
			200,
			100
		)
        visualizer.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
        visualizer.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_corner)

    # draw bars with step for large lists
    for i in range(0, len(lst), draw_info.step):
        val = lst[i]
        x = draw_info.start_x + (i // draw_info.step) * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val+5) * draw_info.block_height
        color = draw_info.GRADIENTS[i % 3]


        if which_quarter and i >= which_quarter[0] and i <= which_quarter[1]:
            color=draw_info.GREEN_GRADIENTS[i%3]

        if which_quarter and i >= which_quarter[0] and i <= which_quarter[1] and FLAG:
            color=draw_info.YELLOW_GRADIENTS[i%3]

        if i in color_positions:
            color = color_positions[i]


        visualizer.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

        # draw target above its bar
        if target_index == i:
            text = draw_info.FONT.render(str(val), 1, draw_info.GOLD)
            draw_info.window.blit(text, (x, y - 25))

    # low/mid/high text
    left_info = draw_info.FONT.render(f"low={low}", 1, draw_info.GREY)
    draw_info.window.blit(left_info, (20, 60))
    
    quarters_info=[f"",f"",f""]
    
    quarter_1_info = draw_info.FONT.render(f"quarter_1={quarter_1}" , 1, draw_info.GREY)
    draw_info.window.blit(quarter_1_info, (20, 80))
    
    quarter_2_info = draw_info.FONT.render(f"quarter_2={quarter_2}", 1, draw_info.GREY)
    draw_info.window.blit(quarter_2_info, (20, 100))
    
    quarter_3_info = draw_info.FONT.render(f"quarter_3={quarter_3}", 1, draw_info.GREY)
    draw_info.window.blit(quarter_3_info, (20, 120))
    
    top_info = draw_info.FONT.render(f"top={top}", 1, draw_info.GREY)
    draw_info.window.blit(top_info, (20, 140))

    if clear_bg:
        visualizer.display.update()
        #input()
        sleep(1)  # controlled slowdown


def generate_starting_list(n, min_val, max_val):
    return sorted(random.randint(min_val, max_val) for _ in range(n))

def quadratic_search(draw_info:DrawInformation, target:int):
    lis=draw_info.lst

    low, top= 0, len(lis)-1
    which_quarter=None
    
    while top-low > 4:
        quarter = low + ((top-low) >> 2)
        quarter_interval = quarter - low
        low_copy=low
        top_copy=top
        if target < lis[quarter]:
            which_quarter=(low,quarter)
            top=quarter-1
        elif target < lis[quarter+quarter_interval]:
            which_quarter=(quarter,quarter+quarter_interval)
            low=quarter
            top=quarter+quarter_interval-1     
        elif target < lis[quarter+quarter_interval*2]:
            which_quarter=(quarter+quarter_interval,quarter+quarter_interval*2)
            low=quarter+quarter_interval
            top=quarter+quarter_interval*2-1
        else:
            which_quarter=(quarter+quarter_interval*2,top)
            low=quarter+quarter_interval*2
        status=None
        draw_list(draw_info, {
            low_copy: draw_info.CYAN,
            quarter: draw_info.BLUE_GRADIENTS[quarter%3],
            quarter+quarter_interval: draw_info.BLUE_GRADIENTS[(quarter+1)%3],
            quarter+quarter_interval*2: draw_info.BLUE_GRADIENTS[(quarter+2)%3],
            top_copy: draw_info.CYAN
        }, True, low=low, quarter_1=quarter,quarter_2=quarter+quarter_interval,quarter_3=quarter+quarter_interval*2, top=top,which_quarter=which_quarter)
        yield status
    draw_list(draw_info=draw_info,which_quarter=which_quarter,clear_bg=True,FLAG=True)
    for i in range(low,top+1):
        draw_list(draw_info, {
            low: draw_info.CYAN,
            top: draw_info.CYAN,
            i: draw_info.BLUE_GRADIENTS[i%3]
        }, True, low=low, quarter_1=quarter,quarter_2=quarter+quarter_interval,quarter_3=quarter+quarter_interval*2, top=top)
        
        if target==lis[i]:
            draw_list(draw_info=draw_info,color_positions={i:draw_info.GOLD}, clear_bg=True,target_index=i)
            yield f"FOUND at index {i}"
            return
        
    yield "Not Found"


def main():
    run = True
    clock = visualizer.time.Clock()

    n = 100
    min_val = 0
    max_val = n

    lis = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1920, 1080, lis)
    print(lis[-1])
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
                    lis = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lis)
                    target_input = ""
                    target = None
                    searching = False
                    status_text = ""
                elif (event.key == visualizer.K_RETURN or event.key == visualizer.K_SPACE) and target_input.isdigit():
                    target = int(target_input)
                    status_text = f"Target set to {target}"
                    searching = True
                    search_generator = quadratic_search(draw_info, target)
                elif event.key == visualizer.K_BACKSPACE:
                    target_input = ""
                else:
                    if event.unicode.isdigit():
                        target_input += event.unicode

    visualizer.quit()


if __name__ == "__main__":
    main()
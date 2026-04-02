import pygame as visualizer
import random
from time import sleep

amount_of_iterations=0
random.seed(77)
visualizer.init()

class VisualizerConfigs:
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


def visualization_handler(VisualizerObject: VisualizerConfigs, title_text, target_input, status_text="", min_val=1, max_val=1):
    VisualizerObject.window.fill(VisualizerObject.BACKGROUND_COLOR)

    # title
    title = VisualizerObject.LARGE_FONT.render(title_text, 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(title, (VisualizerObject.width/2 - title.get_width()/2, 20))

    # controls
    controls = VisualizerObject.FONT.render(
        "R - Reset | SPACE - Start | Type number + ENTER", 1, VisualizerObject.WHITE
    )
    VisualizerObject.window.blit(controls, (VisualizerObject.width/2 - controls.get_width()/2, 60))

    # target input
    input_text = VisualizerObject.FONT.render(f"Target Input: {target_input}", 1, VisualizerObject.GREEN)
    VisualizerObject.window.blit(input_text, (VisualizerObject.width/2 - controls.get_width()/2, 100))

    # status
    status = VisualizerObject.FONT.render(status_text, 1, VisualizerObject.GOLD)
    VisualizerObject.window.blit(status, (VisualizerObject.width/2 - controls.get_width()/2, 120))

    # min/max
    min_text = VisualizerObject.FONT.render(f"Min value={min_val}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(min_text, (20, 20))
    max_text = VisualizerObject.FONT.render(f"Max value={max_val}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(max_text, (20, 40))

    list_visualizer(VisualizerObject)
    visualizer.display.update()

def list_visualizer(VisualizerObject: VisualizerConfigs, color_positions={}, clear_bg=False,
            target_index=None, low=None, quarter_1=None, quarter_2=None, quarter_3=None, top=None, which_quarter=None, FLAG=False):
    lst = VisualizerObject.lst

    if clear_bg:
        # full clear of drawing area
        clear_rect = (
            VisualizerObject.SIDE_PAD // 2,
            VisualizerObject.TOP_PAD,
            VisualizerObject.width - VisualizerObject.SIDE_PAD,
            VisualizerObject.height - VisualizerObject.TOP_PAD
        )
        clear_corner=(
			20,
			60,
			200,
			100
		)
        visualizer.draw.rect(VisualizerObject.window, VisualizerObject.BACKGROUND_COLOR, clear_rect)
        visualizer.draw.rect(VisualizerObject.window, VisualizerObject.BACKGROUND_COLOR, clear_corner)

    # draw bars with step for large lists
    for i in range(0, len(lst), VisualizerObject.step):
        val = lst[i]
        x = VisualizerObject.start_x + (i // VisualizerObject.step) * VisualizerObject.block_width
        y = VisualizerObject.height - (val - VisualizerObject.min_val+5) * VisualizerObject.block_height
        color = VisualizerObject.GRADIENTS[i % 3]


        if which_quarter and i >= which_quarter[0] and i <= which_quarter[1]:
            color=VisualizerObject.GREEN_GRADIENTS[i%3]

        if which_quarter and i >= which_quarter[0] and i <= which_quarter[1] and FLAG:
            color=VisualizerObject.YELLOW_GRADIENTS[i%3]

        if i in color_positions:
            color = color_positions[i]


        visualizer.draw.rect(VisualizerObject.window, color, (x, y, VisualizerObject.block_width, VisualizerObject.height))

        # draw target above its bar
        if target_index == i:
            text = VisualizerObject.FONT.render(str(val), 1, VisualizerObject.GOLD)
            VisualizerObject.window.blit(text, (x, y - 25))

    # low/mid/high text
    left_info = VisualizerObject.FONT.render(f"low={low}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(left_info, (20, 60))
    
    quarters_info=[f"",f"",f""]
    
    quarter_1_info = VisualizerObject.FONT.render(f"quarter_1={quarter_1}" , 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(quarter_1_info, (20, 80))
    
    quarter_2_info = VisualizerObject.FONT.render(f"quarter_2={quarter_2}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(quarter_2_info, (20, 100))
    
    quarter_3_info = VisualizerObject.FONT.render(f"quarter_3={quarter_3}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(quarter_3_info, (20, 120))
    
    top_info = VisualizerObject.FONT.render(f"top={top}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(top_info, (20, 140))
    
    total_iterations = VisualizerObject.FONT.render(f"totol iteration={amount_of_iterations}", 1, VisualizerObject.GREY)
    VisualizerObject.window.blit(total_iterations, (20, 160))
    if clear_bg:
        visualizer.display.update()
        #input()
        sleep(1)  # controlled slowdown


def generate_starting_list(n, min_val, max_val):
    return sorted(random.randint(min_val, max_val) for _ in range(n))

def quadratic_search(VisualizerObject:VisualizerConfigs, target:int):
    lis=VisualizerObject.lst

    low, top= 0, len(lis)-1
    which_quarter=None
    global amount_of_iterations
    amount_of_iterations=0
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
        list_visualizer(VisualizerObject, {
            low_copy: VisualizerObject.CYAN,
            quarter: VisualizerObject.BLUE_GRADIENTS[quarter%3],
            quarter+quarter_interval: VisualizerObject.BLUE_GRADIENTS[(quarter+1)%3],
            quarter+quarter_interval*2: VisualizerObject.BLUE_GRADIENTS[(quarter+2)%3],
            top_copy: VisualizerObject.CYAN
        }, True, low=low, quarter_1=quarter,quarter_2=quarter+quarter_interval,quarter_3=quarter+quarter_interval*2, top=top,which_quarter=which_quarter)
        amount_of_iterations+=1
        yield status
    list_visualizer(VisualizerObject=VisualizerObject,which_quarter=which_quarter,clear_bg=True,FLAG=True,quarter_1=quarter,quarter_2=quarter+quarter_interval,quarter_3=quarter+quarter_interval*2, top=top)
    for i in range(low,top+1):
        list_visualizer(VisualizerObject, {
            low: VisualizerObject.CYAN,
            top: VisualizerObject.CYAN,
            i: VisualizerObject.BLUE_GRADIENTS[i%3]
        }, True, low=low, top=top)
        amount_of_iterations+=1
        if target==lis[i]:

            list_visualizer(VisualizerObject=VisualizerObject,color_positions={i:VisualizerObject.GOLD}, clear_bg=True,target_index=i)
            visualizer.display.update()

            yield f"FOUND at index {i}"
            return
    
    yield "Not Found"


def main():
    run = True
    clock = visualizer.time.Clock()

    n = int(input())
    min_val = 0
    max_val = n

    lis = generate_starting_list(n, min_val, max_val)
    VisualizerObject = VisualizerConfigs(1920, 1080, lis)
    print(lis)
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
            visualization_handler(VisualizerObject, "Quadratic Search", target_input, status_text, min_val, max_val)

        for event in visualizer.event.get():
            if event.type == visualizer.QUIT:
                run = False
            if event.type == visualizer.KEYDOWN:
                if event.key == visualizer.K_r:
                    lis = generate_starting_list(n, min_val, max_val)
                    VisualizerObject.set_list(lis)
                    target_input = ""
                    target = None
                    searching = False
                    status_text = ""
                elif (event.key == visualizer.K_RETURN or event.key == visualizer.K_SPACE) and target_input.isdigit():
                    target = int(target_input)
                    status_text = f"Target set to {target}"
                    searching = True
                    search_generator = quadratic_search(VisualizerObject, target)
                elif event.key == visualizer.K_BACKSPACE:
                    target_input = ""
                else:
                    if event.unicode.isdigit():
                        target_input += event.unicode

    visualizer.quit()


if __name__ == "__main__":
    main()
def quadratic_search(draw_info:DrawInformation, target:int):
    lis=draw_info.lst

    low, top= 0, len(lis)-1
    while top-low > 4:
        mid = low + ((top-low) >> 2)
        quarter_interval = mid - low

        status =None# f"L={low} ({lis[low]})  M={mid} ({lis[mid]})  R={top} ({lis[top]})"
        draw_list(draw_info, {
            low: draw_info.CYAN_1,
            mid: draw_info.CYAN_2,
            mid: draw_info.GREEN
        }, True, left=left, mid=mid, right=right,which_half=which_half)

        yield status

        if target < lis[mid]:
            top=mid-1
        elif target < lis[mid+quarter_interval]:
            low=mid
            top=mid+quarter_interval-1
        elif target < lis[mid+quarter_interval*2]:
            low=mid+quarter_interval
            top=mid+quarter_interval*2-1
        else:
            low=mid+quarter_interval*2
    
    for i in range(low,top+1):
        if target==lis[i]:
            return i
    return -1


def draw_list_(draw_info: DrawInformation, color_positions={}, clear_bg=False,
            target_index=None, low=None, top=None, mid=None,which_half=None):
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

        if which_half is not None:
            if which_half:
                if i > mid and i < top:
                    color=draw_info.GREEN_GRADIENTS[i%3]
            else:
                if i < mid and i > low:
                    color=draw_info.GREEN_GRADIENTS[i%3]

        if i in color_positions:
            color = color_positions[i]

        visualizer.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

        # draw target above its bar
        if target_index == i:
            text = draw_info.FONT.render(str(val), 1, draw_info.GOLD)
            draw_info.window.blit(text, (x, y - 25))

    # low/mid/high text
    left_text = draw_info.FONT.render(f"low={low}", 1, draw_info.GREY)
    draw_info.window.blit(left_text, (20, 60))
    mid_text = draw_info.FONT.render(f"mid={mid}", 1, draw_info.GREY)
    draw_info.window.blit(mid_text, (20, 80))
    right_text = draw_info.FONT.render(f"top={top}", 1, draw_info.GREY)
    draw_info.window.blit(right_text, (20, 100))

    if clear_bg:
        visualizer.display.update()
        sleep(1)  # controlled slowdown

def binary_search(draw_info:DrawInformation, target):
    lst = draw_info.lst
    left = 0
    right = len(lst) - 1
    which_half=True
    while left <= right:
        mid = (left + right) // 2

        if lst[mid] == target:
            draw_list(draw_info, {mid: draw_info.GOLD}, True, target_index=mid)
            yield f"FOUND at index {mid}"
            return
        elif lst[mid] < target:
            which_half=True
            left = mid + 1
        else:
            which_half=False
            right = mid - 1
        status=None
        draw_list(draw_info, {
            left: draw_info.CYAN,
            right: draw_info.CYAN,
            mid: draw_info.GREEN
        }, True, low=left, mid=mid, top=right,which_half=which_half)
        yield status

    yield "NOT FOUND"


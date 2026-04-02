import pygame as visualizer
import numpy as np
from math import floor

visualizer.init()
class Visualizer_config:
    BLACK=0, 0, 0
    WHITE=255, 255, 255
    GREEN=0, 255, 0
    RED=255, 0, 0

    elements_colors=[
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]
    BACKGROUND_COLOR=WHITE
    SIDE_PAD=100
    TOP_PAD=150
    def __init__(self, width, hight, lis):
        self.width=width
        self.hight=hight
        
        self.window=visualizer.display.set_mode((self.width,self.hight))
        visualizer.display.set_caption("Binary Search Visualizer")
        self.set_list(lis)
    
    def set_list(self, lis):
        self.lis=lis
        self.min_value=min(lis)
        self.max_value=max(lis)

        self.block_width=round((self.width-self.SIDE_PAD)/len(lis))
        self.block_hight=floor((self.hight-self.TOP_PAD)/(self.max_value-self.min_value))
        self.start_x=self.SIDE_PAD >> 1

def list_generator(length):
    return np.arange(0,length)

def main_window(visualizer_object:Visualizer_config):
    visualizer_object.window.fill(visualizer_object.BACKGROUND_COLOR)
    draw_list(visualizer_object)
    visualizer.display.update()


def draw_list(visualizer_object:Visualizer_config):
    lis=visualizer_object.lis
    for pos, value in enumerate(lis):
        x= visualizer_object.start_x + pos *visualizer_object.block_width
        y= visualizer_object.hight - (value-visualizer_object.min_value)*visualizer_object.block_hight

        color=visualizer_object.elements_colors[pos%3]

        visualizer.draw.rect(visualizer_object.window, color, (x,y,visualizer_object.block_width, visualizer_object.hight))


def main():
    clock=visualizer.time.Clock()
    running=True
    lis=list_generator(100)
    window=Visualizer_config(800,800,lis)
    while running:
        clock.tick(60)
        main_window(window)
        
        for event in visualizer.event.get():
            visualizer.display.update()
            if event.type==visualizer.QUIT:
                running=False
    visualizer.quit()

if __name__=="__main__":
    main()
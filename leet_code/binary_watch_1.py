def main():
    num=int(input())
    leds=[1, 2, 4, 8, 1, 2, 4, 8, 16, 32]
    combinations=set()
    for i in range(len(leds)):
        hours=0
        minutes=0
        for ii in range(i,len(leds)):
            for iii in range(i,i+num+1):
                if i<4:
                    hours+=combinations[iii]
class Solution:
    def readBinaryWatch(self, turnedOn: int):
        leds=[(0,1), (1,2), (2,4), (3,8), (4,1), (5,2), (6,4), (7,8), (8,16), (9,32)]
        combiniations=set()
        for i in range(len(leds)-turnedOn+1):
            hours=0
            minutes=0
            for ii in range(i,i+turnedOn):
                if leds[ii][0]<4:
                    hours+=leds[ii][1]
                else:
                    minutes=leds[ii][1]
            if hours>11:
                continue
            combiniations.add(f"{hours}:{minutes:02d}")
        return list(combiniations)


#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from collections import deque
from threading import Thread
import time
candle = deque(xrange(12))
def burn(direction, nextSource):
    while True:
        try:
            next_ = nextSource()
        except IndexError:
            break
        else:
            print "%8s: %s" % (direction, next_)
            time.sleep(0.1)
    print "%8s done" % direction
    return

left = Thread(target=burn, args=("Left", candle.popleft))
right = Thread(target=burn, args=("Right", candle.pop))

left.start()
right.start()

right.join()
left.join()

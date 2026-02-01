import threading
import time

x = 0
start_event = threading.Event()
lock = threading.Lock()

def set_x():
    global x
    x = 0

def th_1():
    start_event.wait()
    global x
    with lock:
        x += 1

def th_2():
    start_event.wait()
    global x
    with lock:
        x += 1

def thread_maker():
    th1 = threading.Thread(target=th_1)
    th2 = threading.Thread(target=th_2)
    return th1, th2
t1=int(time.time())
while True:
    if int(time.time()-t1)==10:
        break
    start_event.clear()
    th1, th2 = thread_maker()
    th1.start()
    th2.start()
    start_event.set()

    th1.join()
    th2.join()
    print(x)
    set_x()

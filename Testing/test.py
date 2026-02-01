import threading
x=0
start_event=threading.Event()

def set_x():
    global x
    x=0

def th_1():
    start_event.wait()
    global x
    x+=1

def th_2():
    start_event.wait()
    global x
    x+=1

def thread_maker():
    th1=threading.Thread(target=th_1)
    th2=threading.Thread(target=th_2)
    return (th1,th2)

while True:
    th1,th2=thread_maker()
    th1.start()
    th2.start()
    start_event.set()

    print(x)
    set_x()
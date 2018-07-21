import threading
import time
def fun_timer():
    global Cnt
    Cnt = Cnt+1
   
global Cnt
Cnt = 1
timer = threading.Timer(2, fun_timer)
timer.start()
while True:
    print(Cnt)
    time.sleep(0.5)
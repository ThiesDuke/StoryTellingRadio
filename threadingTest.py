import multiprocessing as mp
from multiprocessing import Process
from threading import Thread

import time
import led

pin_a = 22
pin_b = 23
colors = [0x0000FF, 0xFF0000]
R = 17
G = 18
B = 27


def loop_a():
    global colors
    led.setup(R, G, B)
    while True:
        print("loop a")
        led.setColor(colors[0])
        time.sleep(1)


def loop_b():
    global colors
    led.setup(R, G, B)
    while True:
        print("loop bbbb")
        led.setColor(colors[1])
        time.sleep(1)

def destroy():
    GPIO.cleanup()
    

if __name__ == "__main__":
    try:
        #led.setColor(colors[0])
        
        #Direct run of functions
        #loop_a()
        #loop_b()
        #setup()
        #run()
        
        #Threading of functions
        #ThreadA = Thread(target= loop_a)
        #ThreadB = Thread(target= loop_b)
        #ThreadB.run()
        #time.sleep(5)
        #ThreadA.run()
        #ThreadA.join()
        #ThreadB.join()
        
        #Multiprocessing of functions
        #mp.set_start_method('spawn')
        p_a = mp.Process(target=loop_a)
        p_b= mp.Process(target=loop_b)
        p_a.start()
        p_b.start()
        p_a.join()
        p_b.join()
        #p_b.Process(target=main).start()
        
    except KeyboardInterrupt:
        destroy()
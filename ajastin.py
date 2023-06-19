import time
from pynput.keyboard import Listener

timer = 0

def on_press(key):
    if key == 'w':
        time.sleep(1)
        timer += 1
        print(timer)


with Listener(on_press=on_press) as ls:
    ls.join()

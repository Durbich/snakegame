from keyboard import read_key
import time


class Control:

    def __init__(self):
        self.last_key = None
        self.needed_key = ('w', 'a', 's', 'd')

    def key_wait(self):
        while True:
            key = read_key()
            time.sleep(0.05)
            if key in self.needed_key:
                self.last_key = key

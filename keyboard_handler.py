import keyboard
import time
from threading import Thread
import sys


class KeyboardHandler:
    def __init__(self) -> None:
        self.enable: bool = True
        self.current_key: str = None
        self.last_key: str = None
        self.start()

    def handle_keyboard(self, enable):
        while enable:
            if key := keyboard.read_key():
                if key == self.last_key:
                    self.current_key = None
                else:
                    self.current_key = key

    def get_last_key(self):
        self.last_key = self.current_key
        # self.current_key = key
        return self.last_key

    def start(self):
        Thread(target=self.handle_keyboard, daemon=True, args=(self.enable,)).start()

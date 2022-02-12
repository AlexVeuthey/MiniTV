import tkinter as tk

import yaml
from pynput import keyboard

from minitv.button_grid import ButtonGrid
from minitv.event_manager import manager


def on_press(key):
    try:
        if key.vk == 269025048:
            print("Caught home key")
            manager.emit('quit')
    except Exception:
        pass


def on_release(key):
    pass


def main():
    # main window
    window = tk.Tk()
    window.attributes("-fullscreen", True)

    # setup button grid
    with open('buttons.yml', 'r') as fid:
        config = yaml.safe_load(fid)
    ButtonGrid(window, window.winfo_screenwidth(), window.winfo_screenheight(), config)

    # start keyboard listener thread
    listener = keyboard.Listener(on_press=on_press,
                                 on_release=on_release)

    listener.start()

    window.mainloop()


if __name__ == '__main__':
    main()

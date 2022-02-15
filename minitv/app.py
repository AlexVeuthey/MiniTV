import threading
import tkinter as tk

import alsaaudio
import yaml
from pynput import keyboard

from minitv.button_grid import ButtonGrid
from minitv.event_manager import manager
from minitv.file_manager import check_new_drives


def on_press(key):
    # catch special keys first
    if key == keyboard.Key.enter:
        print("Caught enter key")
        manager.emit('proceed')
    if key == keyboard.Key.esc:
        print("Caught escape key")
        manager.emit('quit')
    if key == keyboard.Key.up:
        print("Caught up key")
        manager.emit('move', (0, -1))
    if key == keyboard.Key.down:
        print("Caught down key")
        manager.emit('move', (0, 1))
    if key == keyboard.Key.left:
        print("Caught left key")
        manager.emit('move', (-1, 0))
    if key == keyboard.Key.right:
        print("Caught right key")
        manager.emit('move', (1, 0))
    # special catch for home key
    try:
        if key.vk == 269025048:
            print("Caught home key")
            manager.emit('quit')
    except Exception:
        pass


def on_release(key):
    pass


def main():
    # set raspberry OS volume to 100% for normalization
    mixer = alsaaudio.Mixer('Master')
    mixer.setvolume(100, alsaaudio.MIXER_CHANNEL_ALL)

    # main window
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.config(cursor='none')

    # setup button grid
    with open('buttons.yml', 'r') as fid:
        config = yaml.safe_load(fid)

    ButtonGrid(window, window.winfo_screenwidth(), window.winfo_screenheight(), config)

    # start keyboard listener thread
    listener = keyboard.Listener(on_press=on_press,
                                 on_release=on_release)
    listener.start()

    # start new media
    media_observer = threading.Thread(target=check_new_drives, daemon=True)
    media_observer.start()

    window.mainloop()


if __name__ == '__main__':
    main()

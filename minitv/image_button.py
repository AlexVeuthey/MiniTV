import abc
import tkinter as tk

from PIL import ImageTk
from pygame import mixer

from minitv.event_manager import manager
from minitv.utils import (open_inactive_image, open_nothover_image,
                          open_resize_image)

mixer.init()

sound = mixer.Sound('minitv/assets/sounds/clic.wav')
sound.set_volume(0.15)

confirm = mixer.Sound('minitv/assets/sounds/confirm.wav')
confirm.set_volume(0.15)

quit_sound = mixer.Sound('minitv/assets/sounds/quit.wav')
quit_sound.set_volume(0.15)


class ImageButton(abc.ABC):

    def __init__(self, canvas, filename, size, position, offset):

        self.position = position
        self.size = size
        self.offset = offset

        self.pixelPosition = (offset[0] + size[0]*position[0], 50+size[1]*position[1])

        self.imgNormal = ImageTk.PhotoImage(open_nothover_image(filename, size))
        self.imgHover = ImageTk.PhotoImage(open_resize_image(filename, size))
        self.imgInactive = ImageTk.PhotoImage(open_inactive_image(filename, size))

        self.image = canvas.create_image(
            self.pixelPosition[0], self.pixelPosition[1], image=self.imgNormal, anchor=tk.NW)

        self.canvas = canvas
        self.active = False

        manager.add_handler("grid_position", self.on_position_changed)
        manager.add_handler("proceed", self.on_proceed)

    def move(self, scroll):
        self.pixelPosition = (self.offset[0] + self.size[0]*self.position[0], 50 +
                              self.size[1]*self.position[1] - scroll*self.size[1])
        self.canvas.moveto(self.image, self.pixelPosition[0], self.pixelPosition[1])

    def destroy(self):
        manager.remove_handler("grid_position", self.on_position_changed)
        manager.remove_handler("proceed", self.on_proceed)
        self.canvas.delete(self.image)

    def on_proceed(self):
        if (self.active):
            confirm.play()
            self.on_click()

    def on_position_changed(self, position):
        (column, row) = position

        if (column == self.position[0]) and (row == self.position[1]):
            if not self.active:
                self.active = True
                self.canvas.itemconfig(self.image, image=self.imgHover)
                self.on_highlighted()

        else:
            self.active = False
            self.canvas.itemconfig(self.image, image=self.imgInactive)

    def on_highlighted(self):
        sound.play()
        pass

    def quit(self):
        quit_sound.play()

    @abc.abstractmethod
    def on_click(self):
        pass

import abc
from pickle import NONE
import tkinter as tk

from PIL import ImageTk

from minitv.event_manager import manager
from minitv.utils import open_nothover_image, open_resize_image, open_inactive_image


class ImageButton(abc.ABC):

    def __init__(self, canvas, filename, size, position, offset):

        self.position = position

        self.pixelPosition = (offset[0] + size[0]*position[0], 50+size[1]*position[1])

        self.imgNormal = ImageTk.PhotoImage(open_nothover_image(filename, size))
        self.imgHover = ImageTk.PhotoImage(open_resize_image(filename, size))
        self.imgInactive = ImageTk.PhotoImage(open_inactive_image(filename, size))

        self.image = canvas.create_image(
            self.pixelPosition[0], self.pixelPosition[1], image=self.imgNormal, anchor=tk.NW)

        self.canvas = canvas
        self.canvas.tag_bind(self.image, '<Enter>', self.on_enter)
        self.canvas.tag_bind(self.image, '<Button-1>', self.on_mouse_click)

        self.active = False
        self.driver = None

        manager.add_handler("grid_position", self.on_position_changed)
        manager.add_handler("proceed", self.on_proceed)
    
    def move(self, offsetY):
        self.pixelPosition = (self.offset[0] + self.size[0]*self.position[0], 50+self.size[1]*self.position[1]-offsetY)


    def on_mouse_click(self, event):
        self.on_click()
        
    def on_proceed(self):
        if (self.active):
            self.on_click()

    def on_position_changed(self, position):
        (column, row) = position

        if (column == self.position[0]) and (row == self.position[1]):
            self.active = True
            self.canvas.itemconfig(self.image, image=self.imgHover)
            self.on_highlighted()

        else:
            self.active = False
            self.canvas.itemconfig(self.image, image=self.imgInactive)

    def on_enter(self, event):
        manager.emit('on_mouse_enter_grid_item', self.position)

    def on_highlighted(self):
        pass


    @abc.abstractmethod
    def on_click(self):
        pass

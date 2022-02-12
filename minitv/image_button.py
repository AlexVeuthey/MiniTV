import abc
import tkinter as tk

from PIL import ImageTk

from minitv.event_manager import manager
from minitv.utils import open_nothover_image, open_resize_image


class ImageButton(abc.ABC):

    def __init__(self, canvas, filename, size, position):
        self.imgNormal = ImageTk.PhotoImage(open_nothover_image(filename, size))
        self.imgHover = ImageTk.PhotoImage(open_resize_image(filename, size))

        self.image = canvas.create_image(position[0], position[1], image=self.imgNormal, anchor=tk.NW)

        self.canvas = canvas
        self.canvas.tag_bind(self.image, '<Enter>', self.on_enter)
        self.canvas.tag_bind(self.image, '<Leave>', self.on_leave)
        self.canvas.tag_bind(self.image, '<Button-1>', self.on_click)

        self.driver = None

    def on_enter(self, event):
        self.canvas.itemconfig(self.image, image=self.imgHover)

    def on_leave(self, event):
        self.canvas.itemconfig(self.image, image=self.imgNormal)

    @abc.abstractmethod
    def on_click(self, event):
        pass

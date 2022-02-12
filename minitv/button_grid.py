import tkinter as tk

from PIL import Image, ImageTk

from minitv.image_button import ImageButton
from minitv.spinner import Spinner


class ButtonGrid(tk.Canvas):

    def __init__(self, parent, width, height, rows=2, columns=4):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.place(x=0, y=0)
        self.img = ImageTk.PhotoImage(Image.open('minitv/assets/images/background.jpg'))
        self.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.init_buttons(width, height, rows, columns)
        self.spinner = Spinner(self, [width // 2, height // 2])

    def init_buttons(self, width, height, rows, columns):
        # setup button sizes
        button_size = [width // 5, width // 5]
        self.offset_x = (width - (button_size[0] * 4)) / 2

        self.setup_button('minitv/assets/buttons/arte-logo.png',
                          button_size, 0, 0)
        self.setup_button('minitv/assets/buttons/youtube-logo.png',
                          button_size, 0, 1)
        self.setup_button('minitv/assets/buttons/mycloud-logo.png',
                          button_size, 0, 2)
        self.setup_button('minitv/assets/buttons/files-manager-logo.png',
                          button_size, 0, 3)

    def setup_button(self, filename, size, row, column):
        ImageButton(self, filename, size, (self.offset_x + size[0]*column, 50+size[1]*row))

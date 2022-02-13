import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from minitv.buttons import chrome_button, video_button
from minitv.spinner import Spinner
from minitv.file_manager import find_video_files


class ButtonGrid(tk.Canvas):

    def __init__(self, parent, width, height, buttons_config, rows=2, columns=4):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.logo_folder = Path(__file__).parent / 'assets' / 'buttons'
        self.place(x=0, y=0)
        self.img = ImageTk.PhotoImage(Image.open('minitv/assets/images/background.jpg'))
        self.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.init_buttons(width, height, rows, columns, buttons_config)
        self.spinner = Spinner(self, [width // 2, height // 2])

    def init_buttons(self, width, height, rows, columns, buttons_config):
        # setup button sizes
        button_size = [width // 5, width // 5]
        self.offset_x = (width - (button_size[0] * 4)) / 2

        for i, button_name in enumerate(buttons_config):
            params = buttons_config[button_name]
            self.setup_button(params, button_size, i // columns, i % columns)

        for j, video_path in enumerate(find_video_files()):
            self.setup_button({
                'button_type': 'video',
                'videopath': video_path
            }, button_size, (i + j + 1) // columns, (i + j + 1) % columns)

    def setup_button(self, params, size, row, column):
        position = (self.offset_x + size[0]*column, 50+size[1]*row)
        if params['button_type'] == 'website':
            chrome_button.ChromeButton(params['url'], self, self.logo_folder / params['logo_path'], size, position)
        elif params['button_type'] == 'video':
            video_button.VideoButton(params['videopath'], self, size, position)
        else:
            print(f"Type {params['button_type']} not supported at the moment")

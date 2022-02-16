import math
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from minitv.buttons import chrome_button, video_button
from minitv.event_manager import manager
from minitv.file_manager import find_video_files
from minitv.infotext import Infotext
from minitv.spinner import Spinner


class ButtonGrid(tk.Canvas):

    def __init__(self, parent, width, height, buttons_config, columns=4):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.logo_folder = Path(__file__).parent / 'assets' / 'buttons'
        self.place(x=0, y=0)
        self.buttons = []
        self.max_item_idx = -1
        self.current_col = 0
        self.current_row = 0
        self.scroll_row = 0
        self.width = width
        self.height = height
        self.columns = columns
        self.buttons_config = buttons_config
        self.bg_img = ImageTk.PhotoImage(Image.open('minitv/assets/images/background.jpg'))
        self.create_image(0, 0, image=self.bg_img, anchor=tk.NW)
        self.init_buttons(width, height, columns, buttons_config)
        self.spinner = Spinner(self, [width // 2, height // 2])

        self.infotext = Infotext(self, (0, height - 100), [width, height])

        manager.add_handler('move', self.on_move)
        manager.add_handler('new_media_found', self.reset_buttons)

    def move_buttons(self, offset):
        print(f"move buttons {offset}")
        for button in self.buttons:
            button.move(offset)

    def change_grid_position(self, position):
        self.current_col = position[0]
        self.current_row = position[1]

        window_size = 2

        if self.current_row > self.scroll_row + window_size - 1:
            self.scroll_row += 1
            self.move_buttons(self.scroll_row)

        if self.current_row < self.scroll_row:
            self.scroll_row -= 1
            self.move_buttons(self.scroll_row)

        manager.emit('grid_position', (self.current_col, self.current_row))

    def on_move(self, delta):
        log_str = f"(current: {(self.current_col, self.current_row)}, delta: {delta})"
        delta_col, delta_row = delta
        new_col = self.current_col + delta_col
        new_row = self.current_row + delta_row
        max_row = math.floor(self.max_item_idx / self.columns)
        # move left when at left-most position
        if new_col < 0:
            if self.current_row > 0:
                # go to previous row, last column if there's a previous row
                self.current_col = self.columns - 1
                self.current_row -= 1
            else:
                print(f"No previous row to loop-back to {log_str}")
        # move right when at right-most position
        elif new_col >= self.columns:
            if max_row > self.current_row:
                # go to next row, first column if there's a next row
                self.current_col = 0
                self.current_row += 1
            else:
                print(f"No next row to loop-forward to {log_str}")
        elif new_row == max_row and new_col > (self.max_item_idx % self.columns):
            print(f"No item to go to in incomplete row {log_str}")
        elif 0 <= new_row <= max_row:
            self.current_col = new_col
            self.current_row = new_row
        else:
            print(f"Move is invalid {log_str}")
        self.change_grid_position((self.current_col, self.current_row))

    def reset_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        self.init_buttons(self.width, self.height, self.columns, self.buttons_config)

    def init_buttons(self, width, height, columns, buttons_config):
        # setup button sizes
        button_size = [width // 5, width // 5]
        self.offset_x = (width - (button_size[0] * 4)) / 2
        self.offset_y = 50

        i = 0
        for i, button_name in enumerate(buttons_config):
            params = buttons_config[button_name]
            self.setup_button(params, button_size, i // columns, i % columns)

        j = 0
        for j, video_path in enumerate(find_video_files()):
            self.setup_button({
                'button_type': 'video',
                'videopath': video_path
            }, button_size, (i + j + 1) // columns, (i + j + 1) % columns)

        self.max_item_idx = i + j

        self.change_grid_position((self.current_col, self.current_row))

    def setup_button(self, params, size, row, column):
        if params['button_type'] == 'website':
            button = chrome_button.ChromeButton(params['url'], self, self.logo_folder /
                                                params['logo_path'], size, (column, row),
                                                (self.offset_x, self.offset_y))
            self.buttons.append(button)
        elif params['button_type'] == 'video':
            button = video_button.VideoButton(params['videopath'], self, size, (column, row),
                                              (self.offset_x, self.offset_y))
            self.buttons.append(button)
        else:
            print(f"Type {params['button_type']} not supported at the moment")

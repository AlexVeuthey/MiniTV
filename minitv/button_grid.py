import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from minitv.buttons import chrome_button, video_button
from minitv.spinner import Spinner
from minitv.infotext import Infotext
from minitv.event_manager import manager
from minitv.file_manager import find_video_files


class ButtonGrid(tk.Canvas):

    def __init__(self, parent, width, height, buttons_config, columns=4):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.logo_folder = Path(__file__).parent / 'assets' / 'buttons'
        self.place(x=0, y=0)
        self.buttons = []
        self.n_items = 0
        self.current_col = 0
        self.current_row = 0
        self.columns = columns
        self.bg_img = ImageTk.PhotoImage(Image.open('minitv/assets/images/background.jpg'))
        self.create_image(0, 0, image=self.bg_img, anchor=tk.NW)
        self.init_buttons(width, height, columns, buttons_config)
        self.spinner = Spinner(self, [width // 2, height // 2])

        self.infotext = Infotext(self, (0, height - 80), [width, height])

        manager.emit('grid_position', (self.current_col, self.current_row))
        manager.add_handler('move', self.on_move)
        manager.add_handler('on_mouse_enter_grid_item', self.on_mouse_move)

    def move_buttons(self, offset):
        for button in self.buttons:
            button.move(offset)

    def on_mouse_move(self, position):
        self.current_col = position[0]
        self.current_row = position[1]
        manager.emit('grid_position', (self.current_col, self.current_row))

    def on_move(self, delta):
        log_str = f"(current: {(self.current_col, self.current_row)}, delta: {delta})"
        delta_col, delta_row = delta
        new_col = self.current_col + delta_col
        new_row = self.current_row + delta_row
        max_row = (self.n_items // self.columns) - 1
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
        elif 0 <= new_row <= max_row:
            self.current_col = new_col
            self.current_row = new_row
        else:
            print(f"Move is invalid {log_str}")
        manager.emit('grid_position', (self.current_col, self.current_row))

    def init_buttons(self, width, height, columns, buttons_config):
        # setup button sizes
        button_size = [width // 5, width // 5]
        self.offset_x = (width - (button_size[0] * 4)) / 2
        self.offset_y = 50

        for i, button_name in enumerate(buttons_config):
            params = buttons_config[button_name]
            self.setup_button(params, button_size, i // columns, i % columns)

        for j, video_path in enumerate(find_video_files()):
            self.setup_button({
                'button_type': 'video',
                'videopath': video_path
            }, button_size, (i + j + 1) // columns, (i + j + 1) % columns)

        self.n_items = i + j + 1

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


from minitv.event_manager import manager
from minitv.image_button import ImageButton
from minitv.utils import open_nothover_image, open_resize_image


class FileManagerButton(ImageButton):

    def __init__(self, canvas, filename, size, position):
        super().__init__(canvas, filename, size, position)

    def on_click(self, event):
        pass

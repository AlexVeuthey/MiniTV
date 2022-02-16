import subprocess
import threading
from os import unlink
from pathlib import Path
from time import sleep

from minitv.event_manager import manager
from minitv.image_button import ImageButton
from minitv.utils import open_inactive_image, open_resize_image
from PIL import ImageTk


class VideoButton(ImageButton):

    def __init__(self, videopath, canvas, size, position, offset):
        logo_path = Path(__file__).parents[1] / 'assets' / 'buttons' / 'video-logo.png'
        super().__init__(canvas, logo_path, size, position, offset)
        self.videopath = videopath
        self.process = None
        self.thumb = None
        self.thumbImg = None
        self.thumbImgInactive = None

        manager.add_handler('thumb_loaded', self.on_thumb_loaded)
        manager.emit('load_thumbnail', videopath, size)

    def destroy(self):
        super().destroy()
        manager.remove_handler('thumb_loaded', self.on_thumb_loaded)
        self.canvas.delete(self.thumb)

    def on_thumb_loaded(self, videopath):
        if videopath == self.videopath:
            self.thumbImgInactive = ImageTk.PhotoImage(open_inactive_image(
                f"{self.videopath}.jpg", (self.size[0], self.size[1]-88)))
            self.thumbImg = ImageTk.PhotoImage(open_resize_image(
                f"{self.videopath}.jpg", (self.size[0], self.size[1]-88)))
            self.thumb = self.canvas.create_image(
                self.pixelPosition[0], self.pixelPosition[1]+44, image=self.thumbImgInactive, anchor="nw")
            unlink(f"{self.videopath}.jpg")

    def on_position_changed(self, position):
        super().on_position_changed(position)

        if self.active:
            if self.thumb:
                self.canvas.itemconfig(self.thumb, image=self.thumbImg)
        else:
            if self.thumb:
                self.canvas.itemconfig(self.thumb, image=self.thumbImgInactive)

    def move(self, scroll):
        super().move(scroll)
        if self.thumb:
            self.canvas.moveto(self.thumb, self.pixelPosition[0], self.pixelPosition[1]+44)

    def on_highlighted(self):
        super().on_highlighted()
        manager.emit('show_text', self.videopath.name)

    def quit(self):
        """Callback to quit VLC"""
        super().quit()
        print('Quitting VLC')
        if self.process is not None:
            self.process.kill()
            self.process.join()
        manager.remove_handler('quit', self.quit)

    def on_click(self):

        manager.emit('show_spinner')

        def start_video():
            self.process = subprocess.Popen(['vlc', f'{self.videopath}', '--fullscreen'])
            manager.add_handler('quit', self.quit)
            sleep(1)
            manager.emit('hide_spinner')

            while self.process is not None and self.process.poll() is None:
                sleep(2)
            manager.emit('quit')

        x = threading.Thread(target=start_video, daemon=True)
        x.start()

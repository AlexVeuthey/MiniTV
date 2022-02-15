import subprocess
import threading
from pathlib import Path
from time import sleep

from minitv.event_manager import manager
from minitv.image_button import ImageButton


class VideoButton(ImageButton):

    def __init__(self, videopath, canvas, size, position, offset):
        logo_path = Path(__file__).parents[1] / 'assets' / 'buttons' / 'video-logo.png'
        super().__init__(canvas, logo_path, size, position, offset)
        self.videopath = videopath
        self.process = None

    def on_highlighted(self):
        super().on_highlighted()
        manager.emit('show_text', self.videopath.name)
        
    def quit(self):
        super().quit()
        """Callback to quit VLC"""
        print('Quitting driver')
        if self.process is not None:
            self.process.kill()
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

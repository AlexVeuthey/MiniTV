import subprocess
from pathlib import Path

from minitv.event_manager import manager
from minitv.image_button import ImageButton


class VideoButton(ImageButton):

    def __init__(self, videopath, canvas, size, position):
        logo_path = Path(__file__).parents[1] / 'assets' / 'buttons' / 'video-logo.png'
        super().__init__(canvas, logo_path, size, position)
        self.videopath = videopath
        self.process = None

    def on_click(self, event):

        def quit():
            """Callback to quit VLC"""
            print('Quitting driver')
            if self.process is not None:
                self.process.kill()
                manager.remove_handler('quit', quit)

        self.process = subprocess.Popen(['vlc', f'{self.videopath}', '--fullscreen'])
        manager.add_handler('quit', quit)

from pathlib import Path
from time import sleep
import os
import subprocess
import shlex
from minitv.event_manager import manager

SUPPORTED_FILES = ['3gp', 'a52', 'dts', 'aac', 'flac', 'dv', 'vid', 'asf', 'wmv', 'asf', 'wmv', 'au', 'avi', 'flv',
                   'mkv', 'mka', 'mov', 'mp4', 'mpg', 'mp3', 'mp2', 'nsc', 'nsv', 'nut', 'ogm', 'ogg', 'ra', 'ram',
                   'rm', 'rv', 'rmbv', 'ts', 'mpg', 'tta', 'tac', 'ty', 'wav', 'dts', 'xa']

polling_is_active = True


def set_polling_active():
    global polling_is_active
    polling_is_active = True


def set_polling_inactive():
    global polling_is_active
    polling_is_active = False
    

thumbQueue = []
    
def load_thumbnail(videopath, size):
    thumbQueue.append((videopath, size))
    pass


def check_new_thumbnails():
    while True:
        sleep(0.1)
        if polling_is_active:
            if (len(thumbQueue) > 0):
                (videopath, size) = thumbQueue.pop(0)
                
                if (os.path.isfile(f"{videopath}.jpg")):
                    os.unlink(f"{videopath}.jpg")
    
  
                process = subprocess.call(shlex.split(f"ffmpeg -ss 00:03:00 -i {videopath} -s {size[0]}x{size[1]} -frames:v 1 {videopath}.jpg"))
                manager.emit('thumb_loaded', videopath)
            

manager.add_handler('proceed', set_polling_inactive)
manager.add_handler('quit', set_polling_active)


manager.add_handler('load_thumbnail', load_thumbnail)



def find_video_files():
    drives_path = Path('/media/pi')
    matches = []
    for ext in SUPPORTED_FILES:
        matches.extend(drives_path.rglob(f'*.{ext}'))
    return sorted(matches)


def check_new_drives():
    drives_path = Path('/media/pi')
    current_content = []
    for child in drives_path.iterdir():
        current_content.extend(sorted(child.iterdir())[0].name)
    while True:
        sleep(3)
        if polling_is_active:
            new_content = []
            for child in drives_path.iterdir():
                new_content.extend(sorted(child.iterdir())[0].name)
            if new_content != current_content:
                current_content = new_content
                manager.emit('new_media_found')

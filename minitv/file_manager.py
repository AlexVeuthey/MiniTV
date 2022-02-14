from pathlib import Path

SUPPORTED_FILES = ['3gp', 'a52', 'dts', 'aac', 'flac', 'dv', 'vid', 'asf', 'wmv', 'asf', 'wmv', 'au', 'avi', 'flv',
                   'mkv', 'mka', 'mov', 'mp4', 'mpg', 'mp3', 'mp2', 'nsc', 'nsv', 'nut', 'ogm', 'ogg', 'ra', 'ram',
                   'rm', 'rv', 'rmbv', 'ts', 'mpg', 'tta', 'tac', 'ty', 'wav', 'dts', 'xa']


def find_video_files():
    drives_path = Path('/media/pi')
    matches = []
    for ext in SUPPORTED_FILES:
        matches.extend(drives_path.rglob(f'*.{ext}'))
    return sorted(matches)

import os
from os.path import splitext, exists
import shutil
import time

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


s_dir = "c:/Users/nikhi/Downloads"
image_dir = "c:/Dimages"
switch_dir = "c:/switch"
wii_dir = "c:/wii"

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]



def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move(dest, file, name):
    if os.path.exists(dest + "/" + name):
        unique_name = makeUnique(name)
        os.rename(file, unique_name)
    shutil.move(file,name)



class Mover(FileSystemEventHandler):
    with os.scandir(s_dir) as files:
        for file in files:
            name = file.name
            dest = s_dir
            if name.endswith(image_extensions):
                dest = image_dir
            elif name.endswith(".nsp") or (".xci"):
                dest = switch_dir



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = s_dir
    event_handler = Mover()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
# TODO better way to do this?
import sys
sys.path.append("/home/bridger/GitHub/Instagram-API-python")
from InstagramAPI import InstagramAPI

import os
import json
import shutil
import traceback
from getpass import getpass
from pathlib import Path
from PIL import Image

DEBUG = True
dbprint = print if DEBUG else lambda *args, **kwargs: None
def hprint(*args, **kwargs):
    print("="*5, end=" ")
    print(*args, **kwargs, end=" ")
    print("="*5)

# These need to exist before the script is run
QUEUE = "queue.json"
POSTED = "posted.json"
IMG_DIR = "img"
POSTED_DIR = "posted"
ALL_COMMENTS = "\n"

def getlogin():
    user = input("Username: ")
    pswd = getpass()
    return (user, pswd)

def generate_queue():
    queue_path = Path(QUEUE)
    if queue_path.is_file():
        ovw = input("File exists. Overwrite? (y/n): ").lower().strip() == "y"
    if ovw:
        hprint("Generating queue")
        queue = []
        for img in sorted(os.listdir(IMG_DIR)):
            print(" ", img)
            queue.append({img:ALL_COMMENTS})
        with open(QUEUE, "w") as fout:
            json.dump(queue, fout)

def start():
    if "generate" in sys.argv:
        generate_queue()
        return None
    hprint("Instagram Uploader")
    api = InstagramAPI(*getlogin())
    print("  Logging in")
    api.login()
    if not api.isLoggedIn:
        print("Login failed")
        return None
    else:
        return api

def fix_format(fpath):
    hprint("Fixing format")
    img = Image.open(fpath)
    img.save(fpath.parent.joinpath(fpath.stem + ".jpg"))

def get_next_image():
    hprint("Fetching image")
    try:
        with open(QUEUE) as fin:
            queue = json.load(fin)
            assert len(queue) >= 1
            nxt = list(queue[-1].items())
            assert len(nxt) == 1
            name, caption = nxt[0]
            dir_path = Path(IMG_DIR)
            image_path = dir_path.joinpath(name).resolve()
            fix_format(image_path)
            return str(image_path), caption
    except:
        print("Error")
        dbprint(traceback.format_exc())

def cleanup():
    hprint("Cleaning up")
    try:
        # Clean up the queue, and add to a "finished" list
        queue = None
        image_path = None
        dir_path = None
        name = None
        caption = None
        with open(QUEUE) as fin:
            queue = json.load(fin)
            assert len(queue) >= 1
            nxt = list(queue.pop().items())
            assert len(nxt) == 1
            name, caption = nxt[0]
            dir_path = Path(IMG_DIR)
            image_path = dir_path.joinpath(name).resolve()
        with open(QUEUE, "w") as fout:
            json.dump(queue, fout)
        finished = None
        with open(POSTED) as fin:
            finished = json.load(fin)
            finished.append({name:caption})
        with open(POSTED, "w") as fout:
            json.dump(finished, fout)

        # Move the file into a "posted" directory
        posted_path = dir_path.parent.joinpath(POSTED_DIR).joinpath(name)
        shutil.move(str(image_path), str(posted_path))
    except:
        print("Error")
        dbprint(traceback.format_exc())

def main():
    api = start()
    if api == None:
        return
    hprint("Uploading photo")
    api.uploadPhoto(*get_next_image())
    response = api.LastResponse # last response JSON
    if response.status_code != 200:
        print("Error")
        dbprint(response.status_code, response.json())
        return
    cleanup()

if __name__ == "__main__":
    main()

import requests
import shutil

from settings import MEDIA_DIR


def download(url, fname) -> str:
    r = requests.get(url, stream=True)
    path = f"{MEDIA_DIR}/{fname}"
    if r.status_code == 200:
        with open(f"{MEDIA_DIR}/{fname}", "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    return path

import time
import os


def purge(days, path):
    now = time.time()

    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.stat(file_path).st_mtime < now - float(days) * 86400:
            if os.path.isfile(file_path):
                os.remove(file_path)

import os
import shutil


def clear_dir(path: str) -> None:
    shutil.rmtree(path)
    os.mkdir(path)

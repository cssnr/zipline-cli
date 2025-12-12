import os
import secrets
import string
from pathlib import Path

from dotenv import find_dotenv


def get_env(file_name: str = ".zipline") -> Path:
    # NOTE: Remove `find_dotenv` and use central config file...
    env_file = Path(os.path.expanduser("~")) / file_name
    if os.path.isfile(env_file):
        return env_file
    dotenv_file = find_dotenv(filename=file_name)
    if dotenv_file:
        dotenv_path = Path(dotenv_file)
        return dotenv_path
    return env_file


def gen_rand(length: int = 4) -> str:
    r = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return "".join(r)


def bytes_to_human(num: float, suffix: str = "B") -> str:
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"

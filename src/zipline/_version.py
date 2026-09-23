import os
import re

SUFFIXES = {"alpha": "a", "beta": "b", "rc": "rc"}


def get_version() -> str:
    version = os.environ.get("GITHUB_REF_NAME", "")
    match = re.match(r"^v?(\d+\.\d+\.\d+)-(alpha|beta|rc)\.(\d+)$", version)
    if match:
        base, suffix, number = match.groups()
        version = f"{base}{SUFFIXES[suffix]}{number}"
    elif version.startswith("v"):
        version = version[1:]
    if re.match(r"^\d+\.\d+\.\d+(?:(?:[abc]|rc)\d*)?$", version):
        return version
    return "0.0.1"


__version__ = get_version()

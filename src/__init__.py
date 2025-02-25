import os
import re


def get_version():
    version = os.environ.get("GITHUB_REF_NAME", "0.0.1")
    pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-(\w+|\d+)\.(\w+|\d+))?$"
    match = re.match(pattern, version)
    return version if match else "0.0.1"


__version__ = get_version()

import os
import re


def get_version() -> str:
    version = os.environ.get("GITHUB_REF_NAME", "")
    suffixes = {"alpha": "a", "beta": "b", "rc": "rc"}
    names = "|".join(suffixes)
    match = re.match(rf"^v?(\d+\.\d+\.\d+)-({names})\.(\d+)$", version)
    if match:
        base, suffix, number = match.groups()
        version = f"{base}{suffixes[suffix]}{number}"
    elif version.startswith("v"):
        version = version[1:]
    letters = "|".join([*suffixes.values(), "c"])
    if re.match(rf"^\d+\.\d+\.\d+(?:({letters})\d*)?$", version):
        return version
    return "0.0.1"


__version__ = get_version()

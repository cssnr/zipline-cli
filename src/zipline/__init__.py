import os
import re
from typing import Optional


Zipline: Optional[type] = None


def get_version() -> str:
    version = os.environ.get("GITHUB_REF_NAME", "0.0.1")
    pattern = r"^\d+\.\d+\.\d+(?:[abc]\d*)?$"
    match = re.match(pattern, version)
    return version if match else "0.0.1"


try:
    from .zipline import Zipline
except ImportError:
    Zipline = None


__version__ = get_version()

__all__ = ["Zipline", "__version__"]

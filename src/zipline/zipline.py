import mimetypes
import warnings
from pathlib import Path
from typing import IO, Dict, Optional

import requests


class ZipURL(object):
    """
    Zipline URL Object
    :param file_url: Zipline File Display URL
    """

    __slots__ = ["url", "raw"]

    def __init__(self, file_url: str):
        self.url: str = file_url
        self.raw: str = self._get_raw(file_url)

    def __repr__(self):
        return f"<url={self.url} raw={self.raw}>"

    def __str__(self):
        return self.url

    @staticmethod
    def _get_raw(url: str) -> str:
        try:
            s = url.split("/", 4)
            return f"{s[0]}//{s[2]}/r/{s[4]}"
        except Exception:  # noqa
            return ""


class Zipline(object):
    """
    Zipline Python API
    :param base_url: Zipline URL
    :param kwargs: Zipline Headers
    """

    # noinspection SpellCheckingInspection
    allowed_headers = [
        # zipline v3
        "format",
        "image_compression_percent",
        "expires_at",
        "password",
        "zws",
        "embed",
        "max_views",
        "uploadtext",
        "authorization",
        "no_json",
        "x_zipline_filename",
        "original_name",
        "override_domain",
        # zipline v4
        "x-zipline-deletes-at",
        "x-zipline-format",
        "x-zipline-image-compression-percent",
        "x-zipline-password",
        "x-zipline-max-views",
        "x-zipline-no-json",
        "x-zipline-original-name",
        "x-zipline-folder",
        "x-zipline-filename",
        "x-zipline-domain",
        "x-zipline-file-extension",
    ]

    def __init__(self, url: str, **kwargs):
        self.base_url: str = url.rstrip("/")
        self._headers: Dict[str, str] = {}
        for header, value in kwargs.items():
            if header.lower() not in self.allowed_headers:
                continue
            if value is None:
                continue
            key = header.replace("_", "-").title()
            self._headers[key] = str(value)

    def send_file(self, file_name: str, file_object: IO, overrides: Optional[dict] = None) -> ZipURL:
        """
        Upload File to Zipline
        :param file_name: Name of File for files tuple
        :param file_object: File to Upload
        :param overrides: Header Overrides
        :return: File URL
        """
        url = self.base_url + "/api/upload"
        path = Path(file_name)
        mime_type = get_type(path)
        # print(f"mime_type: {mime_type}")
        files = {"file": (file_name, file_object, mime_type)}
        headers = self._headers | overrides if overrides else self._headers
        r = requests.post(url, headers=headers, files=files)  # nosec
        r.raise_for_status()
        data = r.json()["files"][0]
        if isinstance(data, dict):
            return ZipURL(data["url"])
        elif isinstance(data, list):
            return ZipURL(data[0])
        else:
            return ZipURL(data)


def get_type(file_path: Path) -> str:  # NOSONAR
    """
    Get MIME type from guess_type or by reading magic headers
    https://en.wikipedia.org/wiki/List_of_file_signatures

    Deprecated since version 3.13: Passing a file path instead of URL is soft deprecated. Use guess_file_type() for this.
    https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type
    """
    mime_type, _ = mimetypes.guess_type(file_path, strict=False)
    if mime_type:
        return mime_type

    if not file_path.is_file():
        return "text/plain"

    with open(file_path, "rb") as file:
        chunk = file.read(512)

    # print(f"chunk: {type(chunk)} - {chunk[:20]}")
    # print(f"test chunk: {chunk[8:11]}")

    if isinstance(chunk, str):  # pragma: no cover
        warnings.warn("This condition should not be True...", stacklevel=2)
        return "text/plain"

    # Images
    if chunk[0:3] == b"\xff\xd8\xff" or chunk[6:10] in (b"JFIF", b"Exif"):
        return "image/jpeg"
    elif chunk.startswith(b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"):
        return "image/png"
    elif chunk.startswith(b"RIFF") and chunk[8:12] == b"WEBP":
        return "image/webp"
    elif chunk.startswith((b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")):
        return "image/gif"
    elif chunk.startswith(b"\x66\x74\x79\x70\x68\x65\x69\x63\x66\x74\79\70\6d") or chunk[4:12] == b"ftypheic":
        return "image/heic"
    elif chunk.startswith(b"\x00\x00\x01\x00"):
        return "image/ico"
    elif chunk.startswith(b"II*") or chunk.startswith(b"II+") or chunk.startswith(b"MM"):
        return "image/tiff"
    elif chunk.startswith(b"BM"):
        return "image/bmp"
    elif chunk[4:12] == b"ftypavif":
        return "image/avif"

    # Video
    elif chunk[4:12] == b"ftypisom" or chunk[4:12] == b"ftypMSNV" or chunk[4:12] == b"ftypmp42":
        return "video/mp4"
    elif chunk[3:11] in (b"\x66\x74\x79\x70\x4d\x53\x4e\x56", b"\x66\x74\x79\x70\x69\x73\x6f\x6d"):
        return "video/mp4"
    elif chunk.startswith(b"\x1a\x45\xdf\xa3"):
        # https://www.loc.gov/preservation/digital/formats//fdd/fdd000342.shtml
        return "video/x-matroska"
    elif chunk.startswith(b"RIFF") and chunk[8:11] == b"AVI":
        return "video/x-msvideo"
    elif chunk.startswith(b"\x30\x26\xb2\x75\x8e\x66\xcf\x11\xa6\xd9\x00\xaa\x00\x62\xce\x6c"):
        # https://www.loc.gov/preservation/digital/formats/fdd/fdd000091.shtml
        return "video/x-ms-asf"
    elif chunk.startswith(b"\x6d\x6f\x6f\x76") or chunk[4:10] == b"ftypqt":
        # https://www.file-recovery.com/mov-signature-format.htm
        return "video/quicktime"

    # Audio
    elif chunk.startswith((b"\xff\xfb", b"\xff\xfb", b"\xff\xfb", b"\x49\x44\x33")):
        return "audio/mp3"
    elif chunk.startswith(b"RIFF") and chunk[8:12] == b"WAVE":
        return "audio/wav"
    elif chunk.startswith(b"OggS"):
        return "application/ogg"

    # Fallback
    try:
        chunk.decode("utf-8")
        return "text/plain"
    except UnicodeDecodeError:
        return "application/octet-stream"

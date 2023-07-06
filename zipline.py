import argparse
import io
import os
import random
import re
import requests
import string
import sys
from decouple import config
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO


class ZipURL(object):
    """
    Zipline URL Object
    :param file_url: str: Zipline File Display URL
    """

    __slots__ = ['url', 'raw']

    def __init__(self, file_url: str):
        self.url: str = file_url
        self.raw: str = self._get_raw(file_url)

    def __repr__(self):
        return f'<url={self.url} raw={self.raw}>'

    def __str__(self):
        return self.url

    @staticmethod
    def _get_raw(url: str) -> str:
        try:
            s = url.split('/', 4)
            return f"{s[0]}//{s[2]}/r/{s[4]}"
        except Exception:
            return ''


class Zipline(object):
    """
    Zipline Python API
    :param base_url: str: Zipline URL
    :param kwargs: Zipline Headers
    """
    allowed_headers = ['format', 'image_compression_percent', 'expires_at',
                       'password', 'zws', 'embed', 'max_views', 'uploadtext',
                       'authorization', 'no_json', 'x_zipline_filename',
                       'original_name', 'override_domain']

    def __init__(self, base_url: str, **kwargs):
        self.base_url: str = base_url.rstrip('/')
        self._headers: Dict[str, str] = {}
        for header, value in kwargs.items():
            if header.lower() not in self.allowed_headers:
                continue
            if value is None:
                continue
            key = header.replace('_', '-').title()
            self._headers[key] = str(value)

    def send_file(self, file_name: str, file_object: TextIO,
                  overrides: Optional[dict] = None) -> ZipURL:
        """
        Send File to Zipline
        :param file_name: str: Name of File for files tuple
        :param file_object: TextIO: File to Upload
        :param overrides: dict: Header Overrides
        :return: str: File URL
        """
        url = self.base_url + '/api/upload'
        files = {'file': (file_name, file_object)}
        headers = self._headers | overrides if overrides else self._headers
        r = requests.post(url, headers=headers, files=files)
        r.raise_for_status()
        return ZipURL(r.json()['files'][0])
        # return f'https://example.com/dummy/{file_name}'


def format_output(filename: str, url: ZipURL) -> str:
    """
    Format URL Output
    :param filename: str: Original or File Name
    :param url: ZipURL: ZipURL to Format
    :return: str: Formatted Output
    """
    if url.raw:
        return f'{filename}\n{url}\n{url.raw}'
    return f'{filename}\n{url}'


def gen_rand(length: Optional[int] = 4) -> str:
    """
    Generate Random Streng at Given length
    :param length: int: Length of Random String
    :return: str: Random String
    """
    length: int = length if not length < 0 else 4
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_default(values: List[str], default: Optional[Any] = None,
                cast: Optional[type] = str, pre: Optional[str] = 'ZIPLINE_',
                suf: Optional[str] = '') -> Optional[str]:
    """
    Get Default Environment Variable from List of values
    :param values: list: List of Values to Check
    :param default: any: Default Value if None
    :param cast: type: Type to Cast Value
    :param pre: str: Environment Variable Prefix
    :param suf: str: Environment Variable Suffix
    :return: str: Environment Variable or None
    """
    for value in values:
        result = config(f'{pre}{value.upper()}{suf}', '', cast)
        if result:
            return result
    return default


def setup(env_file: Path) -> None:
    print('Setting up Environment File...')
    url = input('Zipline URL: ').strip()
    token = input('Zipline Authorization Token: ').strip()
    if not url or not token:
        raise ValueError('Missing URL or Token.')
    output = f'ZIPLINE_URL={url}\nZIPLINE_TOKEN={token}\n'
    embed = input('Enabled Embed? [Yes]/No: ').strip()
    if not embed or embed.lower() not in ['n', 'o', 'no', 'noo']:
        output += 'ZIPLINE_EMBED=true\n'
    expire = input('Default Expire? [Blank for None]: ').strip().lower()
    if expire:
        match = re.search(r'^(\d+)(?:ms|s|m|h|d|w|y)$', expire)
        if not match:
            print(f'Warning: invalid expire format: {expire}. See --help')
        else:
            output += f'ZIPLINE_EXPIRE={expire}\n'
    with open(env_file, 'w') as f:
        f.write(output)
    print(f'Setup Complete. Variables Saved to: {env_file}')
    sys.exit(0)


def main() -> None:
    zipline_file = '.zipline'
    env_file = Path(os.path.expanduser('~')) / zipline_file
    dotenv_path = env_file if os.path.isfile(env_file) else find_dotenv(filename=zipline_file)
    env = load_dotenv(dotenv_path=dotenv_path)

    parser = argparse.ArgumentParser(description='Zipline CLI.')
    parser.add_argument('files', metavar='Files', type=str, nargs='*', help='Files to Upload.')
    parser.add_argument('-u', '--url', type=str, default=get_default(['url']), help='Zipline URL.')
    parser.add_argument('-a', '-t', '--authorization', '--token', type=str,
                        default=get_default(['token', 'authorization']),
                        help='Zipline Access Token for Authorization or ZIPLINE_TOKEN.')
    parser.add_argument('-e', '-x', '--expires_at', '--expire', type=str, default=get_default(['expire', 'expire_at']),
                        help='Ex: 1d, 2w. See: https://zipline.diced.tech/docs/guides/upload-options#image-expiration')
    parser.add_argument('--embed', action='store_true', default=get_default(['embed'], False, bool),
                        help='Enable Embeds on Uploads.')
    parser.add_argument('-s', '--setup', action='store_true', default=False,
                        help='Automatic Setup of Environment Variables.')
    args = parser.parse_args()

    if args.setup:
        setup(env_file)

    if not env and not args.url and not args.authorization and not os.path.isfile(env_file):
        env_file.touch()
        print('First Run Detected, Entering Setup.')
        setup(env_file)

    if not args.url:
        parser.print_help()
        raise ValueError('Missing URL. Use --setup or specify --url')

    if not args.authorization:
        parser.print_help()
        raise ValueError('Missing Token. Use --setup or specify --token')

    if args.expires_at:
        args.expires_at = args.expires_at.strip().lower()
        match = re.search(r'^(\d+)(?:ms|s|m|h|d|w|y)$', args.expires_at)
        if not match:
            parser.print_help()
            raise ValueError(f'Invalid Expire Format: {args.expires_at}.')

    zipline = Zipline(args.url, **vars(args))

    if not args.files:
        content: str = sys.stdin.read().rstrip('\n') + '\n'
        text_f: TextIO = io.StringIO(content)
        name = f'{gen_rand(8)}.txt'
        url: ZipURL = zipline.send_file(name, text_f)
        print(format_output(name, url))
        sys.exit(0)

    exit_code = 1
    for name in args.files:
        if not os.path.isfile(name):
            print(f'Warning: File Not Found: {name}')
            continue
        with open(name) as f:
            # name, ext = os.path.splitext(os.path.basename(filename))
            # ext = f'.{ext}' if ext else ''
            # name = f'{name}-{gen_rand(8)}{ext}'
            # url: str = zipline.send_file(name, f)
            url: ZipURL = zipline.send_file(name, f)
            print(format_output(name, url))
            exit_code = 0
    sys.exit(exit_code)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as error:
        print('\nError: {}'.format(str(error)))
        sys.exit(1)

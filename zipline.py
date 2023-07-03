import argparse
import io
import os
import random
import re
import requests
import string
import sys
from decouple import config
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from typing import Optional, List, Any, TextIO


class Zipline(object):
    """
    Zipline Python API
    :param url: str: Zipline URL
    :param kwargs: Zipline Headers
    """
    allowed_headers = ['format', 'image_compression_percent', 'expires_at',
                       'password', 'zws', 'embed', 'max_views', 'uploadtext',
                       'authorization', 'no_json', 'x_zipline_filename',
                       'original_name', 'override_domain']

    def __init__(self, zipline_url: str, **kwargs):
        self.zipline_url: str = zipline_url.rstrip('/')
        self.headers: dict = {}
        for header, value in kwargs.items():
            if header.lower() not in self.allowed_headers:
                error = f'{header.lower()} not in {self.allowed_headers}'
                raise ValueError(error)
            if value is None:
                continue
            key = header.replace('_', '-').title()
            self.headers[key] = str(value)

    def send_file(self, file_name: str, file_object: TextIO,
                  overrides: Optional[dict] = None) -> str:
        """
        Send File to Zipline
        :param file_name: str: Name of File for files tuple
        :param file_object: TextIO: File to Upload
        :param overrides: dict: Header Overrides
        :return: str: File URL
        """
        url = self.zipline_url + '/api/upload'
        files = {'file': (file_name, file_object)}
        headers = self.headers | overrides if overrides else self.headers
        r = requests.post(url, headers=headers, files=files)
        r.raise_for_status()
        return r.json()['files'][0]
        # return f'https://example.com/dummy/{file_name}'


def gen_rand(length: Optional[int] = 4) -> str:
    length: int = length if not length < 0 else 4
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_default(values: List[str], default: Any = None,
                cast: Optional[type] = str, pre: str = 'ZIPLINE_',
                suf: str = '') -> Optional[str]:
    for value in values:
        result = config(f'{pre}{value.upper()}{suf}', '', cast)
        # print('value', value)
        # print('result', result)
        if result:
            return result
    return default


def main():
    env_file = Path(os.path.expanduser('~')) / '.zipline'
    # print(env_file)
    dotenv_path = env_file if os.path.exists(env_file) else find_dotenv(filename='.zipline')
    load_dotenv(dotenv_path=dotenv_path)
    parser = argparse.ArgumentParser(description='Zipline CLI.')
    parser.add_argument('files', metavar='Files', type=str, nargs='*',
                        help='Files to Upload')
    parser.add_argument('-u', '--url', type=str, default=get_default(['url']),
                        help='Zipline URL.')
    parser.add_argument('-a', '-t', '--authorization', '--token', type=str,
                        default=get_default(['token', 'authorization']),
                        help='Zipline Access Token for Authorization or ZIPLINE_TOKEN')
    parser.add_argument('-e', '-x', '--expires_at', '--expire', type=str, default=get_default(['expire', 'expire_at']),
                        help='Example: 1d. See: https://zipline.diced.tech/docs/guides/upload-options#image-expiration')
    parser.add_argument('--embed', action=argparse.BooleanOptionalAction, default=get_default(['embed'], False, bool),
                        help='Enable Embeds on Uploads')
    parser.add_argument('--setup', action='store_true', default=False,
                        help='Set Required Variables: URL and AUTHORIZATION')
    args = parser.parse_args()
    # print(args)
    if args.setup:
        url = input('Zipline URL: ')
        token = input('Zipline Authorization Token: ')
        if not url or not token:
            raise ValueError('Missing URL or Token.')
        env_file = Path(os.path.expanduser('~')) / '.zipline'
        with open(env_file, 'w') as f:
            f.write(f'ZIPLINE_URL={url}\nZIPLINE_TOKEN={token}')
        print('Setup Success. You can run again to change or update details.')
        sys.exit(0)

    if not args.url:
        parser.print_help()
        error = 'Missing Zipline URL. Use use --setup or specify --url'
        raise ValueError(error)

    if not args.authorization:
        parser.print_help()
        error = 'Missing Zipline Token. Use use --setup or specify --token'
        raise ValueError(error)

    if args.expires_at:
        args.expires_at = args.expires_at.lower()
        match = re.search(r'(\d+(?:ms|s|m|h|d|w|y))', args.expires_at)
        if not match:
            parser.print_help()
            error = f'Invalid Expiration Format: {args.expires_at}. See --help'
            raise ValueError(error)

    url = args.url
    files = args.files
    vars(args).pop('url')
    vars(args).pop('files')
    vars(args).pop('setup')
    # print(vars(args))
    zipline = Zipline(url, **vars(args))

    if not files:
        content: str = sys.stdin.read().rstrip('\n') + '\n'
        text_f: TextIO = io.StringIO(content)
        name = f'{gen_rand(8)}.txt'
        url: str = zipline.send_file(name, text_f)
        print(f'{name} -> {url}')
        sys.exit(0)

    exit_code = 1
    for name in files:
        if not os.path.isfile(name):
            print(f'File Not Found: {name}')
            continue
        with open(name) as f:
            new_name = f'{gen_rand()}-{os.path.basename(name)}'
            url: str = zipline.send_file(new_name, f)
            print(f'{new_name} -> {url}')
            exit_code = 0
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

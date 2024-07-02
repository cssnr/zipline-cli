import os
import re
from setuptools import setup
# from packaging.version import parse, InvalidVersion


# def get_version() -> str:
#     try:
#         ref = os.environ.get('GITHUB_REF_NAME', '0.0.1')
#         version = parse(ref)
#         return version.public
#     except InvalidVersion:
#         return '0.0.1'


def get_version():
    version = os.environ.get('GITHUB_REF_NAME', '0.0.1')
    pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-(\w+|\d+)\.(\w+|\d+))?$'
    match = re.match(pattern, version)
    if match:
        return version
    else:
        return '0.0.1'


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    version=get_version(),
    name='zipline-cli',
    description='Python 3 CLI for Zipline',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cssnr/zipline-cli',
    author='Shane',
    author_email='shane@sapps.me',
    py_modules=['zipline'],
    install_requires=['requests', 'python-decouple', 'python-dotenv'],
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    project_urls={
        # 'Documentation': 'https://zipline-cli.sapps.me/',
        'Source': 'https://github.com/cssnr/zipline-cli',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': [
            'zipline = zipline:main',
        ],
    },
)

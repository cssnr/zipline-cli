import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    version='0.1.4',
    name='zipline-cli',
    description='Python 3 CLI for Zipline',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cssnr/zipline-cli',
    author='Shane',
    author_email='shane@sapps.me',
    py_modules=['zipline'],
    install_requires=['requests', 'python-decouple', 'python-dotenv'],
    python_requires='>=3.6',
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

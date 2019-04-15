try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Hack assembler for "nand2tetris" project 6',
    'author': 'Jonathan Bowen',
    'url': 'URL to get it at.'
    'download_url': 'Where to download it.',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'hack_assembler'
}

setup(**config)

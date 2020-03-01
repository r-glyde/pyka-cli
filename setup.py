from setuptools import setup
import fastentrypoints

setup(
    name='pycli',
    version='0.1.0',
    packages=['pyka'],
    entry_points={
        'console_scripts': [
            'pyka = pyka.__main__:main'
        ]
    })

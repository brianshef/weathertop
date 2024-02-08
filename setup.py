import sys
from setuptools import setup, find_packages


setup(
    name="weathertop",
    version="0.1.1",
    author="Brian Shef",
    author_email="brianshef@gmail.com",
    description="An experimental early-warning system to be used with the game Foxhole. Named after the famous, ancient watchtower in Lord of the Rings.",
    url="https://github.com/brianshef/weathertop",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    scripts=['weathertop/main.py'],
    entry_points={
        'console_scripts': ['weathertop=weathertop.main:main']
    },
)
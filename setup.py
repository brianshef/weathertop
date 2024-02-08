import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("setuptools not installed. Run the following command to resolve: pipenv install setuptools")
    sys.exit(1)
else:
    sys.exit(0)


setup(
    name="weathertop",
    version="0.1.0",
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
    python_requires='>=3.12',
    # scripts=['main.py'],
    entry_points={
        'console_scripts': ['weathertop=weathertop.main:main']
    },
)
# setup.py
from setuptools import setup, Extension

setup(
    name="distance",
    ext_modules=[
        Extension("distance", sources=["distance.c"])
    ]
)

# -*- coding: utf-8 -*-
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding="utf-8")

with open("requirements.txt", "r") as fin:
    REQUIRED_PACKAGES = fin.read()

setup(
    name="llm2json",
    version=open((HERE / "llm2json" / "version.txt"), "r").read().strip(),
    description="Web Based Multi Purpose Annotation Software",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JiehangXie/llm2json",
    author="Jiehang Xie",
    author_email="xiejiehang@foxmail.com",
    license="MIT License",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
    python_requires='>=3.7',
)
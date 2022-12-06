#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.readlines()

setup(
    name="ticktock",
    version="0.1.0",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="kernelmethod",
    author_email="17100608+kernelmethod@users.noreply.github.com",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7.0",
    license="BSD",
)

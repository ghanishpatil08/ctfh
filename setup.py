"""Setup script for CTF-H"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ctfh",
    version="1.0.0",
    author="CTF-H Team",
    description="Interactive CTF, Cryptography & Cybersecurity Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your/ctfh",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Security",
        "Topic :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "colorama>=0.4.6",
        "requests>=2.31.0",
    ],
    extras_require={
        "full": [
            "Pillow>=10.0.0",
            "jsbeautifier>=1.14.0",
            "base58>=2.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ctfh=ctfh.main:main",
        ],
    },
)


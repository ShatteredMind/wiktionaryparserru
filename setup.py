import pathlib
from setuptools import setup

current_location = pathlib.Path(__file__).parent
README = (current_location / "README.md").read_text()

setup(
    name="wiktionary-parser-ru",
    version="0.0.1",
    packages=["wiktionaryparser", "tests"],
    url="https://github.com/ShatteredMind/wiktionaryparserru",
    license="MIT",
    author="internethero",
    author_email="sashalekoncev@gmail.com",
    description="Basic parser for russian wiktionary",
    long_description=README,
    install_requires=["beautifulsoup4", "requests"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)

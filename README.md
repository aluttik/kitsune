<h1 align="center">Kitsune</h1>
<h3 align="center">A prettier way to tail multiple files.</h3>

<p align="center">
<a href="https://travis-ci.org/aluttik/kitsune"><img alt="Build status" src="https://img.shields.io/travis/aluttik/kitsune/master.svg?longCache=true&style=for-the-badge"></a>
<a href="https://pypi.org/project/kitsune/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/kitsune.svg?longCache=true&style=for-the-badge"></a>
<a href="https://pypi.python.org/pypi/kitsune"><img alt="Supported Python versions" src="https://img.shields.io/pypi/pyversions/kitsune.svg?longCache=true&style=for-the-badge"></a>
<a href="https://pypi.python.org/pypi/kitsune"><img alt="License: MIT" src="https://img.shields.io/pypi/l/kitsune.svg?longCache=true&style=for-the-badge"></a>
<a href="https://github.com/aluttik/kitsune"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?longCache=true&style=for-the-badge"></a>
</p>

## Installation

    pip install kitsune

## Command Line Interface

```
usage: kitsune [--color <when>] [-h] [-V] pattern [pattern ...]

A prettier way to tail multiple files.

positional arguments:
  pattern         Files to tail.

optional arguments:
  --color <when>  Specify when to use colored output. The automatic mode only
                  enables colors if an interactive terminal is detected.
                  [default: auto] [possible values: auto, never, always]
  -h, --help      Print this help message.
  -V, --version   Show version information.
```

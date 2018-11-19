<h1 align="center">Kitsune</h1>
<h3 align="center">A prettier way to tail multiple files.</h3>

<p align="center">
<a href="https://travis-ci.org/aluttik/kitsune"><img alt="Build status" src="https://img.shields.io/travis/aluttik/kitsune/master.svg"></a>
<a href="https://pypi.org/project/python-kitsune/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/python-kitsune.svg"></a>
<a href="https://pypi.python.org/pypi/python-kitsune"><img alt="Supported Python versions" src="https://img.shields.io/pypi/pyversions/python-kitsune.svg"></a>
<a href="https://pypi.python.org/pypi/python-kitsune"><img alt="License: MIT" src="https://img.shields.io/pypi/l/python-kitsune.svg"></a>
<a href="https://github.com/aluttik/kitsune"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Installation

    pip install python-kitsune

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

## Screenshot
![Kitsune Example](https://raw.githubusercontent.com/aluttik/kitsune/master/ext/kitsune-example.png)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import itertools
import glob
import os

from . import __title__, __version__
from .tails import KitsunePrinter


def parse_args(args=None):
    p = argparse.ArgumentParser(
        prog='kitsune',
        description="A prettier way to tail multiple files.",
        add_help=False,
    )
    p.add_argument(
        "--color",
        metavar="<when>",
        dest="color",
        default="auto",
        choices=["auto", "never", "always"],
        help="""Specify when to use colored
            output. The automatic mode only
            enables colors if an interactive terminal is detected.
            [default: auto] [possible values: auto, never, always]""",
    )
    p.add_argument("-h", "--help", action="help", help="Print this help message.")
    p.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="Show version information.",
    )
    p.add_argument("pattern", nargs="+", help="Files to tail.")
    parsed = p.parse_args(args=args)
    return parsed


def main():
    args = parse_args()

    uses_color = args.color == "always" or (args.color == "auto" and os.isatty(0))

    paths = map(glob.iglob, args.pattern)
    paths = itertools.chain.from_iterable(paths)
    # paths = map(os.path.abspath, paths)
    paths = filter(os.path.isfile, paths)
    paths = list(paths)

    printer = KitsunePrinter(paths, uses_color)
    printer.run()


if __name__ == "__main__":
    main()

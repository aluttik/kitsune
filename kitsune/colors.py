# -*- coding: utf-8 -*-
import itertools


def color_func(value):
    return lambda x: "\033[{}m{}\033[0m".format(value, x)


grey = color_func("30")
red = color_func("31")
green = color_func("32")
yellow = color_func("33")
blue = color_func("34")
magenta = color_func("35")
cyan = color_func("36")
white = color_func("37")
bold_grey = color_func("30;1")
bold_red = color_func("31;1")
bold_green = color_func("32;1")
bold_yellow = color_func("33;1")
bold_blue = color_func("34;1")
bold_magenta = color_func("35;1")
bold_cyan = color_func("36;1")
bold_white = color_func("37;1")

colors = [
    cyan,
    yellow,
    green,
    magenta,
    red,
    blue,
    bold_cyan,
    bold_yellow,
    bold_green,
    bold_magenta,
    bold_red,
    bold_blue,
]

rainbow = itertools.cycle(colors)
plain = itertools.cycle([lambda x: x])

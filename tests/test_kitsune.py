# -*- coding: utf-8 -*-
import io
import re
import time

from kitsune import KitsunePrinter

# longer delay = more reliable tests
DELAY_SECONDS = 0.5


def test_kitsune_printer_plain(tmpdir):
    a = tmpdir.join("a.log")
    b = tmpdir.join("bb.log")

    # 'touch' the files
    a.ensure(file=True)
    b.ensure(file=True)

    buf = io.StringIO()

    printer = KitsunePrinter([a.strpath, b.strpath], color=False, stream=buf)
    printer.start()
    time.sleep(DELAY_SECONDS)

    a.write("foo\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    b.write("bar\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    a.write("baz\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    output = buf.getvalue().splitlines()
    assert len(output) == 3
    assert output[0] == "a.log  | foo"
    assert output[1] == "bb.log | bar"
    assert output[2] == "a.log  | baz"

    printer.stop()

    a.write("printer already stopped\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    output = buf.getvalue().splitlines()
    assert len(output) == 3
    assert output[0] == "a.log  | foo"
    assert output[1] == "bb.log | bar"
    assert output[2] == "a.log  | baz"


def test_kitsune_printer_rainbow(tmpdir):
    a = tmpdir.join("a.log")
    b = tmpdir.join("bb.log")

    # 'touch' the files
    a.ensure(file=True)
    b.ensure(file=True)

    buf = io.StringIO()

    printer = KitsunePrinter([a.strpath, b.strpath], color=True, stream=buf)
    printer.start()
    time.sleep(DELAY_SECONDS)

    a.write("foo\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    b.write("bar\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    a.write("baz\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    colored_line_regex = re.compile(r"(\x1b\[3[0-7](?:;1)?m)(\w+\..+ +\|\x1b\[0m .*)\n")

    value = buf.getvalue()
    matches = colored_line_regex.findall(value)
    assert len(matches) == 3
    output = tuple(zip(*matches))[1]
    assert output[0] == "a.log  |\033[0m foo"
    assert output[1] == "bb.log |\033[0m bar"
    assert output[2] == "a.log  |\033[0m baz"

    printer.stop()

    a.write("printer already stopped\n", mode="a+")
    time.sleep(DELAY_SECONDS)

    value = buf.getvalue()
    matches = colored_line_regex.findall(value)
    assert len(matches) == 3
    output = tuple(zip(*matches))[1]
    assert output[0] == "a.log  |\033[0m foo"
    assert output[1] == "bb.log |\033[0m bar"
    assert output[2] == "a.log  |\033[0m baz"

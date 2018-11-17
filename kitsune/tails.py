# -*- coding: utf-8 -*-
import sys
import thread as _thread
import time

import Queue
import collections
import os
import six
import threading

from .colors import plain, rainbow
from .file import FileTail

QueueItem = collections.namedtuple("QueueItem", "line exc")


def split_buffer(stream):
    """Given a generator which yields strings and a splitter function,
    joins all input, splits on the separator and yields each chunk.
    Unlike string.split(), each chunk includes the trailing
    separator, except for the last one if none was found on the end
    of the input.
    """
    buffered = six.text_type("")

    for data in stream_as_text(stream):
        buffered += data
        while True:
            index = buffered.find(six.text_type("\n"))
            if index == -1:
                break
            item, buffered = buffered[: index + 1], buffered[index + 1 :]
            yield item

    if buffered:
        yield buffered


class LineFormatter(object):
    prefix_width = 0

    def __init__(self, path, color):
        self.name = os.path.basename(path)
        self.color = color
        self.prefix_width = max([self.prefix_width, len(self.name)])

    def __call__(self, line):
        prefix = self.color(self.name.ljust(self.prefix_width) + " |")
        return "{} {}".format(prefix, line)


def consume_queue(queue):
    """Consume the queue by reading lines off of it and yielding them."""
    while True:
        try:
            item = queue.get(timeout=0.1)
        except Queue.Empty:
            yield None
            continue
        except _thread.error:
            raise ShutdownException()

        if item.exc:
            raise item.exc

        yield item.line


def tail_file(path, formatter, queue):
    tail = FileTail(filename=path)
    try:
        count = 0
        while True:
            for line in tail:
                count += 1
                if count % 1000:
                    time.sleep(0.001)  # release GIL
                item = QueueItem(line=formatter(line), exc=None)
                queue.put(item)
    except Exception as exc:
        item = QueueItem(line=None, exc=exc)
        queue.put(item)
        return


class TailThread(threading.Thread):
    def __init__(self, *args):
        super(TailThread, self).__init__(target=tail_file, args=args)
        self.daemon = True
        self.start()


class KitsunePrinter(object):
    """Print lines from multiple files to a single output stream."""

    def __init__(self, paths, color, stream=sys.stdout):
        self.paths = paths
        self.color = color
        self.stream = stream

    def run(self):
        if not self.paths:
            return

        queue = Queue.Queue()

        thread_map = {}
        for path, color in zip(self.paths, rainbow if self.color else plain):
            formatter = LineFormatter(path, color)
            thread_map[path] = TailThread(path, formatter, queue)

        try:
            for line in consume_queue(queue):
                for path, tail_thread in list(thread_map.items()):
                    if not tail_thread.is_alive():
                        print("popping thread: " + path)
                        thread_map.pop(path, None)

                # stop if all the tails are stopped
                if not line and not thread_map:
                    return

                if line:
                    self.write(line)
        except KeyboardInterrupt:
            pass

    def write(self, line):
        try:
            self.stream.write(line.strip() + "\n")
        except UnicodeEncodeError:
            self.stream.write(line.encode("ascii", "replace").decode())
        self.stream.flush()

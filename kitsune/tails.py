# -*- coding: utf-8 -*-
import collections
import itertools
import os
import Queue
import random
import sys
import thread as _thread
import threading

from .colors import colors, plain, rainbow
from .file import FileTail

QueueItem = collections.namedtuple("QueueItem", "line exc")


def consume_iterator(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)


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


class LineFormatter(object):
    prefix_width = 0

    def __init__(self, path, color):
        self.name = os.path.basename(path)
        self.color = color
        self.prefix_width = max([self.prefix_width, len(self.name)])

    def __call__(self, line):
        prefix = self.color(self.name.ljust(self.prefix_width) + " |")
        return "{} {}".format(prefix, line)


def tail_file(path, formatter, queue):
    tail = FileTail(filename=path)
    try:
        while True:
            for line in tail:
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

        # if color is enabled then start at a random color
        if self.color:
            consume_iterator(rainbow, random.randint(0, len(colors) - 1))

        queue = Queue.Queue()

        thread_map = {}
        for path, color in zip(self.paths, rainbow if self.color else plain):
            formatter = LineFormatter(path, color)
            thread_map[path] = TailThread(path, formatter, queue)

        try:
            for line in consume_queue(queue):
                for path, tail_thread in list(thread_map.items()):
                    if not tail_thread.is_alive():
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
            self.stream.write(line.encode("ascii", "replace").decode().strip() + "\n")
        self.stream.flush()

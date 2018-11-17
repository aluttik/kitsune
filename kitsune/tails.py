# -*- coding: utf-8 -*-
"""
tails.py
~~~~~~~~

Much of this code is based on code from docker-compose
Copyright (C) 2014 Docker, Inc.

https://github.com/docker/compose
"""
import collections
import itertools
import os
import random
import sys
import threading

if sys.version[0] == '2':
    import Queue
    import thread as _thread
else:
    import queue as Queue
    import _thread

from .colors import colors, plain, rainbow
from .file import FileTail

QueueItem = collections.namedtuple("QueueItem", "line exc")


class ShutdownException(Exception):
    pass


class LineFormatter(object):
    prefix_width = 0

    def __init__(self, path, color):
        self.name = os.path.basename(path)
        self.color = color
        self.prefix_width = max([self.prefix_width, len(self.name)])

    def __call__(self, line):
        prefix = self.color(self.name.ljust(self.prefix_width) + " |")
        return "{} {}".format(prefix, line)


class TailThread(threading.Thread):
    queue = None

    def __new__(cls, *args, **kwargs):
        if cls.queue is None:
            cls.queue = Queue.Queue()
        obj = super(TailThread, cls).__new__(cls)
        return obj

    def __init__(self, *args, **kwargs):
        super(TailThread, self).__init__(target=self.tail, args=args, kwargs=kwargs)
        self.daemon = True
        self.start()

    def tail(self, path, formatter):
        tail = FileTail(filename=path)
        try:
            while True:
                for line in tail:
                    item = QueueItem(line=formatter(line), exc=None)
                    self.queue.put(item)
        except Exception as exc:
            item = QueueItem(line=None, exc=exc)
            self.queue.put(item)
            return

    @classmethod
    def consume_queue(cls):
        """Consume the queue by reading lines off of it and yielding them."""
        while True:
            try:
                item = cls.queue.get(timeout=0.1)
            except Queue.Empty:
                yield None
                continue
            except _thread.error:
                raise ShutdownException()

            if item.exc:
                raise item.exc

            yield item.line


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
            n = random.randint(0, len(colors) - 1)
            next(itertools.islice(rainbow, n, n), None)

        thread_map = {}
        for path, color in zip(self.paths, rainbow if self.color else plain):
            formatter = LineFormatter(path, color)
            thread_map[path] = TailThread(path, formatter)

        try:
            for line in TailThread.consume_queue():
                for path, tail_thread in list(thread_map.items()):
                    if not tail_thread.is_alive():
                        thread_map.pop(path, None)

                # stop if all the tails are stopped
                if not line and not thread_map:
                    return

                if line:
                    self.write(line)
        except (KeyboardInterrupt, ShutdownException):
            pass

    def write(self, line):
        try:
            self.stream.write(line.strip() + "\n")
        except UnicodeEncodeError:
            self.stream.write(line.encode("ascii", "replace").decode().strip() + "\n")
        self.stream.flush()

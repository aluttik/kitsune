# -*- coding: utf-8 -*-
"""
kitsune.py
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
import time

if sys.version[0] == "2":
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
    def __init__(self, path, color_func, prefix_width):
        self.name = path
        self.color_func = color_func
        self.prefix_width = prefix_width

    def __call__(self, line):
        prefix = self.color_func(self.name.ljust(self.prefix_width) + " |")
        return "{} {}".format(prefix, line)

    @classmethod
    def from_paths(cls, paths, color):
        paths = [os.path.basename(path) for path in paths]
        color_cycle = rainbow if color else plain
        prefix_width = max(map(len, paths))

        formatters = []
        for path, color_func in zip(paths, color_cycle):
            formatter = cls(path, color_func, prefix_width)
            formatters.append(formatter)

        return formatters


class KitsuneTailThread(threading.Thread):
    queue = None

    def __new__(cls, *args, **kwargs):
        if cls.queue is None:
            cls.queue = Queue.Queue()
        obj = super(KitsuneTailThread, cls).__new__(cls)
        return obj

    def __init__(self, *args, **kwargs):
        super(KitsuneTailThread, self).__init__(
            target=self.tail, args=args, kwargs=kwargs
        )
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


class KitsuneThread(threading.Thread):
    """
    Print lines from multiple files to a single output stream.
    """

    def __init__(self, paths, color, stream=sys.stdout):
        super(KitsuneThread, self).__init__(target=self._run)
        self.daemon = True
        self.running = False
        self.paths = paths
        self.color = color
        self.stream = stream

    def _run(self):
        if not self.paths:
            return

        # if color is enabled then start at a random color
        if self.color:
            n = random.randint(0, len(colors) - 1)
            next(itertools.islice(rainbow, n, n), None)

        formatters = LineFormatter.from_paths(self.paths, self.color)

        worker_threads = {}
        for path, formatter in zip(self.paths, formatters):
            worker_threads[path] = KitsuneTailThread(path, formatter)

        it = KitsuneTailThread.consume_queue()
        while self.running:
            line = next(it)

            for path, tail_thread in list(worker_threads.items()):
                if not tail_thread.is_alive():
                    worker_threads.pop(path, None)

            # stop if all the tails are stopped
            if not line and not worker_threads:
                break
            elif line:
                self.write(line)

    def write(self, line):
        try:
            self.stream.write(line.strip() + u"\n")
        except UnicodeEncodeError:
            self.stream.write(line.encode("ascii", "replace").decode().strip() + u"\n")
        self.stream.flush()


class KitsunePrinter(object):
    def __init__(self, paths, color, stream=sys.stdout):
        self.master_thread = KitsuneThread(paths, color, stream=stream)
        self.stream = stream

    def start(self):
        """
        Start the master thread
        """
        self.master_thread.running = True
        self.master_thread.start()

    def wait(self):
        """
        Run the master thread indefinitely until an exception is raised
        """
        try:
            while self.master_thread.running:
                time.sleep(0.01)
        except (KeyboardInterrupt, ShutdownException):
            self.stop()

    def stop(self):
        """
        Stop the master thread
        """
        self.master_thread.running = False
        self.master_thread.join()

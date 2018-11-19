# -*- coding: utf-8 -*-
import os
import time

OFFSET_CACHE = {}


class FileTail(object):
    """
    Creates an iterable object that returns unread lines

    Based on code from Pygtail, a python "port" of logtail2
    Copyright (C) 2011 Brad Greenlee <brad@footle.org>

    https://github.com/bgreenlee/pygtail/
    """

    def __init__(self, filename):
        self.name = "file:" + filename
        self.filename = filename
        self._fh = None

        # open file and seek to the end
        if self.filename not in OFFSET_CACHE:
            with open(self.filename) as fp:
                fp.seek(0, 2)
                OFFSET_CACHE[self.filename] = fp.tell()

        self._offset = OFFSET_CACHE[self.filename]

        # save inode to determine rotations
        self._inode = self._st_ino()

    def __del__(self):
        try:
            if self._filehandle():
                self._fh.close()
        except StopIteration:
            pass

    def __iter__(self):
        self._filehandle()
        return self

    def __next__(self):
        try:
            return self._get_next_line()
        except StopIteration:
            self._update_inode()  # EOF
            raise

    def _st_ino(self):
        return os.stat(self.filename).st_ino

    def _update_inode(self):
        self._inode = self._st_ino()

    def _update_offset(self):
        self._offset = OFFSET_CACHE[self.filename] = self._filehandle().tell()

    def _is_closed(self):
        return not self._fh or self._fh.closed

    def _get_next_line(self):
        line = self._fh.readline()
        if not line:
            raise StopIteration
        else:
            return line.rstrip("\n\r")

    def _filehandle(self):
        """
        Returns a filehandle to the file being tailed,
        with the position set to the current offset.
        """
        file_was_rotated = self._file_was_rotated()
        is_closed = self._is_closed()

        if is_closed or file_was_rotated:
            if not is_closed:
                self._fh.close()

            if file_was_rotated:
                self._update_inode()
                self._offset = OFFSET_CACHE[self.filename] = 0

            self._fh = open(self.filename)
            self._fh.seek(self._offset)

        return self._fh

    def _file_was_rotated(self):
        """
        Returns True if the file was rotated.
        """
        tries = 0
        new_inode = self._inode

        while tries < 2:
            try:
                new_inode = self._st_ino()
                break
            except:
                time.sleep(0.5)
                tries += 1

        if tries == 2:  # broke out of loop manually
            raise StopIteration

        # check for copytruncate
        # it will use the same file so inode will stay the same
        if new_inode == self._inode and self.filename in OFFSET_CACHE:
            with open(self.filename) as fp:
                fp.seek(0, 2)
                if fp.tell() < OFFSET_CACHE[self.filename]:
                    # this means that the file is now smaller than perviously cached
                    # so file must have been truncated
                    return True

        return new_inode != self._inode

    def readlines(self):
        """Returns a list of all unread lines"""
        return list(self)

    def next(self):
        return self.__next__()

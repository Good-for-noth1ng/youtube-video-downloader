import functools
import gzip
import json
import logging
import os
import re
import warnings
from typing import Any, Callable, Dict, List, Optional, TypeVar
from urllib import request

from downloader.downloader_components.error import RegexMatchError


logger = logging.getLogger(__name__)


class DeferredGeneratorlist():
    def __init__(self, generator):
        self.gen = generator
        self._elements = []
    

    def __eq__(self, other):
        return list(self) == other
    

    def __getitem__(self, key) -> Any:
        if not isinstance(key, (int, slice)):
            raise TypeError('Key must be either a slice or int')

        key_slice = key
        if isinstance(key, int):
            key_slice = slice(key, key + 1, 1)
        
        while len(self._elements) < key_slice.stop:
            try: 
                next_item = next(self.gen)
            except StopIteration:
                raise IndexError
            else:
                self._elements.append(next_item)
        return self._elements[key]


    def __iter__(self):
        iter_index = 0
        while True:
            try: 
                curr_item = self[iter_index]
            except IndexError:
                return
            else:
                yield curr_item
                iter_index += 1


    def __next__(self):
        try:
            curr_element = self[self.iter_index]
        except IndexError:
            raise StopIteration
        self.iter_index += 1
        return curr_element


    def __len__(self):
        self.generate_all()
        return len(self._elements)


    def __repr__(self):
        self.generate_all()
        return str(self._elements)

    def __reversed__(self):
        self.generate_all()
        return self._elements[::-1]

    def generate_all(self):
        while True:
            try:
                next_item = next(self.gen)
            except StopIteration:
                break
            else:
                self._elements.append(next_item)

def regex_search(pattern: str, string: str, group: int) -> str:
    regex = re.compile(pattern=pattern)
    results = regex.search(string=string)
    if not results:
        raise RegexMatchError(caller="regex_search", pattern=pattern)
    logger.debug(f"matched regex search: {pattern}")
    return results.group(group)

def safe_file_name(s: str, max_length: int = 255) -> str:
    ntfs_characters = [chr(i) for i in range(0, 31)]
    characters = [
        r'"',
        r"\#",
        r"\$",
        r"\%",
        r"'",
        r"\*",
        r"\,",
        r"\.",
        r"\/",
        r"\:",
        r'"',
        r"\;",
        r"\<",
        r"\>",
        r"\?",
        r"\\",
        r"\^",
        r"\|",
        r"\~",
        r"\\\\"
    ]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    file_name = regex.sub("", s)
    return file_name[:max_length].rsplit(" ", 0)[0]

def setuo_logger(level: int = logging.ERROR, log_filename: Optional[str] = None) -> None:
    fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    logger = logging.getLogger("downloader")
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    logger.addHandler(stream_handler)

    if log_filename is not None:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(fmt=formatter)
        logger.addHandler(file_handler)

GenericType = TypeVar("GenericType")

def cache(func: Callable[..., GenericType]) -> GenericType:
    return functools.lru_cache()(func)